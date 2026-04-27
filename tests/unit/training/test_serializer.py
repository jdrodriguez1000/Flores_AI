# Trazable: SpecDD §10 | SAD §9.2 | backlog F3-T03
"""
Suite de tests RED para src/training/serializer.py — Serializacion de Modelos.

Fase del ciclo TDD: RED (todos los tests deben fallar con
ModuleNotFoundError porque src/training/serializer.py no existe todavia).

Invariantes cubiertos:
    SM-01  save_model() crea el archivo .joblib en el path inyectado     (SpecDD §10 post-cond)
    SM-02  El objeto guardado es instancia de Pipeline al cargarlo       (SpecDD §10 post-cond)
    SM-03  save_model() lanza TypeError si el argumento no es Pipeline   (SpecDD §10 excepciones)
    LM-01  load_model() retorna instancia de sklearn.pipeline.Pipeline   (SpecDD §10 post-cond)
    LM-02  load_model() lanza FileNotFoundError si la ruta no existe     (SpecDD §10 excepciones)
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# RED: este import DEBE fallar — src/training/serializer.py no existe todavia
from src.training.serializer import load_model, save_model
from src.training.trainer import build_pipeline
from src import config


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def fitted_pipeline() -> Pipeline:
    """Construye y ajusta un Pipeline minimo con un subset de los datos Gold.

    Patron de inyeccion de dependencias: calcula la ruta desde la
    ubicacion de este archivo para no depender de config para el acceso a disco.

    Returns:
        Pipeline: Pipeline fitted (StandardScaler + RandomForestClassifier).
    """
    project_root: Path = Path(__file__).resolve().parent.parent.parent.parent
    X: np.ndarray = pd.read_csv(
        project_root / "data" / "gold" / "X_gold.csv"
    ).to_numpy(dtype=np.float64)[:30]
    y: np.ndarray = pd.read_csv(
        project_root / "data" / "gold" / "y_gold.csv"
    ).to_numpy().flatten()[:30]

    clf = RandomForestClassifier(n_estimators=5, random_state=config.RANDOM_STATE)
    pipeline = build_pipeline(clf)
    pipeline.fit(X, y)
    return pipeline


# ---------------------------------------------------------------------------
# SM-01: save_model() crea el archivo .joblib en tmp_path
# ---------------------------------------------------------------------------
def test_save_model_creates_file(
    fitted_pipeline: Pipeline,
    tmp_path: Path,
) -> None:
    """SM-01: save_model() debe crear el archivo .joblib en la ruta inyectada."""
    model_path: Path = tmp_path / "iris_model.joblib"

    save_model(fitted_pipeline, model_path)

    assert model_path.exists(), (
        f"save_model() no creo el archivo en: {model_path}"
    )


# ---------------------------------------------------------------------------
# SM-02: El objeto guardado es instancia de Pipeline al cargarlo
# ---------------------------------------------------------------------------
def test_save_model_persists_pipeline_instance(
    fitted_pipeline: Pipeline,
    tmp_path: Path,
) -> None:
    """SM-02: El objeto guardado debe poder cargarse y ser instancia de Pipeline."""
    model_path: Path = tmp_path / "iris_model.joblib"

    save_model(fitted_pipeline, model_path)
    loaded_object = joblib.load(model_path)

    assert isinstance(loaded_object, Pipeline), (
        f"El objeto cargado debe ser Pipeline, es: {type(loaded_object)}"
    )


# ---------------------------------------------------------------------------
# SM-03: save_model() lanza TypeError si el argumento no es Pipeline
# ---------------------------------------------------------------------------
def test_save_model_raises_type_error_on_non_pipeline(tmp_path: Path) -> None:
    """SM-03: save_model() debe lanzar TypeError si el argumento no es Pipeline."""
    model_path: Path = tmp_path / "iris_model.joblib"
    not_a_pipeline = {"key": "value"}

    with pytest.raises(TypeError):
        save_model(not_a_pipeline, model_path)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# LM-01: load_model() retorna instancia de Pipeline
# ---------------------------------------------------------------------------
def test_load_model_returns_pipeline(
    fitted_pipeline: Pipeline,
    tmp_path: Path,
) -> None:
    """LM-01: load_model() debe retornar una instancia de sklearn.pipeline.Pipeline."""
    model_path: Path = tmp_path / "iris_model.joblib"
    save_model(fitted_pipeline, model_path)

    loaded_pipeline = load_model(model_path)

    assert isinstance(loaded_pipeline, Pipeline), (
        f"load_model() debe retornar Pipeline, retorno: {type(loaded_pipeline)}"
    )


# ---------------------------------------------------------------------------
# LM-02: load_model() lanza FileNotFoundError si la ruta no existe
# ---------------------------------------------------------------------------
def test_load_model_raises_file_not_found_error(tmp_path: Path) -> None:
    """LM-02: load_model() debe lanzar FileNotFoundError si model_path no existe."""
    nonexistent_path: Path = tmp_path / "nonexistent_model.joblib"

    with pytest.raises(FileNotFoundError):
        load_model(nonexistent_path)
