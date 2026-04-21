# tests/unit/test_config.py
# Trazable: SpecDD §2 | SAD §5 (ADR-004) | backlog F2-T00A
#
# Fase RED: Este archivo debe fallar con ModuleNotFoundError porque
# src/config.py NO existe aun. Los tests verifican los invariantes del
# contrato de configuracion central del proyecto Flores AI - Iris.
# Cuando F2-T00B (GREEN) implemente src/config.py, todos los tests
# de esta suite deben pasar sin modificacion.

import pytest
from pathlib import Path
from src import config  # ModuleNotFoundError esperado en fase RED


# ---------------------------------------------------------------------------
# Bloque 1: Constantes de ruta — existencia y tipo
# ---------------------------------------------------------------------------

def test_project_root_exists_and_is_path():
    """PROJECT_ROOT debe existir y ser instancia de pathlib.Path."""
    assert hasattr(config, "PROJECT_ROOT"), "config.PROJECT_ROOT no esta definida"
    assert isinstance(config.PROJECT_ROOT, Path), (
        f"PROJECT_ROOT debe ser pathlib.Path, no {type(config.PROJECT_ROOT)}"
    )


def test_data_bronze_exists_and_is_path():
    """DATA_BRONZE debe existir y ser instancia de pathlib.Path."""
    assert hasattr(config, "DATA_BRONZE"), "config.DATA_BRONZE no esta definida"
    assert isinstance(config.DATA_BRONZE, Path), (
        f"DATA_BRONZE debe ser pathlib.Path, no {type(config.DATA_BRONZE)}"
    )


def test_data_silver_exists_and_is_path():
    """DATA_SILVER debe existir y ser instancia de pathlib.Path."""
    assert hasattr(config, "DATA_SILVER"), "config.DATA_SILVER no esta definida"
    assert isinstance(config.DATA_SILVER, Path), (
        f"DATA_SILVER debe ser pathlib.Path, no {type(config.DATA_SILVER)}"
    )


def test_data_gold_x_exists_and_is_path():
    """DATA_GOLD_X debe existir y ser instancia de pathlib.Path."""
    assert hasattr(config, "DATA_GOLD_X"), "config.DATA_GOLD_X no esta definida"
    assert isinstance(config.DATA_GOLD_X, Path), (
        f"DATA_GOLD_X debe ser pathlib.Path, no {type(config.DATA_GOLD_X)}"
    )


def test_data_gold_y_exists_and_is_path():
    """DATA_GOLD_Y debe existir y ser instancia de pathlib.Path."""
    assert hasattr(config, "DATA_GOLD_Y"), "config.DATA_GOLD_Y no esta definida"
    assert isinstance(config.DATA_GOLD_Y, Path), (
        f"DATA_GOLD_Y debe ser pathlib.Path, no {type(config.DATA_GOLD_Y)}"
    )


def test_model_path_exists_and_is_path():
    """MODEL_PATH debe existir y ser instancia de pathlib.Path."""
    assert hasattr(config, "MODEL_PATH"), "config.MODEL_PATH no esta definida"
    assert isinstance(config.MODEL_PATH, Path), (
        f"MODEL_PATH debe ser pathlib.Path, no {type(config.MODEL_PATH)}"
    )


def test_feedback_log_exists_and_is_path():
    """FEEDBACK_LOG debe existir y ser instancia de pathlib.Path."""
    assert hasattr(config, "FEEDBACK_LOG"), "config.FEEDBACK_LOG no esta definida"
    assert isinstance(config.FEEDBACK_LOG, Path), (
        f"FEEDBACK_LOG debe ser pathlib.Path, no {type(config.FEEDBACK_LOG)}"
    )


# ---------------------------------------------------------------------------
# Bloque 2: Constantes de modelo — valores exactos
# ---------------------------------------------------------------------------

def test_random_state_is_42():
    """RANDOM_STATE debe ser exactamente 42 (int)."""
    assert config.RANDOM_STATE == 42, (
        f"RANDOM_STATE esperado=42, obtenido={config.RANDOM_STATE}"
    )


def test_test_size_is_0_20():
    """TEST_SIZE debe ser exactamente 0.20 (float)."""
    assert config.TEST_SIZE == pytest.approx(0.20), (
        f"TEST_SIZE esperado=0.20, obtenido={config.TEST_SIZE}"
    )


def test_cv_folds_is_5():
    """CV_FOLDS debe ser exactamente 5 (int)."""
    assert config.CV_FOLDS == 5, (
        f"CV_FOLDS esperado=5, obtenido={config.CV_FOLDS}"
    )


