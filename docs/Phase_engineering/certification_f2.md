# Certificacion F2: Linaje Bronze -> Silver -> Gold

> **Iteracion:** 2.4 | **Responsable:** @ai-data-qa-engineer | **Fecha:** 2026-04-24
> **Trazabilidad:** SpecDD §6–8 | SAD §5 | contract.md §10.2–10.4 | backlog F2-T10

---

## 1. Resumen Ejecutivo

**Veredicto: CERTIFICADO**

La suite completa de 34 tests unitarios pasa sin fallas bajo `pytest tests/unit/data/`. Los tres modulos del pipeline de datos (`bronze_loader.py`, `silver_cleaner.py`, `gold_builder.py`) cumplen los contratos del SpecDD §6–8 y los invariantes BR-01..BR-04, SR-01..SR-05 y GR-01..GR-06 del contrato de datos. No se detectaron rutas absolutas en codigo fuente ni dependencias no declaradas en `requirements.txt`. El linaje Bronze → Silver → Gold esta completamente trazado y es reproducible.

---

## 2. Resultado de la Suite de Tests

### 2.1 Ejecucion `pytest tests/unit/data/`

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\USUARIO\Documents\Work\ML\Flores_AI
configfile: pytest.ini

tests/unit/data/test_bronze_loader.py::test_bronze_row_count PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_column_count PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_zero_nulls PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_valid_species_set PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_column_names_and_order PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_id_dtype PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_numeric_features_dtype PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_species_dtype PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_records_per_class PASSED
tests/unit/data/test_bronze_loader.py::test_bronze_raises_file_not_found_for_missing_csv PASSED
tests/unit/data/test_gold_builder.py::test_gold_X_shape PASSED
tests/unit/data/test_gold_builder.py::test_gold_y_shape PASSED
tests/unit/data/test_gold_builder.py::test_gold_X_dtype PASSED
tests/unit/data/test_gold_builder.py::test_gold_X_zero_nan PASSED
tests/unit/data/test_gold_builder.py::test_gold_X_zero_inf PASSED
tests/unit/data/test_gold_builder.py::test_gold_y_valid_classes PASSED
tests/unit/data/test_gold_builder.py::test_gold_X_column_order PASSED
tests/unit/data/test_gold_builder.py::test_gold_X_y_length_consistency PASSED
tests/unit/data/test_gold_builder.py::test_gold_X_no_species_column PASSED
tests/unit/data/test_gold_builder.py::test_build_gold_raises_key_error_for_missing_feature_column PASSED
tests/unit/data/test_gold_builder.py::test_build_gold_raises_value_error_for_empty_dataframe PASSED
tests/unit/data/test_gold_builder.py::test_save_gold_creates_csv_files_at_given_paths PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_row_count PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_id_column_removed PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_column_names_and_order PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_valid_species_set PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_zero_duplicates PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_zero_nulls PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_numeric_features_dtype PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_species_dtype PASSED
tests/unit/data/test_silver_cleaner.py::test_silver_no_iris_prefix_in_species PASSED
tests/unit/data/test_silver_cleaner.py::test_clean_bronze_raises_key_error_without_id_column PASSED
tests/unit/data/test_silver_cleaner.py::test_clean_bronze_raises_value_error_for_empty_dataframe PASSED
tests/unit/data/test_silver_cleaner.py::test_save_silver_creates_csv_at_given_path PASSED

