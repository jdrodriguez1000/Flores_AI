# decisions.md: Registro Historico de Decisiones

> **Definicion del Documento**
> Este archivo es la memoria historica del proyecto. NUNCA se sobrescribe.
> Cada entrada se agrega al final con separadores claros.
> El "por que" de cada decision es mas importante que la descripcion tecnica del cambio.
>
> **Creado:** 2026-04-19
> **Responsable:** ai-session-steward

---

## Formato de Entrada

Cada entrada debe contener: Fecha, Fase, ID de Decision, Contexto, Decision, Justificacion, Impacto Transversal y Lecciones Aprendidas.

---

---

## Entrada #1 — Sesion 2026-04-19 | Fase 1 - Discovery

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-19

---

### D-001: Eliminacion de columna `Id` antes del entrenamiento

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | feasibility — Analisis de data leakage                                        |
| **Tipo**                | Decision de preprocesamiento de datos                                                     |

**Contexto:** Durante el analisis de factibilidad del dataset Iris se detecto que la columna `Id` es un identificador secuencial correlacionado con el orden de recoleccion de las muestras. Las filas estan ordenadas por especie (primeras 50: Setosa, siguientes 50: Versicolor, ultimas 50: Virginica), lo que genera una correlacion espuria entre el `Id` y la variable objetivo.

**Decision:** La columna `Id` debe ser eliminada del dataset como paso obligatorio (accion M-01) antes de cualquier operacion de entrenamiento, validacion o inferencia. Esta eliminacion debe implementarse en el pipeline de preprocesamiento Silver.

**Justificacion:** Si el modelo aprende a usar el `Id` como feature, obtendra artificialmente metricas de rendimiento infladas en entrenamiento que no se replicaran en produccion real (donde el `Id` no tiene valor predictivo). Mantener el `Id` constituye data leakage clasico.

**Impacto Transversal:**
- `docs/governance/specdd.md`: La firma del modulo de preprocesamiento debe incluir explicitamente la exclusion de `Id`.
- `docs/governance/CONTRACT.md`: El Contrato de Datos debe prohibir `Id` como feature valida.
- `src/`: El pipeline Silver debe implementar esta eliminacion como paso no negociable.
- `tests/`: Debe existir un test unitario que valide la ausencia de `Id` en el conjunto de features.

---

### D-002: Metricas primarias de exito: Accuracy Global + F1-Score Macro

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | BRD — Definicion de KPIs                                                                  |
| **Tipo**                | Decision de criterio de exito del modelo                                                  |

**Contexto:** El problema requiere clasificar tres especies de flores Iris. El dataset es perfectamente balanceado (50 muestras por clase). Se necesitaban metricas que capturen tanto el rendimiento global como el comportamiento por clase, dado el riesgo conocido de confusion entre Versicolor y Virginica.

**Decision:** Las metricas primarias vinculantes son: Accuracy Global >= 95% y F1-Score Macro >= 0.95. La Latencia de inferencia tiene un umbral de <= 3,000 ms (critico para la experiencia en Streamlit). El F1-Score Macro fue elegido sobre el F1-Score Weighted porque en un dataset balanceado ambos convergen, y el Macro penaliza mas equitativamente los errores en clases individuales.

**Justificacion:** Un modelo que logre Accuracy >= 95% pero falle sistematicamente en distinguir Versicolor de Virginica seria inaceptable. El F1-Score Macro obliga al modelo a rendir bien en las tres clases individualmente, no solo en promedio ponderado. Con 150 muestras balanceadas, el 95% de Accuracy implica un maximo de 7-8 errores en el conjunto de prueba.

**Impacto Transversal:**
- `docs/governance/sad.md`: Los experimentos de benchmarking deben reportar ambas metricas.
- `docs/Fase_3/MODEL_QA.md`: El modelo candidato no puede ser certificado si no supera ambos thresholds.
- `tests/`: Los tests de Model QA deben incluir assertions sobre ambas metricas.

---

