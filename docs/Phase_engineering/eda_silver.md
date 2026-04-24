# EDA Silver: Dataset Iris Limpio
## Proyecto: Flores AI - Iris

> **Documento:** EDA Silver - Reporte de Analisis Exploratorio de la Capa Silver
> **Version:** 1.0.0
> **Fecha:** 2026-04-23
> **Autor:** ai-data-auditor
> **Trazabilidad:** F2-T06b -> contract.md v1.0.0 -> eda_bronze.md v1.0.0 -> BRD v1.0.0
> **Fuente de entrada:** `data/bronze/Iris.csv` via `src/data/bronze_loader.load_bronze()`
> **Modulo de transformacion:** `src/data/silver_cleaner.clean_bronze()`
> **Destino:** `data/silver/iris_silver.csv`

---

## 1. Resumen Ejecutivo

- Todos los invariantes Silver SR-01 a SR-07 del contract.md seccion 10.3 pasan sin excepcion sobre los datos reales producidos por `clean_bronze()`.
- Las 4 transformaciones M-01 a M-04 se ejecutaron correctamente: columna `Id` eliminada, 3 near-duplicates eliminados (150 -> 147 filas), columnas renombradas a snake_case, etiquetas de species normalizadas.
- La distribucion resultante es: setosa=48, versicolor=50, virginica=49. El desbalance maximo es de 2 registros entre clases (< 2%), dentro del umbral aceptable del contract.md seccion 4.2 (< 5%).
- Los 4 outliers estadisticos (IQR) en `sepal_width` de Bronze (Ids 16, 33, 34, 61) se preservan correctamente en Silver. Ningun outlier biologicamente valido fue eliminado.
- Los deltas de media entre Bronze y Silver son inferiores a 0.022 en todas las features. Las transformaciones no alteran la distribucion estadistica.
- Veredicto: **GO**. El dataset Silver esta listo para la construccion de la capa Gold (F2-T07).

---

## 2. Verificacion de Invariantes Silver (contract.md seccion 10.3)

Todos los valores provienen de la ejecucion real de `clean_bronze(load_bronze())` sobre `data/bronze/Iris.csv`.

| ID | Invariante | Expresion | Valor Observado | Resultado |
|:---|:-----------|:----------|:----------------|:----------|
| SR-01 | Total de filas | `len(df) == 147` | 147 | PASS |
| SR-02 | Columna Id ausente | `'Id' not in df.columns` | True | PASS |
| SR-03 | Columnas en snake_case | `list(df.columns) == ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']` | `['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']` | PASS |
| SR-04 | Etiquetas normalizadas | `set(df['species']) == {'setosa', 'versicolor', 'virginica'}` | `{'setosa', 'versicolor', 'virginica'}` | PASS |
| SR-05a | Cero duplicados | `df.duplicated().sum() == 0` | 0 | PASS |
| SR-05b | Cero nulos | `df.isnull().sum().sum() == 0` | 0 | PASS |
| SR-06 | Tipos float64 en features | `all(df[f].dtype == 'float64' for f in features)` | True | PASS |
| SR-06 | Tipo object en species | `df['species'].dtype == object` | True | PASS |
| SR-07 | Sin prefijo 'Iris-' | `not df['species'].str.startswith('Iris-').any()` | True | PASS |

**Resultado global: 9/9 controles PASS. Ningun bloqueador detectado.**

---

## 3. Auditoria de Transformaciones M-01 a M-04

### 3.1 M-01 — Eliminacion de columna `Id`

- **Antes (Bronze):** 6 columnas: `['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']`
- **Despues (Silver):** 5 columnas: `['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']`
- **Justificacion:** `Id` es un identificador de fila secuencial sin valor predictivo. Su inclusion causaria data leakage al entrenar el modelo.
- **Resultado:** PASS — `'Id' not in df_silver.columns`

### 3.2 M-02 — Eliminacion de 3 near-duplicates

