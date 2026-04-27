# Trazable: SpecDD §10 | SAD §5.1, §9.2 | backlog F3-T04b

from pathlib import Path

import joblib
from sklearn.pipeline import Pipeline

from src import config


def save_model(
    pipeline: Pipeline,
    model_path: Path = config.MODEL_PATH,
) -> None:
    """Serializa el pipeline entrenado en disco en formato Joblib."""
    if not isinstance(pipeline, Pipeline):
        raise TypeError(
            f"pipeline debe ser instancia de sklearn.pipeline.Pipeline, "
            f"recibido: {type(pipeline)}"
        )

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)


def load_model(model_path: Path = config.MODEL_PATH) -> Pipeline:
    """Carga y valida el pipeline serializado desde el archivo .joblib."""
    if not model_path.exists():
        raise FileNotFoundError(
            f"No se encontro el modelo en: {model_path}"
        )

    loaded = joblib.load(model_path)

    if not isinstance(loaded, Pipeline):
        raise ValueError(
            f"El objeto cargado no es Pipeline, es: {type(loaded)}"
        )

    return loaded
