# EDA Bronze: Dataset Iris Crudo
## Proyecto: Flores AI - Iris

> **Documento:** EDA Bronze - Reporte de Analisis Exploratorio de la Capa Bronze
> **Version:** 1.0.0
> **Fecha:** 2026-04-21
> **Autor:** ai-data-auditor
> **Trazabilidad:** F2-T03b -> contract.md v1.0.0 -> feasibility v1.0.0 -> BRD v1.0.0
> **Fuente de datos:** `data/bronze/Iris.csv`
> **Modulo de carga:** `src/data/bronze_loader.py`

---

## 1. Resumen Ejecutivo

- Todos los invariantes Bronze BR-01 a BR-04 del contract.md seccion 2.2 pasan sin excepcion: 150 filas, 6 columnas, 0 nulos, 3 clases validas con 50 registros exactos por clase.
- El dataset esta perfectamente balanceado en Bronze: distribucion uniforme 50/50/50 (33.33% por clase). No se requieren tecnicas de balanceo en fase de ingesta.
- Se detectan 5 near-duplicates en 2 grupos: {Id 10, 35, 38} con valores identicos en Iris-setosa, y {Id 102, 143} con valores identicos en Iris-virginica. Estos registros tienen `Id` distinto pero mismos valores numericos. Este hallazgo esta alineado con el contract.md seccion 3.2 (mutacion M-02: eliminar 3 near-duplicates para llegar a 147 filas en Silver).
- Se detectan 4 outliers estadisticos (metodo IQR) en `SepalWidthCm`: Ids 16, 33, 34 (valores altos en Iris-setosa) e Id 61 (valor bajo en Iris-versicolor). Estos valores son biologicamente plausibles y no violan los rangos del contract.md seccion 2.1.
- Todos los valores numericos estan dentro de los rangos definidos en el contrato: 0 violaciones de rango en las 4 features.

---

## 2. Verificacion de Invariantes Bronze (contract.md seccion 2.2)

| ID | Invariante | Expresion | Valor Observado | Resultado |
|:---|:-----------|:----------|:----------------|:----------|
| BR-01 | Total de filas | `len(df) == 150` | 150 | PASS |
| BR-02 | Total de columnas | `len(df.columns) == 6` | 6 | PASS |
| BR-03 | Cero nulos | `df.isnull().sum().sum() == 0` | 0 | PASS |
| BR-04 | Clases validas | `set(df['Species']) == {'Iris-setosa', 'Iris-versicolor', 'Iris-virginica'}` | `{'Iris-setosa', 'Iris-versicolor', 'Iris-virginica'}` | PASS |

Invariante adicional verificado (contract.md seccion 2.2, quinta fila):

| Invariante | Expresion | Valor Observado | Resultado |
|:-----------|:----------|:----------------|:----------|
| Registros por clase (50 exactos) | `df['Species'].value_counts()` | Iris-setosa: 50, Iris-versicolor: 50, Iris-virginica: 50 | PASS |

---

## 3. Completitud de Datos

### 3.1 Nulos por Columna

| Columna | Nulos | Porcentaje |
|:--------|:------|:-----------|
| `Id` | 0 | 0.00% |
| `SepalLengthCm` | 0 | 0.00% |
| `SepalWidthCm` | 0 | 0.00% |
| `PetalLengthCm` | 0 | 0.00% |
| `PetalWidthCm` | 0 | 0.00% |
| `Species` | 0 | 0.00% |
| **TOTAL** | **0** | **0.00%** |

### 3.2 Tipos de Datos Observados vs. Esperados

| Columna | Tipo Esperado (contract.md) | Tipo Observado | Conformidad |
|:--------|:----------------------------|:---------------|:------------|
| `Id` | `int64` | `int64` | OK |
| `SepalLengthCm` | `float64` | `float64` | OK |
| `SepalWidthCm` | `float64` | `float64` | OK |
| `PetalLengthCm` | `float64` | `float64` | OK |
| `PetalWidthCm` | `float64` | `float64` | OK |
| `Species` | `object` | `object` | OK |