============================= 34 passed in 1.45s ==============================
```

### 2.2 Tabla Resumen por Suite

| Suite | Tests | Passed | Failed | Estado |
|-------|-------|--------|--------|--------|
| test_bronze_loader.py | 10 | 10 | 0 | PASS |
| test_silver_cleaner.py | 12 | 12 | 0 | PASS |
| test_gold_builder.py | 12 | 12 | 0 | PASS |
| **TOTAL** | **34** | **34** | **0** | **PASS** |

---

## 3. Trazabilidad de Linaje

### 3.1 Capa Bronze — SpecDD §6

**Modulo:** `src/data/bronze_loader.py`
**Funcion certificada:** `load_bronze(csv_path: Path = config.DATA_BRONZE) -> pd.DataFrame`
**Archivo fuente de datos:** `data/bronze/Iris.csv`

| Invariante | Descripcion | Expresion | Estado |
|-----------|-------------|-----------|--------|
| BR-01 | Numero de filas | `len(df) == 150` | PASS |
| BR-02 | Numero de columnas | `len(df.columns) == 6` | PASS |
| BR-03 | Cero nulos totales | `df.isnull().sum().sum() == 0` | PASS |
| BR-04 | Clases validas en Species | `set(df['Species']) == {'Iris-setosa', 'Iris-versicolor', 'Iris-virginica'}` | PASS |
| BR-05 | Columnas exactas en orden | `list(df.columns) == ['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']` | PASS |
| BR-06 | Tipos de datos correctos | Id: int64, medidas: float64, Species: object | PASS |
| BR-07 | Balance de clases | 50 registros exactos por cada clase | PASS |
| BR-08 | Manejo de error FileNotFoundError | Lanzado cuando csv_path no existe | PASS |

**Notas de implementacion:**
- El modulo solo ejecuta `pd.read_csv(csv_path)` sin ningun tipo de transformacion, respetando el principio de inmutabilidad de la capa Bronze.
- La guardia `if not csv_path.exists(): raise FileNotFoundError(...)` cumple el contrato de excepciones del SpecDD §6.
- No importa `sklearn`, `streamlit` ni `pydantic` (cumple prohibicion SAD §5.1).

### 3.2 Capa Silver — SpecDD §7

**Modulo:** `src/data/silver_cleaner.py`
**Funciones certificadas:** `clean_bronze(df_bronze: pd.DataFrame) -> pd.DataFrame`, `save_silver(df_silver, path)`
**Archivo producido:** `data/silver/iris_silver.csv`

| Invariante | Descripcion | Expresion | Estado |
|-----------|-------------|-----------|--------|
| SR-01 | Numero de filas | `len(df) == 147` | PASS |
| SR-02 | Columna Id ausente | `'Id' not in df.columns` | PASS |
| SR-03 | Columnas en snake_case | `list(df.columns) == ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']` | PASS |
| SR-04 | Etiquetas normalizadas | `set(df['species']) == {'setosa', 'versicolor', 'virginica'}` | PASS |
| SR-05 | Cero duplicados | `df.duplicated().sum() == 0` | PASS |
| SR-05b | Cero nulos | `df.isnull().sum().sum() == 0` | PASS |
| SR-06 | Tipos de datos correctos | medidas: float64, species: object | PASS |
| SR-07 | Sin prefijo 'Iris-' en species | ninguna etiqueta comienza con 'Iris-' | PASS |
| SR-08 | KeyError si columna Id ausente | lanzado cuando df_bronze no tiene columna 'Id' | PASS |
| SR-09 | ValueError si df vacio | lanzado cuando df_bronze esta vacio | PASS |
| SR-10 | save_silver() crea CSV | archivo existe en el path inyectado | PASS |

**Transformaciones aplicadas (linaje documentado):**

| ID Mutacion | Descripcion | Origen | Destino |
|------------|-------------|--------|---------|
| M-01 | Eliminar columna 'Id' | Columna Id (int64) | Ausente en Silver |
| M-02 | Eliminar 3 duplicados | 150 filas | 147 filas |
| M-03 | Renombrar a snake_case | SepalLengthCm, etc. | sepal_length, etc. |
| M-04 | Normalizar etiquetas | Iris-setosa, etc. | setosa, etc. |

**Notas de implementacion:**
- `RENAME_MAP` y `LABEL_MAP` declarados como constantes de modulo (SpecDD §7).
- El orden de aplicacion de mutaciones (M-01 → M-04) es determinista y documentado.
- El `reset_index(drop=True)` garantiza indices contiguos tras `drop_duplicates()`.
- No importa `sklearn`, `streamlit` ni `pydantic` (cumple prohibicion SAD §5.1).

### 3.3 Capa Gold — SpecDD §8

**Modulo:** `src/data/gold_builder.py`
**Funciones certificadas:** `build_gold(df_silver: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]`, `save_gold(X, y, path_X, path_y)`
**Archivos producidos:** `data/gold/X_gold.csv`, `data/gold/y_gold.csv`

