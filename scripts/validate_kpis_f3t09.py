# scripts/validate_kpis_f3t09.py
# Script temporal de validacion F3-T09.
# Trazable: BRD §4 | backlog F3-T09
# NO modifica ningun artefacto de src/, models/ ni data/.

import time
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH   = PROJECT_ROOT / "models" / "iris_model.joblib"
DATA_GOLD_X  = PROJECT_ROOT / "data" / "gold" / "X_gold.csv"
DATA_GOLD_Y  = PROJECT_ROOT / "data" / "gold" / "y_gold.csv"

RANDOM_STATE = 42
TEST_SIZE    = 0.20
CLASS_NAMES  = ["setosa", "versicolor", "virginica"]

# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
pipeline = joblib.load(MODEL_PATH)
X = pd.read_csv(DATA_GOLD_X).values
y = pd.read_csv(DATA_GOLD_Y).values.ravel()

# ---------------------------------------------------------------------------
# Hold-out set (identicos parametros al entrenamiento original)
# ---------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# ---------------------------------------------------------------------------
# Metricas de clasificacion
# ---------------------------------------------------------------------------
y_pred = pipeline.predict(X_test)

accuracy  = accuracy_score(y_test, y_pred)
f1_macro  = f1_score(y_test, y_pred, average="macro", zero_division=0)
prec_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
rec_macro  = recall_score(y_test, y_pred, average="macro", zero_division=0)

f1_per_class_arr = f1_score(y_test, y_pred, labels=CLASS_NAMES, average=None, zero_division=0)
f1_per_class = dict(zip(CLASS_NAMES, f1_per_class_arr.tolist()))

report = classification_report(y_test, y_pred, labels=CLASS_NAMES, zero_division=0)

# ---------------------------------------------------------------------------
# Latencia: 100 llamadas de predict sobre una sola muestra (inferencia online)
# ---------------------------------------------------------------------------
sample = X_test[:1]
N_CALLS = 100

start = time.perf_counter()
for _ in range(N_CALLS):
    pipeline.predict(sample)
end = time.perf_counter()

latency_total_ms  = (end - start) * 1000
latency_avg_ms    = latency_total_ms / N_CALLS

# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------
print("=" * 60)
print("VALIDACION DE KPIs F3-T09 — Flores AI - Iris")
print("=" * 60)
print(f"n_train : {len(X_train)}")
print(f"n_test  : {len(X_test)}")
print()
print(f"Accuracy Global          : {accuracy:.4f}")
print(f"F1-Score Macro           : {f1_macro:.4f}")
print(f"Precision Macro          : {prec_macro:.4f}")
print(f"Recall Macro             : {rec_macro:.4f}")
print()
for cls, val in f1_per_class.items():
    print(f"F1 {cls:<12}: {val:.4f}")
print()
print("Classification Report:")
print(report)
print("-" * 60)
print(f"Latencia total  ({N_CALLS} llamadas): {latency_total_ms:.2f} ms")
print(f"Latencia promedio por prediccion   : {latency_avg_ms:.4f} ms")
print("=" * 60)
