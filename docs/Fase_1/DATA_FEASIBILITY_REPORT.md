# DATA FEASIBILITY REPORT
## Proyecto: Flores AI - Iris
### Fase 1 - Discovery | Auditor: ai-data-auditor

| Campo                  | Valor                                      |
| :--------------------- | :----------------------------------------- |
| Fecha de Emision       | 2026-04-19                                 |
| Fuente Auditada        | data/bronze/Iris.csv                       |
| Registros Auditados    | 150                                        |
| Metodologia EDQ        | diagnostic-data-auditor + feasibility-gap-analyzer |
| Veredicto Final        | GO                                         |
| Nivel de Confianza     | Alto                                       |

---

## 1. Inventario de Variables

| Columna CSV        | Nombre BRD      | Tipo Dato | Rol     | Unidad | Notas                                      |
| :----------------- | :-------------- | :-------- | :------ | :----- | :----------------------------------------- |
| Id                 | -               | int64     | IGNORAR | -      | Indice secuencial 1-150. NO es feature. Debe eliminarse antes del entrenamiento. |
| SepalLengthCm      | sepal_length    | float64   | Feature | cm     | Longitud del sepalo en centimetros         |
| SepalWidthCm       | sepal_width     | float64   | Feature | cm     | Ancho del sepalo en centimetros            |
| PetalLengthCm      | petal_length    | float64   | Feature | cm     | Longitud del petalo en centimetros         |
| PetalWidthCm       | petal_width     | float64   | Feature | cm     | Ancho del petalo en centimetros            |
| Species            | species         | object    | Target  | -      | Etiqueta de clase: Iris-setosa, Iris-versicolor, Iris-virginica |

**Observacion de nomenclatura:** Las columnas CSV usan formato PascalCase con sufijo `Cm`. El BRD las referencia en snake_case sin unidad. El proceso Silver debe renombrar a la convencion del BRD. Las etiquetas de `Species` incluyen el prefijo `Iris-` (e.g., `Iris-setosa`) que puede normalizarse a `setosa` segun la convencion que defina el SpecDD.

---

## 2. Diagnostico de Calidad (EDQ Completo)

### 2.1 Volumetria y Completitud

| Metrica                        | Valor        |
| :----------------------------- | :----------- |
| Total de registros             | 150          |
| Total de columnas              | 6            |
| Columnas utiles para ML        | 5 (Id excluido) |
| Valores nulos — SepalLengthCm  | 0 (0.00%)    |
| Valores nulos — SepalWidthCm   | 0 (0.00%)    |
| Valores nulos — PetalLengthCm  | 0 (0.00%)    |
| Valores nulos — PetalWidthCm   | 0 (0.00%)    |
| Valores nulos — Species        | 0 (0.00%)    |

El dataset esta **100% completo**. No se requiere ningun proceso de imputacion.

### 2.2 Duplicados

| Metrica                                    | Valor |
| :----------------------------------------- | :---- |
| Filas duplicadas exactas (incluyendo Id)   | 0     |
| Filas duplicadas excluyendo Id             | 3     |

Se detectaron **3 registros con valores identicos en todas las features y target** (diferenciados unicamente por su Id):

| Id  | SepalLengthCm | SepalWidthCm | PetalLengthCm | PetalWidthCm | Species       |
| :-- | :------------ | :----------- | :------------ | :----------- | :------------ |
| 10  | 4.9           | 3.1          | 1.5           | 0.1          | Iris-setosa   |
| 35  | 4.9           | 3.1          | 1.5           | 0.1          | Iris-setosa   |
| 38  | 4.9           | 3.1          | 1.5           | 0.1          | Iris-setosa   |
| 102 | 5.8           | 2.7          | 5.1           | 1.9          | Iris-virginica |
| 143 | 5.8           | 2.7          | 5.1           | 1.9          | Iris-virginica |