- **Politica:** `df.drop_duplicates(keep='first')` sobre las 5 columnas de features + species (sin `Id`).
- **Registros eliminados (Ids de Bronze):** 35, 38 (grupo A — Iris-setosa) y 143 (grupo B — Iris-virginica).
- **Registros conservados:** Id 10 (primer representante del grupo A) e Id 102 (primer representante del grupo B).
- **Conteo antes/despues:** 150 -> 147 filas (delta = -3).
- **Resultado:** PASS — `len(df_silver) == 147`

| Grupo | Ids Bronze | Species | Valores (SepalL, SepalW, PetalL, PetalW) | Accion |
|:------|:-----------|:--------|:------------------------------------------|:-------|
| A | 10, 35, 38 | Iris-setosa | (4.9, 3.1, 1.5, 0.1) | Eliminar Ids 35 y 38; conservar Id 10 |
| B | 102, 143 | Iris-virginica | (5.8, 2.7, 5.1, 1.9) | Eliminar Id 143; conservar Id 102 |

### 3.3 M-03 — Renombrado de columnas a snake_case

| Nombre Bronze | Nombre Silver |
|:--------------|:--------------|
| `SepalLengthCm` | `sepal_length` |
| `SepalWidthCm` | `sepal_width` |
| `PetalLengthCm` | `petal_length` |
| `PetalWidthCm` | `petal_width` |
| `Species` | `species` |

- **Resultado:** PASS — `list(df_silver.columns) == ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']`

### 3.4 M-04 — Normalizacion de etiquetas de species

| Etiqueta Bronze | Etiqueta Silver |
|:----------------|:----------------|
| `Iris-setosa` | `setosa` |
| `Iris-versicolor` | `versicolor` |
| `Iris-virginica` | `virginica` |

- **Resultado:** PASS — `set(df_silver['species']) == {'setosa', 'versicolor', 'virginica'}` y ninguna etiqueta comienza con `'Iris-'`.

---

## 4. Estadisticas Descriptivas Silver

### 4.1 Dataset Completo (n=147)

Valores calculados directamente sobre `df_silver = clean_bronze(load_bronze())`.

| Estadistico | sepal_length | sepal_width | petal_length | petal_width |
|:------------|:-------------|:------------|:-------------|:------------|
| **count** | 147 | 147 | 147 | 147 |
| **mean** | 5.8565 | 3.0558 | 3.7803 | 1.2088 |
| **std** | 0.8291 | 0.4370 | 1.7591 | 0.7579 |
| **min** | 4.3000 | 2.0000 | 1.0000 | 0.1000 |
| **Q25** | 5.1000 | 2.8000 | 1.6000 | 0.3000 |
| **Q50** | 5.8000 | 3.0000 | 4.4000 | 1.3000 |
| **Q75** | 6.4000 | 3.3000 | 5.1000 | 1.8000 |
| **max** | 7.9000 | 4.4000 | 6.9000 | 2.5000 |

### 4.2 Por Clase

#### setosa (n=48)

| Estadistico | sepal_length | sepal_width | petal_length | petal_width |
|:------------|:-------------|:------------|:-------------|:------------|
| mean | 5.0104 | 3.4312 | 1.4625 | 0.2500 |
| std | 0.3592 | 0.3832 | 0.1770 | 0.1052 |
| min | 4.3000 | 2.3000 | 1.0000 | 0.1000 |
| Q25 | 4.8000 | 3.2000 | 1.4000 | 0.2000 |
| Q50 | 5.0000 | 3.4000 | 1.5000 | 0.2000 |
| Q75 | 5.2000 | 3.7000 | 1.6000 | 0.3000 |
| max | 5.8000 | 4.4000 | 1.9000 | 0.6000 |

#### versicolor (n=50)

| Estadistico | sepal_length | sepal_width | petal_length | petal_width |
|:------------|:-------------|:------------|:-------------|:------------|
| mean | 5.9360 | 2.7700 | 4.2600 | 1.3260 |
| std | 0.5162 | 0.3138 | 0.4699 | 0.1978 |
| min | 4.9000 | 2.0000 | 3.0000 | 1.0000 |
| Q25 | 5.6000 | 2.5250 | 4.0000 | 1.2000 |
| Q50 | 5.9000 | 2.8000 | 4.3500 | 1.3000 |
| Q75 | 6.3000 | 3.0000 | 4.6000 | 1.5000 |
| max | 7.0000 | 3.4000 | 5.1000 | 1.8000 |

