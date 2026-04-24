# EDA Gold: Dataset Iris Feature Store
## Proyecto: Flores AI - Iris

> **Documento:** EDA Gold - Reporte de Analisis Exploratorio de la Capa Gold
> **Version:** 1.0.0
> **Fecha:** 2026-04-24
> **Autor:** ai-data-auditor
> **Trazabilidad:** F2-T09b -> contract.md v1.0.0 -> eda_silver.md v1.0.0
> **Fuente de entrada:** `data/silver/iris_silver.csv` via `src/data/gold_builder.build_gold()`
> **Modulo de transformacion:** `src/data/gold_builder.py`
> **Destinos:** `data/gold/X_gold.csv`, `data/gold/y_gold.csv`, `data/gold/reference_stats.json`

---

## 1. Resumen Ejecutivo

- Todos los invariantes Gold GR-01 a GR-06 del contract.md seccion 10.4 pasan sin excepcion sobre los artefactos reales producidos por `build_gold()`.
- La matriz de correlacion real difiere de la de referencia (contract.md §8.3) en un maximo de ±0.001, dentro de la tolerancia de redondeo. Sin bloqueadores de correlacion.
- Varianza por feature: petal_length (3.0945) y petal_width (0.5744) concentran la mayor informacion discriminativa. sepal_width tiene la menor varianza (0.1910).
- Separabilidad de clases: setosa es perfectamente separable en petal_length (gap de 1.1 cm entre su max=1.9 y el min versicolor=3.0). Versicolor y virginica presentan solapamiento en petal_width [1.4–1.8 cm].
- Ausencia de target leakage confirmada: la columna `species` esta completamente ausente de X. Ningun identificador de fila presente.
- El archivo `data/gold/reference_stats.json` ha sido generado con los valores reales calculados sobre Gold (4 decimales de precision).
- Veredicto: **GO**. La capa Gold es apta para la construccion del pipeline de entrenamiento (Phase Modeling).

---

## 2. Verificacion de Invariantes Gold (contract.md §10.4)

Todos los valores provienen de la ejecucion real sobre `data/gold/X_gold.csv` y `data/gold/y_gold.csv`.

| ID | Invariante | Expresion | Valor Observado | Resultado |
|:---|:-----------|:----------|:----------------|:----------|
| GR-01 | Shape de X | `X.shape == (147, 4)` | (147, 4) | PASS |
| GR-02 | Shape de y | `y.shape == (147,)` | (147,) | PASS |
| GR-03 | Dtype de X | `X.dtype == float64` | float64 | PASS |
| GR-04 | Cero NaN en X | `np.isnan(X).sum() == 0` | 0 | PASS |
| GR-05 | Cero Inf en X | `np.isinf(X).sum() == 0` | 0 | PASS |
| GR-06 | Clases validas en y | `set(np.unique(y)) == {'setosa','versicolor','virginica'}` | {'setosa', 'versicolor', 'virginica'} | PASS |

**Resultado global: 6/6 invariantes PASS. Ningun bloqueador detectado.**

---

## 3. Validacion de Correlaciones (vs. contract.md §8.3)

### 3.1 Matriz de Correlacion Real (X_gold, n=147)

|  | sepal_length | sepal_width | petal_length | petal_width |
|:---|:---|:---|:---|:---|
| **sepal_length** | 1.000 | -0.109 | 0.871 | 0.817 |
| **sepal_width** | -0.109 | 1.000 | -0.421 | -0.356 |
| **petal_length** | 0.871 | -0.421 | 1.000 | 0.962 |
| **petal_width** | 0.817 | -0.356 | 0.962 | 1.000 |

### 3.2 Comparacion contra Referencia (contract.md §8.3)

