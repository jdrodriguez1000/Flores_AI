# src/data/silver_cleaner.py
# Trazable: SpecDD §7 | contract.md §3 | SAD §5.1
#
# Modulo de transformacion de la Capa Silver — Flores AI (Iris).
# Aplica las transformaciones M-01 a M-04 sobre el DataFrame Bronze
# para producir un dataset limpio, sin duplicados y con esquema
# canonico listo para la Capa Gold.
#
# Regla de oro: Clean, don't Fake.
# Ningun valor es inventado; solo se elimina ruido tecnico documentado.

from pathlib import Path

import pandas as pd

from src import config

# ---------------------------------------------------------------------------
# Constantes de modulo (SpecDD §7)
# ---------------------------------------------------------------------------
RENAME_MAP: dict[str, str] = {
    "SepalLengthCm": "sepal_length",
    "SepalWidthCm":  "sepal_width",
    "PetalLengthCm": "petal_length",
    "PetalWidthCm":  "petal_width",
    "Species":       "species",
}

LABEL_MAP: dict[str, str] = {
    "Iris-setosa":     "setosa",
    "Iris-versicolor": "versicolor",
    "Iris-virginica":  "virginica",
}


# ---------------------------------------------------------------------------
# Pipeline de transformacion Silver
# ---------------------------------------------------------------------------
def clean_bronze(df_bronze: pd.DataFrame) -> pd.DataFrame:
    """Transforma el DataFrame Bronze en Silver aplicando M-01 a M-04.

    Transformaciones aplicadas (en orden):
        M-01: Eliminar columna 'Id' (data leakage).
        M-02: Eliminar duplicados (3 registros), conservando primera ocurrencia.
        M-03: Renombrar columnas PascalCase+Cm -> snake_case.
        M-04: Normalizar etiquetas: 'Iris-setosa' -> 'setosa', etc.

    Args:
        df_bronze: DataFrame crudo proveniente de bronze_loader.load_bronze().
                   Se espera shape (150, 6) con los tipos documentados.

    Returns:
        pd.DataFrame: DataFrame limpio con 147 filas y 5 columnas:
                      ['sepal_length', 'sepal_width', 'petal_length',
                       'petal_width', 'species']

    Raises:
        KeyError: Si 'Id' o alguna columna requerida no existe en df_bronze.
        ValueError: Si df_bronze esta vacio.
    """
    # SR-09: Guardia contra DataFrame vacio
    if df_bronze.empty:
        raise ValueError(
            "df_bronze esta vacio. Se requiere un DataFrame con datos validos."
        )

    # SR-08: Guardia contra ausencia de columna 'Id'
    if "Id" not in df_bronze.columns:
        raise KeyError(
            "'Id' no existe en df_bronze. "
            "El DataFrame no proviene de la Capa Bronze."
        )

    # M-01: Eliminar columna 'Id' — evita data leakage en entrenamiento
    df = df_bronze.drop(columns=["Id"])

    # M-02: Eliminar duplicados exactos sobre features + species
    # contract.md §10.3: 3 registros duplicados eliminados -> 147 filas
    # Outliers en SepalWidthCm (Ids 16, 33, 34, 61) son biolog. plausibles
    # y NO se tocan.
    df = df.drop_duplicates(keep="first")

    # M-03: Renombrar columnas PascalCase+Cm a snake_case (SpecDD §7)
    df = df.rename(columns=RENAME_MAP)

    # M-04: Normalizar etiquetas de species — quitar prefijo 'Iris-'
    df["species"] = df["species"].map(LABEL_MAP)

    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Persistencia Silver
# ---------------------------------------------------------------------------
def save_silver(
    df_silver: pd.DataFrame,
    path: Path = config.DATA_SILVER,
) -> None:
    """Persiste el DataFrame Silver en formato CSV.

    Args:
        df_silver: DataFrame limpio (147, 5).
        path:      Ruta de destino. Default: config.DATA_SILVER.

    Raises:
        OSError: Si el directorio de destino no existe y no puede crearse.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df_silver.to_csv(path, index=False)