**Accion requerida en Fase 2 (Silver):** Eliminar los duplicados conservando la primera ocurrencia. Impacto: el dataset quedaria en 147 registros (reduccion del 2.0%). El balance de clases no se altera materialmente.

### 2.3 Distribucion de Clases

| Clase           | Conteo | Porcentaje |
| :-------------- | :----- | :--------- |
| Iris-setosa     | 50     | 33.33%     |
| Iris-versicolor | 50     | 33.33%     |
| Iris-virginica  | 50     | 33.33%     |

El dataset esta **perfectamente balanceado**. No se requiere oversampling (SMOTE), undersampling ni class_weight. Este es un escenario optimo para clasificacion multi-clase.

### 2.4 Estadisticas Descriptivas por Feature

#### Global (150 registros)

| Feature       | Min  | P25  | Mediana | P75  | P95  | Max  | Media  | Std    |
| :------------ | :--- | :--- | :------ | :--- | :--- | :--- | :----- | :----- |
| SepalLengthCm | 4.30 | 5.10 | 5.80    | 6.40 | 7.26 | 7.90 | 5.8433 | 0.8281 |
| SepalWidthCm  | 2.00 | 2.80 | 3.00    | 3.30 | 3.80 | 4.40 | 3.0540 | 0.4336 |
| PetalLengthCm | 1.00 | 1.60 | 4.35    | 5.10 | 6.10 | 6.90 | 3.7587 | 1.7644 |
| PetalWidthCm  | 0.10 | 0.30 | 1.30    | 1.80 | 2.30 | 2.50 | 1.1987 | 0.7632 |

**Observacion:** La alta desviacion estandar de PetalLengthCm (1.76) y PetalWidthCm (0.76) a nivel global refleja la separacion natural entre la clase Setosa y las otras dos. Este patron bimodal es estadisticamente esperado, no un error de datos.

#### Por Clase

**Iris-setosa (n=50)**

| Feature       | Min  | Mediana | Max  | Media  | Std    |
| :------------ | :--- | :------ | :--- | :----- | :----- |
| SepalLengthCm | 4.30 | 5.00    | 5.80 | 5.0060 | 0.3525 |
| SepalWidthCm  | 2.30 | 3.40    | 4.40 | 3.4180 | 0.3810 |
| PetalLengthCm | 1.00 | 1.50    | 1.90 | 1.4640 | 0.1735 |
| PetalWidthCm  | 0.10 | 0.20    | 0.60 | 0.2440 | 0.1072 |

**Iris-versicolor (n=50)**

| Feature       | Min  | Mediana | Max  | Media  | Std    |
| :------------ | :--- | :------ | :--- | :----- | :----- |
| SepalLengthCm | 4.90 | 5.90    | 7.00 | 5.9360 | 0.5162 |
| SepalWidthCm  | 2.00 | 2.80    | 3.40 | 2.7700 | 0.3138 |
| PetalLengthCm | 3.00 | 4.35    | 5.10 | 4.2600 | 0.4699 |
| PetalWidthCm  | 1.00 | 1.30    | 1.80 | 1.3260 | 0.1978 |

**Iris-virginica (n=50)**

| Feature       | Min  | Mediana | Max  | Media  | Std    |
| :------------ | :--- | :------ | :--- | :----- | :----- |
| SepalLengthCm | 4.90 | 6.50    | 7.90 | 6.5880 | 0.6359 |
| SepalWidthCm  | 2.20 | 3.00    | 3.80 | 2.9740 | 0.3225 |
| PetalLengthCm | 4.50 | 5.55    | 6.90 | 5.5520 | 0.5519 |
| PetalWidthCm  | 1.40 | 2.00    | 2.50 | 2.0260 | 0.2747 |

### 2.5 Deteccion de Outliers

#### Metodo IQR (fence = Q1 - 1.5*IQR, Q3 + 1.5*IQR)

