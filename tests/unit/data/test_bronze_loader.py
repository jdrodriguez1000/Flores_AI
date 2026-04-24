# Trazable: SpecDD §6 | contract.md §2 | backlog F2-T01
"""
Suite de tests RED para src/data/bronze_loader.py — Capa Bronze.

Fase del ciclo TDD: RED (todos los tests deben fallar con
ModuleNotFoundError porque src/data/bronze_loader.py no existe todavia).

Invariantes cubiertos:
    BR-01  len(df) == 150                              (contract.md §10.2)
    BR-02  len(df.columns) == 6                        (contract.md §10.2)
    BR-03  df.isnull().sum().sum() == 0                (contract.md §10.2)
    BR-04  set(df['Species']) == tres clases           (contract.md §10.2)
    BR-05  Columnas exactas en orden                   (SpecDD §6 post-condiciones)
    BR-06  Tipos: Id int64, medidas float64, Species object  (contract.md §2.1)
    BR-07  50 registros exactos por clase              (contract.md §2.2)
    BR-08  FileNotFoundError si el CSV no existe       (SpecDD §6 excepciones)
"""
from pathlib import Path

import pytest

from src.data.bronze_loader import load_bronze  # RED: este import DEBE fallar


# ---------------------------------------------------------------------------
# Constantes de referencia del contrato
# ---------------------------------------------------------------------------
EXPECTED_ROWS: int = 150
EXPECTED_COLS: int = 6
EXPECTED_COLUMNS: list[str] = [
    "Id",
    "SepalLengthCm",
    "SepalWidthCm",
    "PetalLengthCm",
    "PetalWidthCm",
    "Species",
]
EXPECTED_SPECIES: set[str] = {
    "Iris-setosa",
    "Iris-versicolor",
    "Iris-virginica",
}
EXPECTED_RECORDS_PER_CLASS: int = 50


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
def bronze_df(bronze_csv_path: Path):
    """Carga el DataFrame Bronze inyectando el path del CSV real.

    Patron de inyeccion de dependencias (SpecDD §12.4): sobreescribe
    el default config.DATA_BRONZE para que el test no dependa de
    src.config, que aun no esta implementado en esta iteracion.

    Args:
        bronze_csv_path: Fixture con la ruta al CSV real.

    Returns:
        pd.DataFrame: DataFrame retornado por load_bronze().
    """
    return load_bronze(csv_path=bronze_csv_path)


# ---------------------------------------------------------------------------
# Tests de volumetria (BR-01, BR-02)
# ---------------------------------------------------------------------------
def test_bronze_row_count(bronze_df) -> None:
    """BR-01: El DataFrame debe tener exactamente 150 filas."""
    assert len(bronze_df) == EXPECTED_ROWS, (
        f"Bronze dataset debe tener {EXPECTED_ROWS} filas, "
        f"encontrado: {len(bronze_df)}"
    )


def test_bronze_column_count(bronze_df) -> None:
    """BR-02: El DataFrame debe tener exactamente 6 columnas."""
    assert len(bronze_df.columns) == EXPECTED_COLS, (
        f"Bronze dataset debe tener {EXPECTED_COLS} columnas, "
        f"encontrado: {len(bronze_df.columns)}"
    )


# ---------------------------------------------------------------------------
# Test de integridad de nulos (BR-03)
# ---------------------------------------------------------------------------
def test_bronze_zero_nulls(bronze_df) -> None:
    """BR-03: El DataFrame no debe contener ningun valor nulo."""
    null_count: int = int(bronze_df.isnull().sum().sum())
    assert null_count == 0, (
        f"Bronze dataset contiene {null_count} valores nulos"
    )


# ---------------------------------------------------------------------------
# Test de clases validas en Species (BR-04)
# ---------------------------------------------------------------------------
def test_bronze_valid_species_set(bronze_df) -> None:
    """BR-04: El conjunto de valores de Species debe ser exactamente
    {'Iris-setosa', 'Iris-versicolor', 'Iris-virginica'}.
    """
    actual_species: set[str] = set(bronze_df["Species"])
    assert actual_species == EXPECTED_SPECIES, (
        f"Clases invalidas en Species. "
        f"Esperado: {EXPECTED_SPECIES}, encontrado: {actual_species}"
    )


# ---------------------------------------------------------------------------
# Test de columnas exactas en orden (SpecDD §6 post-condiciones)
# ---------------------------------------------------------------------------
def test_bronze_column_names_and_order(bronze_df) -> None:
    """BR-05: Las columnas deben ser exactamente las especificadas
    y en el orden definido en SpecDD §6.
    """
    actual_columns: list[str] = list(bronze_df.columns)
    assert actual_columns == EXPECTED_COLUMNS, (
        f"Columnas incorrectas o en orden incorrecto. "
        f"Esperado: {EXPECTED_COLUMNS}, encontrado: {actual_columns}"
    )


# ---------------------------------------------------------------------------
# Tests de tipos de datos (contract.md §2.1)
# ---------------------------------------------------------------------------
def test_bronze_id_dtype(bronze_df) -> None:
    """BR-06a: La columna Id debe ser de tipo int64."""
    assert str(bronze_df["Id"].dtype) == "int64", (
        f"Tipo de Id incorrecto. "
        f"Esperado: int64, encontrado: {bronze_df['Id'].dtype}"
    )


def test_bronze_numeric_features_dtype(bronze_df) -> None:
    """BR-06b: Las cuatro columnas de medidas deben ser float64."""
    numeric_cols: list[str] = [
        "SepalLengthCm",
        "SepalWidthCm",
        "PetalLengthCm",
        "PetalWidthCm",
    ]
    for col in numeric_cols:
        assert str(bronze_df[col].dtype) == "float64", (
            f"Tipo de {col} incorrecto. "
            f"Esperado: float64, encontrado: {bronze_df[col].dtype}"
        )


def test_bronze_species_dtype(bronze_df) -> None:
    """BR-06c: La columna Species debe ser de tipo object (str)."""
    assert str(bronze_df["Species"].dtype) == "object", (
        f"Tipo de Species incorrecto. "
        f"Esperado: object, encontrado: {bronze_df['Species'].dtype}"
    )


# ---------------------------------------------------------------------------
# Test de balance de clases (contract.md §2.2)
# ---------------------------------------------------------------------------
def test_bronze_records_per_class(bronze_df) -> None:
    """BR-07: Cada clase de Species debe tener exactamente 50 registros."""
    class_counts = bronze_df["Species"].value_counts()
    for species in EXPECTED_SPECIES:
        count: int = int(class_counts.get(species, 0))
        assert count == EXPECTED_RECORDS_PER_CLASS, (
            f"Clase '{species}' tiene {count} registros. "
            f"Esperado: {EXPECTED_RECORDS_PER_CLASS}"
        )


# ---------------------------------------------------------------------------
# Test de manejo de errores (SpecDD §6 excepciones)
# ---------------------------------------------------------------------------
def test_bronze_raises_file_not_found_for_missing_csv(
    tmp_path: Path,
) -> None:
    """BR-08: load_bronze() debe lanzar FileNotFoundError si el CSV
    no existe en la ruta indicada.
    """
    nonexistent_path: Path = tmp_path / "does_not_exist.csv"
    with pytest.raises(FileNotFoundError):
        load_bronze(csv_path=nonexistent_path)