### 3.3 Integridad del Indice Id

- Rango esperado: [1, 150], secuencial
- Id minimo observado: 1
- Id maximo observado: 150
- Secuencia completa {1..150}: PASS (sin gaps ni repeticiones en el Id)

---

## 4. Estadisticas Descriptivas

### 4.1 Dataset Completo (n=150)

| Estadistico | SepalLengthCm | SepalWidthCm | PetalLengthCm | PetalWidthCm |
|:------------|:--------------|:-------------|:--------------|:-------------|
| **count** | 150 | 150 | 150 | 150 |
| **mean** | 5.8433 | 3.0540 | 3.7587 | 1.1987 |
| **std** | 0.8281 | 0.4336 | 1.7644 | 0.7632 |
| **min** | 4.3000 | 2.0000 | 1.0000 | 0.1000 |
| **Q25** | 5.1000 | 2.8000 | 1.6000 | 0.3000 |
| **Q50** | 5.8000 | 3.0000 | 4.3500 | 1.3000 |
| **Q75** | 6.4000 | 3.3000 | 5.1000 | 1.8000 |
| **max** | 7.9000 | 4.4000 | 6.9000 | 2.5000 |

### 4.2 Comparacion Bronze vs. Referencia Silver (contract.md seccion 8.2)

Las estadisticas Silver (147 registros post-limpieza) son la referencia de destino. La diferencia Bronze-Silver mide el efecto de eliminar los near-duplicates.

| Feature | Media Bronze | Media Silver | Delta |
|:--------|:-------------|:-------------|:------|
| SepalLengthCm / sepal_length | 5.8433 | 5.848 | +0.005 |
| SepalWidthCm / sepal_width | 3.0540 | 3.052 | -0.002 |
| PetalLengthCm / petal_length | 3.7587 | 3.758 | -0.001 |
| PetalWidthCm / petal_width | 1.1987 | 1.197 | -0.002 |

Los deltas son inferiores a 0.01 en todos los casos. La eliminacion de 3 near-duplicates tiene impacto negligible en las distribuciones de las features.

### 4.3 Estadisticas por Clase

#### Iris-setosa (n=50)

| Estadistico | SepalLengthCm | SepalWidthCm | PetalLengthCm | PetalWidthCm |
|:------------|:--------------|:-------------|:--------------|:-------------|
| mean | 5.0060 | 3.4180 | 1.4640 | 0.2440 |
| std | 0.3525 | 0.3810 | 0.1735 | 0.1072 |
| min | 4.3000 | 2.3000 | 1.0000 | 0.1000 |
| Q25 | 4.8000 | 3.1250 | 1.4000 | 0.2000 |
| Q50 | 5.0000 | 3.4000 | 1.5000 | 0.2000 |
| Q75 | 5.2000 | 3.6750 | 1.5750 | 0.3000 |
| max | 5.8000 | 4.4000 | 1.9000 | 0.6000 |

#### Iris-versicolor (n=50)

| Estadistico | SepalLengthCm | SepalWidthCm | PetalLengthCm | PetalWidthCm |
|:------------|:--------------|:-------------|:--------------|:-------------|
| mean | 5.9360 | 2.7700 | 4.2600 | 1.3260 |
| std | 0.5162 | 0.3138 | 0.4699 | 0.1978 |
| min | 4.9000 | 2.0000 | 3.0000 | 1.0000 |
| Q25 | 5.6000 | 2.5250 | 4.0000 | 1.2000 |
| Q50 | 5.9000 | 2.8000 | 4.3500 | 1.3000 |
| Q75 | 6.3000 | 3.0000 | 4.6000 | 1.5000 |
| max | 7.0000 | 3.4000 | 5.1000 | 1.8000 |

#### Iris-virginica (n=50)