| Feature       | Fence Inferior | Fence Superior | N Outliers | % Outliers | Valores          |
| :------------ | :------------- | :------------- | :--------- | :--------- | :--------------- |
| SepalLengthCm | 3.15           | 8.35           | 0          | 0.00%      | Ninguno          |
| SepalWidthCm  | 2.05           | 4.05           | 4          | 2.67%      | 2.0, 4.1, 4.2, 4.4 |
| PetalLengthCm | -3.65          | 10.35          | 0          | 0.00%      | Ninguno          |
| PetalWidthCm  | -1.95          | 4.05           | 0          | 0.00%      | Ninguno          |

#### Metodo Z-Score (|z| > 3)

| Feature       | N Outliers |
| :------------ | :--------- |
| SepalLengthCm | 0          |
| SepalWidthCm  | 1          |
| PetalLengthCm | 0          |
| PetalWidthCm  | 0          |

**Evaluacion:** Los 4 outliers de SepalWidthCm por IQR (y 1 por Z-score) corresponden a valores biologicamente plausibles para Iris. No son errores de medicion. El valor 2.0 es la minima observada en Versicolor, y 4.1-4.4 son maximos en Setosa. Se recomienda analizar su impacto en la Fase 2 antes de decidir tratamiento, pero **no se anticipan como bloqueo**.

---

## 3. Analisis de Separabilidad de Clases

### 3.1 ANOVA (Separacion global entre las 3 clases)

| Feature       | F-Statistic | p-value    | Interpretacion                    |
| :------------ | :---------- | :--------- | :-------------------------------- |
| SepalLengthCm | 119.26      | 1.67e-31   | Separacion alta                   |
| SepalWidthCm  | 47.36       | 1.33e-16   | Separacion moderada               |
| PetalLengthCm | 1179.03     | 3.05e-91   | Separacion extremadamente alta    |
| PetalWidthCm  | 959.32      | 4.38e-85   | Separacion extremadamente alta    |

PetalLengthCm y PetalWidthCm son los predictores dominantes. Sus F-statistics son un orden de magnitud superiores a los features de sepalo.

### 3.2 Separabilidad por Par de Clases (Overlap Ratio y Cohen's d)

Un `overlap_ratio` cercano a 0 indica separacion casi perfecta. Un `Cohen_d` con valor absoluto > 0.8 indica efecto grande.

**Iris-setosa vs Iris-versicolor** (par mas facil):

| Feature       | Overlap Ratio | Cohen's d | p-value   |
| :------------ | :------------ | :-------- | :-------- |
| SepalLengthCm | 0.333         | -2.104    | 8.99e-18  |
| SepalWidthCm  | 0.458         | +1.857    | 4.36e-15  |
| PetalLengthCm | 0.000         | -7.894    | 5.72e-62  |
| PetalWidthCm  | 0.000         | -6.802    | 4.59e-56  |

Setosa es **perfectamente separable** de Versicolor en las features de petalo (overlap = 0).

**Iris-setosa vs Iris-virginica** (par tambien facil):

| Feature       | Overlap Ratio | Cohen's d | p-value   |
| :------------ | :------------ | :-------- | :-------- |
| SepalLengthCm | 0.250         | -3.077    | 6.89e-28  |
| SepalWidthCm  | 0.682         | +1.258    | 8.92e-09  |
| PetalLengthCm | 0.000         | -9.993    | 1.56e-71  |
| PetalWidthCm  | 0.000         | -8.548    | 3.58e-65  |

Setosa es **perfectamente separable** de Virginica en las features de petalo (overlap = 0).

**Iris-versicolor vs Iris-virginica** (par critico segun BRD):

| Feature       | Overlap Ratio | Cohen's d | p-value   | Evaluacion          |
| :------------ | :------------ | :-------- | :-------- | :------------------ |
| SepalLengthCm | 0.700         | -1.126    | 1.72e-07  | Solapamiento alto   |
| SepalWidthCm  | 0.667         | -0.641    | 1.82e-03  | Solapamiento alto   |
| PetalLengthCm | 0.154         | -2.521    | 3.18e-22  | Solapamiento bajo   |
| PetalWidthCm  | 0.267         | -2.925    | 2.23e-26  | Solapamiento moderado |

