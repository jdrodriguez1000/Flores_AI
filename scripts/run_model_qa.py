# scripts/run_model_qa.py
# Trazable: F3-T07 | BRD §4 | SpecDD §4, §9 | contract.md §1
#
# Ejecuta el protocolo completo de Model QA:
#   1. Benchmarking (metricas sobre hold-out set y CV)
#   2. Matriz de confusion
#   3. Analisis de sesgo por clase
#   4. Stress test con valores en los limites del contrato y fuera de rango
#
# Uso: .venv/Scripts/python scripts/run_model_qa.py

import sys
from pathlib import Path

# -- Asegurar que el proyecto raiz este en el path --------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from src import config
from src.training.serializer import load_model


# ---------------------------------------------------------------------------
# 1. Cargar modelo y datos
# ---------------------------------------------------------------------------
print("=" * 60)
print("MODEL QA — Flores AI - Iris")
print("=" * 60)

pipeline = load_model(config.MODEL_PATH)
print(f"[OK] Modelo cargado desde: {config.MODEL_PATH}")
print(f"     Pipeline steps: {[s[0] for s in pipeline.steps]}")
print(f"     Classifier: {type(pipeline.named_steps['clf']).__name__}")

X = pd.read_csv(config.DATA_GOLD_X).values
y = pd.read_csv(config.DATA_GOLD_Y).values.ravel()
print(f"[OK] Gold data cargada: X.shape={X.shape}, y.shape={y.shape}")


# ---------------------------------------------------------------------------
# 2. Reproducir hold-out split identico al entrenamiento
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=config.TEST_SIZE,
    random_state=config.RANDOM_STATE,
    stratify=y,
)
print(f"[OK] Hold-out split: n_train={len(X_train)}, n_test={len(X_test)}")


# ---------------------------------------------------------------------------
# 3. Predicciones en hold-out set
# ---------------------------------------------------------------------------
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)

classes = config.CLASS_NAMES  # ['setosa', 'versicolor', 'virginica']

accuracy_test = accuracy_score(y_test, y_pred)
f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
f1_scores_raw = f1_score(y_test, y_pred, labels=classes, average=None, zero_division=0)
f1_per_class = dict(zip(classes, f1_scores_raw.tolist()))

cm = confusion_matrix(y_test, y_pred, labels=classes)

print("\n--- BENCHMARKING ---")
print(f"Accuracy (hold-out): {accuracy_test:.4f}")
print(f"F1-Macro (hold-out): {f1_macro:.4f}")
for cls, score in f1_per_class.items():
    print(f"  F1 {cls}: {score:.4f}")

print("\n--- MATRIZ DE CONFUSION ---")
print(f"           {'  '.join(classes)}")
for i, cls in enumerate(classes):
    print(f"  {cls:12s} {cm[i]}")

# Classification report for full detail
print("\n--- CLASSIFICATION REPORT ---")
print(classification_report(y_test, y_pred, labels=classes, zero_division=0))


# ---------------------------------------------------------------------------
# 4. Analisis de sesgo por clase
# ---------------------------------------------------------------------------
print("\n--- ANALISIS DE SESGO POR CLASE ---")
error_rates = {}
for i, cls in enumerate(classes):
    mask = y_test == cls
    n_cls = mask.sum()
    if n_cls == 0:
        error_rates[cls] = {"n": 0, "errors": 0, "error_rate": 0.0}
        continue
    errors = (y_pred[mask] != y_test[mask]).sum()
    error_rate = errors / n_cls
    error_rates[cls] = {"n": int(n_cls), "errors": int(errors), "error_rate": float(error_rate)}
    print(f"  {cls:12s}: n={n_cls}, errores={errors}, tasa_error={error_rate:.4f} ({error_rate*100:.1f}%)")

