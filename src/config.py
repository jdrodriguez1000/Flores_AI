# src/config.py
# Trazable: SpecDD §2 | SAD §5 (ADR-004) | backlog F2-T00B
#
# Modulo de configuracion central del proyecto Flores AI - Iris.
# Unica fuente de verdad para rutas y constantes en todo el proyecto.
# Importable sin efectos secundarios (sin prints, sin I/O al importar).

from pathlib import Path

# ---------------------------------------------------------------------------
# Raiz del proyecto — calculada dinamicamente desde la ubicacion de este archivo
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Constantes de ruta — construidas dinamicamente via pathlib
# ---------------------------------------------------------------------------
DATA_BRONZE:  Path = PROJECT_ROOT / "data" / "bronze" / "Iris.csv"
DATA_SILVER:  Path = PROJECT_ROOT / "data" / "silver" / "iris_silver.csv"
DATA_GOLD_X:  Path = PROJECT_ROOT / "data" / "gold" / "X_gold.csv"
DATA_GOLD_Y:  Path = PROJECT_ROOT / "data" / "gold" / "y_gold.csv"
MODEL_PATH:   Path = PROJECT_ROOT / "models" / "iris_model.joblib"
FEEDBACK_LOG: Path = PROJECT_ROOT / "logs" / "feedback.log"

# ---------------------------------------------------------------------------
# Constantes de modelo
# ---------------------------------------------------------------------------
RANDOM_STATE:           int   = 42
TEST_SIZE:              float = 0.20
CV_FOLDS:               int   = 5
CONFIDENCE_THRESHOLD:   float = 0.60

# ---------------------------------------------------------------------------
# Rangos validos de features para validacion de entradas
# ---------------------------------------------------------------------------
FEATURE_RANGES: dict[str, tuple[float, float]] = {
    "sepal_length": (3.0, 9.0),
    "sepal_width":  (1.5, 5.5),
    "petal_length": (0.5, 8.0),
    "petal_width":  (0.0, 3.5),
}

# ---------------------------------------------------------------------------
# Orden canonico de columnas de features (SpecDD §2)
# ---------------------------------------------------------------------------
FEATURE_COLUMNS: list[str] = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]

# ---------------------------------------------------------------------------
# Nombres canonicos de clases objetivo
# ---------------------------------------------------------------------------
CLASS_NAMES: list[str] = ["setosa", "versicolor", "virginica"]