| Invariante | Descripcion | Expresion | Estado |
|-----------|-------------|-----------|--------|
| GR-01 | Shape de X | `X.shape == (147, 4)` | PASS |
| GR-02 | Shape de y | `y.shape == (147,)` | PASS |
| GR-03 | Dtype de X | `X.dtype == np.float64` | PASS |
| GR-04 | Cero NaN en X | `np.isnan(X).sum() == 0` | PASS |
| GR-05 | Cero Inf en X | `np.isinf(X).sum() == 0` | PASS |
| GR-06 | Clases validas en y | `set(np.unique(y)) == {'setosa', 'versicolor', 'virginica'}` | PASS |
| GR-07 | Orden canonico de columnas en X | X coincide con `config.FEATURE_COLUMNS` | PASS |
| GR-08 | Consistencia X e y | `len(X) == len(y)` | PASS |
| GR-09 | Ausencia de target leakage | columna 'species' no figura en X | PASS |
| GR-10 | KeyError si falta columna de feature | lanzado cuando falta columna requerida | PASS |
| GR-11 | ValueError si df vacio | lanzado cuando df_silver esta vacio | PASS |
| GR-12 | save_gold() crea CSV X e y | ambos archivos existen en los paths inyectados | PASS |

**Notas de implementacion:**
- `TARGET_COLUMN = "species"` declarado como constante de modulo, previniendo leakage accidental.
- La seleccion de features usa `df_silver[config.FEATURE_COLUMNS]` con lista ordenada: orden canonico garantizado.
- La conversion `to_numpy(dtype=np.float64)` es explicita: no hay inferencia implicita de tipo.
- `save_gold()` usa paths independientes para X e y con `mkdir(parents=True, exist_ok=True)` (idempotente).
- No importa `sklearn`, `streamlit` ni `pydantic` (cumple prohibicion SAD §5.1).

---

## 4. Cumplimiento SAD §5

### 4.1 Arquitectura de Modulos

| Modulo | Responsabilidad Unica Definida | Implementada Correctamente | Estado |
|--------|-------------------------------|---------------------------|--------|
| `config.py` | Rutas relativas y constantes via pathlib | `PROJECT_ROOT = Path(__file__).resolve().parent.parent`. Sin logica, sin I/O. | PASS |
| `bronze_loader.py` | Lectura CSV sin transformaciones | Solo `pd.read_csv()` con guardia de existencia de archivo. | PASS |
| `silver_cleaner.py` | Transformaciones M-01 a M-04 | Pipeline atomico en orden, sin construir features ni entrenar. | PASS |
| `gold_builder.py` | Separar X e y, persistir en gold/ | Usa `config.FEATURE_COLUMNS`, sin limpiar datos ni entrenar. | PASS |

### 4.2 Architecture Decision Records (ADRs)

| ADR | Descripcion | Verificacion | Estado |
|-----|-------------|-------------|--------|
| ADR-001 | Streamlit como framework de UI | No aplica a modulos de Phase Engineering. Pipeline de datos es independiente de UI. | N/A |
| ADR-002 | Joblib para serializacion del modelo | No aplica a modulos Bronze/Silver/Gold. No hay serializacion de modelo en esta fase. | N/A |
| ADR-003 | StandardScaler encapsulado en Pipeline | No aplica a Phase Engineering. El scaler no se aplica en capas Bronze/Silver/Gold (previene leakage). | PASS |
| ADR-004 | pathlib.Path para rutas relativas | `config.py` usa `Path(__file__).resolve().parent.parent`. Todos los modulos importan rutas de `config`. Cero strings hardcodeados. | PASS |

**Regla arquitectonica verificada:** Ningun modulo del pipeline offline (`bronze_loader`, `silver_cleaner`, `gold_builder`) importa nada del pipeline online (`app`, `validators`, `predictor`, `feedback`). La separacion de entornos SAD §6.3 esta respetada.

### 4.3 Verificacion de Rutas