# Confusion between versicolor and virginica
vc_idx = classes.index("versicolor")
vg_idx = classes.index("virginica")
vc_misclassified_as_vg = cm[vc_idx][vg_idx]
vg_misclassified_as_vc = cm[vg_idx][vc_idx]
print(f"\n  Confusion critica Versicolor->Virginica: {vc_misclassified_as_vg}")
print(f"  Confusion critica Virginica->Versicolor: {vg_misclassified_as_vc}")

max_error = max(v["error_rate"] for v in error_rates.values())
min_error = min(v["error_rate"] for v in error_rates.values())
disparity = max_error - min_error
print(f"\n  Disparidad maxima de tasa de error entre clases: {disparity:.4f}")


# ---------------------------------------------------------------------------
# 5. Stress test — valores en los limites del contrato (contract.md §1, VR-01..VR-04)
# ---------------------------------------------------------------------------
print("\n--- STRESS TEST: LIMITES DEL CONTRATO ---")

STRESS_CASES = {
    "min_boundary": {
        "sepal_length": 3.0, "sepal_width": 1.5,
        "petal_length": 0.5, "petal_width": 0.0,
        "description": "Todos los features en su minimo contractual",
    },
    "max_boundary": {
        "sepal_length": 9.0, "sepal_width": 5.5,
        "petal_length": 8.0, "petal_width": 3.5,
        "description": "Todos los features en su maximo contractual",
    },
    "typical_setosa": {
        "sepal_length": 5.1, "sepal_width": 3.5,
        "petal_length": 1.4, "petal_width": 0.2,
        "description": "Valor tipico Setosa (BRD §8 happy path)",
    },
    "ambiguous_boundary": {
        "sepal_length": 6.0, "sepal_width": 2.7,
        "petal_length": 4.2, "petal_width": 1.6,
        "description": "Zona de solapamiento Versicolor/Virginica",
    },
    "sepal_only": {
        "sepal_length": 7.0, "sepal_width": 3.0,
        "petal_length": 4.0, "petal_width": 1.5,
        "description": "Valores intermedios, zona gris",
    },
}

stress_results = {}
for case_id, case in STRESS_CASES.items():
    x_vec = np.array([[
        case["sepal_length"], case["sepal_width"],
        case["petal_length"], case["petal_width"]
    ]])
    try:
        pred = pipeline.predict(x_vec)[0]
        proba = pipeline.predict_proba(x_vec)[0]
        confidence = float(proba.max())
        valid_class = pred in config.CLASS_NAMES
        stress_results[case_id] = {
            "status": "OK",
            "predicted": pred,
            "confidence": confidence,
            "valid_class": valid_class,
        }
        print(f"  [{case_id}] {case['description']}")
        print(f"    Prediccion: {pred} | Confianza: {confidence:.4f} | Clase valida: {valid_class}")
    except Exception as e:
        stress_results[case_id] = {"status": "ERROR", "error": str(e)}
        print(f"  [{case_id}] ERROR: {e}")


# ---------------------------------------------------------------------------
# 6. Stress test — valores FUERA de rango (comportamiento documentado)
# ---------------------------------------------------------------------------
print("\n--- STRESS TEST: FUERA DE RANGO (sin validacion) ---")
OUT_OF_RANGE_CASES = {
    "below_min_sepal_length": {
        "vec": [2.0, 3.0, 1.4, 0.2],
        "description": "sepal_length=2.0 (bajo minimo contractual 3.0)",
    },
    "above_max_sepal_length": {
        "vec": [15.0, 3.5, 1.4, 0.2],
        "description": "sepal_length=15.0 (sobre maximo contractual 9.0)",
    },
    "extreme_petal": {
        "vec": [5.0, 3.0, 15.0, 5.0],
        "description": "petal_length=15.0, petal_width=5.0 (extremos biologicamente imposibles)",
    },
    "negative_values": {
        "vec": [-1.0, -1.0, -1.0, -1.0],
        "description": "Todos negativos (imposible biologicamente)",
    },
    "zeros": {
        "vec": [0.0, 0.0, 0.0, 0.0],
        "description": "Todos cero (imposible biologicamente)",
    },
}

