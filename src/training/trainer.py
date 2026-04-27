# Trazable: SpecDD §9 | SAD §5.1, §9.2 | backlog F3-T02b
from typing import Any, TypedDict

import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src import config


class TrainingMetrics(TypedDict):
    accuracy_cv_mean: float
    accuracy_cv_std: float
    accuracy_test: float
    f1_macro_test: float
    f1_per_class: dict[str, float]
    n_train: int
    n_test: int
    random_state: int


def build_pipeline(classifier: Any) -> Pipeline:
    """Construye Pipeline unfitted con StandardScaler + clasificador inyectado."""
    return Pipeline([("scaler", StandardScaler()), ("clf", classifier)])


def train_and_evaluate(
    X: np.ndarray,
    y: np.ndarray,
    classifier: Any,
    test_size: float = config.TEST_SIZE,
    random_state: int = config.RANDOM_STATE,
    cv_folds: int = config.CV_FOLDS,
) -> tuple[Pipeline, TrainingMetrics]:
    """Ejecuta el ciclo completo de entrenamiento y evaluacion.

    Args:
        X: Array de features (n, 4), dtype float64.
        y: Array de targets (n,), valores str.
        classifier: Instancia de clasificador scikit-learn.
        test_size: Fraccion del dataset para test.
        random_state: Semilla de aleatoriedad.
        cv_folds: Numero de folds para CV.

    Returns:
        tuple[Pipeline, TrainingMetrics]: Pipeline fitted y metricas.

    Raises:
        ValueError: Si X o y estan vacios, o si las dimensiones no coinciden.
    """
    if len(X) == 0 or len(y) == 0:
        raise ValueError("X e y no pueden estar vacios.")
    if len(X) != len(y):
        raise ValueError(f"len(X)={len(X)} != len(y)={len(y)}.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    pipeline = build_pipeline(classifier)

    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    classes = config.CLASS_NAMES
    f1_scores = f1_score(y_test, y_pred, labels=classes, average=None, zero_division=0)
    f1_per_class: dict[str, float] = dict(zip(classes, f1_scores.tolist()))

    metrics: TrainingMetrics = {
        "accuracy_cv_mean": float(cv_scores.mean()),
        "accuracy_cv_std": float(cv_scores.std()),
        "accuracy_test": float((y_pred == y_test).mean()),
        "f1_macro_test": float(f1_score(y_test, y_pred, average="macro", zero_division=0)),
        "f1_per_class": f1_per_class,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "random_state": random_state,
    }

    return pipeline, metrics