### D-003: Stack tecnologico confirmado — Python 3.12+ y Streamlit

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | config.md — Definicion de stack                                                           |
| **Tipo**                | Decision de arquitectura tecnologica                                                      |

**Contexto:** El proyecto requiere un lenguaje de ML y una interfaz web para la demostracion de predicciones. Se evaluaron las opciones disponibles segun el protocolo CLAUDE.md (Python 3.12+ obligatorio) y los requisitos del stakeholder.

**Decision:** El stack tecnologico queda confirmado con Python 3.12+ como lenguaje base y Streamlit como framework de la aplicacion web de prediccion. Las librerias especificas de ML (scikit-learn, pandas, etc.) y serializacion (ONNX/Pickle/Joblib) quedaran definidas en la Fase 2 una vez que el SAD este completo.

**Justificacion:** Python 3.12+ es mandatorio segun CLAUDE.md. Streamlit fue elegido sobre Flask/FastAPI por su velocidad de desarrollo para prototipos de ML con interfaces de prediccion simples, su integracion nativa con pandas y su capacidad de despliegue rapido. Para un problema de clasificacion multi-clase con cuatro inputs numericos, Streamlit provee la interfaz optima sin overhead de desarrollo de frontend.

**Impacto Transversal:**
- `docs/governance/sad.md`: Debe documentar la justificacion arquitectonica de Streamlit.
- `requirements.txt`: Primera dependencia a registrar sera streamlit.
- `infra/`: La containerizacion (Docker) debe basarse en imagen Python 3.12.

---

### D-004: Veredicto de Factibilidad — GO con confianza Alta (9.2/10)

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | feasibility — Veredicto final                                                 |
| **Tipo**                | Decision de habilitacion de fase                                                          |

**Contexto:** El analisis de factibilidad del dataset Iris evaluo: completitud de datos, calidad estadistica, alcanzabilidad de KPIs, riesgos de data leakage y near-duplicates.

**Decision:** Se emite veredicto GO con confianza Alta (9.2/10). El proyecto esta habilitado para continuar hacia la Fase 2 (Data & EDA) una vez que los documentos de arquitectura (SAD, SpecDD, CONTRACT) esten completos. Las acciones M-01 (eliminar `Id`) y la eliminacion de 3 near-duplicates son obligatorias antes del primer entrenamiento.

**Justificacion:** El dataset Iris es uno de los datasets mas estudiados en ML. Su calidad es conocida y sus caracteristicas estadisticas son estables. El unico riesgo real es el data leakage por columna `Id`, que es completamente mitigable. La separabilidad de Setosa es perfecta; la confusion Versicolor/Virginica es el desafio tecnico central del problema y justifica la exigencia del F1-Score Macro como metrica primaria.

**Impacto Transversal:**
- Habilita formalmente el inicio de trabajos en SAD, SpecDD y CONTRACT.
- La eliminacion de `Id` y near-duplicates queda registrada como prerequisito no negociable para Fase 2.

---

### Lecciones Aprendidas — Sesion 2026-04-19

| # | Leccion                                                                                                                                          | Categoria              |
| :- | :----------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------- |
| 1 | El orden correcto de documentacion es: config -> estructura de carpetas -> BRD -> FEASIBILITY -> SAD -> SpecDD. Saltarse pasos genera retrabajo. | Proceso / Metodologia  |
| 2 | El data leakage por columnas de ID es el riesgo mas comun y menos visible en datasets tabulares clasicos. Siempre revisar columnas de identificadores primero. | Calidad de Datos       |
| 3 | Un dataset balanceado no garantiza ausencia de near-duplicates. La inspeccion de duplicados debe hacerse sobre el vector de features, no sobre el ID. | Calidad de Datos       |
| 4 | Documentar la hipotesis de confusion entre clases (Versicolor/Virginica) en el BRD desde el inicio obliga al equipo a disenar el modelo con ese riesgo en mente desde la arquitectura. | Diseño de Modelos      |