| Estadistico | SepalLengthCm | SepalWidthCm | PetalLengthCm | PetalWidthCm |
|:------------|:--------------|:-------------|:--------------|:-------------|
| mean | 6.5880 | 2.9740 | 5.5520 | 2.0260 |
| std | 0.6359 | 0.3225 | 0.5519 | 0.2747 |
| min | 4.9000 | 2.2000 | 4.5000 | 1.4000 |
| Q25 | 6.2250 | 2.8000 | 5.1000 | 1.8000 |
| Q50 | 6.5000 | 3.0000 | 5.5500 | 2.0000 |
| Q75 | 6.9000 | 3.1750 | 5.8750 | 2.3000 |
| max | 7.9000 | 3.8000 | 6.9000 | 2.5000 |

---

## 5. Distribucion por Clase (Species)

| Clase | Conteo | Porcentaje | Balance |
|:------|:-------|:-----------|:--------|
| Iris-setosa | 50 | 33.33% | Balanceado |
| Iris-versicolor | 50 | 33.33% | Balanceado |
| Iris-virginica | 50 | 33.33% | Balanceado |
| **TOTAL** | **150** | **100.00%** | **Perfecto** |

El dataset Bronze tiene distribucion exactamente uniforme. El ratio de desbalance es 1.0 (maximo desbalance = 1.0, sin desbalance). No se requieren tecnicas de oversampling (SMOTE) ni undersampling en ninguna etapa del pipeline.

Nota: Tras la limpieza Silver (eliminacion de near-duplicates), el balance resultante sera aproximadamente Setosa: 49, Versicolor: 50, Virginica: 48, con desbalance < 5%, dentro del umbral aceptable segun el contract.md seccion 4.2.

---

## 6. Analisis de Outliers

### 6.1 Metodo IQR (Interquartile Range)

Criterio: Un valor es outlier si cae por debajo de `Q1 - 1.5*IQR` o por encima de `Q3 + 1.5*IQR`.

| Feature | Q1 | Q3 | IQR | Fence Inferior | Fence Superior | Outliers Detectados |
|:--------|:---|:---|:----|:---------------|:---------------|:--------------------|
| SepalLengthCm | 5.1000 | 6.4000 | 1.3000 | 3.1500 | 8.3500 | 0 |
| SepalWidthCm | 2.8000 | 3.3000 | 0.5000 | 2.0500 | 4.0500 | 4 |
| PetalLengthCm | 1.6000 | 5.1000 | 3.5000 | -3.6500 | 10.3500 | 0 |
| PetalWidthCm | 0.3000 | 1.8000 | 1.5000 | -1.9500 | 4.0500 | 0 |

### 6.2 Detalle de Outliers en SepalWidthCm

| Id | SepalWidthCm | Species | Fence Violada | Valor | Diagnostico |
|:---|:-------------|:--------|:--------------|:------|:------------|
| 16 | 4.4000 | Iris-setosa | Superior (>4.05) | +0.35 sobre fence | Biologicamente plausible: Iris-setosa tiene sepalo ancho. El max de setosa es 4.4, consistente con la literatura. |
| 33 | 4.1000 | Iris-setosa | Superior (>4.05) | +0.05 sobre fence | Borderline. Biologicamente normal. |
| 34 | 4.2000 | Iris-setosa | Superior (>4.05) | +0.15 sobre fence | Biologicamente plausible. |
| 61 | 2.0000 | Iris-versicolor | Inferior (<2.05) | -0.05 bajo fence | Borderline. Biologicamente plausible (el min observado en todo el dataset es 2.0). |

Todos los outliers detectados por IQR son borderline o biologicamente validos. Ninguno viola los rangos del contrato (SepalWidthCm: [1.5, 5.5]). No representan errores de medicion.

### 6.3 Near-Duplicates Identificados

Se detectan 5 registros con valores numericos identicos distribuidos en 2 grupos. Estos no son outliers en sentido estadistico sino registros potencialmente redundantes:

