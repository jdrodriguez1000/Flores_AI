# Trazable: SpecDD §8 | contract.md §10.4 | backlog F2-T07
"""
Suite de tests RED para src/data/gold_builder.py — Capa Gold.

Fase del ciclo TDD: RED (todos los tests deben fallar con
ModuleNotFoundError porque src/data/gold_builder.py no existe todavia).

Invariantes cubiertos:
    GR-01  X.shape == (147, 4)                            (contract.md §10.4)
    GR-02  y.shape == (147,)                              (contract.md §10.4)
    GR-03  X.dtype == np.float64                          (contract.md §10.4)
    GR-04  np.isnan(X).sum() == 0                         (contract.md §10.4)
    GR-05  np.isinf(X).sum() == 0                         (contract.md §10.4)
    GR-06  set(np.unique(y)) == clases validas            (contract.md §10.4)
    GR-07  Orden de columnas en X segun config.FEATURE_COLUMNS (SpecDD §8)
    GR-08  len(X) == len(y)                               (contract.md §10.4)
    GR-09  Columna 'species' ausente en X                 (SpecDD §8)
    GR-10  KeyError si falta una columna de features      (SpecDD §8 excepciones)
    GR-11  ValueError si df_silver esta vacio             (SpecDD §8 excepciones)
    GR-12  save_gold() crea los archivos CSV en los paths dados (SpecDD §8)
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# RED: este import DEBE fallar — src/data/gold_builder.py no existe todavia
from src.data.gold_builder import build_gold, save_gold
from src import config


# ---------------------------------------------------------------------------
# Constantes de referencia del contrato
# ---------------------------------------------------------------------------
EXPECTED_X_SHAPE: tuple[int, int] = (147, 4)
EXPECTED_Y_SHAPE: tuple[int] = (147,)
EXPECTED_X_DTYPE: np.dtype = np.float64
EXPECTED_FEATURE_COLUMNS: list[str] = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]
EXPECTED_CLASSES: set[str] = {"setosa", "versicolor", "virginica"}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def silver_csv_path() -> Path:
    """Ruta al CSV Silver calculada desde la ubicacion del archivo de tests.

    La ruta se calcula desde la ubicacion de este archivo
    (tests/unit/data/) subiendo 4 niveles hasta la raiz del proyecto
    y luego bajando a data/silver/iris_silver.csv.

    Returns:
        Path: Ruta absoluta al archivo iris_silver.csv.
    """
    return (
        Path(__file__).resolve().parent.parent.parent.parent
        / "data"
        / "silver"
        / "iris_silver.csv"
    )


@pytest.fixture
def gold_arrays(silver_csv_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Carga el CSV Silver y llama build_gold() para obtener X e y.

    Patron de inyeccion de dependencias: carga el CSV Silver inyectando
    su path y pasa el DataFrame resultante a build_gold(). No importa
    src.config directamente para la ruta del archivo.

    Args:
        silver_csv_path: Fixture con la ruta al CSV Silver real.

    Returns:
        tuple[np.ndarray, np.ndarray]: Arrays X e y retornados por build_gold().
    """
    df_silver: pd.DataFrame = pd.read_csv(silver_csv_path)
    return build_gold(df_silver)


# ---------------------------------------------------------------------------
# GR-01: Shape de X
# ---------------------------------------------------------------------------
def test_gold_X_shape(gold_arrays: tuple[np.ndarray, np.ndarray]) -> None:
    """GR-01: X debe tener shape exacto (147, 4)."""
    X, _ = gold_arrays
    assert X.shape == EXPECTED_X_SHAPE, (
        f"Shape de X incorrecto. "
        f"Esperado: {EXPECTED_X_SHAPE}, encontrado: {X.shape}"
    )


# ---------------------------------------------------------------------------
# GR-02: Shape de y
# ---------------------------------------------------------------------------
def test_gold_y_shape(gold_arrays: tuple[np.ndarray, np.ndarray]) -> None:
    """GR-02: y debe tener shape exacto (147,)."""
    _, y = gold_arrays
    assert y.shape == EXPECTED_Y_SHAPE, (
        f"Shape de y incorrecto. "
        f"Esperado: {EXPECTED_Y_SHAPE}, encontrado: {y.shape}"
    )


# ---------------------------------------------------------------------------
# GR-03: Dtype de X
# ---------------------------------------------------------------------------
def test_gold_X_dtype(gold_arrays: tuple[np.ndarray, np.ndarray]) -> None:
    """GR-03: X debe tener dtype float64."""
    X, _ = gold_arrays
    assert X.dtype == EXPECTED_X_DTYPE, (
        f"Dtype de X incorrecto. "
        f"Esperado: {EXPECTED_X_DTYPE}, encontrado: {X.dtype}"
    )


# ---------------------------------------------------------------------------
# GR-04: Cero NaN en X
# ---------------------------------------------------------------------------
def test_gold_X_zero_nan(gold_arrays: tuple[np.ndarray, np.ndarray]) -> None:
    """GR-04: X no debe contener ningun valor NaN."""
    X, _ = gold_arrays
    nan_count: int = int(np.isnan(X).sum())
    assert nan_count == 0, (
        f"X contiene {nan_count} valores NaN"
    )


