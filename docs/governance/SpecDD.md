# SpecDD: Specification-Driven Development
## Proyecto: Flores AI - Iris

> **Documento:** SpecDD - Especificacion de Interfaces de Software
> **Version:** 1.0.0
> **Estado:** Certificado - Phase Discovery Discovery
> **Fecha de creacion:** 2026-04-19
> **Ultima actualizacion:** 2026-04-19
> **Autor:** ai-solutions-architect
> **Trazabilidad:** SAD v1.0.0 -> SpecDD v1.0.0 -> BRD v1.0.0
> **Regla:** Ningun archivo `.py` en `src/` puede ser implementado sin que su seccion correspondiente en este documento este marcada como Certificada.

---

## Indice

1. [Tipos de Datos Compartidos (Pydantic v2)](#1-tipos-de-datos-compartidos-pydantic-v2)
2. [src/config.py](#2-srcconfigpy)
3. [src/validators.py](#3-srcvalidatorspy)
4. [src/predictor.py](#4-srcpredictorpy)
5. [src/feedback.py](#5-srcfeedbackpy)
6. [src/data/bronze_loader.py](#6-srcdatabronze_loaderpy)
7. [src/data/silver_cleaner.py](#7-srcdatasilver_cleanerpy)
8. [src/data/gold_builder.py](#8-srcdatagold_builderpy)
9. [src/training/trainer.py](#9-srctrainingtrainerpy)
10. [src/training/serializer.py](#10-srctrainingserializerpy)
11. [src/app.py](#11-srcapppy)
12. [Estandares de Ingenieria](#12-estandares-de-ingenieria)
13. [Protocolo de Mock para Desarrollo Paralelo](#13-protocolo-de-mock-para-desarrollo-paralelo)
14. [Check de Certificacion SpecDD](#14-check-de-certificacion-specdd)

---

## 1. Tipos de Datos Compartidos (Pydantic v2)

Estos tipos son los contratos de frontera del sistema. Son la unica fuente de verdad para la forma de los datos que cruzan limites entre modulos.

### 1.1 IrisInput

**Ubicacion:** `src/validators.py`
**Proposito:** Contrato de entrada del usuario. Valida tipos y rangos antes de que el dato llegue al modelo.

```python
class IrisInput(BaseModel):
    sepal_length: float = Field(..., ge=3.0, le=9.0,
                                description="Longitud del sepalo en cm")
    sepal_width:  float = Field(..., ge=1.5, le=5.5,
                                description="Ancho del sepalo en cm")
    petal_length: float = Field(..., ge=0.5, le=8.0,
                                description="Longitud del petalo en cm")
    petal_width:  float = Field(..., ge=0.0, le=3.5,
                                description="Ancho del petalo en cm")
```

**Restricciones de validacion:**

| Campo | Tipo | Minimo (ge) | Maximo (le) | Nulidad |
| :--- | :--- | :--- | :--- | :--- |
| sepal_length | float | 3.0 | 9.0 | No nulo (required) |
| sepal_width | float | 1.5 | 5.5 | No nulo (required) |
| petal_length | float | 0.5 | 8.0 | No nulo (required) |
| petal_width | float | 0.0 | 3.5 | No nulo (required) |

**Comportamiento ante falla:** Lanza `pydantic.ValidationError` con mensajes descriptivos por campo. El mensaje de error NO expone trazas de Python. La capa `app.py` captura esta excepcion y renderiza el mensaje de Pydantic en el componente `st.error()`.

### 1.2 PredictionResult

**Ubicacion:** `src/predictor.py`
**Proposito:** Contrato de salida de inferencia. Todo lo que `app.py` necesita saber del resultado del modelo.

```python
class PredictionResult(BaseModel):
    species:        str
    confidence:     float
    probabilities:  dict[str, float]
    low_confidence: bool

    @field_validator('species')
    @classmethod
    def species_must_be_valid(cls, v: str) -> str:
        valid = {'setosa', 'versicolor', 'virginica'}
        if v not in valid:
            raise ValueError(f"Especie desconocida: {v}. Validas: {valid}")
        return v

    @field_validator('confidence')
    @classmethod
    def confidence_must_be_probability(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("confidence debe estar en [0.0, 1.0]")
        return v
```

**Regla de negocio:** `low_confidence = True` cuando `confidence < 0.60`. Esta regla se evalua en `predictor.py` al construir el objeto, no en `app.py`.

### 1.3 FeedbackRecord

**Ubicacion:** `src/feedback.py`
**Proposito:** Contrato de un registro de feedback. Define la estructura del JSON que se escribe en `logs/feedback.log`.

```python
class FeedbackRecord(BaseModel):
    timestamp:         str    # ISO-8601, e.g.: "2026-04-19T15:30:00Z"
    sepal_length:      float
    sepal_width:       float
    petal_length:      float
    petal_width:       float
    predicted_species: str
    confidence:        float
```

### 1.4 TrainingMetrics

**Ubicacion:** `src/training/trainer.py`
**Proposito:** Contrato de retorno del proceso de entrenamiento. Permite que el agente de Model QA valide las metricas sin acceder al pipeline directamente.

```python
class TrainingMetrics(TypedDict):
    accuracy_cv_mean:  float   # Media de accuracy en K-Fold CV
    accuracy_cv_std:   float   # Desviacion estandar de accuracy en K-Fold CV
    accuracy_test:     float   # Accuracy en hold-out test set
    f1_macro_test:     float   # F1-Score Macro en hold-out test set
    f1_per_class:      dict[str, float]  # {'setosa': 0.99, 'versicolor': 0.95, 'virginica': 0.96}
    n_train:           int     # Numero de registros usados en entrenamiento
    n_test:            int     # Numero de registros usados en test
    random_state:      int     # Siempre 42
```

---

## 2. src/config.py

**Estado:** Certificado
**Responsabilidad unica:** Centralizar todas las rutas relativas y constantes del proyecto.
**Importado por:** Todos los demas modulos de `src/`.
**No importa:** pandas, scikit-learn, streamlit, pydantic.

### Interfaz Publica

```python
# Constantes de ruta (pathlib.Path objects)
PROJECT_ROOT: Path   # Raiz del repositorio
DATA_BRONZE:  Path   # data/bronze/Iris.csv
DATA_SILVER:  Path   # data/silver/iris_silver.csv
DATA_GOLD_X:  Path   # data/gold/X_gold.csv
DATA_GOLD_Y:  Path   # data/gold/y_gold.csv
MODEL_PATH:   Path   # models/iris_model.joblib
FEEDBACK_LOG: Path   # logs/feedback.log

# Constantes de modelo
RANDOM_STATE:      int   = 42
TEST_SIZE:         float = 0.20
CV_FOLDS:          int   = 5
CONFIDENCE_THRESHOLD: float = 0.60

# Constantes de validacion de entrada
FEATURE_RANGES: dict[str, tuple[float, float]] = {
    "sepal_length": (3.0, 9.0),
    "sepal_width":  (1.5, 5.5),
    "petal_length": (0.5, 8.0),
    "petal_width":  (0.0, 3.5),
}

# Orden canonico de features (critico para garantizar que el array de inferencia
# tenga el mismo orden que el array de entrenamiento)
FEATURE_COLUMNS: list[str] = [
    "sepal_length", "sepal_width", "petal_length", "petal_width"
]

# Clases validas en orden canonico (debe coincidir con el orden que scikit-learn
# asigna internamente; se verifica en test_predictor.py)
CLASS_NAMES: list[str] = ["setosa", "versicolor", "virginica"]
```

### Pre-condiciones

- `config.py` esta ubicado en `src/config.py`.
- `PROJECT_ROOT` se calcula como `Path(__file__).resolve().parent.parent`.

### Post-condiciones

- Todas las rutas son objetos `pathlib.Path`.
- Ninguna ruta es absoluta hardcodeada.
- `FEATURE_COLUMNS` define el orden canonico que todos los modulos deben respetar al construir arrays de numpy.

### Excepciones

- Ningun `FileNotFoundError` se lanza desde `config.py`. Las rutas representan ubicaciones esperadas; la existencia del archivo es validada por el modulo que lo consume.

---

## 3. src/validators.py

**Estado:** Certificado
**Responsabilidad unica:** Definir el tipo `IrisInput` y exponer la funcion de validacion.
**Importa:** `pydantic`, `src.config`
**No importa:** pandas, scikit-learn, streamlit.

### Interfaz Publica

```python
class IrisInput(BaseModel):
    """Ver seccion 1.1 para definicion completa con Field y validadores."""
    sepal_length: float
    sepal_width:  float
    petal_length: float
    petal_width:  float


def validate_input(
    sepal_length: float,
    sepal_width:  float,
    petal_length: float,
    petal_width:  float,
) -> IrisInput:
    """
    Construye y valida un IrisInput desde los valores crudos del formulario.

    Args:
        sepal_length: Longitud del sepalo en cm.
        sepal_width:  Ancho del sepalo en cm.
        petal_length: Longitud del petalo en cm.
        petal_width:  Ancho del petalo en cm.

    Returns:
        IrisInput: Objeto validado y dentro de rango.

    Raises:
        pydantic.ValidationError: Si alguno de los valores esta fuera del rango
            definido en config.FEATURE_RANGES o no es de tipo float.
    """
```

### Pre-condiciones

- Los cuatro argumentos son valores numericos (int o float) provenientes del formulario de Streamlit.

### Post-condiciones

- Si retorna `IrisInput`, todos los campos estan dentro de sus rangos definidos en `config.FEATURE_RANGES`.
- Si lanza `ValidationError`, el error contiene mensajes legibles por campo (e.g., "sepal_length: Value should be greater than or equal to 3.0").

### Excepciones

| Excepcion | Condicion |
| :--- | :--- |
| `pydantic.ValidationError` | Cualquier campo fuera de rango, nulo, o de tipo incorrecto. |

### Comportamiento Mock

Para desarrollo paralelo, un mock de `validate_input` puede retornar directamente un `IrisInput` con valores fijos:
```python
def validate_input_mock(*args) -> IrisInput:
    return IrisInput(sepal_length=5.1, sepal_width=3.5,
                     petal_length=1.4, petal_width=0.2)
```

---

## 4. src/predictor.py

**Estado:** Certificado
**Responsabilidad unica:** Cargar el pipeline serializado y ejecutar inferencia.
**Importa:** `numpy`, `joblib`, `sklearn.pipeline`, `pydantic`, `src.config`, `src.validators` (IrisInput), `src.predictor` (PredictionResult)
**No importa:** pandas, streamlit.

### Interfaz Publica

```python
class PredictionResult(BaseModel):
    """Ver seccion 1.2 para definicion completa con validadores."""
    species:        str
    confidence:     float
    probabilities:  dict[str, float]
    low_confidence: bool


def load_pipeline(model_path: Path = config.MODEL_PATH) -> Pipeline:
    """
    Carga el pipeline scikit-learn desde el archivo .joblib.
    Debe ser invocada con st.cache_resource en app.py para evitar
    recargas en cada interaccion del usuario.

    Args:
        model_path: Ruta al archivo .joblib. Default: config.MODEL_PATH.

    Returns:
        sklearn.pipeline.Pipeline: Pipeline fitted (Scaler + Clasificador).

    Raises:
        FileNotFoundError: Si el archivo no existe en model_path.
        ValueError: Si el objeto cargado no es una instancia de Pipeline.
    """


def predict(iris_input: IrisInput, pipeline: Pipeline) -> PredictionResult:
    """
    Ejecuta inferencia sobre un unico registro de entrada.

    Args:
        iris_input: Objeto IrisInput validado (proveniente de validators.py).
        pipeline:   Pipeline scikit-learn fitted (proveniente de load_pipeline).

    Returns:
        PredictionResult: Resultado de inferencia con especie, confianza,
                          probabilidades y flag de baja confianza.

    Raises:
        RuntimeError: Si pipeline.predict() o pipeline.predict_proba() fallan
                      por razon interna del modelo.
    """
```

### Pre-condiciones para `predict()`

- `iris_input` fue producido por `validators.validate_input()` y paso la validacion.
- `pipeline` fue cargado con `load_pipeline()` y es un objeto `sklearn.pipeline.Pipeline` fitted.
- El pipeline fue entrenado con features en el orden definido por `config.FEATURE_COLUMNS`.

### Post-condiciones para `predict()`

- `result.species` es uno de `{'setosa', 'versicolor', 'virginica'}`.
- `result.confidence` es el maximo de `result.probabilities.values()`.
- `sum(result.probabilities.values()) == 1.0` (tolerancia de punto flotante: abs < 1e-6).
- `result.low_confidence == (result.confidence < config.CONFIDENCE_THRESHOLD)`.

### Logica de Construccion del Array de Inferencia

```
X_infer = np.array([[
    iris_input.sepal_length,
    iris_input.sepal_width,
    iris_input.petal_length,
    iris_input.petal_width,
]])  # shape: (1, 4)
# El orden debe coincidir exactamente con config.FEATURE_COLUMNS
```

### Excepciones

| Excepcion | Condicion |
| :--- | :--- |
| `FileNotFoundError` | `model_path` no existe en `load_pipeline()`. |
| `ValueError` | El objeto cargado no es `sklearn.pipeline.Pipeline`. |
| `RuntimeError` | Falla interna durante `pipeline.predict()`. |

### Comportamiento Mock

```python
def predict_mock(iris_input: IrisInput, pipeline: Any) -> PredictionResult:
    return PredictionResult(
        species="setosa",
        confidence=0.97,
        probabilities={"setosa": 0.97, "versicolor": 0.02, "virginica": 0.01},
        low_confidence=False,
    )
```

---

## 5. src/feedback.py

**Estado:** Certificado
**Responsabilidad unica:** Registrar eventos de feedback del usuario en `logs/feedback.log`.
**Importa:** `json`, `datetime`, `pathlib`, `src.config`, `src.validators` (IrisInput), `src.predictor` (PredictionResult)
**No importa:** pandas, scikit-learn, streamlit.

### Interfaz Publica

```python
class FeedbackRecord(BaseModel):
    """Ver seccion 1.3 para definicion completa."""
    timestamp:         str
    sepal_length:      float
    sepal_width:       float
    petal_length:      float
    petal_width:       float
    predicted_species: str
    confidence:        float


def log_feedback(
    iris_input:        IrisInput,
    prediction_result: PredictionResult,
    log_path:          Path = config.FEEDBACK_LOG,
) -> None:
    """
    Registra un evento de feedback en el archivo de log.
    Cada registro es una linea JSON independiente (JSON Lines format).

    Args:
        iris_input:        Las features ingresadas por el usuario.
        prediction_result: El resultado de prediccion que el usuario rechazo.
        log_path:          Ruta al archivo de log. Default: config.FEEDBACK_LOG.

    Returns:
        None

    Raises:
        OSError: Si el directorio de `log_path` no existe y no puede ser creado.
    """
```

### Pre-condiciones

- `iris_input` fue validado por `validators.validate_input()`.
- `prediction_result` fue producido por `predictor.predict()`.

### Post-condiciones

- El archivo `logs/feedback.log` contiene una nueva linea al final.
- La linea es un JSON valido que puede ser deserializado a `FeedbackRecord`.
- El campo `timestamp` esta en formato ISO-8601 UTC.

### Formato del Archivo de Log (JSON Lines)

```
{"timestamp": "2026-04-19T15:30:00Z", "sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2, "predicted_species": "setosa", "confidence": 0.97}
{"timestamp": "2026-04-19T15:32:10Z", "sepal_length": 6.3, "sepal_width": 2.8, "petal_length": 5.1, "petal_width": 1.5, "predicted_species": "versicolor", "confidence": 0.61}
```

### Excepciones

| Excepcion | Condicion |
| :--- | :--- |
| `OSError` | El directorio `logs/` no existe y `mkdir()` falla por permisos. |

### Comportamiento de Creacion de Directorio

Si `log_path.parent` no existe, `log_feedback()` intenta crearlo con `log_path.parent.mkdir(parents=True, exist_ok=True)` antes de escribir.

---

## 6. src/data/bronze_loader.py

**Estado:** Certificado
**Responsabilidad unica:** Leer el CSV crudo y retornar el DataFrame sin transformaciones.
**Importa:** `pandas`, `pathlib`, `src.config`
**No importa:** scikit-learn, streamlit, pydantic.

### Interfaz Publica

```python
def load_bronze(csv_path: Path = config.DATA_BRONZE) -> pd.DataFrame:
    """
    Lee el archivo CSV crudo del dataset Iris.
    No realiza ninguna transformacion sobre los datos.

    Args:
        csv_path: Ruta al archivo CSV. Default: config.DATA_BRONZE.

    Returns:
        pd.DataFrame: DataFrame con 150 filas y 6 columnas:
                      ['Id', 'SepalLengthCm', 'SepalWidthCm',
                       'PetalLengthCm', 'PetalWidthCm', 'Species']
                      Tipos: int64 (Id), float64 (x4), object (Species).

    Raises:
        FileNotFoundError: Si csv_path no existe.
        pd.errors.ParserError: Si el archivo no es un CSV valido.
    """
```

### Pre-condiciones

- El archivo `data/bronze/Iris.csv` existe en la ruta relativa desde `PROJECT_ROOT`.

### Post-condiciones

- El DataFrame retornado tiene exactamente 150 filas.
- El DataFrame tiene exactamente 6 columnas: `['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']`.
- Cero valores nulos en ninguna columna.
- Tipos de datos: `Id: int64`, `SepalLengthCm/SepalWidthCm/PetalLengthCm/PetalWidthCm: float64`, `Species: object`.

### Excepciones

| Excepcion | Condicion |
| :--- | :--- |
| `FileNotFoundError` | `csv_path` no existe. |
| `pd.errors.ParserError` | El CSV esta malformado. |

---

## 7. src/data/silver_cleaner.py

**Estado:** Certificado
**Responsabilidad unica:** Aplicar las transformaciones de limpieza M-01 a M-04 sobre el DataFrame Bronze.
**Importa:** `pandas`, `src.config`
**No importa:** scikit-learn, streamlit, pydantic.

### Interfaz Publica

```python
def clean_bronze(df_bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica las mutaciones de calidad de datos definidas en el feasibility.
    Cada transformacion es atomica y aplicada en el orden documentado.

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
                      Tipos: float64 (x4), object (species).

    Raises:
        KeyError: Si 'Id' o alguna columna requerida no existe en df_bronze.
        ValueError: Si df_bronze esta vacio.
    """


def save_silver(df_silver: pd.DataFrame, path: Path = config.DATA_SILVER) -> None:
    """
    Persiste el DataFrame Silver en formato CSV.

    Args:
        df_silver: DataFrame limpio (147, 5).
        path:      Ruta de destino. Default: config.DATA_SILVER.

    Returns:
        None

    Raises:
        OSError: Si el directorio de destino no existe y no puede crearse.
    """
```

### Mapa de Renombrado (M-03)

```python
RENAME_MAP: dict[str, str] = {
    "SepalLengthCm": "sepal_length",
    "SepalWidthCm":  "sepal_width",
    "PetalLengthCm": "petal_length",
    "PetalWidthCm":  "petal_width",
    "Species":       "species",
}
```

### Mapa de Normalizacion de Etiquetas (M-04)

```python
LABEL_MAP: dict[str, str] = {
    "Iris-setosa":     "setosa",
    "Iris-versicolor": "versicolor",
    "Iris-virginica":  "virginica",
}
```

### Post-condiciones

- Shape del DataFrame retornado: `(147, 5)`.
- Columnas en orden: `['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']`.
- Valores unicos en `species`: `{'setosa', 'versicolor', 'virginica'}`.
- Cero valores nulos.
- Cero filas duplicadas.

### Excepciones

| Excepcion | Condicion |
| :--- | :--- |
| `KeyError` | La columna `Id` o cualquier columna de features no existe en `df_bronze`. |
| `ValueError` | `df_bronze` esta vacio (0 filas). |

---

## 8. src/data/gold_builder.py

**Estado:** Certificado
**Responsabilidad unica:** Separar features (X) y target (y), y persistir en `data/gold/`.
**Importa:** `pandas`, `numpy`, `pathlib`, `src.config`
**No importa:** scikit-learn, streamlit, pydantic.

### Interfaz Publica

```python
def build_gold(
    df_silver: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Separa el DataFrame Silver en arrays de features (X) y target (y).
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


def save_gold(
    X: np.ndarray,
    y: np.ndarray,
    path_X: Path = config.DATA_GOLD_X,
    path_y: Path = config.DATA_GOLD_Y,
) -> None:
    """
    Persiste X e y en formato CSV en data/gold/.

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
```

### Post-condiciones para `build_gold()`

- `X.shape == (147, 4)`.
- `y.shape == (147,)`.
- `X.dtype == np.float64`.
- El orden de columnas en `X` es el definido por `config.FEATURE_COLUMNS`.
- `np.unique(y)` retorna `['setosa', 'versicolor', 'virginica']` (orden alfabetico de numpy).

---

## 9. src/training/trainer.py

**Estado:** Certificado
**Responsabilidad unica:** Construir, ajustar y evaluar el Pipeline de scikit-learn.
**Importa:** `numpy`, `sklearn.*`, `src.config`
**No importa:** pandas (acepta arrays numpy), streamlit, pydantic.

### Interfaz Publica

```python
from typing import TypedDict

class TrainingMetrics(TypedDict):
    """Ver seccion 1.4 para definicion completa."""
    accuracy_cv_mean:  float
    accuracy_cv_std:   float
    accuracy_test:     float
    f1_macro_test:     float
    f1_per_class:      dict[str, float]
    n_train:           int
    n_test:            int
    random_state:      int


def build_pipeline(classifier) -> Pipeline:
    """
    Construye el Pipeline de scikit-learn con StandardScaler + clasificador.

    Args:
        classifier: Instancia de un clasificador scikit-learn compatible con
                    predict_proba() (e.g., RandomForestClassifier, SVC con
                    probability=True, LogisticRegression, KNeighborsClassifier).

    Returns:
        sklearn.pipeline.Pipeline: Pipeline sin ajustar (unfitted).
            Steps: [('scaler', StandardScaler()), ('clf', classifier)]
    """


def train_and_evaluate(
    X: np.ndarray,
    y: np.ndarray,
    classifier,
    test_size:    float = config.TEST_SIZE,
    random_state: int   = config.RANDOM_STATE,
    cv_folds:     int   = config.CV_FOLDS,
) -> tuple[Pipeline, TrainingMetrics]:
    """
    Ejecuta el ciclo completo de entrenamiento y evaluacion.

    Proceso interno:
        1. train_test_split(X, y, test_size, random_state, stratify=y)
        2. build_pipeline(classifier)
        3. K-Fold CV sobre X_train (k=cv_folds, scoring='accuracy')
        4. pipeline.fit(X_train, y_train)
        5. pipeline.predict(X_test) -> calcular accuracy, f1_macro, f1_per_class
        6. Construir TrainingMetrics

    Args:
        X:            Array de features (147, 4), dtype float64.
        y:            Array de targets (147,), valores str.
        classifier:   Instancia de clasificador scikit-learn.
        test_size:    Fraccion del dataset para test. Default: 0.20.
        random_state: Semilla de aleatoriedad. Default: 42.
        cv_folds:     Numero de folds para CV. Default: 5.

    Returns:
        tuple[Pipeline, TrainingMetrics]:
            Pipeline: Pipeline fitted sobre X_train completo.
            TrainingMetrics: Diccionario de metricas de evaluacion.

    Raises:
        ValueError: Si X o y estan vacios, o si las dimensiones no coinciden.
        sklearn.exceptions.NotFittedError: (no debe ocurrir; interno al proceso)
    """
```

### Post-condiciones para `train_and_evaluate()`

- El `Pipeline` retornado esta fitted sobre `X_train` (80% de 147 = ~117 registros).
- `metrics['accuracy_test'] >= 0.90` (umbral minimo RED del BRD; si no se alcanza, el agente de Model QA falla el test).
- `metrics['n_train'] + metrics['n_test'] == len(X)`.
- `metrics['random_state'] == 42`.

### Excepciones

| Excepcion | Condicion |
| :--- | :--- |
| `ValueError` | `X` o `y` vacios, o `len(X) != len(y)`. |

---

## 10. src/training/serializer.py

**Estado:** Certificado
**Responsabilidad unica:** Serializar y deserializar el pipeline entrenado.
**Importa:** `joblib`, `pathlib`, `sklearn.pipeline`, `src.config`
**No importa:** pandas, streamlit, pydantic, numpy.

### Interfaz Publica

```python
def save_model(
    pipeline:   Pipeline,
    model_path: Path = config.MODEL_PATH,
) -> None:
    """
    Serializa el pipeline entrenado en formato Joblib.

    Args:
        pipeline:   Pipeline scikit-learn fitted.
        model_path: Ruta de destino. Default: config.MODEL_PATH.

    Returns:
        None

    Raises:
        TypeError: Si `pipeline` no es instancia de sklearn.pipeline.Pipeline.
        OSError:   Si el directorio `models/` no puede ser creado.
    """


def load_model(model_path: Path = config.MODEL_PATH) -> Pipeline:
    """
    Carga el pipeline serializado desde el archivo .joblib.
    Nota: Este metodo es equivalente a predictor.load_pipeline().
    Existe aqui para uso en tests de integracion del pipeline de entrenamiento.

    Args:
        model_path: Ruta al archivo .joblib. Default: config.MODEL_PATH.

    Returns:
        sklearn.pipeline.Pipeline: Pipeline fitted.

    Raises:
        FileNotFoundError: Si model_path no existe.
        ValueError:        Si el objeto cargado no es Pipeline.
    """
```

### Post-condiciones para `save_model()`

- El archivo `models/iris_model.joblib` existe tras la llamada.
- El archivo puede ser cargado con `joblib.load(model_path)` sin errores.
- El objeto cargado es una instancia de `sklearn.pipeline.Pipeline`.

### Excepciones

| Excepcion | Condicion |
| :--- | :--- |
| `TypeError` | `pipeline` no es instancia de `sklearn.pipeline.Pipeline`. |
| `OSError` | El directorio `models/` no existe y no puede ser creado. |
| `FileNotFoundError` | `model_path` no existe en `load_model()`. |

---

## 11. src/app.py

**Estado:** Certificado
**Responsabilidad unica:** Punto de entrada de la aplicacion Streamlit. Orquesta la UI completa.
**Importa:** `streamlit`, `plotly.express`, `src.config`, `src.validators`, `src.predictor`, `src.feedback`
**No importa:** pandas, numpy (directamente), sklearn, bronze_loader, silver_cleaner, gold_builder, trainer, serializer.

### Estructura Funcional (no firmas de funciones sino responsabilidades de bloque)

```
[INICIALIZACION]
- st.set_page_config(title="Flores AI - Iris", layout="centered")
- pipeline = st.cache_resource(predictor.load_pipeline)()

[CABECERA]
- st.title("Flores AI - Clasificador de Iris")
- st.markdown(descripcion del dominio)

[FORMULARIO DE ENTRADA]
- st.number_input() para cada feature con:
    - label descriptivo + unidad (cm)
    - min_value / max_value segun config.FEATURE_RANGES
    - step=0.1, format="%.1f"

[BOTON DE PREDICCION]
- if st.button("Predecir Especie"):
    try:
        iris_input = validators.validate_input(...)
        result = predictor.predict(iris_input, pipeline)
        [RENDER RESULTADO]
    except pydantic.ValidationError as e:
        st.error(mensaje_limpio_sin_traceback)

[RENDER RESULTADO]
- st.success(f"Especie predicha: {result.species}")
- st.metric("Confianza", f"{result.confidence:.1%}")
- if result.low_confidence:
    st.warning("Resultado de baja confianza. Verifique las medidas ingresadas.")
- [GRAFICO DE BARRAS de result.probabilities]
- [BOTON DE FEEDBACK]

[GRAFICO DE BARRAS]
- plotly.express.bar(x=species_names, y=probabilities, ...)
- st.plotly_chart(fig, use_container_width=True)

[BOTON DE FEEDBACK]
- if st.button("Esta prediccion es incorrecta"):
    feedback.log_feedback(iris_input, result)
    st.info("Gracias por tu retroalimentacion. Se ha registrado.")
```

### Manejo de Excepciones en app.py

| Excepcion Capturada | Componente de UI Mostrado |
| :--- | :--- |
| `pydantic.ValidationError` | `st.error()` con el mensaje del campo fallido. Sin traceback. |
| `FileNotFoundError` (modelo no existe) | `st.error("El modelo no esta disponible. Ejecute el pipeline de entrenamiento primero.")` |
| `RuntimeError` (fallo en prediccion) | `st.error("Error interno al realizar la prediccion. Contacte al administrador.")` |

---

## 12. Estandares de Ingenieria

### 12.1 Linting y Formato

| Herramienta | Configuracion | Aplicacion |
| :--- | :--- | :--- |
| `black` | Longitud de linea: 88 caracteres (default) | Obligatorio antes de cada commit en `src/`. |
| `isort` | Profile: black (compatible con black) | Obligatorio. Ordena imports: stdlib -> third-party -> local. |
| PEP 8 | Enforced por black automaticamente | No se admiten violaciones. |

### 12.2 Formato de Logs de Aplicacion

Todo modulo que requiera logging (distinto del feedback de usuario) debe usar el modulo estandar `logging` de Python con el siguiente formato:

```
FORMAT: "%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d | %(message)s"
DATEFMT: "%Y-%m-%dT%H:%M:%SZ"
LEVEL: INFO (produccion), DEBUG (desarrollo)
```

Ejemplo de linea de log:
```
2026-04-19T15:30:00Z | INFO     | predictor:load_pipeline:45 | Pipeline cargado desde models/iris_model.joblib
```

### 12.3 Convencion de Docstrings

Todos los modulos y funciones publicas usan el estilo Google Docstrings:

```python
def funcion(param: tipo) -> tipo_retorno:
    """Resumen de una linea.

    Descripcion extendida opcional.

    Args:
        param: Descripcion del parametro.

    Returns:
        Descripcion del valor de retorno.

    Raises:
        ExcepcionTipo: Condicion bajo la cual se lanza.
    """
```

### 12.4 Puntos de Inyeccion de Dependencias

Para facilitar el testing unitario, las dependencias externas (rutas de archivo, pipelines) se inyectan como parametros con defaults configurados en `config.py`:

- `bronze_loader.load_bronze(csv_path=config.DATA_BRONZE)`: El path puede sobreescribirse en tests.
- `predictor.load_pipeline(model_path=config.MODEL_PATH)`: El path puede apuntar a un modelo fixture en tests.
- `feedback.log_feedback(..., log_path=config.FEEDBACK_LOG)`: En tests, `tmp_path` de pytest se inyecta aqui.

Este patron evita el uso de `unittest.mock.patch` para rutas de archivo y hace los tests mas legibles.

---

## 13. Protocolo de Mock para Desarrollo Paralelo

Los siguientes mocks permiten que el agente de UI (`interactive-dashboard-builder`) trabaje en `app.py` antes de que el pipeline de ML este completo.

### Mock de predictor.py

```python
# tests/mocks/mock_predictor.py
from src.validators import IrisInput
from src.predictor import PredictionResult

def load_pipeline(model_path=None):
    """Mock: retorna None. La UI no debe llamar metodos sobre este objeto directamente."""
    return None

def predict(iris_input: IrisInput, pipeline=None) -> PredictionResult:
    """Mock: retorna siempre 'setosa' con alta confianza."""
    return PredictionResult(
        species="setosa",
        confidence=0.97,
        probabilities={"setosa": 0.97, "versicolor": 0.02, "virginica": 0.01},
        low_confidence=False,
    )
```

### Mock de validators.py

```python
# tests/mocks/mock_validators.py
from src.validators import IrisInput

def validate_input(sepal_length, sepal_width, petal_length, petal_width) -> IrisInput:
    """Mock: acepta cualquier valor sin validar rangos."""
    return IrisInput(
        sepal_length=sepal_length,
        sepal_width=sepal_width,
        petal_length=petal_length,
        petal_width=petal_width,
    )
```

---

## 14. Check de Certificacion SpecDD

| Criterio | Estado | Evidencia |
| :--- | :--- | :--- |
| Cada archivo `.py` en `src/` tiene su interfaz definida antes de ser creado | Aprobado | Secciones 2-11 de este documento. |
| Las definiciones permiten que el agente de QA escriba tests sin ver el codigo interno | Aprobado | Pre/Post condiciones y excepciones documentadas por funcion. Los mocks en seccion 13 permiten desarrollo desacoplado. |
| Se han definido tipos personalizados (Pydantic, TypedDict) para datos complejos | Aprobado | `IrisInput`, `PredictionResult`, `FeedbackRecord`, `TrainingMetrics` definidos en seccion 1. |
| Todas las firmas tienen tipos de retorno y tipos de argumento definidos | Aprobado | Cada firma usa type annotations de Python (float, str, Path, np.ndarray, pd.DataFrame, etc.). |
| Los puntos de inyeccion de dependencias estan documentados | Aprobado | Seccion 12.4 y defaults en cada firma de funcion. |
| El SpecDD es trazable al SAD | Aprobado | SAD v1.0.0 seccion 5 define los mismos modulos. SAD seccion 6.1 define los mismos tipos de datos. |

---

> **Nota de Gobernanza:** Este documento es la fuente de verdad para la implementacion de todos los modulos en `src/`. El agente `ai-developer` (Phase Delivery) y el agente `ai-ml-engineer` (Phase Modeling) deben verificar que cada funcion implementada cumple exactamente con la firma, pre-condiciones, post-condiciones y excepciones documentadas aqui. El `ai-solutions-architect` es el unico agente con autoridad para modificar este documento.
>
> **Trazabilidad:** SpecDD v1.0.0 <- SAD v1.0.0 <- BRD v1.0.0 <- feasibility v1.0.0