| Grupo | Ids afectados | Species | SepalLengthCm | SepalWidthCm | PetalLengthCm | PetalWidthCm |
|:------|:--------------|:--------|:--------------|:-------------|:--------------|:-------------|
| A | 10, 35, 38 | Iris-setosa | 4.9 | 3.1 | 1.5 | 0.1 |
| B | 102, 143 | Iris-virginica | 5.8 | 2.7 | 5.1 | 1.9 |

El contract.md (mutacion M-02) ya establece la politica de eliminar 3 near-duplicates para producir 147 filas en Silver. Este hallazgo confirma que la especificacion es correcta: del grupo A se eliminaran 2 registros (quedara 1), del grupo B se eliminara 1 (quedara 1), resultando en 147 filas.

### 6.4 Violaciones de Rango del Contrato

| Feature | Rango Contrato | Violaciones Observadas |
|:--------|:---------------|:-----------------------|
| SepalLengthCm | (3.0, 9.0) | 0 |
| SepalWidthCm | (1.5, 5.5) | 0 |
| PetalLengthCm | (0.5, 8.0) | 0 |
| PetalWidthCm | (0.0, 3.5) | 0 |

Ninguna observacion viola los rangos de contrato. El dato crudo es consistente con las restricciones de dominio establecidas en el contract.md seccion 2.1.

---

## 7. Veredicto de Calidad

**VEREDICTO: GO**

### Justificacion Tecnica

El dataset Bronze `data/bronze/Iris.csv` supera todos los controles de calidad requeridos para avanzar a la capa Silver:

1. **Invariantes formales:** Los 4 invariantes BR-01 a BR-04 del contract.md seccion 2.2 pasan sin excepcion. El dataset tiene exactamente 150 filas, 6 columnas, 0 nulos, y las 3 clases esperadas con 50 registros exactos cada una.

2. **Completitud:** Tasa de completitud del 100% en todas las columnas. No se require imputacion en ninguna fase, en linea con la politica de nulos del contract.md seccion 9.

3. **Conformidad de tipos:** Los 6 tipos de datos observados coinciden exactamente con los tipos esperados en el esquema Bronze (contract.md seccion 2.1).

4. **Integridad referencial:** El campo `Id` es secuencial y completo en el rango [1, 150], sin gaps ni repeticiones.

5. **Calidad de outliers:** Los 4 outliers estadisticos detectados por IQR en `SepalWidthCm` son biologicamente plausibles y no violan los rangos del contrato. No requieren tratamiento especial.

6. **Ruido por near-duplicates:** Los 5 near-duplicates identificados en 2 grupos son ruido de recoleccion esperado y estan contemplados en el plan de limpieza Silver (mutacion M-02, contract.md seccion 3.3). No representan un bloqueador.

7. **Balance de clases:** Distribucion exactamente uniforme (33.33% por clase). Sin riesgo de sesgo por desbalance en la capa Bronze.

### Riesgos Identificados (No Bloqueadores)

| Riesgo | Severidad | Mitigacion | Responsable |
|:-------|:----------|:-----------|:------------|
| 5 near-duplicates en 2 grupos | Baja | Eliminacion en Silver (mutacion M-02 ya especificada en contract.md) | ai-data-engineer (F2-T04) |
| 4 outliers en SepalWidthCm | Baja | No requieren accion: son biologicamente validos. Documentar en EDA Silver. | ai-data-auditor (EDA Silver) |

### Autorizacion de Paso a Silver

El dataset Bronze es apto para ingresar al pipeline de limpieza Silver. El agente `ai-data-engineer` puede proceder con F2-T04 (implementacion de `silver_cleaner.py`) usando este dataset como entrada, siguiendo las especificaciones del contract.md seccion 3.

---

> **Trazabilidad del Documento:**
> `eda_bronze.md` <- `data/bronze/Iris.csv` <- `contract.md v1.0.0` <- `feasibility v1.0.0`
>
> **Proximo documento:** `docs/Phase_engineering/eda_silver.md` (producir tras F2-T04)