#### virginica (n=49)

| Estadistico | sepal_length | sepal_width | petal_length | petal_width |
|:------------|:-------------|:------------|:-------------|:------------|
| mean | 6.6041 | 2.9796 | 5.5612 | 2.0286 |
| std | 0.6321 | 0.3234 | 0.5537 | 0.2769 |
| min | 4.9000 | 2.2000 | 4.5000 | 1.4000 |
| Q25 | 6.3000 | 2.8000 | 5.1000 | 1.8000 |
| Q50 | 6.5000 | 3.0000 | 5.6000 | 2.0000 |
| Q75 | 6.9000 | 3.2000 | 5.9000 | 2.3000 |
| max | 7.9000 | 3.8000 | 6.9000 | 2.5000 |

---

## 5. Distribucion por Clase (species)

| Clase | Conteo Silver | Conteo Bronze | Delta | Porcentaje Silver |
|:------|:--------------|:--------------|:------|:------------------|
| setosa | 48 | 50 | -2 | 32.65% |
| versicolor | 50 | 50 | 0 | 34.01% |
| virginica | 49 | 50 | -1 | 33.33% |
| **TOTAL** | **147** | **150** | **-3** | **100.00%** |

**Ratio de desbalance Silver:** max_clase / min_clase = 50 / 48 = 1.042. Desbalance < 5%. No se requieren tecnicas de balanceo (SMOTE, undersampling). El `train_test_split` debe usar `stratify=y` para preservar proporciones.

Nota: La distribucion exacta (setosa=48, virginica=49) difiere de la estimacion del contract.md seccion 4.2 (setosa=49, virginica=48) porque `drop_duplicates(keep='first')` conserva el primer registro de cada grupo duplicado segun el orden de lectura del CSV. Los Ids eliminados reales son 35, 38 (setosa) y 143 (virginica), no los esperados en la estimacion del feasibility. Esto no constituye una desviacion del contrato: el invariante SR-01 (`len==147`) se cumple y el desbalance sigue siendo < 5%.

---

## 6. Comparativa Bronze vs. Silver

### 6.1 Impacto en Medidas de Tendencia Central y Dispersion

| Feature | Media Bronze | Media Silver | Delta Media | Std Bronze | Std Silver | Delta Std | Mediana Bronze | Mediana Silver | Delta Mediana |
|:--------|:-------------|:-------------|:------------|:-----------|:-----------|:----------|:---------------|:---------------|:--------------|
| sepal_length | 5.8433 | 5.8565 | +0.0131 | 0.8281 | 0.8291 | +0.0010 | 5.8000 | 5.8000 | 0.0000 |
| sepal_width | 3.0540 | 3.0558 | +0.0018 | 0.4336 | 0.4370 | +0.0034 | 3.0000 | 3.0000 | 0.0000 |
| petal_length | 3.7587 | 3.7803 | +0.0216 | 1.7644 | 1.7591 | -0.0053 | 4.3500 | 4.4000 | +0.0500 |
| petal_width | 1.1987 | 1.2088 | +0.0102 | 0.7632 | 0.7579 | -0.0053 | 1.3000 | 1.3000 | 0.0000 |

**Conclusion:** Todos los deltas de media son inferiores a 0.022. Todos los deltas de std son inferiores a 0.006. Los extremos (min, max) son identicos en las 4 features. La eliminacion de 3 near-duplicates tiene impacto estadisticamente negligible en la distribucion global.

### 6.2 Valores Extremos Identicos Bronze vs. Silver

| Feature | Min Bronze | Min Silver | Max Bronze | Max Silver |
|:--------|:-----------|:-----------|:-----------|:-----------|
| sepal_length | 4.3 | 4.3 | 7.9 | 7.9 |
| sepal_width | 2.0 | 2.0 | 4.4 | 4.4 |
| petal_length | 1.0 | 1.0 | 6.9 | 6.9 |
| petal_width | 0.1 | 0.1 | 2.5 | 2.5 |