---

*Fin de entrada #1.*

---

---

## Entrada #2 — Sesion 2026-04-19 | Fase 1 - Discovery (Cierre de Arquitectura y Diseno)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-19 (segunda sesion)

---

### D-005: Mockup aprobado por el Stakeholder

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | mockup.md — Revision de prototipo con Stakeholder                                         |
| **Tipo**                | Decision de diseno de interfaz de usuario                                                 |

**Contexto:** El agente `ai-ux-designer` produjo un prototipo HTML interactivo de alta fidelidad con cuatro estados de pantalla: estado inicial (formulario con 4 sliders), resultado exitoso (alta confianza), resultado de baja confianza (advertencia prominente) y error de validacion (campos invalidos con mensajes descriptivos). El prototipo fue presentado al Stakeholder en sesion.

**Decision:** El mockup fue aprobado por el Stakeholder sin modificaciones. La UI de Streamlit implementada en `src/app.py` durante la Fase 4 debe seguir fielmente este diseno. Cualquier desviacion requiere un Control de Cambios aprobado por el Stakeholder.

**Justificacion:** Aprobar el mockup antes de comenzar el desarrollo del pipeline de datos y el modelo garantiza que la experiencia de usuario esta definida y congelada desde la Fase 1. Esto evita el retrabajo tipico de proyectos donde la UI se disena al final y obliga a modificar la logica de negocio para adaptarse. El patron "UI First" reduce el riesgo de desalineacion entre expectativa del usuario y producto final.

**Impacto Transversal:**
- `src/app.py`: Debe replicar los cuatro estados del mockup (inicial, exito, baja confianza, error) usando los mismos colores, jerarquia visual y mensajes de texto.
- `docs/governance/specdd.md`: La seccion de `src/app.py` esta condicionada por los estados de pantalla del mockup.
- `tests/`: Los tests de `app.py` deben validar que cada estado de pantalla se dispara con las condiciones correctas (confidence < 0.60 para baja confianza, validacion fallida para error).

---

### D-006: Patron arquitectonico — Monolito Modular con Medallion Architecture

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | SAD v1.0.0 — Seccion 1: Vision General de la Arquitectura                                 |
| **Tipo**                | Decision de arquitectura de sistema                                                       |

**Contexto:** Se evaluaron tres patrones arquitectonicos para el sistema: Monolito Modular, Microservicios y Pipeline Funcional puro. El proyecto tiene un dataset de 150 registros estaticos, un equipo de 1 desarrollador + agentes de IA, y un requisito de latencia de inferencia <= 3,000 ms dominado por el render de Streamlit, no por el modelo.

**Decision:** Se adopta el patron Monolito Modular con separacion de capas de datos Medallion (Bronze / Silver / Gold). La estructura de `src/` queda definida en 5 modulos raiz (`config.py`, `validators.py`, `predictor.py`, `feedback.py`, `app.py`) y 2 sub-paquetes (`src/data/` con 3 modulos, `src/training/` con 2 modulos).

**Justificacion:** Los microservicios generan sobrecarga operativa (networking, serialization, deployment complexity) injustificada para 150 registros. El Monolito Modular provee la separacion de responsabilidades necesaria (cada capa tiene un contrato de interfaz rigido) sin el overhead de microservicios. El patron Medallion (Bronze/Silver/Gold) es el estandar de la industria para pipelines de datos con transformacion progresiva y es directamente auditable. El diseno garantiza que cada capa puede ser extraida a un servicio independiente en el futuro sin reescribir logica de negocio.

**Impacto Transversal:**
- `src/`: La estructura de modulos es mandatoria. No se pueden crear archivos `.py` fuera de la jerarquia definida en el SAD.
- `docs/governance/specdd.md`: Cada modulo de `src/` tiene su seccion de especificacion de interfaz en el SpecDD.
- `tests/`: Los tests se organizan en espejo de la estructura de `src/`: `tests/unit/`, `tests/integration/`, `tests/e2e/`, `tests/model_qa/`.
- `data/`: Las tres subcarpetas `bronze/`, `silver/`, `gold/` corresponden a las capas Medallion definidas en el SAD.

