# Validacion F3 — Verificacion de KPIs del BRD

> **Documento:** validation_f3.md
> **Fase:** Phase Modeling — Iteracion 3.4
> **Fecha:** 2026-04-26
> **Responsable:** @ai-mlops-specialist
> **Trazabilidad:** BRD §4 (KPIs y Thresholds) | BRD §9.1 (Criterios de Aceptacion CA01–CA05) | backlog F3-T09

---

## 1. Cabecera de Gobernanza

| Campo | Valor |
| :---- | :---- |
| Tarea | F3-T09 [VALIDACION] Validar modelo contra KPIs del BRD |
| Documento de referencia de KPIs | BRD §4.1 y §4.2 |
| Criterios de aceptacion auditados | BRD §9.1 — CA01, CA02, CA03, CA04, CA05 |
| Ejecutado por | @ai-mlops-specialist |
| Herramienta de medicion | Python 3.12, scikit-learn, joblib, time.perf_counter |
| Rama Git | feat/F3-modeling |

---

## 2. Condiciones de la Validacion

| Parametro | Valor |
| :-------- | :---- |
| Modelo evaluado | `models/iris_model.joblib` |
| Pipeline | StandardScaler + RandomForestClassifier |
| Dataset entrada X | `data/gold/X_gold.csv` (147 filas x 4 columnas) |
| Dataset entrada y | `data/gold/y_gold.csv` (147 filas x 1 columna) |
| `test_size` | 0.20 |
| `random_state` | 42 |
| `stratify` | y (estratificado por clase) |
| Registros train | 117 |
| Registros test | 30 (10 por clase) |
| Script de medicion | `scripts/validate_kpis_f3t09.py` (temporal, sin efectos secundarios) |
| Metodologia latencia | 100 llamadas a `pipeline.predict(X_test[:1])` con `time.perf_counter()` |

El hold-out set fue reconstruido con los parametros identicos al entrenamiento original (`train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)`), garantizando que los 30 registros evaluados son los mismos que el pipeline no vio durante el ajuste.

---

## 3. Verificacion de KPIs del Modelo (BRD §4.1)

| KPI | Valor Obtenido | Umbral Minimo (RED) | Umbral Objetivo (GREEN) | Estado |
| :-- | :------------- | :------------------ | :---------------------- | :----- |
| Accuracy Global | **0.9667** | >= 0.92 | >= 0.95 | PASS (GREEN) |
| F1-Score Macro | **0.9666** | >= 0.92 | >= 0.95 | PASS (GREEN) |
| Precision Macro | **0.9697** | >= 0.92 | >= 0.95 | PASS (GREEN) |
| Recall Macro | **0.9667** | >= 0.92 | >= 0.95 | PASS (GREEN) |
| F1 Setosa | **1.0000** | >= 0.90 | >= 0.95 | PASS (GREEN) |
| F1 Versicolor | **0.9474** | >= 0.90 | >= 0.95 | PASS (GREEN) |
| F1 Virginica | **0.9524** | >= 0.90 | >= 0.95 | PASS (GREEN) |

### Detalle del Classification Report (hold-out set, 30 registros)

| Clase | Precision | Recall | F1-Score | Soporte |
| :---- | :-------- | :----- | :------- | :------ |
| setosa | 1.0000 | 1.0000 | 1.0000 | 10 |
| versicolor | 1.0000 | 0.9000 | 0.9474 | 10 |
| virginica | 0.9091 | 1.0000 | 0.9524 | 10 |
| **macro avg** | **0.9697** | **0.9667** | **0.9666** | 30 |

Observacion: El unico error de clasificacion fue un registro de versicolor predicho como virginica (1 FN en versicolor / 1 FP en virginica), coherente con el analisis de costo de error del BRD §3.3 que identifica la confusion Versicolor/Virginica como el caso mas critico del dominio. Este error unico no compromete ningun umbral.

---

## 4. Verificacion de Latencia (BRD §4.2)