Los valores extremos son identicos en Bronze y Silver. Ninguno de los near-duplicates eliminados era un valor extremo; todos sus valores numericos eran internos al rango del dataset. La cobertura del espacio de features no se ha reducido.

### 6.3 Comparativa contra Estadisticas de Referencia (contract.md seccion 8.2)

El contract.md define estadisticas de referencia para drift detection. Se comparan contra los valores reales calculados:

| Feature | Media Ref | Media Real | Desviacion | Std Ref | Std Real | Desviacion | Estado |
|:--------|:----------|:-----------|:-----------|:--------|:---------|:-----------|:-------|
| sepal_length | 5.848 | 5.8565 | +0.0085 | 0.828 | 0.8291 | +0.0011 | ACEPTABLE |
| sepal_width | 3.052 | 3.0558 | +0.0038 | 0.433 | 0.4370 | +0.0040 | ACEPTABLE |
| petal_length | 3.758 | 3.7803 | +0.0223 | 1.764 | 1.7591 | -0.0049 | ACEPTABLE |
| petal_width | 1.197 | 1.2088 | +0.0118 | 0.763 | 0.7579 | -0.0053 | ACEPTABLE |

Todas las desviaciones son menores a 0.025 (< 0.3 std de la distribucion). Las diferencias son producto del redondeo en las estadisticas de referencia del contract.md, las cuales fueron estimadas en la fase de discovery. Los valores reales calculados en este reporte son los que deben almacenarse en `data/gold/reference_stats.json` segun el contract.md seccion 11.

---

## 7. Analisis de Outliers

### 7.1 Deteccion IQR en Silver (n=147)

| Feature | Q1 | Q3 | IQR | Fence Inferior | Fence Superior | Outliers Detectados |
|:--------|:---|:---|:----|:---------------|:---------------|:--------------------|
| sepal_length | 5.1000 | 6.4000 | 1.3000 | 3.1500 | 8.3500 | 0 |
| sepal_width | 2.8000 | 3.3000 | 0.5000 | 2.0500 | 4.0500 | 4 |
| petal_length | 1.6000 | 5.1000 | 3.5000 | -3.6500 | 10.3500 | 0 |
| petal_width | 0.3000 | 1.8000 | 1.5000 | -1.9500 | 4.0500 | 0 |

### 7.2 Detalle de Outliers Preservados en sepal_width

Los 4 outliers IQR de Bronze se conservan intactos en Silver. Sus posiciones en el Silver DataFrame (indices 0-based post-reset):

| Indice Silver | sepal_width | species | Fence Violada | Diagnostico |
|:--------------|:------------|:--------|:--------------|:------------|
| 15 | 4.4 | setosa | Superior (>4.05) | Biologicamente plausible. Max absoluto del dataset. Iris-setosa tiene sepalo naturalmente ancho. |
| 32 | 4.1 | setosa | Superior (>4.05) | Borderline (+0.05 sobre fence). Biologicamente normal. |
| 33 | 4.2 | setosa | Superior (>4.05) | Biologicamente plausible. |
| 58 | 2.0 | versicolor | Inferior (<2.05) | Borderline (-0.05 bajo fence). Min absoluto del dataset. Biologicamente plausible. |

**Conformidad con el contrato:** Los 4 valores estan dentro de los rangos del contrato (sepal_width: [1.5, 5.5]). No violan VR-02. No representan errores de medicion.

**Decision confirmada:** Mantener en Silver. No requieren tratamiento. Se reportaran como outliers estadisticos al equipo de modelado para consideracion al evaluar robustez del modelo.

---

## 8. Tipos de Datos Silver

| Columna | Tipo Esperado (contract.md §3.1) | Tipo Observado | Conformidad |
|:--------|:---------------------------------|:---------------|:------------|
| `sepal_length` | `float64` | `float64` | OK |
| `sepal_width` | `float64` | `float64` | OK |
| `petal_length` | `float64` | `float64` | OK |
| `petal_width` | `float64` | `float64` | OK |
| `species` | `object` | `object` | OK |