| Par de Features | Correlacion Referencia | Correlacion Real | Desviacion | Estado |
|:----------------|:----------------------|:-----------------|:-----------|:-------|
| sepal_length / sepal_width | -0.109 | -0.109 | 0.000 | PASS |
| sepal_length / petal_length | 0.872 | 0.871 | -0.001 | PASS |
| sepal_length / petal_width | 0.818 | 0.817 | -0.001 | PASS |
| sepal_width / petal_length | -0.421 | -0.421 | 0.000 | PASS |
| sepal_width / petal_width | -0.357 | -0.356 | +0.001 | PASS |
| petal_length / petal_width | 0.963 | 0.962 | -0.001 | PASS |

**Desviacion maxima observada:** ±0.001. Dentro de la tolerancia de redondeo de 3 decimales del contrato. No se detectan desviaciones estructurales.

### 3.3 Interpretacion de Correlaciones Criticas

- **petal_length / petal_width (0.962):** Correlacion biologica esperada. Las flores con petalos largos tambien tienen petalos anchos. No constituye target leakage porque ambas son variables de entrada al modelo, no proxies del target.
- **sepal_length / petal_length (0.871):** Correlacion inter-feature moderadamente alta. No eliminar: ambas aportan informacion discriminativa segun el ANOVA (seeccion 6).
- **sepal_width (correlaciones bajas con el resto):** Feature relativamente independiente. Contribuye informacion ortogonal al resto del feature set.

---

## 4. Estadisticas Descriptivas Gold (X)

### 4.1 Dataset Completo (n=147)

Valores calculados directamente sobre `data/gold/X_gold.csv`.

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

### 4.2 Distribucion de Clases en y (n=147)

| Clase | Conteo | Porcentaje |
|:------|:-------|:-----------|
| setosa | 48 | 32.65% |
| versicolor | 50 | 34.01% |
| virginica | 49 | 33.33% |
| **TOTAL** | **147** | **100.00%** |

**Ratio de desbalance Gold:** max_clase / min_clase = 50 / 48 = 1.042. Desbalance < 5%. No se requieren tecnicas de balanceo. Confirma invariante del contract.md seccion 4.2.

---

## 5. Varianza por Feature

La varianza (ddof=1) mide la dispersion de cada feature en el espacio Gold. Features con mayor varianza aportan mas informacion al modelo.

| Feature | Varianza | Std | CV (%) | Interpretacion |
|:--------|:---------|:----|:-------|:---------------|
| sepal_length | 0.6874 | 0.8291 | 14.16% | Varianza moderada. Buen poder discriminativo entre clases. |
| sepal_width | 0.1910 | 0.4370 | 14.30% | Menor varianza del set. Feature con alta solapamiento entre clases pero contribuye informacion ortogonal. |
| petal_length | 3.0945 | 1.7591 | 46.53% | Mayor varianza absoluta. Feature dominante para separacion setosa vs. el resto. |
| petal_width | 0.5744 | 0.7579 | 62.69% | Mayor coeficiente de variacion relativa. Feature critica en zona de solapamiento versicolor/virginica. |

**Conclusion de varianza:** Las 4 features tienen varianza no-nula y estadisticamente significativa. Ninguna feature es constante ni cuasi-constante. No se justifica eliminar ninguna feature en esta etapa.

---

## 6. Separabilidad de Clases

### 6.1 Estadisticas por Clase

| Feature | setosa (n=48) | versicolor (n=50) | virginica (n=49) |
|:--------|:-------------|:------------------|:-----------------|
| sepal_length | 5.0104 ± 0.3592 | 5.9360 ± 0.5162 | 6.6041 ± 0.6321 |
| sepal_width | 3.4312 ± 0.3832 | 2.7700 ± 0.3138 | 2.9796 ± 0.3234 |
| petal_length | 1.4625 ± 0.1770 | 4.2600 ± 0.4699 | 5.5612 ± 0.5537 |
| petal_width | 0.2500 ± 0.1052 | 1.3260 ± 0.1978 | 2.0286 ± 0.2769 |

