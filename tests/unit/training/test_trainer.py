# Trazable: SpecDD §9 | SAD §9.2 | backlog F3-T01
"""
Suite de tests RED para src/training/trainer.py — Pipeline de Entrenamiento.

Fase del ciclo TDD: RED (todos los tests deben fallar con
ModuleNotFoundError porque src/training/trainer.py no existe todavia).

Invariantes cubiertos:
    BP-01  build_pipeline() retorna instancia de Pipeline              (SpecDD §9)
    BP-02  Pipeline tiene exactamente 2 steps                          (SpecDD §9)
    BP-03  Primer step: ('scaler', StandardScaler())                   (SpecDD §9)
    BP-04  Segundo step: ('clf', clasificador inyectado)               (SpecDD §9)
    BP-05  Pipeline retornado es unfitted (NotFittedError al predecir) (SpecDD §9)
    TA-01  train_and_evaluate() retorna tuple(Pipeline, TrainingMetrics)(SpecDD §9)
    TA-02  TrainingMetrics contiene exactamente 8 claves del contrato  (SpecDD §9, §1.4)
    TA-03  metrics['n_train'] + metrics['n_test'] == len(X)            (SpecDD §9)
    TA-04  metrics['random_state'] == 42                               (SpecDD §9)
    TA-05  metrics['accuracy_test'] >= 0.90                            (SpecDD §9, BRD KPI-01)
    TA-06  Pipeline retornado esta fitted (predice sin error)          (SpecDD §9)
    TA-07  metrics['f1_per_class'] es dict con las 3 clases validas    (SpecDD §9)
    TA-08  Todas las metricas float estan en rango [0.0, 1.0]          (SpecDD §9)
    TA-09  ValueError si X esta vacio                                   (SpecDD §9 excepciones)
    TA-10  ValueError si len(X) != len(y)                              (SpecDD §9 excepciones)
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# RED: este import DEBE fallar — src/training/trainer.py no existe todavia
from src.training.trainer import TrainingMetrics, build_pipeline, train_and_evaluate
from src import config


# ---------------------------------------------------------------------------
# Constantes de referencia del contrato
# ---------------------------------------------------------------------------
REQUIRED_METRICS_KEYS: set[str] = {
    "accuracy_cv_mean",
    "accuracy_cv_std",
    "accuracy_test",
    "f1_macro_test",
    "f1_per_class",
    "n_train",
    "n_test",
    "random_state",
}
EXPECTED_CLASSES: set[str] = {"setosa", "versicolor", "virginica"}
MIN_ACCURACY_TEST: float = 0.90


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def gold_arrays() -> tuple[np.ndarray, np.ndarray]:
    """Carga los arrays Gold desde los archivos CSV del Feature Store.

    Patron de inyeccion de dependencias: calcula la ruta desde la
    ubicacion de este archivo, sin importar config para la ruta.

    Returns:
        tuple[np.ndarray, np.ndarray]: Arrays X (147, 4) e y (147,).
    """
    project_root: Path = Path(__file__).resolve().parent.parent.parent.parent
    X: np.ndarray = pd.read_csv(
        project_root / "data" / "gold" / "X_gold.csv"
    ).to_numpy(dtype=np.float64)
    y: np.ndarray = pd.read_csv(
        project_root / "data" / "gold" / "y_gold.csv"
    ).to_numpy().flatten()
    return X, y


@pytest.fixture
def classifier() -> RandomForestClassifier:
    """Clasificador base para pruebas de estructura del pipeline."""
    return RandomForestClassifier(n_estimators=10, random_state=config.RANDOM_STATE)


@pytest.fixture
def training_result(
    gold_arrays: tuple[np.ndarray, np.ndarray],
    classifier: RandomForestClassifier,
) -> tuple[Pipeline, TrainingMetrics]:
    """Ejecuta train_and_evaluate() con los datos Gold y retorna el resultado."""
    X, y = gold_arrays
    return train_and_evaluate(X, y, classifier)


# ---------------------------------------------------------------------------
# BP-01: build_pipeline retorna Pipeline
# ---------------------------------------------------------------------------
def test_build_pipeline_returns_pipeline(classifier: RandomForestClassifier) -> None:
    """BP-01: build_pipeline() debe retornar una instancia de sklearn.pipeline.Pipeline."""
    pipeline = build_pipeline(classifier)
    assert isinstance(pipeline, Pipeline), (
        f"build_pipeline() debe retornar Pipeline, retorno: {type(pipeline)}"
    )


# ---------------------------------------------------------------------------
# BP-02: Pipeline tiene exactamente 2 steps
# ---------------------------------------------------------------------------
def test_build_pipeline_has_two_steps(classifier: RandomForestClassifier) -> None:
    """BP-02: El Pipeline debe tener exactamente 2 steps: scaler y clf."""
    pipeline = build_pipeline(classifier)
    assert len(pipeline.steps) == 2, (
        f"Pipeline debe tener 2 steps, tiene: {len(pipeline.steps)}"
    )


# ---------------------------------------------------------------------------
# BP-03: Primer step es ('scaler', StandardScaler())
# ---------------------------------------------------------------------------
def test_build_pipeline_scaler_step(classifier: RandomForestClassifier) -> None:
    """BP-03: El primer step debe ser ('scaler', StandardScaler())."""
    pipeline = build_pipeline(classifier)
    step_name, step_obj = pipeline.steps[0]
    assert step_name == "scaler", (
        f"Nombre del primer step incorrecto. Esperado: 'scaler', encontrado: '{step_name}'"
    )
    assert isinstance(step_obj, StandardScaler), (
        f"Tipo del primer step incorrecto. Esperado: StandardScaler, encontrado: {type(step_obj)}"
    )


# ---------------------------------------------------------------------------
# BP-04: Segundo step es ('clf', clasificador inyectado)
# ---------------------------------------------------------------------------
def test_build_pipeline_clf_step(classifier: RandomForestClassifier) -> None:
    """BP-04: El segundo step debe ser ('clf', clasificador inyectado)."""
    pipeline = build_pipeline(classifier)
    step_name, step_obj = pipeline.steps[1]
    assert step_name == "clf", (
        f"Nombre del segundo step incorrecto. Esperado: 'clf', encontrado: '{step_name}'"
    )
    assert step_obj is classifier, (
        "El segundo step debe ser la misma instancia del clasificador inyectado"
    )


# ---------------------------------------------------------------------------
# BP-05: Pipeline retornado es unfitted
# ---------------------------------------------------------------------------
def test_build_pipeline_is_unfitted(classifier: RandomForestClassifier) -> None:
    """BP-05: El Pipeline retornado no debe estar fitted (unfitted)."""
    pipeline = build_pipeline(classifier)
    X_dummy: np.ndarray = np.zeros((1, 4))
    with pytest.raises(NotFittedError):
        pipeline.predict(X_dummy)


# ---------------------------------------------------------------------------
# TA-01: train_and_evaluate retorna tuple(Pipeline, TrainingMetrics)
# ---------------------------------------------------------------------------
def test_train_and_evaluate_return_type(
    training_result: tuple[Pipeline, TrainingMetrics],
) -> None:
    """TA-01: train_and_evaluate() debe retornar un tuple (Pipeline, dict)."""
    pipeline, metrics = training_result
    assert isinstance(pipeline, Pipeline), (
        f"Primer elemento debe ser Pipeline, es: {type(pipeline)}"
    )
    assert isinstance(metrics, dict), (
        f"Segundo elemento debe ser dict (TrainingMetrics), es: {type(metrics)}"
    )


# ---------------------------------------------------------------------------
# TA-02: TrainingMetrics contiene las 8 claves del contrato
# ---------------------------------------------------------------------------
def test_training_metrics_required_keys(
    training_result: tuple[Pipeline, TrainingMetrics],
) -> None:
    """TA-02: TrainingMetrics debe contener exactamente las 8 claves del SpecDD §1.4."""
    _, metrics = training_result
    missing_keys: set[str] = REQUIRED_METRICS_KEYS - set(metrics.keys())
    assert not missing_keys, (
        f"TrainingMetrics faltan claves requeridas: {missing_keys}"
    )


# ---------------------------------------------------------------------------
# TA-03: n_train + n_test == len(X)
# ---------------------------------------------------------------------------
def test_training_metrics_n_split_consistency(
    gold_arrays: tuple[np.ndarray, np.ndarray],
    training_result: tuple[Pipeline, TrainingMetrics],
) -> None:
    """TA-03: metrics['n_train'] + metrics['n_test'] debe ser igual a len(X)."""
    X, _ = gold_arrays
    _, metrics = training_result
    total: int = metrics["n_train"] + metrics["n_test"]
    assert total == len(X), (
        f"n_train ({metrics['n_train']}) + n_test ({metrics['n_test']}) = {total} "
        f"!= len(X) = {len(X)}"
    )


# ---------------------------------------------------------------------------
# TA-04: metrics['random_state'] == 42
# ---------------------------------------------------------------------------
def test_training_metrics_random_state(
    training_result: tuple[Pipeline, TrainingMetrics],
) -> None:
    """TA-04: metrics['random_state'] debe ser 42 (config.RANDOM_STATE)."""
    _, metrics = training_result
    assert metrics["random_state"] == 42, (
        f"random_state incorrecto. Esperado: 42, encontrado: {metrics['random_state']}"
    )


# ---------------------------------------------------------------------------
# TA-05: accuracy_test >= 0.90
# ---------------------------------------------------------------------------
def test_training_metrics_accuracy_threshold(
    training_result: tuple[Pipeline, TrainingMetrics],
) -> None:
    """TA-05: metrics['accuracy_test'] debe ser >= 0.90 (umbral minimo BRD KPI-01)."""
    _, metrics = training_result
    assert metrics["accuracy_test"] >= MIN_ACCURACY_TEST, (
        f"accuracy_test = {metrics['accuracy_test']:.4f} < umbral minimo {MIN_ACCURACY_TEST}"
    )


# ---------------------------------------------------------------------------
# TA-06: Pipeline retornado esta fitted
# ---------------------------------------------------------------------------
def test_train_and_evaluate_pipeline_is_fitted(
    training_result: tuple[Pipeline, TrainingMetrics],
) -> None:
    """TA-06: El Pipeline retornado debe estar fitted (puede predecir sin error)."""
    pipeline, _ = training_result
    X_sample: np.ndarray = np.array([[5.1, 3.5, 1.4, 0.2]])
    predictions = pipeline.predict(X_sample)
    assert len(predictions) == 1, (
        "Pipeline fitted debe retornar 1 prediccion para 1 muestra"
    )


# ---------------------------------------------------------------------------
# TA-07: f1_per_class es dict con las 3 clases validas
# ---------------------------------------------------------------------------
def test_training_metrics_f1_per_class_structure(
    training_result: tuple[Pipeline, TrainingMetrics],
) -> None:
    """TA-07: metrics['f1_per_class'] debe ser un dict con las 3 clases validas."""
    _, metrics = training_result
    f1_per_class = metrics["f1_per_class"]
    assert isinstance(f1_per_class, dict), (
        f"f1_per_class debe ser dict, es: {type(f1_per_class)}"
    )
    actual_classes: set[str] = set(f1_per_class.keys())
    assert actual_classes == EXPECTED_CLASSES, (
        f"Clases en f1_per_class incorrectas. "
        f"Esperado: {EXPECTED_CLASSES}, encontrado: {actual_classes}"
    )


# ---------------------------------------------------------------------------
# TA-08: Todas las metricas float estan en [0.0, 1.0]
# ---------------------------------------------------------------------------
def test_training_metrics_float_values_in_range(
    training_result: tuple[Pipeline, TrainingMetrics],
) -> None:
    """TA-08: accuracy_cv_mean, accuracy_cv_std, accuracy_test y f1_macro_test
    deben estar en el rango [0.0, 1.0].
    """
    _, metrics = training_result
    float_keys: list[str] = [
        "accuracy_cv_mean",
        "accuracy_cv_std",
        "accuracy_test",
        "f1_macro_test",
    ]
    for key in float_keys:
        value: float = metrics[key]
        assert 0.0 <= value <= 1.0, (
            f"metrics['{key}'] = {value} esta fuera del rango [0.0, 1.0]"
        )


# ---------------------------------------------------------------------------
# TA-09: ValueError si X esta vacio
# ---------------------------------------------------------------------------
def test_train_and_evaluate_empty_X_raises_value_error(
    classifier: RandomForestClassifier,
) -> None:
    """TA-09: train_and_evaluate() debe lanzar ValueError si X esta vacio."""
    X_empty: np.ndarray = np.empty((0, 4))
    y_empty: np.ndarray = np.array([], dtype=str)
    with pytest.raises(ValueError):
        train_and_evaluate(X_empty, y_empty, classifier)


# ---------------------------------------------------------------------------
# TA-10: ValueError si len(X) != len(y)
# ---------------------------------------------------------------------------
def test_train_and_evaluate_mismatched_dimensions_raises_value_error(
    classifier: RandomForestClassifier,
) -> None:
    """TA-10: train_and_evaluate() debe lanzar ValueError si len(X) != len(y)."""
    X: np.ndarray = np.random.rand(10, 4)
    y: np.ndarray = np.array(["setosa"] * 8)
    with pytest.raises(ValueError):
        train_and_evaluate(X, y, classifier)
