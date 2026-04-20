# Data Contract
## Proyecto: Flores AI - Iris

> **Documento:** Data Contract - Contrato de Datos
> **Version:** 1.0.0
> **Estado:** Certificado - Phase Discovery Discovery
> **Fecha de creacion:** 2026-04-19
> **Ultima actualizacion:** 2026-04-19
> **Autor:** ai-solutions-architect
> **Trazabilidad:** SpecDD v1.0.0 -> DATA_CONTRACT v1.0.0 -> BRD v1.0.0 -> feasibility v1.0.0
> **Version del Contrato:** v1.0.0
> **Aceptado por:** ai-data-engineer (Phase Engineering), ai-ml-engineer (Phase Modeling)

---

## Indice

1. [Proposito y Alcance](#1-proposito-y-alcance)
2. [Capa Bronze: Esquema del CSV Crudo](#2-capa-bronze-esquema-del-csv-crudo)
3. [Capa Silver: Esquema del DataFrame Limpio](#3-capa-silver-esquema-del-dataframe-limpio)
4. [Capa Gold: Esquema de Arrays de ML](#4-capa-gold-esquema-de-arrays-de-ml)
5. [Contrato de Entrada de Inferencia (IrisInput)](#5-contrato-de-entrada-de-inferencia-irisinput)
6. [Contrato de Salida de Inferencia (PredictionResult)](#6-contrato-de-salida-de-inferencia-predictionresult)
7. [Contrato de Feedback (FeedbackRecord)](#7-contrato-de-feedback-feedbackrecord)
8. [Diccionario de Datos Tecnico](#8-diccionario-de-datos-tecnico)
9. [Politica de Nulos (Null Policy)](#9-politica-de-nulos-null-policy)
10. [Reglas de Validacion Matematica](#10-reglas-de-validacion-matematica)
11. [Deteccion de Data Drift](#11-deteccion-de-data-drift)
12. [Mensajes de Error Estandarizados](#12-mensajes-de-error-estandarizados)
13. [Sensibilidad de Datos (PII)](#13-sensibilidad-de-datos-pii)
14. [Control de Versiones del Contrato](#14-control-de-versiones-del-contrato)
15. [Check de Certificacion del Contrato](#15-check-de-certificacion-del-contrato)

---

## 1. Proposito y Alcance

Este documento define los esquemas rigidos, las reglas de validacion y los invariantes matematicos para cada frontera de datos del sistema Flores AI - Iris. Es el contrato entre:

- El **agente Data Engineer** (Phase Engineering): debe producir capas Silver y Gold que cumplan este esquema.
- El **agente ML Engineer** (Phase Modeling): debe consumir la capa Gold y producir un artefacto de modelo que acepte el `IrisInput` definido en la seccion 5.
- El **agente Developer** (Phase Delivery): debe construir el formulario de Streamlit cuyos valores satisfacen el contrato de la seccion 5.

**Principio Fail-Fast:** Todo dato que viole este contrato en la frontera del sistema (entrada de usuario, lectura de archivo, carga de modelo) debe ser rechazado antes de llegar al nucleo de procesamiento. Ningun modulo interno debe recibir datos no validados.

---

## 2. Capa Bronze: Esquema del CSV Crudo

**Origen:** `data/bronze/Iris.csv`
**Modulo responsable:** `src/data/bronze_loader.py`
**Modo de acceso:** Solo lectura. Este archivo jamas es modificado por ningun modulo.

### 2.1 Esquema de Columnas

| # | Nombre Columna | Tipo pandas | Nulidad | Valores Esperados | Rol en ML |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `Id` | `int64` | No nulo | Enteros en rango [1, 150], secuenciales | IGNORAR - data leakage |
| 2 | `SepalLengthCm` | `float64` | No nulo | Decimales en (3.0, 9.0) cm | Feature |
| 3 | `SepalWidthCm` | `float64` | No nulo | Decimales en (1.5, 5.5) cm | Feature |
| 4 | `PetalLengthCm` | `float64` | No nulo | Decimales en (0.5, 8.0) cm | Feature |
| 5 | `PetalWidthCm` | `float64` | No nulo | Decimales en (0.0, 3.5) cm | Feature |
| 6 | `Species` | `object` (str) | No nulo | `{'Iris-setosa', 'Iris-versicolor', 'Iris-virginica'}` | Target |

### 2.2 Invariantes de la Capa Bronze

| Invariante | Valor Esperado | Accion si Falla |
| :--- | :--- | :--- |
| Total de filas | 150 | Lanzar `ValueError: "Bronze dataset debe tener 150 filas, encontrado: {n}"` |
| Total de columnas | 6 | Lanzar `ValueError: "Bronze dataset debe tener 6 columnas"` |
| Valores nulos totales | 0 | Lanzar `ValueError: "Bronze dataset contiene {n} valores nulos"` |
| Clases unicas en Species | 3 (`Iris-setosa`, `Iris-versicolor`, `Iris-virginica`) | Lanzar `ValueError` |
| Registros por clase | 50 exactos por cada clase | Lanzar `ValueError` |

---

## 3. Capa Silver: Esquema del DataFrame Limpio

**Origen:** Producida por `src/data/silver_cleaner.py`
**Persistido en:** `data/silver/iris_silver.csv`
**Modulo responsable:** `src/data/silver_cleaner.py`

### 3.1 Esquema de Columnas

| # | Nombre Columna | Tipo pandas | Nulidad | Valores Esperados | Rol en ML |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `sepal_length` | `float64` | No nulo | Decimales en [3.0, 9.0] cm | Feature |
| 2 | `sepal_width` | `float64` | No nulo | Decimales en [1.5, 5.5] cm | Feature |
| 3 | `petal_length` | `float64` | No nulo | Decimales en [0.5, 8.0] cm | Feature |
| 4 | `petal_width` | `float64` | No nulo | Decimales en [0.0, 3.5] cm | Feature |
| 5 | `species` | `object` (str) | No nulo | `{'setosa', 'versicolor', 'virginica'}` | Target |

### 3.2 Invariantes de la Capa Silver

| Invariante | Valor Esperado | Accion si Falla |
| :--- | :--- | :--- |
| Total de filas | 147 (150 - 3 duplicados) | Lanzar `ValueError` |
| Total de columnas | 5 (sin columna `Id`) | Lanzar `ValueError` |
| Valores nulos totales | 0 | Lanzar `ValueError` |
| Filas duplicadas | 0 | Lanzar `ValueError` |
| Columnas en snake_case | Todas las 5 | Lanzar `KeyError` si alguna esta en PascalCase |
| Prefijo `Iris-` en species | 0 ocurrencias | Lanzar `ValueError` |
| Clases unicas en species | `{'setosa', 'versicolor', 'virginica'}` | Lanzar `ValueError` |

### 3.3 Transformaciones Aplicadas (Linaje)

| ID Mutacion | Descripcion | Origen (Bronze) | Destino (Silver) |
| :--- | :--- | :--- | :--- |
| M-01 | Eliminar columna `Id` | Columna `Id` (int64) | Ausente |
| M-02 | Eliminar 3 near-duplicates | 150 filas | 147 filas |
| M-03 | Renombrar a snake_case | `SepalLengthCm`, etc. | `sepal_length`, etc. |
| M-04 | Normalizar etiquetas | `Iris-setosa`, etc. | `setosa`, etc. |

---

## 4. Capa Gold: Esquema de Arrays de ML

**Origen:** Producida por `src/data/gold_builder.py`
**Persistido en:** `data/gold/X_gold.csv`, `data/gold/y_gold.csv`
**Modulo responsable:** `src/data/gold_builder.py`

### 4.1 Array de Features (X)

| Atributo | Valor |
| :--- | :--- |
| Tipo | `numpy.ndarray` |
| Shape | `(147, 4)` |
| Dtype | `float64` |
| Orden de columnas | `['sepal_length', 'sepal_width', 'petal_length', 'petal_width']` |
| Valores nulos (NaN) | 0 |
| Valores infinitos | 0 |

**Invariante critico:** El orden de columnas en X debe ser identico al orden en que el Pipeline fue entrenado. Este orden esta definido en `config.FEATURE_COLUMNS` y es la fuente de verdad absoluta. Cualquier desalineacion produce predicciones silenciosamente incorrectas (no lanza excepcion).

### 4.2 Array de Target (y)

| Atributo | Valor |
| :--- | :--- |
| Tipo | `numpy.ndarray` |
| Shape | `(147,)` |
| Dtype | `object` (strings) |
| Valores validos | `{'setosa', 'versicolor', 'virginica'}` |
| Balance de clases | Versicolor: 50, Setosa: 50, Virginica: 47 (despues de eliminar 3 duplicados de Virginica) |

**Nota sobre balance:** Despues de eliminar los 3 duplicados detectados en el FEASIBILITY REPORT (2 de Virginica, 1 de Setosa segun los Ids 10/35/38 y 102/143), el balance resultante es: Setosa: 49, Versicolor: 50, Virginica: 48. Este leve desbalance (< 5%) no requiere tecnicas de balanceo. El `train_test_split` debe usar `stratify=y` para preservar las proporciones en train y test.

### 4.3 Invariantes de la Capa Gold

| Invariante | Valor Esperado |
| :--- | :--- |
| `X.shape` | `(147, 4)` |
| `y.shape` | `(147,)` |
| `len(X) == len(y)` | True |
| `X.dtype` | `float64` |
| `np.isnan(X).sum()` | `0` |
| `np.isinf(X).sum()` | `0` |
| `np.unique(y)` | `['setosa', 'versicolor', 'virginica']` |

---

## 5. Contrato de Entrada de Inferencia (IrisInput)

**Modulo responsable:** `src/validators.py`
**Proposito:** Define exactamente que datos acepta el sistema en tiempo de inferencia.

### 5.1 Esquema de Campos

| Campo | Tipo Python | Tipo JSON | Nulidad | Rango Valido | Unidad | Precision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `sepal_length` | `float` | `number` | No nulo | [3.0, 9.0] | cm | 1 decimal recomendado |
| `sepal_width` | `float` | `number` | No nulo | [1.5, 5.5] | cm | 1 decimal recomendado |
| `petal_length` | `float` | `number` | No nulo | [0.5, 8.0] | cm | 1 decimal recomendado |
| `petal_width` | `float` | `number` | No nulo | [0.0, 3.5] | cm | 1 decimal recomendado |

### 5.2 Justificacion de Rangos de Validacion

Los rangos se calculan con un margen del ~20% sobre los valores observados en el dataset Iris (datos del FEASIBILITY REPORT), para tolerar variabilidad biologica real sin ser excesivamente permisivos:

| Feature | Min Observado | Max Observado | Min Contrato | Max Contrato | Margen |
| :--- | :--- | :--- | :--- | :--- | :--- |
| sepal_length | 4.3 | 7.9 | 3.0 | 9.0 | ~20% |
| sepal_width | 2.0 | 4.4 | 1.5 | 5.5 | ~25% |
| petal_length | 1.0 | 6.9 | 0.5 | 8.0 | ~16% |
| petal_width | 0.1 | 2.5 | 0.0 | 3.5 | ~40% |

### 5.3 Casos de Rechazo (Fail-Fast)

| Caso de Entrada | Respuesta del Sistema |
| :--- | :--- |
| `sepal_length = None` | `ValidationError: sepal_length: Field required` |
| `sepal_length = "cinco"` (string) | `ValidationError: sepal_length: Input should be a valid number` |
| `sepal_length = 2.9` (bajo minimo) | `ValidationError: sepal_length: Input should be greater than or equal to 3.0` |
| `sepal_length = 9.1` (sobre maximo) | `ValidationError: sepal_length: Input should be less than or equal to 9.0` |
| `petal_width = -0.1` (negativo) | `ValidationError: petal_width: Input should be greater than or equal to 0.0` |

---

## 6. Contrato de Salida de Inferencia (PredictionResult)

**Modulo responsable:** `src/predictor.py`
**Proposito:** Define exactamente que datos produce el sistema en tiempo de inferencia.

### 6.1 Esquema de Campos

| Campo | Tipo Python | Tipo JSON | Nulidad | Valores Validos | Descripcion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `species` | `str` | `string` | No nulo | `'setosa'`, `'versicolor'`, `'virginica'` | Clase predicha por el modelo. |
| `confidence` | `float` | `number` | No nulo | [0.0, 1.0] | Probabilidad maxima sobre las 3 clases. |
| `probabilities` | `dict[str, float]` | `object` | No nulo | Claves: las 3 especies. Valores: [0.0, 1.0]. | Distribucion de probabilidad completa. |
| `low_confidence` | `bool` | `boolean` | No nulo | `True` o `False` | `True` si `confidence < 0.60`. |

### 6.2 Invariantes del PredictionResult

| Invariante | Regla |
| :--- | :--- |
| Completitud de probabilidades | `len(probabilities) == 3` |
| Claves de probabilidades | `set(probabilities.keys()) == {'setosa', 'versicolor', 'virginica'}` |
| Suma de probabilidades | `abs(sum(probabilities.values()) - 1.0) < 1e-6` |
| Coherencia de confianza | `confidence == max(probabilities.values())` |
| Coherencia de species | `probabilities[species] == confidence` |
| Coherencia de low_confidence | `low_confidence == (confidence < 0.60)` |

---

## 7. Contrato de Feedback (FeedbackRecord)

**Modulo responsable:** `src/feedback.py`
**Persistido en:** `logs/feedback.log`
**Formato de archivo:** JSON Lines (una entrada JSON por linea).

### 7.1 Esquema de Campos

| Campo | Tipo Python | Formato | Nulidad | Descripcion |
| :--- | :--- | :--- | :--- | :--- |
| `timestamp` | `str` | ISO-8601 UTC: `YYYY-MM-DDTHH:MM:SSZ` | No nulo | Momento exacto del evento de feedback. |
| `sepal_length` | `float` | Decimal | No nulo | Valor ingresado por el usuario. |
| `sepal_width` | `float` | Decimal | No nulo | Valor ingresado por el usuario. |
| `petal_length` | `float` | Decimal | No nulo | Valor ingresado por el usuario. |
| `petal_width` | `float` | Decimal | No nulo | Valor ingresado por el usuario. |
| `predicted_species` | `str` | snake_case | No nulo | Clase que el modelo predijo y el usuario rechazo. |
| `confidence` | `float` | [0.0, 1.0] | No nulo | Confianza del modelo en la prediccion rechazada. |

### 7.2 Ejemplo de Registro Valido

```json
{"timestamp": "2026-04-19T15:30:00Z", "sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "predicted_species": "setosa", "confidence": 0.97}
```

---

## 8. Diccionario de Datos Tecnico

### 8.1 Variables de Dominio

| Variable Canonica | Descripcion Tecnica | Origen Biologico | Unidad | Rango Biologico Real | Rango Contrato Sistema |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `sepal_length` | Longitud del organo fotosintético exterior de la flor (sepalo). Feature con correlacion moderada con la especie. | Medicion fisica de la flor viva o preservada. | cm | [4.3, 7.9] | [3.0, 9.0] |
| `sepal_width` | Ancho del sepalo. Presenta solapamiento entre clases; outliers biologicamente validos detectados en FEASIBILITY. | Medicion fisica de la flor viva o preservada. | cm | [2.0, 4.4] | [1.5, 5.5] |
| `petal_length` | Longitud del petalo. Feature dominante (F-statistic: 1179). Setosa tiene petalos < 2.5 cm, completamente separada del resto. | Medicion fisica de la flor viva o preservada. | cm | [1.0, 6.9] | [0.5, 8.0] |
| `petal_width` | Ancho del petalo. Segunda feature mas discriminativa. Zona critica de solapamiento Versicolor/Virginica: [1.4, 1.8] cm. | Medicion fisica de la flor viva o preservada. | cm | [0.1, 2.5] | [0.0, 3.5] |
| `species` | Etiqueta de clase. Clasificacion taxonomica de la especie de Iris. | Pre-etiquetado por Ronald Fisher (1936). | - | {setosa, versicolor, virginica} | {setosa, versicolor, virginica} |

### 8.2 Estadisticas de Referencia por Feature (Dataset Silver, 147 registros)

Estas estadisticas son los parametros base para la deteccion de data drift en produccion.

| Feature | Media | Std | Min | Q25 | Q50 | Q75 | Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| sepal_length | 5.848 | 0.828 | 4.3 | 5.1 | 5.8 | 6.4 | 7.9 |
| sepal_width | 3.052 | 0.433 | 2.0 | 2.8 | 3.0 | 3.3 | 4.4 |
| petal_length | 3.758 | 1.764 | 1.0 | 1.6 | 4.3 | 5.1 | 6.9 |
| petal_width | 1.197 | 0.763 | 0.1 | 0.3 | 1.3 | 1.8 | 2.5 |

*Nota: Estadisticas derivadas del feasibility. Deben ser recalculadas sobre el dataset Silver definitivo en Phase Engineering y almacenadas en `data/gold/reference_stats.json` para uso en el modulo de drift detection.*

### 8.3 Matriz de Correlacion de Referencia

| | sepal_length | sepal_width | petal_length | petal_width |
| :--- | :--- | :--- | :--- | :--- |
| **sepal_length** | 1.000 | -0.109 | 0.872 | 0.818 |
| **sepal_width** | -0.109 | 1.000 | -0.421 | -0.357 |
| **petal_length** | 0.872 | -0.421 | 1.000 | 0.963 |
| **petal_width** | 0.818 | -0.357 | 0.963 | 1.000 |

*Alta correlacion petal_length/petal_width (0.963): correlacion biologica esperada, no data leakage.*

---

## 9. Politica de Nulos (Null Policy)

| Campo | Acepta Nulo | Valor Default | Estrategia si Nulo |
| :--- | :--- | :--- | :--- |
| `sepal_length` (inferencia) | No | No aplica | `ValidationError` inmediato. Fail-Fast. |
| `sepal_width` (inferencia) | No | No aplica | `ValidationError` inmediato. Fail-Fast. |
| `petal_length` (inferencia) | No | No aplica | `ValidationError` inmediato. Fail-Fast. |
| `petal_width` (inferencia) | No | No aplica | `ValidationError` inmediato. Fail-Fast. |
| `sepal_length` (training) | No | No aplica | El FEASIBILITY confirma 0 nulos. Si aparece nulo en Bronze, lanzar `ValueError` y detener el pipeline. No imputar en Phase Engineering. |
| `species` (training) | No | No aplica | Lanzar `ValueError`. Una etiqueta nula corrompe el entrenamiento. |
| `confidence` (feedback) | No | No aplica | `ValidationError`. El registro de feedback debe ser completo. |

**Politica General:** Este sistema NO implementa imputacion de valores nulos en ninguna capa. El dataset Iris esta 100% completo (verificado en FEASIBILITY). Si aparece un nulo en cualquier frontera del sistema, el comportamiento correcto es rechazar el dato, no imputarlo. La imputacion silenciosa enmascara problemas de calidad de datos.

---

## 10. Reglas de Validacion Matematica

### 10.1 Validaciones en Frontera de Inferencia (validators.py)

| ID Regla | Campo | Condicion de Validez | Expresion Matematica |
| :--- | :--- | :--- | :--- |
| VR-01 | sepal_length | Dentro de rango | `3.0 <= sepal_length <= 9.0` |
| VR-02 | sepal_width | Dentro de rango | `1.5 <= sepal_width <= 5.5` |
| VR-03 | petal_length | Dentro de rango | `0.5 <= petal_length <= 8.0` |
| VR-04 | petal_width | Dentro de rango | `0.0 <= petal_width <= 3.5` |
| VR-05 | Todos los campos | Tipo numerico | `isinstance(v, (int, float))` |
| VR-06 | Todos los campos | No NaN, no Inf | `not math.isnan(v) and not math.isinf(v)` |

*Nota: Pydantic v2 con `Field(ge=..., le=...)` implementa VR-01 a VR-04 automaticamente. VR-05 es aplicado por el tipo `float`. VR-06 debe ser agregado como `@field_validator` si Pydantic v2 no lo cubre por defecto en el modo estricto.*

### 10.2 Validaciones de Capa Bronze (bronze_loader.py)

| ID Regla | Condicion | Expresion |
| :--- | :--- | :--- |
| BR-01 | Numero de filas | `len(df) == 150` |
| BR-02 | Numero de columnas | `len(df.columns) == 6` |
| BR-03 | Cero nulos | `df.isnull().sum().sum() == 0` |
| BR-04 | Clases validas | `set(df['Species']) == {'Iris-setosa', 'Iris-versicolor', 'Iris-virginica'}` |

### 10.3 Validaciones de Capa Silver (silver_cleaner.py)

| ID Regla | Condicion | Expresion |
| :--- | :--- | :--- |
| SR-01 | Numero de filas | `len(df) == 147` |
| SR-02 | Columna Id ausente | `'Id' not in df.columns` |
| SR-03 | Nombres en snake_case | `list(df.columns) == ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']` |
| SR-04 | Etiquetas normalizadas | `set(df['species']) == {'setosa', 'versicolor', 'virginica'}` |
| SR-05 | Cero duplicados | `df.duplicated().sum() == 0` |

### 10.4 Validaciones de Capa Gold (gold_builder.py)

| ID Regla | Condicion | Expresion |
| :--- | :--- | :--- |
| GR-01 | Shape de X | `X.shape == (147, 4)` |
| GR-02 | Shape de y | `y.shape == (147,)` |
| GR-03 | Dtype de X | `X.dtype == np.float64` |
| GR-04 | Cero NaN en X | `np.isnan(X).sum() == 0` |
| GR-05 | Cero Inf en X | `np.isinf(X).sum() == 0` |
| GR-06 | Clases validas en y | `set(np.unique(y)) == {'setosa', 'versicolor', 'virginica'}` |

### 10.5 Validaciones del PredictionResult (predictor.py)

| ID Regla | Condicion | Expresion |
| :--- | :--- | :--- |
| PR-01 | Species valida | `result.species in {'setosa', 'versicolor', 'virginica'}` |
| PR-02 | Confidence en rango | `0.0 <= result.confidence <= 1.0` |
| PR-03 | Suma de probabilidades | `abs(sum(result.probabilities.values()) - 1.0) < 1e-6` |
| PR-04 | Coherencia confidence/species | `result.probabilities[result.species] == result.confidence` |
| PR-05 | Coherencia low_confidence | `result.low_confidence == (result.confidence < 0.60)` |
| PR-06 | Claves de probabilidades | `set(result.probabilities.keys()) == {'setosa', 'versicolor', 'virginica'}` |

---

## 11. Deteccion de Data Drift

### 11.1 Parametros Base (Training Distribution)

Los siguientes parametros se almacenan en `data/gold/reference_stats.json` al finalizar la Phase Engineering. Son la distribucion de referencia contra la cual se detecta drift en produccion.

```json
{
  "version": "1.0.0",
  "n_samples": 147,
  "features": {
    "sepal_length": {"mean": 5.848, "std": 0.828, "min": 4.3, "max": 7.9},
    "sepal_width":  {"mean": 3.052, "std": 0.433, "min": 2.0, "max": 4.4},
    "petal_length": {"mean": 3.758, "std": 1.764, "min": 1.0, "max": 6.9},
    "petal_width":  {"mean": 1.197, "std": 0.763, "min": 0.1, "max": 2.5}
  }
}
```

*Estos valores son aproximaciones del FEASIBILITY REPORT. Los valores exactos deben calcularse sobre el dataset Silver definitivo en Phase Engineering.*

### 11.2 Criterios de Alerta de Drift

En produccion (cuando el archivo `logs/feedback.log` tenga suficientes entradas), se considera que hay drift potencial si:

| Metrica | Criterio de Alerta | Accion |
| :--- | :--- | :--- |
| Media de cualquier feature | Desviacion > 2 std de la distribucion de referencia | Log de advertencia en el sistema. Considerar reentrenamiento en v2.0. |
| Porcentaje de predicciones con `low_confidence=True` | > 20% de las solicitudes recientes | Alerta de drift: el modelo puede estar fuera de distribucion. |
| Porcentaje de feedback negativo | > 10% de las solicitudes | Indicador de degradacion percibida por el usuario. |

*Nota: La implementacion del monitor de drift esta fuera del alcance de v1.0. Este documento establece los parametros base para que v2.0 pueda implementarlo sin redefinir el contrato.*

---

## 12. Mensajes de Error Estandarizados

Todos los mensajes de error visibles al usuario en la UI de Streamlit deben seguir este estandar. Los mensajes no deben exponer detalles de implementacion interna (stack traces, nombres de clases de Python, rutas de archivo).

| Codigo de Error | Condicion | Mensaje al Usuario (UI) | Nivel de Log Interno |
| :--- | :--- | :--- | :--- |
| `ERR-V01` | `sepal_length` fuera de rango | "Longitud del sepalo debe estar entre 3.0 y 9.0 cm." | WARNING |
| `ERR-V02` | `sepal_width` fuera de rango | "Ancho del sepalo debe estar entre 1.5 y 5.5 cm." | WARNING |
| `ERR-V03` | `petal_length` fuera de rango | "Longitud del petalo debe estar entre 0.5 y 8.0 cm." | WARNING |
| `ERR-V04` | `petal_width` fuera de rango | "Ancho del petalo debe estar entre 0.0 y 3.5 cm." | WARNING |
| `ERR-V05` | Tipo de dato invalido (no numerico) | "Por favor ingrese un valor numerico valido." | WARNING |
| `ERR-M01` | Modelo no encontrado en `models/` | "El modelo no esta disponible. Ejecute el pipeline de entrenamiento primero." | ERROR |
| `ERR-M02` | Fallo interno de prediccion | "Error interno al realizar la prediccion. Contacte al administrador." | ERROR |
| `ERR-F01` | Fallo al escribir feedback log | No mostrar al usuario. Solo log interno. | ERROR |
| `WARN-C01` | Confianza < 60% | "Resultado de baja confianza. Verifique las medidas ingresadas." | INFO |

---

## 13. Sensibilidad de Datos (PII)

| Campo | Categoria de Sensibilidad | Requiere Cifrado | Requiere Anonimizacion | Justificacion |
| :--- | :--- | :--- | :--- | :--- |
| `sepal_length`, `sepal_width`, `petal_length`, `petal_width` | No sensible | No | No | Mediciones fisicas de flores. No identifican personas. |
| `species` | No sensible | No | No | Clasificacion biologica publica. |
| Todos los campos de `FeedbackRecord` | No sensible | No | No | El sistema no captura ningun dato personal del usuario. No hay autenticacion. |

**Declaracion de Privacidad:** El sistema Flores AI - Iris v1.0 no recopila, almacena ni procesa datos personales identificables (PII). Los unicos datos persistidos son las mediciones de flores y las predicciones del modelo en `logs/feedback.log`. No se requieren medidas especiales de seguridad de datos personales.

---

## 14. Control de Versiones del Contrato

| Version | Fecha | Cambios | Impacto |
| :--- | :--- | :--- | :--- |
| `1.0.0` | 2026-04-19 | Version inicial. Contrato completo para las 4 capas de datos y los 2 contratos de inferencia. | Ninguno (version inicial). |

### Politica de Versionado

- **Cambio de version MAYOR** (e.g., 1.0.0 -> 2.0.0): Cambio en el esquema de campos (agregar/eliminar campos, cambiar tipos). Requiere Control de Cambios aprobado y actualizacion del SpecDD y SAD.
- **Cambio de version MENOR** (e.g., 1.0.0 -> 1.1.0): Cambio en rangos de validacion o mensajes de error. Requiere Control de Cambios aprobado.
- **Cambio de PATCH** (e.g., 1.0.0 -> 1.0.1): Correcciones de typos o aclaraciones de documentacion. No requiere Control de Cambios formal.

---

## 15. Check de Certificacion del Contrato

| Criterio | Estado | Evidencia |
| :--- | :--- | :--- |
| El esquema de entrada de inferencia (IrisInput) coincide exactamente con el SpecDD | Aprobado | Seccion 5 de este documento vs. Seccion 1.1 y Seccion 3 del SpecDD. Tipos y rangos identicos. |
| Se han definido mensajes de error claros cuando la validacion del esquema falla | Aprobado | Seccion 12 define el catalogo completo de mensajes de error con codigos. |
| El contrato de datos es compartido y aceptado por el Data Engineer y el ML Engineer | Pendiente | Debe ser firmado digitalmente al inicio de Phase Engineering y Phase Modeling respectivamente. |
| Se han definido los invariantes matematicos para cada capa de datos | Aprobado | Secciones 2.2, 3.2, 4.3, 10.1-10.5 definen las condiciones exactas. |
| Se ha definido la politica de nulos por campo | Aprobado | Seccion 9 cubre todos los campos en todas las capas. |
| Se han definido los parametros base de referencia para deteccion de drift | Aprobado | Seccion 11.1 define los estadisticos de referencia del training set. |
| La sensibilidad de datos (PII) ha sido auditada | Aprobado | Seccion 13 confirma: ningun campo contiene PII. No se requieren medidas especiales. |
| El contrato tiene version y politica de versionado definida | Aprobado | Seccion 14. Version inicial: 1.0.0. |

---

> **Nota de Gobernanza:** Este documento es vinculante para los agentes `ai-data-engineer` (Phase Engineering) y `ai-ml-engineer` (Phase Modeling). Ninguna transformacion de datos o proceso de entrenamiento puede producir esquemas que violen los invariantes aqui definidos. Cualquier desviacion debe pasar por el Protocolo de Control de Cambios antes de ser implementada. El `ai-solutions-architect` es el unico agente con autoridad para modificar este documento.
>
> **Trazabilidad:** DATA_CONTRACT v1.0.0 <- SpecDD v1.0.0 <- SAD v1.0.0 <- BRD v1.0.0 <- feasibility v1.0.0