---

### D-007: Serializacion del modelo — Joblib en lugar de Pickle

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | SAD v1.0.0 — ADR-002: Joblib como mecanismo de serializacion                              |
| **Tipo**                | Decision de tecnologia de serializacion                                                   |

**Contexto:** El sistema requiere serializar y deserializar el pipeline de ML (StandardScaler + clasificador) para desacoplar el entrenamiento offline de la inferencia online. Se evaluaron: Pickle (stdlib), Joblib (scikit-learn) y ONNX (formato abierto).

**Decision:** Se adopta Joblib como mecanismo de serializacion. El artefacto se almacena en `models/iris_model.joblib`. Este archivo es el unico punto de acoplamiento entre el pipeline offline (entrenamiento) y el pipeline online (inferencia en Streamlit).

**Justificacion:** Joblib es el mecanismo recomendado oficialmente por scikit-learn para serializar pipelines que contienen arrays NumPy (como los parametros de StandardScaler). Es entre 2x y 10x mas rapido que Pickle para objetos con grandes arrays numericos. ONNX fue descartado por agregar complejidad de conversion sin beneficio observable en un modelo de clasificacion tabular simple. El formato `.joblib` es legible por cualquier entorno Python con scikit-learn instalado, garantizando portabilidad.

**Impacto Transversal:**
- `models/iris_model.joblib`: Unico artefacto de modelo permitido en produccion.
- `src/training/serializer.py`: Responsable exclusivo de serializar y deserializar usando `joblib.dump()` / `joblib.load()`.
- `src/predictor.py`: Carga el modelo via `serializer.load_model()`. No llama a `joblib` directamente.
- `requirements.txt`: `joblib` debe estar listado como dependencia explicita (aunque scikit-learn lo instala transitivamente).
- `tests/`: El test de carga del modelo debe verificar que el archivo `.joblib` existe y que el objeto cargado es una instancia de `sklearn.pipeline.Pipeline`.

---

### D-008: StandardScaler dentro de sklearn.Pipeline (no como paso independiente)

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | SAD v1.0.0 — ADR-003: StandardScaler encapsulado en Pipeline                              |
| **Tipo**                | Decision de prevencion de Data Leakage en el pipeline de ML                               |

**Contexto:** El pipeline de ML requiere normalizacion de features antes del clasificador. Existen dos formas de implementarlo: (a) ajustar el StandardScaler sobre todo el dataset y luego hacer train/test split, o (b) encapsularlo dentro de `sklearn.Pipeline` para que el ajuste ocurra solo sobre el conjunto de entrenamiento.

**Decision:** El StandardScaler se encapsula obligatoriamente dentro de `sklearn.Pipeline` como primer paso. El pipeline completo (scaler + clasificador) es lo que se serializa en `models/iris_model.joblib`. El scaler nunca se ajusta sobre datos de validacion o test.

**Justificacion:** Ajustar el StandardScaler sobre todo el dataset antes del split constituye Data Leakage de preprocesamiento (RT3 del BRD). La informacion estadistica del conjunto de validacion "contamina" el entrenamiento, produciendo metricas optimistas que no se replicaran en produccion. Encapsulando el scaler en `sklearn.Pipeline`, el metodo `.fit()` ajusta el scaler solo sobre los datos de entrenamiento, y `.transform()` en validacion/test usa los parametros aprendidos del entrenamiento. Esta es la unica implementacion que elimina completamente este riesgo.