**Zona de solapamiento critica en PetalWidthCm [1.4 - 1.8]:**
- Registros de Versicolor en la zona: 22
- Registros de Virginica en la zona: 16
- Total en zona de ambiguedad: 38 registros (25.3% del dataset)

**Zona de solapamiento critica en PetalLengthCm [4.5 - 5.1]:**
- Registros de Versicolor en la zona: 21
- Registros de Virginica en la zona: 16
- Total en zona de ambiguedad: 37 registros (24.7% del dataset)

**Confirmacion de la hipotesis del BRD:** La confusion Versicolor/Virginica identificada como el error mas critico en el BRD queda **estadisticamente confirmada**. Es el unico par donde existe solapamiento real en las features de petalo. Sin embargo, los valores de Cohen's d (-2.521 para PetalLengthCm y -2.925 para PetalWidthCm) son suficientemente grandes como para que algoritmos no lineales (SVM con kernel RBF, Random Forest, Gradient Boosting) logren separacion con alta precision.

---

## 4. Gap Analysis: Requerimientos del BRD vs Realidad de los Datos

### 4.1 Cruze de Variables (BRD vs CSV)

| Variable BRD    | Disponible en CSV | Calidad   | Brecha         |
| :-------------- | :---------------- | :-------- | :------------- |
| sepal_length    | Si (SepalLengthCm) | Alta     | Ninguna        |
| sepal_width     | Si (SepalWidthCm)  | Alta     | 4 outliers IQR (biologicamente validos) |
| petal_length    | Si (PetalLengthCm) | Alta     | Ninguna        |
| petal_width     | Si (PetalWidthCm)  | Alta     | Ninguna        |
| species (target)| Si (Species)       | Alta     | Formato de etiqueta: `Iris-X` vs `X` |

**Conclusion:** No existe ninguna Brecha de Disponibilidad. Todas las variables requeridas por el BRD estan presentes y son de alta calidad.

### 4.2 Clasificacion de Brechas Detectadas

| ID   | Tipo                  | Descripcion                                         | Severidad  | Bloqueo |
| :--- | :-------------------- | :-------------------------------------------------- | :--------- | :------ |
| G-01 | Brecha de Calidad     | 3 registros near-duplicates (2.0% del dataset)      | Baja       | No      |
| G-02 | Brecha de Calidad     | 4 outliers IQR en SepalWidthCm (biologicamente validos) | Muy Baja | No      |
| G-03 | Brecha de Calidad     | Columna `Id` presente: riesgo de leakage si no se elimina | Media  | No (prevenible) |
| G-04 | Brecha de Calidad     | Etiquetas con prefijo `Iris-` vs convencion BRD     | Muy Baja   | No      |
| G-05 | Brecha de Volumen     | 150 registros: suficiente para ML clasico, limitante para deep learning | Baja | No |

**No se detectaron Brechas de Disponibilidad ni Brechas de Accesibilidad.**

### 4.3 Analisis de Riesgo de Data Leakage

| Riesgo                                    | Evaluacion                                                        |
| :---------------------------------------- | :---------------------------------------------------------------- |
| Columna `Id` como feature                 | RIESGO REAL si no se elimina antes del split train/test. El Id es un indice secuencial correlacionado con el orden de las clases en el archivo (1-50 Setosa, 51-100 Versicolor, 101-150 Virginica). Si se incluye como feature, el modelo aprenderia el indice, no la biologia. |
| Variables proxy del target                | No detectadas. Ninguna feature codifica directamente la especie.   |
| Fugas temporales                          | No aplica. Dataset no tiene dimension temporal.                    |
| Solapamiento train/test por near-duplicates | Riesgo bajo pero real: los 3 grupos de near-duplicates podrian aparecer en train y test simultaneamente, inflando artificialmente las metricas de evaluacion. Mitigacion: eliminar antes del split. |

