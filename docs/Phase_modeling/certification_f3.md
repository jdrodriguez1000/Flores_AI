# Certificacion F3 — Linaje Gold → Pipeline → .joblib

> **Documento:** certification_f3.md
> **Fase:** Phase Modeling — Iteracion 3.4
> **Fecha:** 2026-04-26
> **Responsable:** @ai-data-qa-engineer
> **Trazabilidad:** SAD §9 | SpecDD §9–10 | BRD §4

---

## 1. Evidencia de Tests (pytest tests/unit/training/)

Comando ejecutado:

```
python -m pytest tests/unit/training/ -v
```

Output exacto:

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\USUARIO\Documents\Work\ML\Flores_AI
configfile: pytest.ini

collected 20 items

tests/unit/training/test_serializer.py::test_save_model_creates_file PASSED [  5%]
tests/unit/training/test_serializer.py::test_save_model_persists_pipeline_instance PASSED [ 10%]
tests/unit/training/test_serializer.py::test_save_model_raises_type_error_on_non_pipeline PASSED [ 15%]
tests/unit/training/test_serializer.py::test_load_model_returns_pipeline PASSED [ 20%]
tests/unit/training/test_serializer.py::test_load_model_raises_file_not_found_error PASSED [ 25%]
tests/unit/training/test_trainer.py::test_build_pipeline_returns_pipeline PASSED [ 30%]
tests/unit/training/test_trainer.py::test_build_pipeline_has_two_steps PASSED [ 35%]
tests/unit/training/test_trainer.py::test_build_pipeline_scaler_step PASSED [ 40%]
tests/unit/training/test_trainer.py::test_build_pipeline_clf_step PASSED [ 45%]
tests/unit/training/test_trainer.py::test_build_pipeline_is_unfitted PASSED [ 50%]
tests/unit/training/test_trainer.py::test_train_and_evaluate_return_type PASSED [ 55%]
tests/unit/training/test_trainer.py::test_training_metrics_required_keys PASSED [ 60%]
tests/unit/training/test_trainer.py::test_training_metrics_n_split_consistency PASSED [ 65%]
tests/unit/training/test_trainer.py::test_training_metrics_random_state PASSED [ 70%]
tests/unit/training/test_trainer.py::test_training_metrics_accuracy_threshold PASSED [ 75%]
tests/unit/training/test_trainer.py::test_train_and_evaluate_pipeline_is_fitted PASSED [ 80%]
tests/unit/training/test_trainer.py::test_training_metrics_f1_per_class_structure PASSED [ 85%]
tests/unit/training/test_trainer.py::test_training_metrics_float_values_in_range PASSED [ 90%]
tests/unit/training/test_trainer.py::test_train_and_evaluate_empty_X_raises_value_error PASSED [ 95%]
tests/unit/training/test_trainer.py::test_train_and_evaluate_mismatched_dimensions_raises_value_error PASSED [100%]