# ---------------------------------------------------------------------------
# GR-05: Cero Inf en X
# ---------------------------------------------------------------------------
def test_gold_X_zero_inf(gold_arrays: tuple[np.ndarray, np.ndarray]) -> None:
    """GR-05: X no debe contener ningun valor infinito."""
    X, _ = gold_arrays
    inf_count: int = int(np.isinf(X).sum())
    assert inf_count == 0, (
        f"X contiene {inf_count} valores infinitos"
    )


# ---------------------------------------------------------------------------
# GR-06: Clases validas en y
# ---------------------------------------------------------------------------
def test_gold_y_valid_classes(gold_arrays: tuple[np.ndarray, np.ndarray]) -> None:
    """GR-06: El conjunto de clases unicas en y debe ser exactamente
    {'setosa', 'versicolor', 'virginica'}.
    """
    _, y = gold_arrays
    actual_classes: set[str] = set(np.unique(y))
    assert actual_classes == EXPECTED_CLASSES, (
        f"Clases invalidas en y. "
        f"Esperado: {EXPECTED_CLASSES}, encontrado: {actual_classes}"
    )


# ---------------------------------------------------------------------------
# GR-07: Orden de columnas en X segun config.FEATURE_COLUMNS
# ---------------------------------------------------------------------------
def test_gold_X_column_order(
    silver_csv_path: Path,
    gold_arrays: tuple[np.ndarray, np.ndarray],
) -> None:
    """GR-07: El orden de columnas en X debe coincidir exactamente con
    config.FEATURE_COLUMNS, verificado reconstruyendo el DataFrame Silver.
    """
    X, _ = gold_arrays
    df_silver: pd.DataFrame = pd.read_csv(silver_csv_path)
    expected_X_values: np.ndarray = (
        df_silver[config.FEATURE_COLUMNS].to_numpy(dtype=np.float64)
    )
    assert np.array_equal(X, expected_X_values), (
        "El orden de columnas en X no coincide con config.FEATURE_COLUMNS. "
        f"Orden esperado: {config.FEATURE_COLUMNS}"
    )


# ---------------------------------------------------------------------------
# GR-08: Consistencia entre X e y
# ---------------------------------------------------------------------------
def test_gold_X_y_length_consistency(
    gold_arrays: tuple[np.ndarray, np.ndarray],
) -> None:
    """GR-08: len(X) debe ser igual a len(y) para garantizar la
    consistencia entre features y targets.
    """
    X, y = gold_arrays
    assert len(X) == len(y), (
        f"Inconsistencia de longitud entre X ({len(X)}) e y ({len(y)})"
    )


# ---------------------------------------------------------------------------
# GR-09: Ausencia de target leakage en X
# ---------------------------------------------------------------------------
def test_gold_X_no_species_column(
    silver_csv_path: Path,
) -> None:
    """GR-09: La columna 'species' no debe estar presente en X
    (ausencia de target leakage).
    """
    df_silver: pd.DataFrame = pd.read_csv(silver_csv_path)
    X, _ = build_gold(df_silver)
    # X es un ndarray; verificamos que sus columnas sean exactamente 4
    # (sin la columna species) comparando el shape con FEATURE_COLUMNS
    assert X.shape[1] == len(EXPECTED_FEATURE_COLUMNS), (
        f"X tiene {X.shape[1]} columnas cuando debe tener "
        f"{len(EXPECTED_FEATURE_COLUMNS)}. Posible target leakage."
    )


# ---------------------------------------------------------------------------
# GR-10: KeyError si falta una columna de features
# ---------------------------------------------------------------------------
def test_build_gold_raises_key_error_for_missing_feature_column() -> None:
    """GR-10: build_gold() debe lanzar KeyError si falta alguna columna
    definida en config.FEATURE_COLUMNS en el DataFrame de entrada.
    """
    df_missing_col: pd.DataFrame = pd.DataFrame(
        {
            "sepal_length": [5.1, 4.9],
            "sepal_width": [3.5, 3.0],
            # petal_length ausente intencionalmente
            "petal_width": [0.2, 0.2],
            "species": ["setosa", "setosa"],
        }
    )
    with pytest.raises(KeyError):
        build_gold(df_missing_col)


# ---------------------------------------------------------------------------
# GR-11: ValueError si df_silver esta vacio
# ---------------------------------------------------------------------------
def test_build_gold_raises_value_error_for_empty_dataframe() -> None:
    """GR-11: build_gold() debe lanzar ValueError si el DataFrame
    de entrada esta vacio.
    """
    df_empty: pd.DataFrame = pd.DataFrame()
    with pytest.raises(ValueError):
        build_gold(df_empty)


# ---------------------------------------------------------------------------
# GR-12: save_gold() crea los archivos CSV en los paths inyectados
# ---------------------------------------------------------------------------
def test_save_gold_creates_csv_files_at_given_paths(
    gold_arrays: tuple[np.ndarray, np.ndarray],
    tmp_path: Path,
) -> None:
    """GR-12: save_gold() debe crear los archivos X_gold.csv e y_gold.csv
    en los paths inyectados via parametros path_X y path_y.
    """
    X, y = gold_arrays
    output_X: Path = tmp_path / "X_gold_test.csv"
    output_y: Path = tmp_path / "y_gold_test.csv"
    save_gold(X, y, path_X=output_X, path_y=output_y)
    assert output_X.exists(), (
        f"save_gold() no creo el archivo X en: {output_X}"
    )
    assert output_y.exists(), (
        f"save_gold() no creo el archivo y en: {output_y}"
    )