---

## 5. Plan de Mitigacion para Fase 2 (Silver Layer)

Las siguientes acciones son el insumo directo para el `silver-layer-architect` en la Fase 2:

| ID   | Accion                          | Prioridad | Justificacion                                                 |
| :--- | :------------------------------ | :-------- | :------------------------------------------------------------ |
| M-01 | Eliminar columna `Id`           | CRITICA   | Previene leakage. El Id esta correlacionado con el orden de clases en el CSV original. |
| M-02 | Eliminar near-duplicates        | ALTA      | 3 filas duplicadas (solo en features + target). Conservar primera ocurrencia. Dataset resultante: 147 registros. |
| M-03 | Renombrar columnas a convencion BRD | MEDIA | Normalizar de PascalCase+Cm a snake_case (SepalLengthCm -> sepal_length) para cumplir con el contrato de datos del SpecDD. |
| M-04 | Normalizar etiquetas de Species | MEDIA     | Decidir si usar `Iris-setosa` o `setosa`. Documentar en CONTRACT.md. |
| M-05 | Tratamiento de outliers SepalWidthCm | BAJA | Evaluar impacto real en Fase 2. Se recomienda conservar (son biologicamente validos) y documentar en EDA. |
| M-06 | Feature Scaling                 | MEDIA     | Las features tienen rangos distintos (PetalLengthCm: 1.0-6.9 vs PetalWidthCm: 0.1-2.5). Los algoritmos basados en distancia (SVM, KNN) requieren StandardScaler o MinMaxScaler. Los basados en arboles (RF, XGBoost) no lo requieren. |

---

## 6. Scorecard de Salud del Dataset

| Dimension                          | Puntuacion | Evidencia                                      |
| :--------------------------------- | :--------- | :--------------------------------------------- |
| Completitud (nulos)                | 10/10      | 0% de nulos en todas las columnas              |
| Unicidad (duplicados exactos)      | 10/10      | 0 filas completamente duplicadas               |
| Near-duplicates                    | 8/10       | 3 filas (2.0%) con valores identicos sin Id    |
| Validez de rangos                  | 10/10      | Todos los valores en rangos biologicos validos |
| Outliers                           | 9/10       | 4 outliers IQR en SepalWidthCm, biologicamente plausibles |
| Balance de clases                  | 10/10      | Perfecto 50/50/50 por clase                    |
| Volumen                            | 8/10       | 150 registros: optimo para ML clasico          |
| Consistencia de esquema            | 10/10      | Una sola fuente, esquema uniforme              |
| Riesgo de leakage                  | 8/10       | Columna Id presente, prevenible con M-01       |
| Formato de etiquetas               | 9/10       | Prefijo Iris- menor, facil de normalizar       |

**PUNTUACION GLOBAL DE SALUD: 9.2 / 10**

---

## 7. Veredicto de Factibilidad

### 7.1 Posibilidad de Alcanzar los KPIs del BRD

| KPI del BRD                     | Factible | Justificacion                                                     |
| :------------------------------- | :------- | :---------------------------------------------------------------- |
| Accuracy >= 92% (minimo)         | Si       | La literatura cientifica reporta accuracy > 95% con SVM, RF y KNN en este dataset. Los F-statistics de ANOVA (hasta 1179 para PetalLengthCm) confirman separabilidad estadistica robusta. |
| Accuracy >= 95% (objetivo)       | Si       | Con SVM kernel RBF o Random Forest, el estado del arte en Iris es 96-98%. Los datos lo soportan. |
| F1-Score Macro >= 0.95           | Si       | El balance perfecto de clases (50/50/50) elimina el sesgo de clase mayoritaria. El F1-Score Macro y Weighted seran equivalentes. |
| Latencia UI <= 3,000 ms          | Si       | Los modelos clasicos (SVM, RF) tienen inferencia en microsegundos para un solo vector de 4 features. Streamlit con modelo serializado en Pickle/Joblib no superara 500ms en condiciones normales. |
| Error critico: confusion Versicolor/Virginica | Gestionable | Confirmado estadisticamente. El solapamiento existe pero es cuantificable y manejable. Un modelo no lineal con tuning de hiperparametros puede minimizar estos errores a < 5%. |

