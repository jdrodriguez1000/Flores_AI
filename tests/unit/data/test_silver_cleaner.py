# Trazable: SpecDD §7 | contract.md §3 | backlog F2-T04
"""
Suite de tests RED para src/data/silver_cleaner.py — Capa Silver.

Fase del ciclo TDD: RED (todos los tests deben fallar con
ModuleNotFoundError porque src/data/silver_cleaner.py no existe todavia).

Invariantes cubiertos:
    SR-01  len(df) == 147                              (contract.md §10.3)
    SR-02  'Id' not in df.columns                      (contract.md §10.3)
    SR-03  list(df.columns) == columnas snake_case     (contract.md §10.3)
    SR-04  set(df['species']) sin prefijo 'Iris-'      (contract.md §10.3)
    SR-05  duplicados == 0 y nulos == 0                (contract.md §10.3)
    SR-06  Tipos: medidas float64, species object      (contract.md §3.2)
    SR-07  Ningun valor en species comienza con 'Iris-'(contract.md §3.2)
    SR-08  KeyError si 'Id' no existe en df_bronze     (SpecDD §7 excepciones)
    SR-09  ValueError si df_bronze esta vacio          (SpecDD §7 excepciones)
    SR-10  save_silver() crea el CSV en el path dado   (SpecDD §7)
"""
from pathlib import Path

import pandas as pd
import pytest

from src.data.bronze_loader import load_bronze
# RED: este import DEBE fallar — src/data/silver_cleaner.py no existe todavia
from src.data.silver_cleaner import clean_bronze, save_silver


# ---------------------------------------------------------------------------
# Constantes de referencia del contrato
# ---------------------------------------------------------------------------
EXPECTED_ROWS: int = 147
EXPECTED_COLS: int = 5
EXPECTED_COLUMNS: list[str] = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "species",
]
EXPECTED_SPECIES: set[str] = {"setosa", "versicolor", "virginica"}
NUMERIC_COLS: list[str] = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def bronze_csv_path() -> Path:
    """Retorna la ruta absoluta al CSV real de la capa Bronze.

    La ruta se calcula desde la ubicacion de este archivo
    (tests/unit/data/) subiendo 3 niveles hasta la raiz del proyecto
    y luego bajando a data/bronze/Iris.csv.

    Returns:
        Path: Ruta absoluta al archivo Iris.csv.
    """
    return (
        Path(__file__).resolve().parent.parent.parent.parent
        / "data"
        / "bronze"
        / "Iris.csv"
    )


@pytest.fixture
def silver_df(bronze_csv_path: Path) -> pd.DataFrame:
    """Carga el DataFrame Bronze y aplica clean_bronze() para obtener Silver.

    Patron de inyeccion de dependencias (D-028): carga el CSV Bronze
    inyectando su path, luego pasa el DataFrame resultante a clean_bronze()
    sin argumento de ruta. No importa src.config directamente.

    Args:
        bronze_csv_path: Fixture con la ruta al CSV Bronze real.

    Returns:
        pd.DataFrame: DataFrame Silver retornado por clean_bronze().
    """
    df_bronze: pd.DataFrame = load_bronze(csv_path=bronze_csv_path)
    return clean_bronze(df_bronze)


# ---------------------------------------------------------------------------
# Tests de volumetria (SR-01)
# ---------------------------------------------------------------------------
def test_silver_row_count(silver_df: pd.DataFrame) -> None:
    """SR-01: El DataFrame Silver debe tener exactamente 147 filas."""
    assert len(silver_df) == EXPECTED_ROWS, (
        f"Silver dataset debe tener {EXPECTED_ROWS} filas, "
        f"encontrado: {len(silver_df)}"
    )


# ---------------------------------------------------------------------------
# Test de ausencia de columna 'Id' (SR-02)
# ---------------------------------------------------------------------------
def test_silver_id_column_removed(silver_df: pd.DataFrame) -> None:
    """SR-02: La columna 'Id' no debe existir en el DataFrame Silver."""
    assert "Id" not in silver_df.columns, (
        "La columna 'Id' todavia esta presente en el DataFrame Silver"
    )


# ---------------------------------------------------------------------------
# Test de columnas exactas en orden y snake_case (SR-03)
# ---------------------------------------------------------------------------
def test_silver_column_names_and_order(silver_df: pd.DataFrame) -> None:
    """SR-03: Las columnas deben ser exactamente las especificadas
    en snake_case y en el orden definido en SpecDD §7.
    """
    actual_columns: list[str] = list(silver_df.columns)
    assert actual_columns == EXPECTED_COLUMNS, (
        f"Columnas incorrectas o en orden incorrecto. "
        f"Esperado: {EXPECTED_COLUMNS}, encontrado: {actual_columns}"
    )