### 6.2 ANOVA de Una Via (F-Statistic)

| Feature | F-Statistic | p-valor | Conclusion |
|:--------|:-----------|:--------|:-----------|
| sepal_length | 116.7 | 7.53e-31 | Alta separabilidad. |
| sepal_width | 47.9 | 1.15e-16 | Separabilidad significativa aunque menor que el resto. |
| petal_length | 1132.4 | 8.18e-89 | Feature dominante. Separabilidad maxima en el set. |
| petal_width | 915.2 | 1.35e-82 | Feature critica. Segunda mayor separabilidad. |

Todos los p-valores son << 0.05. Las 4 features rechazan la hipotesis nula de medias iguales entre clases.

### 6.3 Analisis de Gaps y Solapamiento

**setosa — separacion perfecta en petal_length:**
- Max petal_length setosa: **1.9 cm**
- Min petal_length versicolor: **3.0 cm**
- Gap de separacion: **1.1 cm** (sin solapamiento)
- Conclusion: un umbral simple `petal_length < 2.0 cm` clasifica setosa con precision perfecta sobre este dataset. Consistent con la descripcion en el BRD y el contrato (petal_length Feature dominante, F=1179 en feasibility).

**versicolor / virginica — zona de solapamiento en petal_width:**
- Max petal_width versicolor: **1.8 cm**
- Min petal_width virginica: **1.4 cm**
- Zona de solapamiento: **[1.4, 1.8] cm** (4 mm de amplitud)
- Conclusion: la separacion versicolor/virginica no es linealmente perfecta en ninguna feature individual. El modelo necesitara las 4 features para maximizar la precision en esta frontera. Este solapamiento es el principal reto de clasificacion del proyecto, consistente con el BRD.

---

## 7. Verificacion de Ausencia de Target Leakage en X

| Verificacion | Resultado | Detalle |
|:-------------|:----------|:--------|
| Columna `species` ausente de X | PASS | `'species' not in X.columns` — confirmado |
| Columna `target` ausente de X | PASS | `'target' not in X.columns` — confirmado |
| Columna `Id` ausente de X | PASS | Eliminada en transformacion M-01 (Silver). No propagada a Gold. |
| Columnas de X = 4 features de dominio | PASS | `list(X.columns) == ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']` |
| Correlacion de cualquier feature con y | INFORMATIVO | Las correlaciones son de dominio biologico, no de fuga de informacion. Verificado en la seccion de correlaciones. |

**Conclusion:** No existe target leakage en X. El array de features contiene exclusivamente las 4 mediciones morfologicas definidas en el contrato. La alta correlacion de petal_length y petal_width con la especie es una caracteristica biologica del dataset Iris, no una fuga de datos.

---

## 8. Tipos de Datos Gold

| Artefacto | Columna | Tipo Esperado (contract.md §4.1-4.2) | Tipo Observado | Conformidad |
|:----------|:--------|:--------------------------------------|:---------------|:------------|
| X_gold | `sepal_length` | `float64` | `float64` | OK |
| X_gold | `sepal_width` | `float64` | `float64` | OK |
| X_gold | `petal_length` | `float64` | `float64` | OK |
| X_gold | `petal_width` | `float64` | `float64` | OK |
| y_gold | `species` | `object` (strings) | `object` | OK |

Todos los tipos de datos son conformes con el esquema Gold del contract.md secciones 4.1 y 4.2. La capa Gold no introduce conversiones de tipo respecto a Silver.

---

## 9. Estadisticas de Referencia — reference_stats.json

Los siguientes valores reales han sido calculados sobre `data/gold/X_gold.csv` (n=147) y escritos en `data/gold/reference_stats.json` con 4 decimales de precision, segun el contrato §11.1.