### 7.2 Riesgos Residuales

| Riesgo                              | Probabilidad | Impacto | Mitigacion                                          |
| :---------------------------------- | :----------- | :------ | :-------------------------------------------------- |
| Overfitting por volumen bajo (150)  | Media        | Medio   | Usar cross-validation k-fold (k=10) y regularizacion |
| Confusion persistente Versicolor/Virginica | Alta  | Medio   | Algoritmo no lineal + tuning. Monitorear recall por clase. |
| Degradacion en produccion por drift | Baja         | Alto    | Dataset estatico sin actualizacion. Definir politica de reentrenamiento. |

### 7.3 Veredicto Final

**VEREDICTO: GO**

**Nivel de Confianza: Alto**

**Justificacion:** El dataset `Iris.csv` es una fuente de datos de calidad excepcional (9.2/10). Tiene cero valores nulos, balance perfecto de clases y separabilidad estadistica robusta en sus features de petalo (F-statistic hasta 1179, Cohen's d hasta -9.99). Las brechas detectadas (G-01 a G-05) son todas menores y prevenibles con el plan de mitigacion documentado (M-01 a M-06). La unica complejidad real — la confusion Versicolor/Virginica — es conocida desde el BRD, esta cuantificada y es manejable con algoritmos no lineales. No existen bloqueos criticos.

El equipo de ingenieria de datos puede proceder a la Fase 2 (Silver Layer + EDA) con confianza plena.

---

## 8. Informacion de Linaje de la Fuente

| Campo                       | Valor                                   |
| :-------------------------- | :-------------------------------------- |
| Nombre del archivo          | Iris.csv                                |
| Ruta Bronze                 | data/bronze/Iris.csv                    |
| Origen conocido             | UCI Machine Learning Repository (dataset publico) |
| Frecuencia de actualizacion | Estatico (dataset de referencia, no se actualiza) |
| Tipo de ingesta             | Batch (archivo plano CSV)               |
| Codificacion                | UTF-8 (sin caracteres especiales)       |
| Separador                   | Coma (,)                                |
| Header                      | Si (primera fila)                       |
| Frescura de datos           | Dataset historico estandar, sin fecha de medicion |

---

## 9. Checklist de Certificacion de Auditoria

- [x] Se identificaron todas las fuentes necesarias para construir la variable objetivo (`Species` presente y completa)
- [x] Se evaluo la presencia de nulos y placeholders (resultado: 0% de nulos)
- [x] Se detecto patron de near-duplicates (3 filas, 2.0%, no MNAR — son mediciones repetidas)
- [x] Se confirmo que la volumetria soporta el modelo propuesto (150 registros, ML clasico)
- [x] Se notifico al estratega sobre los KPIs que son alcanzables con los datos actuales (todos factibles)
- [x] Se valido que no hay fugas de datos obvias (columna Id documentada como riesgo prevenible G-03)
- [x] El plan de mitigacion es realista con el stack tecnologico (pandas + scikit-learn, documentado en SAD pendiente)
- [x] Se detecto desbalance de clases (resultado: balance perfecto, no requiere accion)
- [x] Se confirmo o refruto la hipotesis de confusion Versicolor/Virginica del BRD (CONFIRMADA con datos)
- [x] Se documento el linaje completo de la fuente de datos

---

*Documento generado por: ai-data-auditor | Protocolo: diagnostic-data-auditor + feasibility-gap-analyzer | Fecha: 2026-04-19*