============================= 20 passed in 4.57s ==============================
```

Suites cubiertas:
- `test_serializer.py`: 5 tests — invariantes SM-01, SM-02, SM-03, LM-01, LM-02 (SpecDD §10)
- `test_trainer.py`: 15 tests — invariantes BP-01..BP-05, TA-01..TA-10 (SpecDD §9)

**Veredicto:** PASSED

---

## 2. Trazabilidad del Linaje

| Capa | Artefacto | Tamano / MD5 (12 chars) | Estado |
| :--- | :-------- | :---------------------- | :----- |
| Gold (entrada X) | data/gold/X_gold.csv | 2 550 bytes / eb41b668d317 | OK |
| Gold (entrada y) | data/gold/y_gold.csv | 1 532 bytes / 4b919470da35 | OK |
| Codigo | src/training/trainer.py | 2 865 bytes / f5b6d4e34b5f | OK |
| Codigo | src/training/serializer.py | 1 097 bytes / fb9661de1e1b | OK |
| Modelo | models/iris_model.joblib | 161.21 KB / ab7918087f7f | OK |

Cadena verificada: `data/gold/X_gold.csv` + `data/gold/y_gold.csv` → `trainer.train_and_evaluate()` → `serializer.save_model()` → `models/iris_model.joblib`

El artefacto cargado es instancia de `sklearn.pipeline.Pipeline` con steps `['scaler', 'clf']`, consistente con la arquitectura definida en SAD §2.2 (StandardScaler + RandomForestClassifier).

---

## 3. Reproducibilidad (Semilla 42)

Ejecutado `train_and_evaluate()` dos veces independientes con `RandomForestClassifier(random_state=42)` sobre los mismos arrays Gold.

```
Reproducibilidad OK: setosa == setosa
Run 1 accuracy_test: 0.9667
Run 2 accuracy_test: 0.9667
accuracy_test identico en ambas ejecuciones: OK
```

**accuracy_test Run 1:** 0.9667
**accuracy_test Run 2:** 0.9667
**Prediccion fixture (5.1, 3.5, 1.4, 0.2):** Run1=[setosa] | Run2=[setosa]
**Veredicto:** REPRODUCIBLE

---

## 4. Validacion de Inferencia (PredictionResult)

**Fixture utilizado:** `IrisInput(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)` — setosa clasico

Ejecutado directamente sobre `models/iris_model.joblib`:

```
Especie predicha: setosa
Probabilidades raw: [[1. 0. 0.]]
Probabilidades: {setosa: 1.0, versicolor: 0.0, virginica: 0.0}
Confidence: 1.0000
low_confidence flag: False
species en CLASS_NAMES: True
```

**Especie predicha:** setosa
**Confidence:** 1.0000
**Probabilidades:** {setosa: 1.0000, versicolor: 0.0000, virginica: 0.0000}
**low_confidence flag:** False (confidence 1.0000 > umbral 0.60)
**species en CLASS_NAMES:** True (valor pertenece a {'setosa', 'versicolor', 'virginica'})

El fixture (5.1, 3.5, 1.4, 0.2) esta dentro de los rangos contractuales de IrisInput definidos en SpecDD §1.1 y contract.md §1. La prediccion es determinista y coherente con el Stress Test documentado en model_qa_report.md §5.1 (caso `typical_setosa`).

---

## 5. Auditoria de Ingenieria

### 5.1 Rutas absolutas

Auditoria ejecutada sobre archivos `.py` en `src/training/`:

```
Inspeccion de src/training/trainer.py y src/training/serializer.py
Patrones buscados: C:/, /home/, /Users/, letra de unidad Windows

Resultado: CLEAN — Sin rutas absolutas hardcoded en .py de src/training/
```

El grep que reporto coincidencias en la primera ejecucion fue sobre archivos binarios `.pyc` de `__pycache__` (compilados por Python), no sobre codigo fuente. Los archivos `.py` auditados no contienen ninguna ruta absoluta. Las rutas se resuelven exclusivamente via `src/config.py` usando `Path(__file__).resolve().parent.parent` (ADR-004 del SAD §7).

### 5.2 Dependencias en requirements.txt

```
scikit-learn>=1.4
joblib>=1.3
```

Ambas dependencias criticas del pipeline de modelado estan declaradas en `requirements.txt`. La constriccion de version es compatible con el stack definido en SAD §4.1 (scikit-learn 1.5.x, joblib 1.4.x). No se detectaron dependencias implicitas no declaradas.

---

## 6. Veredicto Final

| Criterio | Resultado |
| :------- | :-------- |
| Tests F3 en verde (pytest tests/unit/training/) | 20/20 PASSED |
| Trazabilidad Gold → trainer → serializer → .joblib | OK |
| Reproducibilidad (semilla 42) | REPRODUCIBLE |
| Sin rutas absolutas en src/training/ | OK |
| Dependencias declaradas en requirements.txt | OK |
| PredictionResult valido sobre fixture | OK |

**CERTIFICACION FASE 3:** CERTIFICADO

---

> Firmado por: @ai-data-qa-engineer — 2026-04-26
> Trazable a: SAD §9 | SpecDD §9–10 | BRD §4 | backlog F3-T08