**Impacto Transversal:**
- `src/training/trainer.py`: Debe construir el pipeline con `sklearn.pipeline.Pipeline([('scaler', StandardScaler()), ('classifier', <modelo>)])`.
- `src/training/serializer.py`: Serializa el objeto `Pipeline` completo, no el clasificador aislado.
- `src/predictor.py`: Llama a `pipeline.predict()` directamente; el scaler se aplica automaticamente en cada prediccion.
- `tests/model_qa/`: Debe incluir un test que verifique que el scaler fue ajustado solo sobre datos de entrenamiento.
- `docs/Fase_3/MODEL_QA.md`: Debe documentar que RT3 (Data Leakage) fue mitigado mediante esta decision arquitectonica.

---

### D-009: pathlib.Path en src/config.py como unico gestor de rutas

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | SAD v1.0.0 — ADR-004: pathlib para gestion de rutas                                       |
| **Tipo**                | Decision de ingenieria de software (portabilidad y mantenibilidad)                        |

**Contexto:** El proyecto debe ejecutarse en Windows, macOS y Linux sin modificaciones de codigo. Las rutas de archivos (dataset CSV, modelo serializado, directorio de logs) deben ser gestionadas de forma centralizada y portable.

**Decision:** Todas las rutas del sistema se definen en `src/config.py` usando `pathlib.Path`. La raiz del proyecto se calcula dinamicamente con `Path(__file__).parent.parent`. Ningun otro modulo de `src/` puede contener strings hardcodeados de rutas. Los modulos que necesitan una ruta importan la constante correspondiente desde `config.py`.