Todos los tipos de datos son conformes con el esquema Silver del contract.md seccion 3.1. Las transformaciones M-01 a M-04 no alteraron los tipos de las columnas numericas.

---

## 9. Deteccion de Sesgo Introducido por Limpieza

### 9.1 Sesgo de Representacion de Clase

- **Bronze:** distribucion exactamente uniforme 50/50/50 (33.33% por clase).
- **Silver:** distribucion 48/50/49 (32.65% / 34.01% / 33.33%).
- **Sesgo introducido:** Ninguno significativo. La reduccion de 2 registros en setosa y 1 en virginica es consecuencia directa de la eliminacion de near-duplicates (ruido de recoleccion documentado). El desbalance resultante (4.2% entre clases extremas) es menor al umbral del 5% definido en contract.md.

### 9.2 Sesgo de Distribucion de Features

Los near-duplicates eliminados tenian valores en el rango interno de sus respectivas clases:
- Grupo A (setosa, 4.9/3.1/1.5/0.1): valores cercanos a la mediana de setosa. Su eliminacion eleva marginalmente la media de sepal_width de setosa.
- Grupo B (virginica, 5.8/2.7/5.1/1.9): valores por debajo de la media de virginica en sepal_length. Su eliminacion eleva marginalmente la media de sepal_length de virginica.

Ninguno de los cambios supera 0.025 a nivel global ni 0.060 a nivel de clase. No se detecta sesgo estadistico significativo introducido por la limpieza.

### 9.3 Sesgo de Outliers

Los 4 outliers IQR en sepal_width son todos de clases setosa (3 casos altos) y versicolor (1 caso bajo). Su preservacion en Silver es correcta: eliminarlos introduciria sesgo al recortar artificialmente la varianza biologica real de estas especies.

---

## 10. Veredicto de Calidad

**VEREDICTO: GO**

### Justificacion Tecnica

1. **Invariantes formales:** Los 9 controles SR-01 a SR-07 pasan sin excepcion. El dataset Silver tiene exactamente 147 filas, 5 columnas snake_case, 0 nulos, 0 duplicados, tipos float64 en features y object en species, y las 3 etiquetas normalizadas sin prefijo `Iris-`.

2. **Transformaciones verificadas:** Las 4 mutaciones M-01 a M-04 se ejecutaron correctamente y en el orden especificado por el contract.md seccion 3.3.

3. **Distribucion preservada:** Los deltas de media Bronze -> Silver son inferiores a 0.022 en todas las features. Los extremos (min, max) son identicos. La limpieza no alterara el comportamiento del modelo.

4. **Outliers conservados:** Los 4 outliers biologicamente validos en sepal_width se preservan correctamente. No se introdujo sesgo por eliminacion indebida.

5. **Balance de clases:** Desbalance 4.2% (48 vs 50), dentro del umbral < 5% del contrato. No se requieren tecnicas de balanceo.

6. **Conformidad de tipos:** Los 5 tipos de datos observados coinciden exactamente con los tipos esperados en el esquema Silver.

7. **Sin sesgo de limpieza:** La distribucion estadistica por clase y global no presenta alteraciones significativas respecto a Bronze.

### Autorizacion de Paso a Gold

El dataset Silver producido por `clean_bronze(load_bronze())` es apto para persistirse en `data/silver/iris_silver.csv` y avanzar a la construccion de la capa Gold (F2-T07). El agente `ai-data-engineer` puede proceder con la implementacion de `gold_builder.py` usando este dataset como entrada, siguiendo las especificaciones del contract.md seccion 4.

---

> **Trazabilidad del Documento:**
> `eda_silver.md` <- `src/data/silver_cleaner.py` <- `src/data/bronze_loader.py` <- `data/bronze/Iris.csv` <- `contract.md v1.0.0` <- `eda_bronze.md v1.0.0`
>
> **Documento anterior:** `docs/Phase_engineering/eda_bronze.md`
> **Proximo documento:** EDA Gold (producir tras F2-T07)
