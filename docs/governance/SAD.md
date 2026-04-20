# Software Architecture Document (SAD)
## Proyecto: Flores AI - Iris

> **Documento:** Software Architecture Document (SAD)
> **Version:** 1.0.0
> **Estado:** Aprobado - Phase Discovery Discovery
> **Fecha de creacion:** 2026-04-19
> **Ultima actualizacion:** 2026-04-19
> **Autor:** ai-solutions-architect
> **Trazabilidad:** BRD v1.0.0 -> feasibility v1.0.0 -> SAD v1.0.0
> **Repositorio:** https://github.com/jdrodriguez1000/Flores_AI.git

---

## Indice

1. [Vision General de la Arquitectura](#1-vision-general-de-la-arquitectura)
2. [Diagrama de Componentes - C4 Nivel 2](#2-diagrama-de-componentes---c4-nivel-2)
3. [Diagrama de Flujo de Datos](#3-diagrama-de-flujo-de-datos)
4. [Stack Tecnologico Definitivo](#4-stack-tecnologico-definitivo)
5. [Estructura de Modulos src/](#5-estructura-de-modulos-src)
6. [Contratos de Comunicacion entre Modulos](#6-contratos-de-comunicacion-entre-modulos)
7. [Architecture Decision Records (ADR)](#7-architecture-decision-records-adr)
8. [Requisitos No Funcionales](#8-requisitos-no-funcionales)
9. [Estrategia de Testing](#9-estrategia-de-testing)
10. [Check de Certificacion Arquitectonica](#10-check-de-certificacion-arquitectonica)

---

## 1. Vision General de la Arquitectura

### 1.1 Patron Arquitectonico Elegido: Monolito Modular con Medallion Architecture

**Patron seleccionado:** Monolito Modular con separacion de capas de datos Medallion (Bronze / Silver / Gold).

**Justificacion tecnica:**

| Criterio | Evaluacion |
| :--- | :--- |
| Tamano del equipo | 1 desarrollador + agentes de IA especializados. Un monolito modular elimina la sobrecarga operativa de microservicios. |
| Volumen de datos | 150 registros estaticos. No existe justificacion tecnica para una arquitectura distribuida. |
| Latencia requerida | <= 3,000 ms para prediccion. El modelo scikit-learn sobre datos tabulares es sub-milisegundo; la latencia es dominada por el render de Streamlit, no por la inferencia. |
| Escalabilidad futura | El patron modular garantiza que cada capa (ingesta, limpieza, features, modelo, UI) puede ser extraida a un servicio independiente sin reescribir logica de negocio. |
| Desacoplamiento del modelo | La capa de inferencia (`predictor.py`) no conoce nada de la UI. La UI (`app.py`) no conoce nada del pipeline de datos. El modelo puede ser reemplazado modificando unicamente el artefacto serializado y su wrapper. |

**Regla "Decoupling is King" aplicada:**

El modelo de ML puede ser reemplazado (e.g., de RandomForest a SVM) modificando exclusivamente:
1. El artefacto en `models/` (nuevo archivo `.joblib`).
2. La configuracion de ruta en `src/config.py`.

Ningun cambio en `src/app.py`, `src/data/`, ni en `tests/` es necesario si la firma de `predict()` se mantiene invariante.

### 1.2 Principios Arquitectonicos Vinculantes

| Principio | Implementacion |
| :--- | :--- |
| **Decoupling is King** | `app.py` solo invoca `predictor.predict()`. No importa nada de `data/` ni de `training/`. |
| **Strict Typing** | Todos los modulos usan Pydantic v2 para validacion de entrada. Ninguna funcion acepta `dict` no tipado en sus fronteras. |
| **Fail-Fast Design** | La validacion de rango ocurre en `validators.py` antes de que el tensor llegue al modelo. El modelo nunca recibe datos fuera de contrato. |
| **Spec Before Code** | Ningun archivo `.py` en `src/` se crea sin su seccion correspondiente en `specdd.md`. |
| **Rutas Relativas** | `pathlib.Path(__file__).parent` es el unico mecanismo de resolucion de rutas. Cero strings hardcodeados. |

---

## 2. Diagrama de Componentes - C4 Nivel 2

### 2.1 Diagrama de Contenedores (C4 Level 1 - Contexto)

```
+-----------------------------------------------------------+
|                    USUARIO FINAL                          |
|   (Persona sin conocimiento tecnico, accede via browser)  |
+----------------------------+------------------------------+
                             |
                    HTTP / localhost:8501
                             |
+----------------------------v------------------------------+
|                  SISTEMA: Flores AI - Iris                |
|                                                           |
|   +---------------------------------------------------+   |
|   |          Aplicacion Streamlit (src/app.py)        |   |
|   |   - Formulario de entrada (4 features)            |   |
|   |   - Validacion de rangos (src/validators.py)      |   |
|   |   - Visualizacion de probabilidades               |   |
|   |   - Sistema de feedback (logs/feedback.log)       |   |
|   +-------------------+-------------------------------+   |
|                       |                                   |
|          Llama a: predictor.predict()                     |
|                       |                                   |
|   +-------------------v-------------------------------+   |
|   |          Motor de Inferencia (src/predictor.py)   |   |
|   |   - Carga modelo desde models/                    |   |
|   |   - Aplica scaler (si aplica)                     |   |
|   |   - Retorna clase + probabilidades                |   |
|   +-------------------+-------------------------------+   |
|                       |                                   |
|          Lee: modelo serializado (.joblib)                |
|                       |                                   |
|   +-------------------v-------------------------------+   |
|   |   Artefacto de Modelo (models/iris_model.joblib)  |   |
|   |   - Pipeline scikit-learn (Scaler + Clasificador) |   |
|   +---------------------------------------------------+   |
|                                                           |
|   [Pipeline de Datos - Offline, ejecutado en Phase Engineering/3]   |
|   +---------------------------------------------------+   |
|   | Bronze Loader -> Silver Cleaner -> Gold Builder   |   |
|   | -> Model Trainer -> Model Serializer              |   |
|   +---------------------------------------------------+   |
|                                                           |
+-----------------------------------------------------------+
```

### 2.2 Diagrama de Componentes del Pipeline de Datos (C4 Level 2)

```
+------------------------------------------------------------------+
|                    PIPELINE DE DATOS (Offline)                   |
|                                                                  |
|  +--------------------+                                          |
|  |  Bronze Loader     |  Entrada: data/bronze/Iris.csv           |
|  |  src/data/         |  Salida:  pd.DataFrame (raw, 150x6)      |
|  |  bronze_loader.py  |  Accion:  Leer CSV, sin transformaciones |
|  +--------+-----------+                                          |
|           | DataFrame(150 rows, 6 cols, raw dtypes)              |
|           v                                                      |
|  +--------+-----------+                                          |
|  |  Silver Cleaner    |  Entrada: DataFrame raw                  |
|  |  src/data/         |  Salida:  pd.DataFrame (clean, 147x5)    |
|  |  silver_cleaner.py |  Acciones:                               |
|  |                    |    - Eliminar columna Id (M-01)          |
|  |                    |    - Eliminar 3 near-duplicates (M-02)   |
|  |                    |    - Renombrar a snake_case (M-03)       |
|  |                    |    - Normalizar etiquetas (M-04)         |
|  +--------+-----------+                                          |
|           | DataFrame(147 rows, 5 cols, clean dtypes)            |
|           v                                                      |
|  +--------+-----------+                                          |
|  |  Gold Builder      |  Entrada: DataFrame silver               |
|  |  src/data/         |  Salida:  X (np.ndarray), y (np.ndarray) |
|  |  gold_builder.py   |  Acciones:                               |
|  |                    |    - Separar features/target             |
|  |                    |    - Guardar data/gold/X_gold.csv        |
|  |                    |    - Guardar data/gold/y_gold.csv        |
|  +--------+-----------+                                          |
|           | X: ndarray(147, 4), y: ndarray(147,)                |
|           v                                                      |
|  +--------+-----------+                                          |
|  |  Model Trainer     |  Entrada: X, y                           |
|  |  src/training/     |  Salida:  sklearn.Pipeline entrenado     |
|  |  trainer.py        |  Acciones:                               |
|  |                    |    - Train/test split (80/20, seed=42)   |
|  |                    |    - Construir Pipeline(Scaler + Model)  |
|  |                    |    - K-Fold CV (k=5)                     |
|  |                    |    - Calcular metricas (Accuracy, F1)    |
|  +--------+-----------+                                          |
|           | sklearn.Pipeline (fitted)                            |
|           v                                                      |
|  +--------+-----------+                                          |
|  |  Model Serializer  |  Entrada: sklearn.Pipeline               |
|  |  src/training/     |  Salida:  models/iris_model.joblib       |
|  |  serializer.py     |  Accion:  joblib.dump() al path relativo |
|  +--------------------+                                          |
|                                                                  |
+------------------------------------------------------------------+

+------------------------------------------------------------------+
|                    PIPELINE DE INFERENCIA (Online)               |
|                                                                  |
|  +--------------------+                                          |
|  |  Streamlit App     |  Entrada: 4 floats via formulario HTML   |
|  |  src/app.py        |  Salida:  HTML renderizado               |
|  |                    |  Acciones:                               |
|  |                    |    - st.cache_resource -> cargar modelo  |
|  |                    |    - Invocar validators.validate_input() |
|  |                    |    - Invocar predictor.predict()         |
|  |                    |    - Renderizar resultado + probabilidades|
|  |                    |    - Gestionar boton de feedback         |
|  +--------+-----------+                                          |
|           |                                                      |
|           | IrisInput (Pydantic model)                           |
|           v                                                      |
|  +--------+-----------+                                          |
|  |  Input Validator   |  Entrada: IrisInput                      |
|  |  src/validators.py |  Salida:  IrisInput validado             |
|  |                    |  Falla:   ValidationError (Pydantic)     |
|  +--------+-----------+                                          |
|           | IrisInput (validado y dentro de rango)               |
|           v                                                      |
|  +--------+-----------+                                          |
|  |  Predictor         |  Entrada: IrisInput                      |
|  |  src/predictor.py  |  Salida:  PredictionResult (Pydantic)    |
|  |                    |  Acciones:                               |
|  |                    |    - Convertir a np.ndarray              |
|  |                    |    - pipeline.predict() + predict_proba()|
|  |                    |    - Retornar clase + probabilidades      |
|  +--------+-----------+                                          |
|           | PredictionResult                                     |
|           v                                                      |
|  +--------+-----------+                                          |
|  |  Feedback Logger   |  Entrada: IrisInput + PredictionResult   |
|  |  src/feedback.py   |  Salida:  logs/feedback.log (append)     |
|  |                    |  Trigger: Boton "Prediccion incorrecta"  |
|  +--------------------+                                          |
|                                                                  |
+------------------------------------------------------------------+
```

---

## 3. Diagrama de Flujo de Datos

### 3.1 Flujo Offline: Construccion del Artefacto de Modelo

```
data/bronze/Iris.csv
        |
        | pd.read_csv() — sin transformaciones
        v
[BRONZE LAYER] DataFrame(150, 6) — raw
  Columnas: Id, SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm, Species
  Tipos: int64, float64x4, object
        |
        | M-01: drop('Id')
        | M-02: drop_duplicates() -> 147 rows
        | M-03: rename(snake_case)
        | M-04: normalize labels ('Iris-setosa' -> 'setosa')
        v
[SILVER LAYER] DataFrame(147, 5) — clean
  Columnas: sepal_length, sepal_width, petal_length, petal_width, species
  Tipos: float64x4, object
  Guardado en: data/silver/iris_silver.csv
        |
        | Separacion X / y
        | X = df[['sepal_length','sepal_width','petal_length','petal_width']]
        | y = df['species']
        v
[GOLD LAYER] X: ndarray(147, 4), y: ndarray(147,)
  Guardado en: data/gold/X_gold.csv, data/gold/y_gold.csv
        |
        | train_test_split(test_size=0.20, random_state=42, stratify=y)
        | Pipeline(steps=[('scaler', StandardScaler()), ('clf', <Modelo>)])
        | K-Fold CV (k=5, scoring='accuracy')
        v
[MODELO ENTRENADO] sklearn.Pipeline (fitted)
  Contiene: scaler ajustado + clasificador ajustado
        |
        | joblib.dump()
        v
models/iris_model.joblib
```

### 3.2 Flujo Online: Inferencia en Tiempo Real

```
Usuario ingresa 4 valores en formulario Streamlit
        |
        | IrisInput(sepal_length=?, sepal_width=?, petal_length=?, petal_width=?)
        v
[VALIDACION] validators.validate_input(IrisInput)
  - sepal_length: [3.0, 9.0]
  - sepal_width:  [1.5, 5.5]
  - petal_length: [0.5, 8.0]
  - petal_width:  [0.0, 3.5]
  Si FALLA -> ValidationError -> UI muestra mensaje rojo, TERMINA
        |
        | IrisInput validado
        v
[INFERENCIA] predictor.predict(IrisInput, pipeline)
  - numpy array shape (1, 4)
  - pipeline.predict() -> ['setosa']
  - pipeline.predict_proba() -> [[0.95, 0.03, 0.02]]
        |
        | PredictionResult(species='setosa', confidence=0.95, probabilities={...})
        v
[RENDER UI]
  - Mostrar: especie predicha
  - Si confidence < 0.60: mostrar advertencia de baja confianza
  - Grafico de barras: probabilidades de las 3 clases
  - Boton: "Esta prediccion es incorrecta"
        |
        | Si usuario hace clic en feedback
        v
[FEEDBACK LOGGER] feedback.log_feedback(IrisInput, PredictionResult)
  Escribe en logs/feedback.log:
  {timestamp, sepal_length, sepal_width, petal_length, petal_width, predicted_species, confidence}
```

---

## 4. Stack Tecnologico Definitivo

### 4.1 Dependencias de Produccion

| Libreria | Version Recomendada | Capa de Uso | Justificacion |
| :--- | :--- | :--- | :--- |
| `python` | 3.12.x | Global | Mandatorio por CLAUDE.md |
| `streamlit` | 1.35.x | UI / App | Mandatorio por BRD. Framework de interfaz web. |
| `scikit-learn` | 1.5.x | ML / Training / Inference | Pipeline, clasificadores, metricas, StandardScaler. Compatible Python 3.12. |
| `pandas` | 2.2.x | Data Pipeline | Lectura CSV, transformaciones DataFrame en capas Bronze y Silver. |
| `numpy` | 1.26.x | Data / Inference | Conversion de arrays para inferencia. Dependencia de scikit-learn. |
| `joblib` | 1.4.x | Model Serialization | Formato de serializacion primario. Mas eficiente que pickle para arrays numpy. |
| `pydantic` | 2.7.x | Validation | Modelos de datos tipados estrictos para IrisInput y PredictionResult. Fail-Fast en frontera. |
| `plotly` | 5.22.x | Visualization | Grafico de barras de probabilidades en Streamlit. Compatible con `st.plotly_chart`. |

### 4.2 Dependencias de Desarrollo y Testing

| Libreria | Version Recomendada | Proposito |
| :--- | :--- | :--- |
| `pytest` | 8.2.x | Framework de testing unitario e integrado. |
| `pytest-cov` | 5.0.x | Medicion de cobertura de tests (objetivo >= 80%). |
| `black` | 24.x | Formateo automatico de codigo (PEP 8). |
| `isort` | 5.13.x | Ordenamiento de imports. |

### 4.3 Versiones de compatibilidad verificadas

Todas las versiones listadas son compatibles entre si bajo Python 3.12 segun la matriz de compatibilidad de scikit-learn 1.5 y Streamlit 1.35. El archivo `requirements.txt` en la raiz del proyecto es la unica fuente de verdad para versiones instaladas.

---

## 5. Estructura de Modulos src/

Esta es la topologia definitiva de archivos `.py` que existiran en produccion. Cada archivo es la unidad de contrato para el SpecDD.

```
src/
├── config.py                   # Rutas relativas y constantes del proyecto (pathlib)
├── app.py                      # Punto de entrada Streamlit. Orquesta UI completa.
├── validators.py               # Validacion de rangos de entrada. Pydantic v2.
├── predictor.py                # Motor de inferencia. Carga modelo, ejecuta predict().
├── feedback.py                 # Logger de feedback de usuario. Escribe feedback.log.
├── data/
│   ├── __init__.py
│   ├── bronze_loader.py        # Lectura del CSV crudo desde data/bronze/.
│   ├── silver_cleaner.py       # Limpieza: drop Id, dedup, rename, normalize labels.
│   └── gold_builder.py         # Construccion de X, y. Guarda data/gold/.
└── training/
    ├── __init__.py
    ├── trainer.py              # Construccion del Pipeline, train/test split, CV.
    └── serializer.py           # Serializacion del modelo entrenado en models/.
```

### 5.1 Responsabilidad Unica de Cada Modulo

| Modulo | Responsabilidad Unica | Prohibiciones |
| :--- | :--- | :--- |
| `config.py` | Exponer rutas y constantes como objetos `pathlib.Path`. | No contiene logica. No importa pandas, sklearn, ni streamlit. |
| `app.py` | Renderizar la UI de Streamlit. Conectar validators y predictor. | No implementa logica de ML. No lee archivos CSV directamente. |
| `validators.py` | Definir `IrisInput` (Pydantic) y validar rangos. Retornar `IrisInput` validado o lanzar `ValidationError`. | No conoce el modelo. No tiene acceso a datos historicos. |
| `predictor.py` | Cargar el pipeline serializado. Ejecutar `predict()` y `predict_proba()`. Retornar `PredictionResult`. | No renderiza UI. No escribe archivos. No transforma datos de entrenamiento. |
| `feedback.py` | Recibir `IrisInput` + `PredictionResult` y escribir un registro JSON en `logs/feedback.log`. | No hace predicciones. No valida entradas. |
| `bronze_loader.py` | Leer `data/bronze/Iris.csv` y retornar DataFrame raw. | No realiza ninguna transformacion. Solo lectura. |
| `silver_cleaner.py` | Recibir DataFrame raw y retornar DataFrame limpio (147x5, snake_case, labels normalizados). | No construye features. No entrena modelos. |
| `gold_builder.py` | Separar X e y del DataFrame Silver. Guardar en `data/gold/`. | No limpia datos. No entrena modelos. |
| `trainer.py` | Construir y ajustar el Pipeline de scikit-learn. Retornar pipeline fitted + metricas de CV. | No serializa. No carga datos crudos. |
| `serializer.py` | Recibir pipeline fitted y guardarlo en `models/iris_model.joblib`. | No entrena. No evalua metricas. |

---

## 6. Contratos de Comunicacion entre Modulos

### 6.1 Tipos de Datos Compartidos (Pydantic v2)

Los siguientes tipos son los contratos de frontera. Estan definidos aqui como especificacion; su implementacion precisa se documenta en `specdd.md`.

**IrisInput** — Contrato de entrada de usuario:
```
IrisInput:
  sepal_length: float   # Rango valido: [3.0, 9.0] cm
  sepal_width:  float   # Rango valido: [1.5, 5.5] cm
  petal_length: float   # Rango valido: [0.5, 8.0] cm
  petal_width:  float   # Rango valido: [0.0, 3.5] cm
```

**PredictionResult** — Contrato de salida de inferencia:
```
PredictionResult:
  species:       str              # Clase predicha: 'setosa' | 'versicolor' | 'virginica'
  confidence:    float            # Probabilidad maxima: [0.0, 1.0]
  probabilities: dict[str, float] # {'setosa': 0.95, 'versicolor': 0.03, 'virginica': 0.02}
  low_confidence: bool            # True si confidence < 0.60
```

**FeedbackRecord** — Contrato de registro de feedback:
```
FeedbackRecord:
  timestamp:         str   # ISO-8601
  sepal_length:      float
  sepal_width:       float
  petal_length:      float
  petal_width:       float
  predicted_species: str
  confidence:        float
```

### 6.2 Formas de DataFrames por Capa

| Capa | Filas | Columnas | Tipos | Archivo Persistido |
| :--- | :--- | :--- | :--- | :--- |
| Bronze | 150 | 6: Id, SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm, Species | int64, float64x4, object | `data/bronze/Iris.csv` (lectura) |
| Silver | 147 | 5: sepal_length, sepal_width, petal_length, petal_width, species | float64x4, object | `data/silver/iris_silver.csv` |
| Gold X | 147 | 4: sepal_length, sepal_width, petal_length, petal_width | float64x4 | `data/gold/X_gold.csv` |
| Gold y | 147 | 1: species | object (str) | `data/gold/y_gold.csv` |

### 6.3 Mapa de Dependencias entre Modulos

```
config.py
    ^--- importado por: bronze_loader, silver_cleaner, gold_builder,
                        trainer, serializer, predictor, feedback, app

bronze_loader.py -> silver_cleaner.py -> gold_builder.py -> trainer.py -> serializer.py
                                                                  (pipeline offline)

app.py -> validators.py -> predictor.py
app.py -> feedback.py
                                                                  (pipeline online)
```

Regla arquitectonica: Ningun modulo del pipeline online (`app`, `validators`, `predictor`, `feedback`) importa nada del pipeline offline (`bronze_loader`, `silver_cleaner`, `gold_builder`, `trainer`, `serializer`). La unica interfaz entre ambos es el artefacto `models/iris_model.joblib`.

---

## 7. Architecture Decision Records (ADR)

### ADR-001: Eleccion de Streamlit como Framework de UI

| Campo | Valor |
| :--- | :--- |
| **ID** | ADR-001 |
| **Titulo** | Adopcion de Streamlit como unico framework de interfaz web |
| **Estado** | Aprobado |
| **Fecha** | 2026-04-19 |
| **Autor** | ai-solutions-architect |

**Contexto:** El BRD requiere una aplicacion web que permita a usuarios sin conocimiento tecnico ingresar 4 valores numericos, recibir una prediccion y visualizar probabilidades. La restriccion RT2 del BRD establece Streamlit como framework mandatorio.

**Decision:** Utilizar Streamlit como framework de interfaz web integrado (frontend + backend en un mismo proceso Python). No se implementara una API REST separada (excluido en BRD, seccion 6.2, OS7).

**Consecuencias positivas:**
- Tiempo de desarrollo reducido: un solo archivo `app.py` maneja toda la UI.
- Despliegue simplificado: `streamlit run src/app.py` es el unico comando de arranque (criterio CA09 del BRD).
- Comparticion de estado trivial: `st.cache_resource` garantiza que el modelo se cargue una sola vez (mitigacion RT4 del BRD).

**Consecuencias negativas:**
- Personalizacion visual limitada respecto a React/Vue.
- Si en una iteracion futura (v2.0) se requiere una API REST independiente, `app.py` debera ser refactorizado y `predictor.py` extraido como servicio. El diseno modular actual facilita esta migracion.

**Alternativas rechazadas:**
- Flask/FastAPI + frontend separado: sobrecarga de infraestructura injustificada para un dataset de 150 registros y un equipo de 1 persona.
- Gradio: menor ecosistema de visualizaciones y menor familiaridad en el stack del equipo.

---

### ADR-002: Eleccion de Joblib como Formato de Serializacion del Modelo

| Campo | Valor |
| :--- | :--- |
| **ID** | ADR-002 |
| **Titulo** | Serializacion del pipeline scikit-learn con Joblib |
| **Estado** | Aprobado |
| **Fecha** | 2026-04-19 |
| **Autor** | ai-solutions-architect |

**Contexto:** El BRD (RT4) permite Pickle o Joblib. El modelo serializado es un `sklearn.Pipeline` que contiene arrays numpy (el StandardScaler almacena `mean_` y `scale_` como arrays). Se requiere portabilidad total del repositorio.

**Decision:** Utilizar `joblib.dump()` / `joblib.load()` para serializar y deserializar el pipeline entrenado. El artefacto se almacena en `models/iris_model.joblib`.

**Justificacion tecnica:**
- Joblib esta optimizado para la serializacion eficiente de arrays numpy grandes (mmap, compresion). Aunque el modelo Iris es pequeño, el patron es correcto para escalar.
- Joblib es la forma recomendada por la documentacion oficial de scikit-learn para persistir modelos.
- Pickle es la alternativa pero tiene riesgo de incompatibilidades de version entre Python 3.x menor a 3.x cuando el repositorio es compartido.

**Consecuencias:** El archivo `models/iris_model.joblib` es el unico artefacto de modelo certificado. El `serializer.py` no permite multiples formatos de salida para evitar ambiguedad sobre cual version es la activa.

**Alternativas rechazadas:**
- ONNX: Requiere conversion del pipeline sklearn a ONNX, que introduce una capa de complejidad injustificada para un modelo de portafolio que nunca se desplegara en un runtime ONNX puro.
- Pickle nativo: Descartado por la nota de la documentacion scikit-learn que recomienda Joblib sobre Pickle para modelos con arrays numpy.

---

### ADR-003: Estrategia de Feature Scaling

| Campo | Valor |
| :--- | :--- |
| **ID** | ADR-003 |
| **Titulo** | StandardScaler encapsulado en sklearn.Pipeline como estrategia de Feature Scaling |
| **Estado** | Aprobado |
| **Fecha** | 2026-04-19 |
| **Autor** | ai-solutions-architect |

**Contexto:** La M-06 del feasibility indica que los algoritmos basados en distancia (SVM, KNN) requieren Feature Scaling, mientras que los basados en arboles (Random Forest, Decision Tree) no lo requieren. La Phase Modeling explorara multiples algoritmos. El riesgo RT3 del BRD alerta sobre Data Leakage si el scaler se ajusta con datos de test.

**Decision:** El StandardScaler se incluye **siempre** en el `sklearn.Pipeline`, independientemente del algoritmo elegido en Phase Modeling. El Pipeline garantiza que el `scaler.fit()` solo ocurre sobre `X_train`. La llamada `pipeline.predict()` aplica automaticamente la transformacion sobre datos nuevos.

**Justificacion:**
- Elimina completamente el riesgo de Data Leakage (RT3 del BRD) porque el Pipeline aplica `transform` en `predict` usando los parametros ajustados solo en `fit`.
- Unifica el contrato de serializacion: un solo objeto `Pipeline` contiene tanto el preprocesamiento como el modelo. `predictor.py` no necesita conocer si el scaler fue aplicado o no.
- StandardScaler es robusto ante las distribuciones del dataset Iris (segun el FEASIBILITY REPORT, ninguna feature tiene distribucion extremadamente asimetrica que justifique MinMaxScaler).
- Si en Phase Modeling se selecciona un modelo basado en arboles, el StandardScaler no perjudica el rendimiento (los arboles son invariantes a escalado monotono); si se selecciona SVM o KNN, el escalado es critico para alcanzar el KPI de Accuracy >= 95%.

**Consecuencias:** El scaler esta encapsulado en el artefacto `models/iris_model.joblib`. El `predictor.py` recibe un `IrisInput` con valores en cm (no escalados) y el pipeline aplica el escalado internamente. La UI nunca conoce que existe un scaler.

**Alternativas rechazadas:**
- Aplicar scaling fuera del Pipeline en `silver_cleaner.py` o `gold_builder.py`: Rechazado por riesgo de Data Leakage si los datos de test son transformados usando estadisticas del dataset completo.
- MinMaxScaler: Rechazado porque es mas sensible a outliers. El FEASIBILITY detecta outliers en SepalWidthCm. StandardScaler es mas robusto en este contexto.
- No aplicar scaling: Rechazado porque la Phase Modeling debe evaluar SVM y KNN como candidatos, y estos requieren datos escalados para alcanzar el KPI de Accuracy >= 95%.

---

### ADR-004: Estrategia de Configuracion de Rutas (pathlib vs. variables de entorno)

| Campo | Valor |
| :--- | :--- |
| **ID** | ADR-004 |
| **Titulo** | Uso de pathlib.Path para resolucion de rutas relativas |
| **Estado** | Aprobado |
| **Fecha** | 2026-04-19 |
| **Autor** | ai-solutions-architect |

**Contexto:** El CLAUDE.md y el BRD (RT5) prohiben el uso de rutas absolutas. El sistema debe poder ejecutarse desde cualquier directorio clonando el repositorio.

**Decision:** Crear `src/config.py` como modulo centralizador de todas las rutas del proyecto. Las rutas se calculan dinamicamente usando `pathlib.Path(__file__).resolve().parent.parent` para navegar desde `src/config.py` hasta la raiz del proyecto.

**Ejemplo de implementacion (especificacion, no codigo productivo):**
```
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_BRONZE  = PROJECT_ROOT / "data" / "bronze" / "Iris.csv"
DATA_SILVER  = PROJECT_ROOT / "data" / "silver" / "iris_silver.csv"
DATA_GOLD_X  = PROJECT_ROOT / "data" / "gold" / "X_gold.csv"
DATA_GOLD_Y  = PROJECT_ROOT / "data" / "gold" / "y_gold.csv"
MODEL_PATH   = PROJECT_ROOT / "models" / "iris_model.joblib"
FEEDBACK_LOG = PROJECT_ROOT / "logs" / "feedback.log"
```

**Consecuencias:** Ningun otro modulo en `src/` hardcodea rutas. Todos importan las constantes de `config.py`. Si el repositorio se mueve a otro directorio, solo `config.py` necesita verificacion (y en este diseno no necesita cambios porque usa rutas relativas dinamicas).

---

## 8. Requisitos No Funcionales

### 8.1 Rendimiento y Latencia

| Requisito | Valor | Estrategia de Cumplimiento |
| :--- | :--- | :--- |
| Latencia de prediccion | <= 3,000 ms (objetivo <= 1,000 ms) | `st.cache_resource` para cargar el pipeline una sola vez. La inferencia sklearn sobre (1,4) es sub-milisegundo. |
| Tiempo de arranque de la app | <= 10 segundos | El modelo `.joblib` tiene < 1 MB. La carga en arranque es instantanea. |
| Tiempo de ejecucion del pipeline offline | Sin restriccion critica | Dataset de 147 registros. El pipeline completo ejecuta en < 5 segundos. |

### 8.2 Disponibilidad

| Requisito | Valor | Alcance |
| :--- | :--- | :--- |
| Uptime | >= 95% (objetivo >= 99%) | Alcance: despliegue local. No aplica SLA de cloud. El uptime depende del hardware del usuario. |
| Recuperacion ante error | La aplicacion no debe mostrar tracebacks de Python al usuario final | Implementado via manejo de excepciones en `app.py` que captura `ValidationError` y cualquier excepcion de `predictor.py`. |

### 8.3 Seguridad y Portabilidad

| Requisito | Implementacion |
| :--- | :--- |
| Cero rutas absolutas en codigo | Todas las rutas via `src/config.py` con `pathlib`. Verificado en code review. |
| Cero credenciales hardcodeadas | El proyecto no conecta a servicios externos. No existen credenciales. Si se agregan en futuras versiones, deben ir en `.env` (excluido del repositorio via `.gitignore`). |
| Portabilidad del repositorio | El repositorio debe poder clonarse y ejecutarse con `pip install -r requirements.txt` + `streamlit run src/app.py` sin configuracion adicional. |
| Reproducibilidad del entrenamiento | `random_state=42` en todos los metodos estocasticos (`train_test_split`, `KFold`, clasificadores que lo soporten). |

### 8.4 Mantenibilidad

| Requisito | Implementacion |
| :--- | :--- |
| Cobertura de tests >= 80% | Medida con `pytest-cov`. Reportada en Phase Delivery. |
| Trazabilidad SpecDD | 100% de las funciones en `src/` tienen su firma definida en `specdd.md` antes de ser implementadas. |
| Linaje de datos | Cada capa de datos (Bronze, Silver, Gold) tiene su archivo persistido en `data/`. El pipeline es reproducible ejecutando los modulos en orden. |

---

## 9. Estrategia de Testing

### 9.1 Estructura de la Suite de Tests

```
tests/
├── unit/
│   ├── test_config.py              # Verifica que las rutas de config.py existen
│   ├── test_validators.py          # Prueba IrisInput: valores validos, invalidos, limites
│   ├── test_predictor.py           # Prueba predict() con modelo mock o fixture
│   ├── test_feedback.py            # Prueba que feedback.log recibe el formato correcto
│   ├── data/
│   │   ├── test_bronze_loader.py   # Verifica schema del DataFrame raw (6 cols, 150 rows, tipos)
│   │   ├── test_silver_cleaner.py  # Verifica transformaciones M-01 a M-04
│   │   └── test_gold_builder.py    # Verifica forma de X e y, persistencia en data/gold/
│   └── training/
│       ├── test_trainer.py         # Verifica que el Pipeline entrena y produce metricas
│       └── test_serializer.py      # Verifica que el archivo .joblib se crea y puede cargarse
├── integration/
│   └── test_pipeline_e2e.py        # Bronze -> Silver -> Gold -> Trainer -> Serializer -> Predictor
└── model_qa/
    └── test_model_performance.py   # Verifica Accuracy >= 95%, F1 >= 0.95 (usa el modelo certificado)
```

### 9.2 Tipos de Tests por Modulo

| Modulo | Tipo de Test | Criterio de Exito |
| :--- | :--- | :--- |
| `config.py` | Unit | Las rutas `DATA_BRONZE`, `MODEL_PATH`, etc. resuelven a paths existentes. |
| `validators.py` | Unit | `validate_input()` retorna `IrisInput` con valores validos; lanza `ValidationError` con valores fuera de rango, negativos, o tipo incorrecto. |
| `predictor.py` | Unit | `predict()` retorna `PredictionResult` con `species` en `{'setosa','versicolor','virginica'}` y `confidence` en `[0,1]`. Usar fixture de pipeline. |
| `feedback.py` | Unit | `log_feedback()` escribe una linea JSON valida en el archivo de log. Verificar estructura del JSON. |
| `bronze_loader.py` | Unit | El DataFrame retornado tiene shape `(150, 6)`, columnas correctas, tipos correctos, cero nulos. |
| `silver_cleaner.py` | Unit | El DataFrame retornado tiene shape `(147, 5)`, nombres snake_case, etiquetas sin prefijo `Iris-`, sin columna `Id`. |
| `gold_builder.py` | Unit | `X` tiene shape `(147, 4)` dtype float64. `y` tiene shape `(147,)`. Los archivos gold existen en `data/gold/`. |
| `trainer.py` | Unit | El Pipeline fitted tiene atributo `named_steps`. Las metricas de CV contienen `accuracy` y `f1_macro`. |
| `serializer.py` | Unit | El archivo `models/iris_model.joblib` existe tras llamar `save_model()`. Puede cargarse con `joblib.load()`. |
| `test_pipeline_e2e.py` | Integration | Ejecutar bronze -> serializer completo produce un archivo `.joblib` cargable que hace predicciones validas sobre datos de test. |
| `test_model_performance.py` | Model QA | Accuracy >= 0.95, F1 Macro >= 0.95, F1 por clase >= 0.90. Este test falla si el modelo no cumple los KPIs del BRD. |

### 9.3 Fixtures y Mocks

- **Pipeline fixture:** Un `sklearn.Pipeline` entrenado sobre el dataset completo con `random_state=42`, guardado en `tests/fixtures/test_model.joblib`. Usado en `test_predictor.py` para aislar la prueba del modelo de produccion.
- **DataFrame fixtures:** DataFrames de muestra (5-10 filas) que representan el estado Bronze, Silver y Gold. Definidos como constantes en `tests/conftest.py`.
- **Mock del logger:** En `test_feedback.py`, el archivo de log se escribe en un directorio temporal (`tmp_path` de pytest) para no contaminar `logs/feedback.log` de produccion.

### 9.4 Comando de Ejecucion

```
pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80
```

Este comando ejecuta toda la suite y falla si la cobertura de `src/` cae por debajo del 80% (criterio CA12 del BRD).

---

## 10. Check de Certificacion Arquitectonica

| Criterio | Estado | Evidencia |
| :--- | :--- | :--- |
| El diseno garantiza desacoplamiento entre logica de ML (Phase Modeling) y la UI (Phase Delivery) | Aprobado | `app.py` solo invoca `predictor.predict()`. El pipeline de datos offline no es importado por ningun modulo online. |
| El modelo puede ser reemplazado sin modificar la UI | Aprobado | Solo se reemplaza `models/iris_model.joblib` y eventualmente la ruta en `config.py`. La firma de `predict()` es invariante. |
| Se ha definido una estrategia contra Data Leakage | Aprobado | ADR-003: StandardScaler encapsulado en `sklearn.Pipeline`. El `fit` ocurre exclusivamente sobre `X_train`. |
| Todas las rutas son relativas y portables | Aprobado | ADR-004: `src/config.py` centraliza rutas via `pathlib.Path(__file__).resolve().parent.parent`. |
| El sistema falla en la frontera (Fail-Fast) | Aprobado | `validators.py` con Pydantic v2 valida rangos antes de invocar `predictor.py`. El modelo nunca recibe datos fuera de contrato. |
| El SAD es la fuente de verdad para el SpecDD y el CONTRACT | Aprobado | La seccion 5 define los modulos exactos. La seccion 6.1 define los tipos de datos compartidos. Ambos documentos deben trazarse a esta seccion. |
| La estrategia de testing cubre >= 80% del codigo de `src/` | Aprobado | Seccion 9 define cobertura por modulo y el comando de verificacion con `pytest-cov`. |

---

> **Nota de Gobernanza:** Este documento es la fuente de verdad arquitectonica para los agentes `ai-data-engineer`, `ai-ml-engineer` y `ai-developer` en las Fases 2, 3 y 4. Cualquier desviacion de la topologia de modulos, los tipos de datos o los ADRs aqui definidos debe pasar por el Protocolo de Control de Cambios antes de ser implementada. El `ai-solutions-architect` es el unico agente con autoridad para modificar este documento.
>
> **Trazabilidad:** SAD v1.0.0 <- BRD v1.0.0 <- feasibility v1.0.0