oor_results = {}
for case_id, case in OUT_OF_RANGE_CASES.items():
    x_vec = np.array([case["vec"]])
    try:
        pred = pipeline.predict(x_vec)[0]
        proba = pipeline.predict_proba(x_vec)[0]
        confidence = float(proba.max())
        valid_class = pred in config.CLASS_NAMES
        oor_results[case_id] = {
            "status": "PREDICTED_WITHOUT_ERROR",
            "predicted": pred,
            "confidence": confidence,
            "valid_class": valid_class,
        }
        print(f"  [{case_id}] {case['description']}")
        print(f"    -> Modelo NO lanza excepcion. Predice: {pred} | Confianza: {confidence:.4f}")
        print(f"       NOTA: La validacion de rango debe ocurrir en validators.py (IrisInput), no en el Pipeline.")
    except Exception as e:
        oor_results[case_id] = {"status": "EXCEPTION", "error": str(e)}
        print(f"  [{case_id}] Excepcion lanzada: {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# 7. Veredicto GO/NO-GO
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("VEREDICTO GO/NO-GO")
print("=" * 60)

# BRD §4.1 thresholds
THRESHOLD_ACCURACY = 0.95  # GREEN
THRESHOLD_F1_MACRO = 0.95  # GREEN
THRESHOLD_F1_CLASS = 0.90  # RED (minimo por clase)

checks = {
    "accuracy_test >= 0.95": accuracy_test >= THRESHOLD_ACCURACY,
    "f1_macro_test >= 0.95": f1_macro >= THRESHOLD_F1_MACRO,
    "f1_setosa >= 0.90": f1_per_class["setosa"] >= THRESHOLD_F1_CLASS,
    "f1_versicolor >= 0.90": f1_per_class["versicolor"] >= THRESHOLD_F1_CLASS,
    "f1_virginica >= 0.90": f1_per_class["virginica"] >= THRESHOLD_F1_CLASS,
    "stress_boundary_no_exception": all(
        v["status"] == "OK" for v in stress_results.values()
    ),
    "stress_boundary_valid_class": all(
        v.get("valid_class", False) for v in stress_results.values()
    ),
}

all_pass = all(checks.values())
for check_name, passed in checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {check_name}")

print()
if all_pass:
    print("VEREDICTO FINAL: ** GO ** — El modelo cumple todos los criterios del BRD §4.")
else:
    failed = [k for k, v in checks.items() if not v]
    print("VEREDICTO FINAL: ** NO-GO ** — Criterios fallidos:")
    for f in failed:
        print(f"  - {f}")


# ---------------------------------------------------------------------------
# 8. Exportar resultados como JSON (para uso en el reporte)
# ---------------------------------------------------------------------------
results_summary = {
    "accuracy_test": accuracy_test,
    "f1_macro_test": f1_macro,
    "f1_per_class": f1_per_class,
    "confusion_matrix": cm.tolist(),
    "error_rates": error_rates,
    "vc_vg_confusion": {
        "versicolor_as_virginica": int(vc_misclassified_as_vg),
        "virginica_as_versicolor": int(vg_misclassified_as_vc),
    },
    "disparity_max_min_error": disparity,
    "stress_results": stress_results,
    "oor_results": oor_results,
    "verdict": "GO" if all_pass else "NO-GO",
    "checks": checks,
    "n_train": len(X_train),
    "n_test": len(X_test),
    "random_state": config.RANDOM_STATE,
    "test_size": config.TEST_SIZE,
    "classifier_type": type(pipeline.named_steps['clf']).__name__,
}

output_path = PROJECT_ROOT / "scripts" / "qa_results.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results_summary, f, indent=2)
print(f"\n[OK] Resultados exportados a: {output_path}")
