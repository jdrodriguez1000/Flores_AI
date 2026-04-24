# src/data/gold_builder.py
# Trazable: SpecDD §8 | contract.md §10.4 | SAD §5.1 | backlog F2-T08, F2-T09a
#
# Modulo de construccion de la Capa Gold — Flores AI (Iris).
# Separa el DataFrame Silver en arrays de features (X) y target (y)
# listos para entrenamiento, garantizando orden canonico de columnas
# y ausencia de target leakage.
#
# Regla de oro: No Leakage — TARGET_COLUMN nunca ingresa en X.

from pathlib import Path

import numpy as np
import pandas as pd

from src import config

# ---------------------------------------------------------------------------
# Constantes de modulo (SpecDD §8)
# ---------------------------------------------------------------------------
# Columna objetivo: declarada explicitamente para evitar leakage accidental.
# Es la unica variable de salida valida del dataset Silver.
TARGET_COLUMN: str = "species"


# ---------------------------------------------------------------------------
# Construccion de arrays Gold (SpecDD §8)
# ---------------------------------------------------------------------------
def build_gold(
    df_silver: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    """Separa el DataFrame Silver en arrays de features (X) y target (y).

    El orden de columnas en X sigue config.FEATURE_COLUMNS.

    Args:
        df_silver: DataFrame limpio (147, 5) proveniente de silver_cleaner.

    Returns:
        tuple[np.ndarray, np.ndarray]:
            X: Array de features con shape (147, 4), dtype float64.
               Orden de columnas: config.FEATURE_COLUMNS.
            y: Array de targets con shape (147,), dtype object (str).
               Valores: 'setosa', 'versicolor', 'virginica'.

    Raises:
        KeyError: Si alguna columna de config.FEATURE_COLUMNS no existe en df_silver.
        ValueError: Si df_silver esta vacio.
    """
    if df_silver.empty:
        raise ValueError(
            "df_silver esta vacio. Se requiere un DataFrame con datos validos."
        )

    # Contrato de entrada: todas las features canonicas deben estar presentes
    missing = [col for col in config.FEATURE_COLUMNS if col not in df_silver.columns]
    if missing:
        raise KeyError(
            f"Columnas requeridas ausentes en df_silver: {missing}. "
            f"Columnas presentes: {list(df_silver.columns)}"
        )

    # Seleccionar features en orden canonico — determinismo garantizado por
    # la lista ordenada config.FEATURE_COLUMNS (no depende del orden del CSV)
    X: np.ndarray = df_silver[config.FEATURE_COLUMNS].to_numpy(dtype=np.float64)

    # Extraer target usando la constante de modulo — previene leakage accidental
    y: np.ndarray = df_silver[TARGET_COLUMN].to_numpy()

    return X, y


# ---------------------------------------------------------------------------
# Persistencia Gold (SpecDD §8)
# ---------------------------------------------------------------------------
def save_gold(
    X: np.ndarray,
    y: np.ndarray,
    path_X: Path = config.DATA_GOLD_X,
    path_y: Path = config.DATA_GOLD_Y,
) -> None:
    """Persiste X e y en formato CSV en data/gold/.

    Args:
        X:      Array de features (147, 4).
        y:      Array de targets (147,).
        path_X: Ruta de destino para X. Default: config.DATA_GOLD_X.
        path_y: Ruta de destino para y. Default: config.DATA_GOLD_Y.

    Returns:
        None

    Raises:
        OSError: Si el directorio gold no puede ser creado.
    """
    # Un solo mkdir cubre ambos paths: por defecto ambos apuntan a data/gold/.
    # exist_ok=True hace la llamada idempotente para paths distintos.
    path_X.parent.mkdir(parents=True, exist_ok=True)
    path_y.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(X, columns=config.FEATURE_COLUMNS).to_csv(path_X, index=False)
    pd.DataFrame(y, columns=[TARGET_COLUMN]).to_csv(path_y, index=False)