- Sin rutas absolutas en archivos `.py`: PASS
- Inspeccion realizada sobre: `src/data/bronze_loader.py`, `src/data/silver_cleaner.py`, `src/data/gold_builder.py`, `src/config.py`, `tests/unit/data/test_bronze_loader.py`, `tests/unit/data/test_silver_cleaner.py`, `tests/unit/data/test_gold_builder.py`
- Metodo de inspeccion: busqueda de patrones `C:\`, `/home/`, `/Users/` en codigo fuente `.py`
- Resultado: ninguna coincidencia en archivos fuente. Los archivos `.pyc` compilados del cache de Python contienen rutas del sistema (esperado e inofensivo, ya que son artefactos de compilacion no versionados).
- Las fixtures de tests calculan rutas con `Path(__file__).resolve().parent.parent.parent.parent / "data" / ...` (patron identico a config.py, relativo a la ubicacion del archivo).

---

## 5. Verificacion de Dependencias

Las siguientes librerias son importadas en los modulos `src/data/` y `src/config.py`. Se verifica su declaracion en `requirements.txt`.

| Libreria usada | Modulos que la importan | Declarada en requirements.txt | Version requerida | Estado |
|----------------|------------------------|-------------------------------|-------------------|--------|
| `pandas` | bronze_loader.py, silver_cleaner.py, gold_builder.py | Si | `>=2.2` | PASS |
| `numpy` | gold_builder.py | Si | `>=1.26` | PASS |
| `pathlib` | config.py, bronze_loader.py, silver_cleaner.py, gold_builder.py | Stdlib Python 3.4+ — no requiere declaracion | N/A | PASS |
| `pytest` | tests/unit/data/ (dependencia de test) | Si | `>=8.0` | PASS |

**Librerias prohibidas verificadas (SAD §5.1):** `sklearn`, `streamlit`, `pydantic` no aparecen en ninguno de los modulos del pipeline de datos. PASS.

---

## 6. Cadena de Linaje: Bronze → Silver → Gold

```
data/bronze/Iris.csv
    [150 filas, 6 columnas: Id, SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm, Species]
    [Tipos: int64, float64x4, object]
    |
    | bronze_loader.load_bronze() — solo lectura, cero transformaciones
    v
DataFrame Bronze (150, 6) — invariantes BR-01..BR-08 verificados
    |
    | silver_cleaner.clean_bronze()
    | M-01: drop('Id')
    | M-02: drop_duplicates() [150 -> 147 filas]
    | M-03: rename(RENAME_MAP) [PascalCase+Cm -> snake_case]
    | M-04: map(LABEL_MAP) [Iris-<especie> -> <especie>]
    v
DataFrame Silver (147, 5) — invariantes SR-01..SR-10 verificados
    | Persistido en: data/silver/iris_silver.csv
    |
    | gold_builder.build_gold()
    | X = df_silver[config.FEATURE_COLUMNS].to_numpy(dtype=float64)
    | y = df_silver['species'].to_numpy()
    v
Arrays Gold: X (147, 4) float64, y (147,) object — invariantes GR-01..GR-12 verificados
    Persistidos en: data/gold/X_gold.csv, data/gold/y_gold.csv
```

**Determinismo garantizado:** La cadena completa es reproducible. Las tres transformaciones son deterministas: `drop_duplicates(keep="first")`, renombrado por mapa fijo, y normalizacion de etiquetas por mapa fijo. No existe aleatoriedad en Phase Engineering.

---

## 7. Veredicto Final

**Estado: CERTIFICADO**

| Criterio DoD | Requerimiento | Resultado |
|-------------|--------------|-----------|
| Tests pasan en conjunto | `pytest tests/unit/data/` — 34 tests | 34 passed, 0 failed |
| Trazabilidad Bronze | SpecDD §6, contract.md §10.2 (BR-01..BR-04) | Certificado |
| Trazabilidad Silver | SpecDD §7, contract.md §10.3 (SR-01..SR-05) | Certificado |
| Trazabilidad Gold | SpecDD §8, contract.md §10.4 (GR-01..GR-06) | Certificado |
| Cumplimiento SAD §5 | Responsabilidades unicas, separacion de entornos, ADR-004 | Certificado |
| Sin rutas absolutas | Inspeccion de archivos .py en src/data/ y tests/unit/data/ | PASS |
| Dependencias declaradas | requirements.txt cubre pandas, numpy, pytest | PASS |

**Condicion para avanzar a F2-T11 (Validacion):** Cumplida. El dataset Gold (`data/gold/X_gold.csv`, `data/gold/y_gold.csv`) esta certificado tecnicamente y esta disponible para la validacion de KPIs de negocio del BRD.

**Firma:** @ai-data-qa-engineer | 2026-04-24