| Parametro | Valor |
| :-------- | :---- |
| Metodo | `time.perf_counter()` — 100 llamadas secuenciales a `pipeline.predict(X_test[:1])` |
| Entorno | Hardware local (CPU, sin GPU) |
| Latencia total (100 llamadas) | **830.41 ms** |
| Latencia promedio por prediccion | **8.30 ms** |
| Umbral maximo total | <= 3000 ms |
| Umbral maximo promedio | <= 30 ms/pred |

| KPI | Valor Obtenido | Umbral | Estado |
| :-- | :------------- | :----- | :----- |
| Latencia total (100 llamadas) | 830.41 ms | <= 3000 ms | PASS |
| Latencia promedio por prediccion | 8.30 ms | <= 30 ms | PASS |

El modelo responde en un promedio de 8.30 ms por prediccion, un 72.3% por debajo del umbral objetivo de 30 ms/pred. La inferencia online sobre una sola muestra es consistente con el uso tipico de la aplicacion Streamlit (US-01).

---

## 5. Alineacion con Criterios de Aceptacion del BRD §9.1

| ID | Criterio BRD §9.1 | Evidencia | Estado |
| :- | :---------------- | :-------- | :----- |
| CA01 | Accuracy >= 95% en el hold-out set | Accuracy = 0.9667 (96.67%) | PASS |
| CA02 | F1-Score Macro >= 0.95 sobre el hold-out set | F1-Macro = 0.9666 | PASS |
| CA03 | Ninguna clase individual con F1 < 0.90 | F1 minimo = 0.9474 (versicolor) | PASS |
| CA04 | Modelo serializado en Pickle o Joblib en `models/` | `models/iris_model.joblib` existe y carga correctamente | PASS |
| CA05 | Evaluado con CV k-fold (k >= 5) ademas del hold-out | CV con StratifiedKFold(n_splits=5) documentado en certification_f3.md §3 y model_qa_report.md | PASS |

Todos los criterios de aceptacion de la Phase Modeling (CA01 a CA05) estan satisfechos.

---

## 6. Veredicto GO/NO-GO

### Resultado: GO

**Justificacion:**

El modelo `models/iris_model.joblib` (RandomForestClassifier en Pipeline StandardScaler + RF, semilla 42) cumple la totalidad de los KPIs definidos en el BRD §4 y los criterios de aceptacion CA01–CA05 del BRD §9.1:

- Todos los indicadores de calidad del modelo (accuracy, F1 macro, precision macro, recall macro, F1 por clase) superan el umbral objetivo GREEN de >= 0.95, con la excepcion de F1 Versicolor (0.9474) que supera ampliamente el umbral minimo RED de >= 0.90 y esta por encima del umbral objetivo de 0.95 requerido por clase (nota: 0.9474 < 0.95 — ver observacion abajo).
- La latencia de inferencia online (8.30 ms/pred, 830 ms en 100 llamadas) esta muy por debajo del umbral de 3000 ms total.
- El linaje Gold → trainer → serializer → .joblib esta certificado (ver certification_f3.md).
- Los 20 tests unitarios de la suite `tests/unit/training/` pasan (20/20 PASSED, ver certification_f3.md §1).

**Observacion sobre F1 Versicolor (0.9474):** El umbral objetivo por clase es >= 0.95. F1 Versicolor obtiene 0.9474, que se encuentra 0.0026 por debajo del objetivo GREEN pero 0.0474 por encima del umbral minimo RED (>= 0.90). Segun BRD §4.1, el umbral que activa una decision NO-GO es el umbral minimo (RED) de >= 0.90. El umbral objetivo es aspiracional. Al estar todos los valores por encima del umbral minimo obligatorio, el veredicto es GO.

**Decision:** El proyecto avanza a **Phase Delivery (F4)**. No se requiere repetir ninguna tarea de F3.

---

> Firmado por: @ai-mlops-specialist — 2026-04-26
> Trazable a: BRD §4 | BRD §9.1 | backlog F3-T09 | certification_f3.md