| Feature | mean | std | min | max |
|:--------|:-----|:----|:----|:----|
| sepal_length | 5.8565 | 0.8291 | 4.3 | 7.9 |
| sepal_width | 3.0558 | 0.4370 | 2.0 | 4.4 |
| petal_length | 3.7803 | 1.7591 | 1.0 | 6.9 |
| petal_width | 1.2088 | 0.7579 | 0.1 | 2.5 |

**Comparacion con valores del contrato §11.1 (aproximaciones del feasibility):**

| Feature | mean contrato | mean real | delta | std contrato | std real | delta |
|:--------|:-------------|:----------|:------|:------------|:---------|:------|
| sepal_length | 5.848 | 5.8565 | +0.0085 | 0.828 | 0.8291 | +0.0011 |
| sepal_width | 3.052 | 3.0558 | +0.0038 | 0.433 | 0.4370 | +0.0040 |
| petal_length | 3.758 | 3.7803 | +0.0223 | 1.764 | 1.7591 | -0.0049 |
| petal_width | 1.197 | 1.2088 | +0.0118 | 0.763 | 0.7579 | -0.0053 |

Todas las desviaciones son menores a 0.025. Las diferencias respecto al contrato son producto del redondeo de las estimaciones del feasibility. Los valores reales calculados en Phase Engineering son los definitivos para drift detection en produccion.

**Archivo generado:** `data/gold/reference_stats.json` — version 1.0.0.

---

## 10. Veredicto de Calidad

**VEREDICTO: GO**

### Justificacion Tecnica

1. **Invariantes formales:** Los 6 controles GR-01 a GR-06 pasan sin excepcion. X tiene shape (147, 4), dtype float64, 0 NaN, 0 Inf. y tiene shape (147,) con las 3 clases validas.

2. **Correlaciones dentro de tolerancia:** La desviacion maxima entre la matriz real y la de referencia del contract.md §8.3 es ±0.001, dentro de la tolerancia de redondeo. La correlacion critica petal_length/petal_width (0.962) es de origen biologico, no constituye leakage.

3. **Varianza significativa en las 4 features:** Ninguna feature es constante ni cuasi-constante. petal_length (var=3.0945) y petal_width (var=0.5744) concentran la mayor informacion discriminativa. El ANOVA confirma separabilidad estadistica altamente significativa en las 4 features (todos los p-valores < 1e-16).

4. **Separabilidad de clases documentada:** setosa es perfectamente separable en petal_length (gap=1.1 cm). El solapamiento versicolor/virginica en petal_width [1.4–1.8 cm] es el principal desafio de clasificacion; el modelo requiere las 4 features para resolverlo eficazmente.

5. **Ausencia confirmada de target leakage:** X contiene exclusivamente las 4 features morfologicas. `species`, `Id` y cualquier proxy del target estan ausentes. El pipeline de `gold_builder.py` no introduce contaminacion.

6. **Tipos de datos conformes:** Los 5 tipos observados (4 float64 en X + object en y) coinciden exactamente con el contrato.

7. **reference_stats.json generado:** Los estadisticos de referencia estan escritos con valores reales calculados sobre Gold (no estimaciones del feasibility). Listos para su uso en el modulo de drift detection de la Phase Delivery.

### Autorizacion de Paso a Phase Modeling

La capa Gold producida por `build_gold()` es apta para ser consumida por el pipeline de entrenamiento. El agente `ai-ml-engineer` puede proceder con la implementacion del modelo usando `data/gold/X_gold.csv` y `data/gold/y_gold.csv` como insumos, siguiendo las especificaciones del contract.md seccion 4 y el SAD.

---

> **Trazabilidad del Documento:**
> `eda_gold.md` <- `src/data/gold_builder.py` <- `data/silver/iris_silver.csv` <- `src/data/silver_cleaner.py` <- `data/bronze/Iris.csv` <- `contract.md v1.0.0` <- `eda_silver.md v1.0.0`
>
> **Documento anterior:** `docs/Phase_engineering/eda_silver.md`
> **Proximo documento:** Model QA Report (Phase Modeling)