**Justificacion:** `os.path` (alternativa anterior) produce strings que no son portables entre sistemas operativos sin manipulacion manual. `pathlib.Path` maneja automaticamente los separadores de ruta (`/` vs `\`) en todos los sistemas operativos. La centralizacion en `config.py` garantiza que cambiar la ubicacion de cualquier artefacto (e.g., mover el modelo a un bucket S3 en el futuro) requiere modificar un solo archivo. La prohibicion de strings hardcodeados en el resto del codigo es auditabe mediante un grep simple en el repositorio.

**Impacto Transversal:**
- `src/config.py`: Unica fuente de verdad para rutas. Debe exportar constantes como `BRONZE_PATH`, `SILVER_PATH`, `GOLD_PATH`, `MODEL_PATH`.
- Todos los modulos de `src/`: Deben importar rutas desde `config.py`, nunca construirlas localmente.
- `tests/`: Los tests deben usar `config.MODEL_PATH` y similares, nunca rutas literales.
- CLAUDE.md confirma: "Se prohíbe el uso de rutas absolutas" — esta decision es la implementacion tecnica de esa regla.

---

### D-010: Pipeline offline y online completamente desacoplados

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | SAD v1.0.0 — Seccion 1.1: Principio "Decoupling is King"                                  |
| **Tipo**                | Decision de arquitectura de sistema (separacion de responsabilidades)                     |

**Contexto:** El sistema tiene dos flujos de trabajo con ciclos de vida distintos: (a) el pipeline offline de entrenamiento (carga de datos, limpieza, features, train/test split, entrenamiento, serializacion) que se ejecuta una vez o periodicamente, y (b) el pipeline online de inferencia (cargar modelo, recibir input del usuario, predecir, mostrar resultado) que se ejecuta en tiempo real en Streamlit.

**Decision:** Los pipelines offline y online son completamente independientes. `src/app.py` (online) unicamente importa `src/predictor.py` y `src/validators.py`. Nunca importa modulos de `src/data/` ni de `src/training/`. El unico punto de acoplamiento entre ambos pipelines es el artefacto `models/iris_model.joblib`.

**Justificacion:** Acoplar el pipeline de entrenamiento con la aplicacion web produce sistemas fragiles donde un cambio en la logica de datos puede romper la UI, y donde el tiempo de inicio de la aplicacion incluye el tiempo de carga del dataset completo. El desacoplamiento total garantiza que: (1) la app de inferencia es extremadamente liviana, (2) el modelo puede ser reentrenado y actualizado sin tocar el codigo de la UI, (3) los tests de cada pipeline son independientes y mas simples. Este principio es la base para una eventual migracion a microservicios sin reescritura.

**Impacto Transversal:**
- `src/app.py`: Las unicas importaciones de `src/` permitidas son `from src.predictor import predict` y `from src.validators import IrisInput`. Cualquier otra importacion es una violacion arquitectonica.
- `src/training/`: El sub-paquete completo es invisible para la UI. Puede ser removido del contenedor de produccion sin afectar la inferencia.
- `tests/integration/`: Deben verificar que `app.py` no importa modulos de `data/` ni `training/` (test de dependencias).
- `infra/`: El Dockerfile de produccion puede excluir `src/data/` y `src/training/` para reducir la superficie de ataque.

---

### Lecciones Aprendidas — Sesion 2026-04-19 (Segunda sesion)

| # | Leccion                                                                                                                                                                          | Categoria              |
| :- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------- |
| 1 | Producir el Mockup antes del SAD permite que el arquitecto conozca exactamente que estados de la UI necesitan ser soportados por la logica de negocio. Mockup → SAD → SpecDD es el orden correcto. | Proceso / Metodologia  |
| 2 | Encapsular el StandardScaler dentro de `sklearn.Pipeline` no es una buena practica opcional; es la unica forma de garantizar que no hay Data Leakage de preprocesamiento. Debe ser una regla no negociable en cualquier pipeline de ML con normalizacion. | Calidad de Modelos     |
| 3 | El principio "Decoupling is King" debe establecerse en el SAD antes de escribir una sola linea de codigo. Intentar desacoplar pipelines offline/online despues de la implementacion es costoso y propenso a errores. | Arquitectura           |
| 4 | Centralizar las rutas en `config.py` con `pathlib` es una decision que parece menor pero que evita bugs de portabilidad criticos en entornos CI/CD donde las rutas absolutas del desarrollador no existen. | Ingenieria de Software |
| 5 | La aprobacion del Stakeholder del Mockup en sesion, antes de escribir codigo de UI, elimina el riesgo de "esto no era lo que imaginaba" al momento de la demo final. | Gestion de Stakeholders |

---

*Fin de entrada #2.*

---

---

## Entrada #3 — Sesion 2026-04-19 | Fase 1 - Discovery (Cierre Formal y Consolidacion)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-19 (tercera sesion — cierre formal de Fase 1)

---

### D-011: backlog.md como primer entregable automatico del proceso de inicializacion

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | Ajuste #7 a skills `repository-governance` y `project-config`                             |
| **Tipo**                | Decision de proceso / metodologia de inicializacion de proyectos                         |

**Contexto:** Durante la sesion se detecto que el skill `repository-governance` no generaba el `backlog.md` como parte del proceso `initialize_repo`, y que el skill `project-config` no gestionaba el ciclo de vida de ese archivo (marcarlo IN_PROGRESS al iniciar, DONE al finalizar). El `backlog.md` fue el ultimo entregable de Fase 1 en completarse, lo que significo que durante la mayor parte de la fase no existia el documento de orquestacion de tareas.

**Decision:** Se actualizaron ambos skills para que en cualquier proyecto futuro que use esta metodologia, el `backlog.md` sea generado automaticamente por `initialize_repo` como parte de la estructura inicial del repositorio, con las tareas de Fase 1 pre-cargadas. El skill `project-config` ahora verifica la existencia del backlog y gestiona su estado durante el Bootstrap.

**Justificacion:** El backlog es el documento de orquestacion central. Iniciar cualquier fase sin un backlog aprobado significa trabajar sin trazabilidad de tareas, sin Definition of Done verificable y sin capacidad de medir progreso. La decision de crear el backlog al final de Fase 1 (en lugar de al inicio) fue una deuda de proceso que se corrigio retroactivamente. En proyectos futuros, el backlog debe existir desde el dia cero para que todos los agentes operen con visibilidad completa de lo que falta.

**Impacto Transversal:**
- `.claude/skills/repository-governance/SKILL.md`: `initialize_repo` ahora incluye la generacion de `backlog.md` con estructura de Fase 1.
- `.claude/skills/project-config/SKILL.md`: El Bootstrap verifica existencia de `backlog.md` y gestiona el estado de `[F1-T01]`.
- Proyectos futuros: El `backlog.md` sera el primer archivo de gobernanza en existir, antes que el BRD.

---

### D-012: Convencion de nombres canonica para documentos de gobernanza — minusculas sin prefijos

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | Renombrado de `DATA_FEASIBILITY_REPORT.md` a `feasibility.md`                             |
| **Tipo**                | Decision de convencion de nombres / higiene documental                                    |

**Contexto:** El documento de factibilidad fue creado originalmente con el nombre `DATA_FEASIBILITY_REPORT.md` (SCREAMING_SNAKE_CASE con prefijo descriptivo). Este nombre era inconsistente con el resto de los documentos de gobernanza (`brd.md`, `sad.md`, `specdd.md`, `contract.md`, `backlog.md`), todos en minusculas sin prefijos. Ademas, las referencias a este archivo en `contract.md`, `sad.md`, `specdd.md` y `decisions.md` usaban el nombre antiguo, creando inconsistencias internas.

**Decision:** El documento de factibilidad se renombra a `feasibility.md`. La convencion de nombres para todos los documentos de gobernanza queda fijada como: **nombre semantico en minusculas, sin prefijos descriptivos, extension `.md`**. Todas las referencias cruzadas fueron actualizadas para usar el nuevo nombre.

**Justificacion:** La consistencia en los nombres de archivo reduce la carga cognitiva del agente que lee el repositorio y elimina la posibilidad de referencias rotas por divergencia de nombres. El patron minusculas-sin-prefijos es mas robusto en sistemas de archivos case-sensitive (Linux, CI/CD) y es la convencion dominante en la industria para documentacion tecnica en repositorios de software.

**Impacto Transversal:**
- `docs/Fase_1/feasibility.md`: Nombre canonico definitivo. El nombre antiguo no debe usarse en ningun documento nuevo.
- `docs/governance/contract.md`, `sad.md`, `specdd.md`, `backlog.md`: Referencias actualizadas.
- `docs/references/decisions.md`: Referencias anteriores al nombre antiguo ya fueron corregidas en las entradas previas.
- Proyectos futuros: El skill `project-config` debe generar el archivo con el nombre `feasibility.md` desde el inicio.

---

### Lecciones Aprendidas — Sesion 2026-04-19 (Tercera sesion — Cierre Formal)

| # | Leccion                                                                                                                                                                                           | Categoria              |
| :- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------- |
| 1 | El backlog debe crearse al inicio del proyecto, no al final de la primera fase. Sin backlog, los agentes no tienen visibilidad de las tareas pendientes ni pueden verificar el DoD de cada entregable. Esto genero que la Fase 1 se completara sin un registro formal de progreso hasta el ultimo momento. | Proceso / Metodologia  |
| 2 | La convencion de nombres de archivos debe definirse en el primer documento de gobernanza (config.md) y no debe modificarse posteriormente. Un nombre inconsistente como `DATA_FEASIBILITY_REPORT.md` obligo a actualizar referencias en cinco archivos distintos, lo que es trabajo de retrabajo evitable. | Higiene Documental     |
| 3 | Al actualizar el nombre de un archivo referenciado en multiples documentos, la busqueda de referencias cruzadas debe hacerse sistematicamente antes de renombrar. El orden correcto es: (1) identificar todas las referencias, (2) renombrar el archivo, (3) actualizar todas las referencias en una sola pasada. | Proceso de Refactoring |
| 4 | Los skills de los agentes especializados son documentos vivos que deben evolucionar con las lecciones del proyecto. Un skill que no refleja las decisiones tomadas en el proyecto genera inconsistencias en sesiones futuras. Actualizar los skills es tan importante como actualizar el codigo. | Gestion de Agentes     |

---

*Fin de entrada #3. La proxima entrada se agregara al cierre de la primera sesion de Fase 2.*