# ---------------------------------------------------------------------------
# Test de clases validas en species sin prefijo 'Iris-' (SR-04)
# ---------------------------------------------------------------------------
def test_silver_valid_species_set(silver_df: pd.DataFrame) -> None:
    """SR-04: El conjunto de valores de species debe ser exactamente
    {'setosa', 'versicolor', 'virginica'}, sin prefijo 'Iris-'.
    """
    actual_species: set[str] = set(silver_df["species"])
    assert actual_species == EXPECTED_SPECIES, (
        f"Clases invalidas en species. "
        f"Esperado: {EXPECTED_SPECIES}, encontrado: {actual_species}"
    )


# ---------------------------------------------------------------------------
# Tests de integridad: duplicados y nulos (SR-05)
# ---------------------------------------------------------------------------
def test_silver_zero_duplicates(silver_df: pd.DataFrame) -> None:
    """SR-05a: El DataFrame Silver no debe contener filas duplicadas."""
    dup_count: int = int(silver_df.duplicated().sum())
    assert dup_count == 0, (
        f"Silver dataset contiene {dup_count} filas duplicadas"
    )


def test_silver_zero_nulls(silver_df: pd.DataFrame) -> None:
    """SR-05b: El DataFrame Silver no debe contener ningun valor nulo."""
    null_count: int = int(silver_df.isnull().sum().sum())
    assert null_count == 0, (
        f"Silver dataset contiene {null_count} valores nulos"
    )


# ---------------------------------------------------------------------------
# Tests de tipos de datos (SR-06)
# ---------------------------------------------------------------------------
def test_silver_numeric_features_dtype(silver_df: pd.DataFrame) -> None:
    """SR-06a: Las cuatro columnas de medidas deben ser float64."""
    for col in NUMERIC_COLS:
        assert str(silver_df[col].dtype) == "float64", (
            f"Tipo de {col} incorrecto. "
            f"Esperado: float64, encontrado: {silver_df[col].dtype}"
        )


def test_silver_species_dtype(silver_df: pd.DataFrame) -> None:
    """SR-06b: La columna species debe ser de tipo object (str)."""
    assert str(silver_df["species"].dtype) == "object", (
        f"Tipo de species incorrecto. "
        f"Esperado: object, encontrado: {silver_df['species'].dtype}"
    )


# ---------------------------------------------------------------------------
# Test de ausencia del prefijo 'Iris-' en species (SR-07)
# ---------------------------------------------------------------------------
def test_silver_no_iris_prefix_in_species(silver_df: pd.DataFrame) -> None:
    """SR-07: Ningun valor en la columna species debe comenzar con 'Iris-'."""
    values_with_prefix: list[str] = [
        v for v in silver_df["species"] if str(v).startswith("Iris-")
    ]
    assert len(values_with_prefix) == 0, (
        f"Valores con prefijo 'Iris-' encontrados: {values_with_prefix}"
    )


# ---------------------------------------------------------------------------
# Tests de manejo de errores (SR-08, SR-09)
# ---------------------------------------------------------------------------
def test_clean_bronze_raises_key_error_without_id_column() -> None:
    """SR-08: clean_bronze() debe lanzar KeyError si el DataFrame
    de entrada no contiene la columna 'Id'.
    """
    df_without_id: pd.DataFrame = pd.DataFrame(
        {
            "SepalLengthCm": [5.1],
            "SepalWidthCm": [3.5],
            "PetalLengthCm": [1.4],
            "PetalWidthCm": [0.2],
            "Species": ["Iris-setosa"],
        }
    )
    with pytest.raises(KeyError):
        clean_bronze(df_without_id)


def test_clean_bronze_raises_value_error_for_empty_dataframe() -> None:
    """SR-09: clean_bronze() debe lanzar ValueError si el DataFrame
    de entrada esta vacio.
    """
    df_empty: pd.DataFrame = pd.DataFrame()
    with pytest.raises(ValueError):
        clean_bronze(df_empty)


# ---------------------------------------------------------------------------
# Test de persistencia save_silver() (SR-10)
# ---------------------------------------------------------------------------
def test_save_silver_creates_csv_at_given_path(
    silver_df: pd.DataFrame,
    tmp_path: Path,
) -> None:
    """SR-10: save_silver() debe crear el archivo CSV en el path inyectado."""
    output_path: Path = tmp_path / "silver_test.csv"
    save_silver(silver_df, path=output_path)
    assert output_path.exists(), (
        f"save_silver() no creo el archivo en: {output_path}"
    )