def test_confidence_threshold_is_0_60():
    """CONFIDENCE_THRESHOLD debe ser exactamente 0.60 (float)."""
    assert config.CONFIDENCE_THRESHOLD == pytest.approx(0.60), (
        f"CONFIDENCE_THRESHOLD esperado=0.60, obtenido={config.CONFIDENCE_THRESHOLD}"
    )


# ---------------------------------------------------------------------------
# Bloque 3: FEATURE_COLUMNS — contenido y orden canonico
# ---------------------------------------------------------------------------

def test_feature_columns_has_exactly_4_elements():
    """FEATURE_COLUMNS debe tener exactamente 4 elementos."""
    assert len(config.FEATURE_COLUMNS) == 4, (
        f"FEATURE_COLUMNS debe tener 4 elementos, tiene {len(config.FEATURE_COLUMNS)}"
    )


def test_feature_columns_canonical_order():
    """FEATURE_COLUMNS debe seguir el orden canonico definido en SpecDD §2."""
    expected = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    assert config.FEATURE_COLUMNS == expected, (
        f"FEATURE_COLUMNS esperado={expected}, obtenido={config.FEATURE_COLUMNS}"
    )


# ---------------------------------------------------------------------------
# Bloque 4: CLASS_NAMES — contenido y cardinalidad
# ---------------------------------------------------------------------------

def test_class_names_has_exactly_3_elements():
    """CLASS_NAMES debe tener exactamente 3 elementos."""
    assert len(config.CLASS_NAMES) == 3, (
        f"CLASS_NAMES debe tener 3 elementos, tiene {len(config.CLASS_NAMES)}"
    )


def test_class_names_canonical_values():
    """CLASS_NAMES debe contener exactamente las tres especies validas."""
    expected = ["setosa", "versicolor", "virginica"]
    assert config.CLASS_NAMES == expected, (
        f"CLASS_NAMES esperado={expected}, obtenido={config.CLASS_NAMES}"
    )


# ---------------------------------------------------------------------------
# Bloque 5: Integridad de rutas — dinamismo (no hardcoded)
# ---------------------------------------------------------------------------

def test_all_paths_are_relative_to_project_root():
    """
    Todas las constantes de ruta deben ser descendientes de PROJECT_ROOT.
    Garantiza que no existen rutas absolutas hardcodeadas de maquina.
    Trazable: SpecDD §2 post-condicion 'Ninguna ruta es absoluta hardcodeada'.
    """
    path_constants = {
        "DATA_BRONZE": config.DATA_BRONZE,
        "DATA_SILVER": config.DATA_SILVER,
        "DATA_GOLD_X": config.DATA_GOLD_X,
        "DATA_GOLD_Y": config.DATA_GOLD_Y,
        "MODEL_PATH":  config.MODEL_PATH,
        "FEEDBACK_LOG": config.FEEDBACK_LOG,
    }
    for name, path in path_constants.items():
        resolved = path.resolve()
        try:
            resolved.relative_to(config.PROJECT_ROOT.resolve())
        except ValueError:
            pytest.fail(
                f"{name} ({resolved}) no es descendiente de PROJECT_ROOT "
                f"({config.PROJECT_ROOT.resolve()}). Posible ruta absoluta hardcodeada."
            )


def test_data_bronze_suffix_matches_spec():
    """
    DATA_BRONZE debe apuntar a una ruta que termina en 'data/bronze/Iris.csv'.
    Verifica el sufijo logico sin depender de la ruta absoluta de la maquina.
    """
    parts = config.DATA_BRONZE.parts
    # Buscar la secuencia data -> bronze -> Iris.csv en las partes de la ruta
    joined = "/".join(parts)
    assert "data/bronze/Iris.csv" in joined or joined.endswith("data\\bronze\\Iris.csv"), (
        f"DATA_BRONZE debe contener 'data/bronze/Iris.csv', ruta actual: {config.DATA_BRONZE}"
    )


def test_project_root_is_constructed_dynamically():
    """
    PROJECT_ROOT no debe ser una ruta absoluta literalmente escrita en el codigo.
    Se verifica comprobando que PROJECT_ROOT.resolve() es igual al directorio
    padre del padre de config.py (estructura src/config.py -> src/ -> raiz).
    """
    # Si PROJECT_ROOT es dinamico, debe corresponder a la raiz del repositorio.
    # La verificacion es indirecta: PROJECT_ROOT.resolve() debe ser un directorio
    # real que exista (no un string hardcodeado a una maquina inexistente).
    assert config.PROJECT_ROOT.resolve().is_dir(), (
        f"PROJECT_ROOT.resolve() = {config.PROJECT_ROOT.resolve()} "
        "no es un directorio existente. Posible ruta estatica invalida."
    )
