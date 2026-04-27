# Trazable: SpecDD §9-10 | BRD §4.1 KPI-01 | backlog F3-T06
"""
Script de entrenamiento certificado — Flores AI (Iris).

Ejecuta el ciclo completo de entrenamiento sobre el dataset Gold, verifica
que las metricas superen los umbrales BRD KPI-01, y persiste el pipeline
en models/iris_model.joblib.

Uso:
    python -m src.training.run_training
    # o directamente:
    .venv/Scripts/python src/training/run_training.py

Algoritmo ganador: RandomForestClassifier
Criterio de seleccion: Simplicidad Primero — modelo mas simple que supera
    f1_macro_test >= 0.95 (BRD §4.1 KPI-01), segun notebook 03_model_selection.ipynb.
    LogisticRegression obtuvo f1_macro_test=0.9333 (por debajo del umbral GREEN).
    RandomForestClassifier obtuvo f1_macro_test=0.9666 (supera el umbral).
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from src import config
from src.training.trainer import TrainingMetrics, train_and_evaluate
from src.training.serializer import save_model


# ---------------------------------------------------------------------------
# Umbral de aceptacion BRD §4.1 KPI-01
# ---------------------------------------------------------------------------
ACCURACY_TEST_THRESHOLD: float = 0.95


def load_gold_data() -> tuple[np.ndarray, np.ndarray]:
    """Carga los arrays Gold desde el Feature Store en data/gold/.

    Returns:
        tuple[np.ndarray, np.ndarray]:
            X: Array de features con shape (147, 4), dtype float64.
            y: Array de targets con shape (147,), dtype object.

    Raises:
        FileNotFoundError: Si DATA_GOLD_X o DATA_GOLD_Y no existen.
    """
    if not config.DATA_GOLD_X.exists():
        raise FileNotFoundError(
            f"Feature Store X no encontrado: {config.DATA_GOLD_X}"
        )
    if not config.DATA_GOLD_Y.exists():
        raise FileNotFoundError(
            f"Feature Store y no encontrado: {config.DATA_GOLD_Y}"
        )

    X: np.ndarray = pd.read_csv(config.DATA_GOLD_X).to_numpy(dtype=np.float64)
    y: np.ndarray = pd.read_csv(config.DATA_GOLD_Y)["species"].to_numpy()
    return X, y


def verify_kpi(metrics: TrainingMetrics, threshold: float = ACCURACY_TEST_THRESHOLD) -> None:
    """Verifica que accuracy_test supere el umbral BRD KPI-01.

    Args:
        metrics:   Diccionario TrainingMetrics retornado por train_and_evaluate().
        threshold: Umbral minimo de accuracy_test. Default: 0.95 (BRD KPI-01 GREEN).

    Raises:
        AssertionError: Si metrics['accuracy_test'] < threshold.
    """
    actual: float = metrics["accuracy_test"]
    assert actual >= threshold, (
        f"KPI-01 FAIL: accuracy_test={actual:.4f} < umbral={threshold:.2f}. "
        f"El modelo no cumple el umbral BRD §4.1 KPI-01."
    )


def main() -> None:
    """Punto de entrada principal del script de entrenamiento certificado."""
    print("=" * 60)
    print("Flores AI — Script de Entrenamiento Certificado (F3-T06)")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. Carga de datos Gold
    # ------------------------------------------------------------------
    print(f"\n[1/4] Cargando datos Gold desde:")
    print(f"       X: {config.DATA_GOLD_X}")
    print(f"       y: {config.DATA_GOLD_Y}")

    X, y = load_gold_data()
    print(f"       X shape: {X.shape} | dtype: {X.dtype}")
    print(f"       y shape: {y.shape} | clases: {list(np.unique(y))}")

    # ------------------------------------------------------------------
    # 2. Instanciar el clasificador ganador
    #    RandomForestClassifier — ganador por Simplicidad Primero
    #    (primer candidato que supera f1_macro_test >= 0.95, segun F3-T05)
    # ------------------------------------------------------------------
    print(f"\n[2/4] Instanciando clasificador ganador: RandomForestClassifier")
    print(f"       random_state={config.RANDOM_STATE} (canonico config.py)")

    classifier = RandomForestClassifier(random_state=config.RANDOM_STATE)

    # ------------------------------------------------------------------
    # 3. Entrenar y evaluar
    # ------------------------------------------------------------------
    print(f"\n[3/4] Ejecutando train_and_evaluate() ...")
    print(f"       test_size={config.TEST_SIZE} | cv_folds={config.CV_FOLDS} | random_state={config.RANDOM_STATE}")

    pipeline, metrics = train_and_evaluate(
        X=X,
        y=y,
        classifier=classifier,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        cv_folds=config.CV_FOLDS,
    )

    print("\n--- Metricas de Evaluacion ---")
    print(f"  accuracy_cv_mean : {metrics['accuracy_cv_mean']:.4f}")
    print(f"  accuracy_cv_std  : {metrics['accuracy_cv_std']:.4f}")
    print(f"  accuracy_test    : {metrics['accuracy_test']:.4f}")
    print(f"  f1_macro_test    : {metrics['f1_macro_test']:.4f}")
    print(f"  f1_per_class     : {metrics['f1_per_class']}")
    print(f"  n_train          : {metrics['n_train']}")
    print(f"  n_test           : {metrics['n_test']}")
    print(f"  random_state     : {metrics['random_state']}")

    # ------------------------------------------------------------------
    # 4. Verificacion de KPI-01 (BRD §4.1)
    # ------------------------------------------------------------------
    print(f"\n[4/4] Verificando KPI-01: accuracy_test >= {ACCURACY_TEST_THRESHOLD:.2f} ...")
    verify_kpi(metrics, ACCURACY_TEST_THRESHOLD)
    print(f"  [PASS] accuracy_test={metrics['accuracy_test']:.4f} >= {ACCURACY_TEST_THRESHOLD:.2f}")

    # ------------------------------------------------------------------
    # 5. Persistir el modelo
    # ------------------------------------------------------------------
    print(f"\n[5/5] Persistiendo pipeline en: {config.MODEL_PATH}")
    save_model(pipeline, config.MODEL_PATH)

    file_size_bytes: int = config.MODEL_PATH.stat().st_size
    file_size_kb: float = file_size_bytes / 1024
    file_size_mb: float = file_size_kb / 1024

    print(f"  Archivo creado: {config.MODEL_PATH}")
    print(f"  Tamano: {file_size_kb:.2f} KB ({file_size_mb:.4f} MB)")

    assert file_size_mb < 10.0, (
        f"El modelo supera el limite de 10 MB: {file_size_mb:.4f} MB"
    )
    print(f"  [PASS] Tamano < 10 MB")

    print("\n" + "=" * 60)
    print("Entrenamiento completado — models/iris_model.joblib CERTIFICADO")
    print("=" * 60)


if __name__ == "__main__":
    main()
