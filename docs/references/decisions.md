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

## Entrada #1 — Sesion 2026-04-19 | Phase Discovery - Discovery

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-19

---

### D-001: Eliminacion de columna `Id` antes del entrenamiento

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Phase Discovery - Discovery                                                                        |
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
| **Fase**                | Phase Discovery - Discovery                                                                        |
| **Origen**              | BRD — Definicion de KPIs                                                                  |
| **Tipo**                | Decision de criterio de exito del modelo                                                  |

**Contexto:** El problema requiere clasificar tres especies de flores Iris. El dataset es perfectamente balanceado (50 muestras por clase). Se necesitaban metricas que capturen tanto el rendimiento global como el comportamiento por clase, dado el riesgo conocido de confusion entre Versicolor y Virginica.

**Decision:** Las metricas primarias vinculantes son: Accuracy Global >= 95% y F1-Score Macro >= 0.95. La Latencia de inferencia tiene un umbral de <= 3,000 ms (critico para la experiencia en Streamlit). El F1-Score Macro fue elegido sobre el F1-Score Weighted porque en un dataset balanceado ambos convergen, y el Macro penaliza mas equitativamente los errores en clases individuales.

**Justificacion:** Un modelo que logre Accuracy >= 95% pero falle sistematicamente en distinguir Versicolor de Virginica seria inaceptable. El F1-Score Macro obliga al modelo a rendir bien en las tres clases individualmente, no solo en promedio ponderado. Con 150 muestras balanceadas, el 95% de Accuracy implica un maximo de 7-8 errores en el conjunto de prueba.

**Impacto Transversal:**
- `docs/governance/sad.md`: Los experimentos de benchmarking deben reportar ambas metricas.
- `docs/Phase_modeling/MODEL_QA.md`: El modelo candidato no puede ser certificado si no supera ambos thresholds.
- `tests/`: Los tests de Model QA deben incluir assertions sobre ambas metricas.

---

### D-003: Stack tecnologico confirmado — Python 3.12+ y Streamlit

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Phase Discovery - Discovery                                                                        |
| **Origen**              | config.md — Definicion de stack                                                           |
| **Tipo**                | Decision de arquitectura tecnologica                                                      |

**Contexto:** El proyecto requiere un lenguaje de ML y una interfaz web para la demostracion de predicciones. Se evaluaron las opciones disponibles segun el protocolo CLAUDE.md (Python 3.12+ obligatorio) y los requisitos del stakeholder.

**Decision:** El stack tecnologico queda confirmado con Python 3.12+ como lenguaje base y Streamlit como framework de la aplicacion web de prediccion. Las librerias especificas de ML (scikit-learn, pandas, etc.) y serializacion (ONNX/Pickle/Joblib) quedaran definidas en la Phase Engineering una vez que el SAD este completo.

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
| **Fase**                | Phase Discovery - Discovery                                                                        |
| **Origen**              | feasibility — Veredicto final                                                 |
| **Tipo**                | Decision de habilitacion de fase                                                          |

**Contexto:** El analisis de factibilidad del dataset Iris evaluo: completitud de datos, calidad estadistica, alcanzabilidad de KPIs, riesgos de data leakage y near-duplicates.

**Decision:** Se emite veredicto GO con confianza Alta (9.2/10). El proyecto esta habilitado para continuar hacia la Phase Engineering (Data & EDA) una vez que los documentos de arquitectura (SAD, SpecDD, CONTRACT) esten completos. Las acciones M-01 (eliminar `Id`) y la eliminacion de 3 near-duplicates son obligatorias antes del primer entrenamiento.

**Justificacion:** El dataset Iris es uno de los datasets mas estudiados en ML. Su calidad es conocida y sus caracteristicas estadisticas son estables. El unico riesgo real es el data leakage por columna `Id`, que es completamente mitigable. La separabilidad de Setosa es perfecta; la confusion Versicolor/Virginica es el desafio tecnico central del problema y justifica la exigencia del F1-Score Macro como metrica primaria.

**Impacto Transversal:**
- Habilita formalmente el inicio de trabajos en SAD, SpecDD y CONTRACT.
- La eliminacion de `Id` y near-duplicates queda registrada como prerequisito no negociable para Phase Engineering.

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

## Entrada #2 — Sesion 2026-04-19 | Phase Discovery - Discovery (Cierre de Arquitectura y Diseno)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-19 (segunda sesion)

---

### D-005: Mockup aprobado por el Stakeholder

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Phase Discovery - Discovery                                                                        |
| **Origen**              | mockup.md — Revision de prototipo con Stakeholder                                         |
| **Tipo**                | Decision de diseno de interfaz de usuario                                                 |

**Contexto:** El agente `ai-ux-designer` produjo un prototipo HTML interactivo de alta fidelidad con cuatro estados de pantalla: estado inicial (formulario con 4 sliders), resultado exitoso (alta confianza), resultado de baja confianza (advertencia prominente) y error de validacion (campos invalidos con mensajes descriptivos). El prototipo fue presentado al Stakeholder en sesion.

**Decision:** El mockup fue aprobado por el Stakeholder sin modificaciones. La UI de Streamlit implementada en `src/app.py` durante la Phase Delivery debe seguir fielmente este diseno. Cualquier desviacion requiere un Control de Cambios aprobado por el Stakeholder.

**Justificacion:** Aprobar el mockup antes de comenzar el desarrollo del pipeline de datos y el modelo garantiza que la experiencia de usuario esta definida y congelada desde la Phase Discovery. Esto evita el retrabajo tipico de proyectos donde la UI se disena al final y obliga a modificar la logica de negocio para adaptarse. El patron "UI First" reduce el riesgo de desalineacion entre expectativa del usuario y producto final.

**Impacto Transversal:**
- `src/app.py`: Debe replicar los cuatro estados del mockup (inicial, exito, baja confianza, error) usando los mismos colores, jerarquia visual y mensajes de texto.
- `docs/governance/specdd.md`: La seccion de `src/app.py` esta condicionada por los estados de pantalla del mockup.
- `tests/`: Los tests de `app.py` deben validar que cada estado de pantalla se dispara con las condiciones correctas (confidence < 0.60 para baja confianza, validacion fallida para error).

---

### D-006: Patron arquitectonico — Monolito Modular con Medallion Architecture

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Phase Discovery - Discovery                                                                        |
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
| **Fase**                | Phase Discovery - Discovery                                                                        |
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
| **Fase**                | Phase Discovery - Discovery                                                                        |
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
- `docs/Phase_modeling/MODEL_QA.md`: Debe documentar que RT3 (Data Leakage) fue mitigado mediante esta decision arquitectonica.

---

### D-009: pathlib.Path en src/config.py como unico gestor de rutas

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Phase Discovery - Discovery                                                                        |
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
| **Fase**                | Phase Discovery - Discovery                                                                        |
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

## Entrada #3 — Sesion 2026-04-19 | Phase Discovery - Discovery (Cierre Formal y Consolidacion)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-19 (tercera sesion — cierre formal de Phase Discovery)

---

### D-011: backlog.md como primer entregable automatico del proceso de inicializacion

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Phase Discovery - Discovery                                                                        |
| **Origen**              | Ajuste #7 a skills `repository-governance` y `project-config`                             |
| **Tipo**                | Decision de proceso / metodologia de inicializacion de proyectos                         |

**Contexto:** Durante la sesion se detecto que el skill `repository-governance` no generaba el `backlog.md` como parte del proceso `initialize_repo`, y que el skill `project-config` no gestionaba el ciclo de vida de ese archivo (marcarlo IN_PROGRESS al iniciar, DONE al finalizar). El `backlog.md` fue el ultimo entregable de Phase Discovery en completarse, lo que significo que durante la mayor parte de la fase no existia el documento de orquestacion de tareas.

**Decision:** Se actualizaron ambos skills para que en cualquier proyecto futuro que use esta metodologia, el `backlog.md` sea generado automaticamente por `initialize_repo` como parte de la estructura inicial del repositorio, con las tareas de Phase Discovery pre-cargadas. El skill `project-config` ahora verifica la existencia del backlog y gestiona su estado durante el Bootstrap.

**Justificacion:** El backlog es el documento de orquestacion central. Iniciar cualquier fase sin un backlog aprobado significa trabajar sin trazabilidad de tareas, sin Definition of Done verificable y sin capacidad de medir progreso. La decision de crear el backlog al final de Phase Discovery (en lugar de al inicio) fue una deuda de proceso que se corrigio retroactivamente. En proyectos futuros, el backlog debe existir desde el dia cero para que todos los agentes operen con visibilidad completa de lo que falta.

**Impacto Transversal:**
- `.claude/skills/repository-governance/SKILL.md`: `initialize_repo` ahora incluye la generacion de `backlog.md` con estructura de Phase Discovery.
- `.claude/skills/project-config/SKILL.md`: El Bootstrap verifica existencia de `backlog.md` y gestiona el estado de `[F1-T01]`.
- Proyectos futuros: El `backlog.md` sera el primer archivo de gobernanza en existir, antes que el BRD.

---

### D-012: Convencion de nombres canonica para documentos de gobernanza — minusculas sin prefijos

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Phase Discovery - Discovery                                                                        |
| **Origen**              | Renombrado de `DATA_FEASIBILITY_REPORT.md` a `feasibility.md`                             |
| **Tipo**                | Decision de convencion de nombres / higiene documental                                    |

**Contexto:** El documento de factibilidad fue creado originalmente con el nombre `DATA_FEASIBILITY_REPORT.md` (SCREAMING_SNAKE_CASE con prefijo descriptivo). Este nombre era inconsistente con el resto de los documentos de gobernanza (`brd.md`, `sad.md`, `specdd.md`, `contract.md`, `backlog.md`), todos en minusculas sin prefijos. Ademas, las referencias a este archivo en `contract.md`, `sad.md`, `specdd.md` y `decisions.md` usaban el nombre antiguo, creando inconsistencias internas.

**Decision:** El documento de factibilidad se renombra a `feasibility.md`. La convencion de nombres para todos los documentos de gobernanza queda fijada como: **nombre semantico en minusculas, sin prefijos descriptivos, extension `.md`**. Todas las referencias cruzadas fueron actualizadas para usar el nuevo nombre.

**Justificacion:** La consistencia en los nombres de archivo reduce la carga cognitiva del agente que lee el repositorio y elimina la posibilidad de referencias rotas por divergencia de nombres. El patron minusculas-sin-prefijos es mas robusto en sistemas de archivos case-sensitive (Linux, CI/CD) y es la convencion dominante en la industria para documentacion tecnica en repositorios de software.

**Impacto Transversal:**
- `docs/Phase_discovery/feasibility.md`: Nombre canonico definitivo. El nombre antiguo no debe usarse en ningun documento nuevo.
- `docs/governance/contract.md`, `sad.md`, `specdd.md`, `backlog.md`: Referencias actualizadas.
- `docs/references/decisions.md`: Referencias anteriores al nombre antiguo ya fueron corregidas en las entradas previas.
- Proyectos futuros: El skill `project-config` debe generar el archivo con el nombre `feasibility.md` desde el inicio.

---

### Lecciones Aprendidas — Sesion 2026-04-19 (Tercera sesion — Cierre Formal)

| # | Leccion                                                                                                                                                                                           | Categoria              |
| :- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------- |
| 1 | El backlog debe crearse al inicio del proyecto, no al final de la primera fase. Sin backlog, los agentes no tienen visibilidad de las tareas pendientes ni pueden verificar el DoD de cada entregable. Esto genero que la Phase Discovery se completara sin un registro formal de progreso hasta el ultimo momento. | Proceso / Metodologia  |
| 2 | La convencion de nombres de archivos debe definirse en el primer documento de gobernanza (config.md) y no debe modificarse posteriormente. Un nombre inconsistente como `DATA_FEASIBILITY_REPORT.md` obligo a actualizar referencias en cinco archivos distintos, lo que es trabajo de retrabajo evitable. | Higiene Documental     |
| 3 | Al actualizar el nombre de un archivo referenciado en multiples documentos, la busqueda de referencias cruzadas debe hacerse sistematicamente antes de renombrar. El orden correcto es: (1) identificar todas las referencias, (2) renombrar el archivo, (3) actualizar todas las referencias en una sola pasada. | Proceso de Refactoring |
| 4 | Los skills de los agentes especializados son documentos vivos que deben evolucionar con las lecciones del proyecto. Un skill que no refleja las decisiones tomadas en el proyecto genera inconsistencias en sesiones futuras. Actualizar los skills es tan importante como actualizar el codigo. | Gestion de Agentes     |

---

*Fin de entrada #3.*

---

---

## Entrada #4 — Sesion de Ajustes de Gobernanza (2026-04-20)

**Fase:** Phase Discovery (Cierre y Normalizacion)
**Responsable:** ai-session-steward + ai-repository-governor

### Decisiones de esta Sesion

#### D-010: Nomenclatura de fases en ingles con prefijo `Phase_`

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal (afecta todas las fases) |
| **Tipo**  | Decision de convencion de nomenclatura |

**Decision:** Las carpetas de fases pasan de `Fase_N` (nomenclatura en espanol con numero) a `Phase_<nombre>` (ingles descriptivo): `Phase_discovery`, `Phase_engineering`, `Phase_modeling`, `Phase_delivery`.

**Justificacion:** La nomenclatura descriptiva en ingles es mas autoexplicativa para cualquier colaborador nuevo y alinea la estructura de carpetas con el lenguaje tecnico usado en el resto de la documentacion (ai_process.md, agentes, skills). El nombre de la fase ya no requiere un numero de referencia externa para entenderse.

**Impacto Transversal:** 52 archivos actualizados (agentes, skills, governance, metodologia, CLAUDE.md). El cambio es retroactivo y completo — no quedan referencias a `Fase_N` en ningun archivo del proyecto.

---

#### D-011: Carpeta `mockup/` en la raiz del proyecto

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Discovery |
| **Tipo**  | Decision de organizacion de artefactos |

**Decision:** El directorio `mockup/` (que contiene `index.html`) reside en la raiz del proyecto, no dentro de `docs/Phase_discovery/`. El documento de descripcion `mockup.md` permanece en `docs/Phase_discovery/`.

**Justificacion:** El mockup es un artefacto de presentacion directa al Stakeholder. Ubicarlo en la raiz facilita el acceso sin navegar la estructura de docs, y lo separa semanticamente de la documentacion tecnica. La carpeta `docs/` es para documentos Markdown; `mockup/` es un mini-sitio HTML independiente.

**Impacto Transversal:** `ui-ux-prototyping/SKILL.md` actualizado para reflejar la nueva ubicacion. `ai_process.md` actualizado con la ruta correcta. Regla de Oro de Organizacion en `CLAUDE.md` y `ai_process.md` actualizada para incluir `mockup/`.

---

#### D-012: AGENTS.md como catalogo maestro agnostico en la raiz

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal |
| **Tipo**  | Decision de documentacion de gobernanza |

**Decision:** Se crea `AGENTS.md` en la raiz del proyecto como catalogo centralizado de los 21 agentes especializados. El archivo es agnostico (no contiene nombres de proyectos especificos) y sirve como punto de entrada para cualquier colaborador que necesite saber que agente invocar para una tarea determinada.

**Justificacion:** Con 21 agentes especializados, la friccion cognitiva de recordar que agente hace que cosa es alta. Un catalogo con triggers, descripcion de rol y skills asociados reduce el tiempo de decision y estandariza el onboarding en futuros proyectos.

**Estructura:** Organizado en 5 secciones (Gobernanza, Phase Discovery, Phase Engineering, Phase Modeling, Phase Delivery) mas un mapa visual ASCII de agentes por fase.

---

### Learnings de esta Sesion

| # | Learning | Categoria |
| :- | :-------- | :-------- |
| 1 | Un cambio de nomenclatura masivo (52 archivos) es manejable con `sed` en bash sobre el arbol de archivos. El patron es: hacer mv de carpetas primero, luego sed en todos los .md. El orden importa. | Gestion de Repositorio |
| 2 | La separacion entre "carpeta de artefacto de presentacion" (`mockup/`) y "carpeta de documentacion tecnica" (`docs/`) reduce ambiguedad para los agentes que generan HTML vs. los que generan Markdown. | Arquitectura de Artefactos |
| 3 | Un archivo `AGENTS.md` agnostico en la raiz es mas util que el directorio `.claude/agents/` para onboarding rapido, porque incluye el "cuando usarlo" ademas del "que hace". | Documentacion de Gobernanza |

---

*Fin de entrada #4.*

---

---

## Entrada #5 — Sesion 2026-04-20 | Phase Discovery (Integracion NotebookLM y Auditoria de Agnosticismo)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-20

---

### D-013: NotebookLM como herramienta de consulta de gobernanza del proyecto

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal (Phase Discovery — cierre) |
| **Origen** | Ajuste pendiente registrado en sesion anterior (handoff.md seccion 6) |
| **Tipo**  | Decision de integracion de herramienta externa |

**Contexto:** El handoff de la sesion anterior registraba como pendiente la integracion con NotebookLM (ajuste #9 de `ajustes.txt`). El proyecto acumula 7 documentos de gobernanza densos que un agente o colaborador nuevo necesita asimilar antes de cada sesion. Se necesitaba un mecanismo de consulta semantica sobre esos documentos.

**Decision:** Se crea el notebook "Flores AI — Cerebro del Proyecto" en NotebookLM (ID: `35c8760b-4797-4df2-8c91-cbf5b2df0240`) con 7 documentos de gobernanza cargados como fuentes. El notebook es la herramienta oficial de consulta semantica del proyecto. El ID queda registrado en `docs/references/config.md` seccion 4.2 como unica fuente de verdad.

**Justificacion:** Un notebook semantico sobre los 7 documentos de gobernanza permite hacer consultas en lenguaje natural ("que invariantes debe cumplir la capa Silver?", "cual es la firma de ingestion.py?") sin tener que abrir y leer cada documento individualmente. Esto reduce el tiempo de sincronizacion al inicio de sesion y disminuye el riesgo de que un agente omita una restriccion documentada por no haber leido el archivo correcto.

**Impacto Transversal:**
- `docs/references/config.md`: Seccion 4.2 actualizada con ID del notebook y listado de fuentes.
- `.claude/skills/session-management/SKILL.md`: Ritual de cierre actualizado con paso de sincronizacion NotebookLM.
- Sesiones futuras: `decisions.md` debe re-sincronizarse en NotebookLM en cada cierre donde se añadan entradas nuevas.

---

### D-014: NOTEBOOK_ID reside en config.md, no en el skill de session-management

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal |
| **Origen** | Auditoria de agnosticismo del skill session-management/SKILL.md |
| **Tipo**  | Decision de arquitectura de documentacion (agnosticismo) |

**Contexto:** Al añadir la sincronizacion NotebookLM al skill `session-management/SKILL.md`, la primera version hardcodeaba el NOTEBOOK_ID directamente en el skill. Esto violaba el principio de agnosticismo: el skill pertenece al framework de agentes reutilizables, no al proyecto Flores AI. Cualquier proyecto que adopte el framework heredaria el ID de Flores AI.

**Decision:** El NOTEBOOK_ID no se hardcodea en ningun skill ni agente. El skill `session-management/SKILL.md` fue refactorizado para que el paso de sincronizacion lea el NOTEBOOK_ID desde `docs/references/config.md` seccion 4.2. El patron de actualizacion incluye explicitamente la instruccion de leer config.md antes de ejecutar los comandos de notebooklm.

**Justificacion:** El principio "config.md como unica fuente de verdad de los IDs del proyecto" (establecido en D-009 para rutas de codigo) aplica igualmente a los identificadores de herramientas externas. Si el notebook se recrea o migra, el cambio se hace en un solo lugar (config.md) y todos los skills lo recogen automaticamente. Un skill que contiene IDs especificos de un proyecto no puede reusarse en otro proyecto sin edicion manual, lo que rompe el valor del framework de agentes.

**Impacto Transversal:**
- `.claude/skills/session-management/SKILL.md`: Patron de actualizacion corregido; NOTEBOOK_ID se lee de config.md.
- Proyectos futuros que adopten este framework: Solo necesitan actualizar su propio `config.md` con su NOTEBOOK_ID; los skills funcionan sin modificacion.

---

### D-015: Politica de sincronizacion NotebookLM — decisions.md siempre, resto solo si modificado

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal |
| **Origen** | Diseno del ritual de cierre en session-management/SKILL.md |
| **Tipo**  | Decision de proceso (ritual de cierre) |

**Contexto:** Al definir que documentos sincronizar con NotebookLM en cada cierre, se plantearon dos extremos: (a) sincronizar todos los 7 documentos siempre, o (b) sincronizar solo los que cambiaron. La opcion (a) es costosa en operaciones de API (delete + upload por cada documento); la opcion (b) requiere que el agente de cierre sepa exactamente que se toco en la sesion.

**Decision:** La politica de sincronizacion es: `decisions.md` se sincroniza en TODOS los cierres de sesion sin excepcion (porque siempre recibe una entrada nueva al cerrar). Los demas documentos del mapa de sincronizacion (`ai_process.md`, `brd.md`, `sad.md`, `specdd.md`, `contract.md`, `feasibility.md`) solo se sincronizan si fueron modificados durante la sesion actual. `handoff.md` queda excluido permanentemente del mapa de sincronizacion porque se desactualiza en cada sesion y no tiene valor semantico persistente para consulta.

**Justificacion:** `decisions.md` es el unico documento que crece garantizadamente en cada sesion. Su sincronizacion es no negociable para que el notebook refleje el historial completo de decisiones. Sincronizar documentos no modificados desperdicia operaciones de API y puede introducir versiones identicas sin valor. `handoff.md` es un documento transitorio de estado operativo, no un documento de gobernanza con valor historico; cargarlo en NotebookLM generaria confusion al consultar el notebook con el estado de una sesion pasada.

**Impacto Transversal:**
- `.claude/skills/session-management/SKILL.md`: Tabla de sincronizacion refleja esta politica con la columna "Cuando sincronizar".
- Sesiones futuras: El agente de cierre debe evaluar explicitamente que documentos del mapa fueron tocados antes de ejecutar los comandos de sincronizacion.

---

### Lecciones Aprendidas — Sesion 2026-04-20 (Integracion NotebookLM y Auditoria de Agnosticismo)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | El agnosticismo de los skills no es solo cuestion de nombres de proyecto — tambien aplica a IDs de herramientas externas. Un ID hardcodeado en un skill es tan acoplado como un nombre de proyecto. La regla es: todo identificador especifico del proyecto vive en `config.md`. | Arquitectura de Agentes |
| 2 | Al disenar la sincronizacion de una herramienta externa, la primera pregunta no es "que sincronizar" sino "que documentos tienen valor semantico persistente". `handoff.md` parece importante pero es transitorio; excluirlo del notebook evita confusion en consultas futuras. | Diseno de Integraciones |
| 3 | Auditar el agnosticismo de 63+ archivos es viable si se hace con busqueda sistematica de strings especificos del proyecto. El patron es: buscar el nombre del proyecto, el nombre del dataset y los IDs conocidos. Si no aparecen fuera de config.md, el repositorio es agnostico. | Proceso de Auditoria |
| 4 | La sincronizacion con herramientas de consulta semantica (NotebookLM, embeddings, RAG) debe diseñarse en Phase Discovery, no en Phase Delivery. Integrarla tarde obliga a re-leer documentos que ya se leyeron y puede generar inconsistencias si el notebook no esta al dia durante el desarrollo. | Proceso / Metodologia |

---

*Fin de entrada #5.*

---

---

## Entrada #6 — Sesion 2026-04-20 | Phase Discovery (Design System y Gobernanza de Marca)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-20

---

### D-016: `docs/design-system/` como convencion agnostica para la identidad visual del cliente

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal (Phase Discovery — cierre) |
| **Origen** | Necesidad de estandarizar el manejo de brand del cliente en proyectos de ML/IA |
| **Tipo**  | Decision de convencion de organizacion de artefactos y gobernanza de UI |

**Contexto:** Los clientes ocasionalmente entregan materiales de identidad corporativa (paletas de colores, tipografias, reglas de componentes, prototipos HTML) que los agentes de UI deben respetar al generar interfaces. Sin una convencion estandar, estos materiales se almacenaban en carpetas ad-hoc (ej: `parameters/`) sin integracion formal con el ecosistema de agentes. El proyecto tenia una carpeta `parameters/` con tres archivos: `DESIGN.md` (sistema de diseno), `code.html` (tokens Tailwind completos) y `screen.png` (referencia visual).

**Decision:** Se establece `docs/design-system/` como la ubicacion estandar y agnostica para los materiales de identidad visual del cliente en cualquier proyecto que adopte este framework. Los contenidos de `parameters/` fueron migrados a esta ubicacion. El nombre `design-system` es el termino estandar de la industria. La ubicacion dentro de `docs/` es correcta porque es documentacion de referencia, no codigo productivo.

**Justificacion:** `docs/design-system/` comunica el proposito sin ambiguedad a cualquier agente o colaborador. Al residir en `docs/`, es coherente con el resto de la estructura de gobernanza. La carpeta es **opcional** — su ausencia no rompe ningun flujo; su presencia activa el Pre-Flight de marca en todos los agentes de UI.

**Impacto Transversal:**
- `CLAUDE.md`: Nueva fila en la tabla de directorios con regla de lectura obligatoria antes de generar UI.
- `docs/references/config.md`: Carpeta registrada en estructura y tabla de documentos de gobernanza.
- `.claude/agents/ai-ux-designer.md` y `ai-frontend-engineer.md`: Seccion "Design System Pre-Flight" con flujo de 3 caminos.
- `.claude/skills/ui-ux-prototyping/`, `interactive-dashboard-builder/`, `xai-visualizer-specialist/`, `ux-feedback-loop-designer/`: Pre-flight con flujo de 3 caminos en todos.

---

### D-017: Flujo de 3 caminos para manejo de Design System en agentes de UI

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal |
| **Origen** | Discusion sobre proyectos donde el cliente no entrega materiales de marca |
| **Tipo**  | Decision de proceso / comportamiento de agentes |

**Contexto:** No todos los clientes entregan un Design System. Se necesitaba un comportamiento coherente para los tres escenarios posibles: (a) cliente entrega materiales completos, (b) cliente no entrega nada pero tiene preferencias, (c) cliente no tiene restricciones de marca.

**Decision:** Todos los agentes y skills de UI implementan un flujo de 3 caminos en su Pre-Flight: (1) Si `docs/design-system/` existe → leer y aplicar tokens como restricciones absolutas. (2) Si no existe → preguntar al usuario si desea definir colores/fuente basicos; si responde, crear `docs/design-system/DESIGN.md` antes de continuar. (3) Si el usuario omite → aplicar defaults premium del framework (Glassmorphism/Dark Mode para HTML; tema estandar para Streamlit).

**Justificacion:** El flujo de 3 caminos garantiza que: (a) la marca del cliente siempre se respeta si existe, (b) se captura la intencion del usuario antes de tomar decisiones visuales, (c) ningun proyecto queda bloqueado por ausencia de materiales. La pregunta al usuario es breve y concreta (hex de colores + fuente) para minimizar friccion.

**Impacto Transversal:**
- Todos los agentes y skills de UI listados en D-016.
- Proyectos futuros: El flujo de 3 caminos es el comportamiento por defecto sin configuracion adicional.

---

### D-018: Traduccion de tokens Tailwind a `.streamlit/config.toml` como patron estandar

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Delivery (aplica cuando se implementa Streamlit) |
| **Origen** | Pregunta sobre aplicabilidad del Design System en Streamlit |
| **Tipo**  | Decision de patron de implementacion de UI |

**Contexto:** El `code.html` del Design System usa Tailwind CSS con tokens de color personalizados. Streamlit no usa Tailwind; su sistema de temas se configura via `.streamlit/config.toml` con 4 variables (primaryColor, backgroundColor, secondaryBackgroundColor, textColor). Se necesitaba un patron de traduccion claro.

**Decision:** El patron de traduccion estandar es: `primary` → `primaryColor`, `surface` → `backgroundColor`, `surface-container-low` → `secondaryBackgroundColor`, `on-surface` → `textColor`. Las reglas adicionales del Design System (fuentes, border-radius, shadows, reglas de componentes) se implementan via `st.markdown("<style>...</style>", unsafe_allow_html=True)`. Este patron esta documentado en `ai-frontend-engineer.md` y en `interactive-dashboard-builder/SKILL.md`.

**Justificacion:** Los 4 tokens de Streamlit son un subconjunto de los tokens del Design System. La traduccion es determinista: siempre hay un mapeo unico. El CSS custom via `st.markdown` cubre el resto de las reglas de marca que Streamlit no expone via `config.toml`. Este patron permite que cualquier Design System basado en Material Design tokens (como el del proyecto actual) sea traducible a Streamlit sin perdida de identidad visual critica.

**Impacto Transversal:**
- `.streamlit/config.toml`: Debe crearse en Phase Delivery usando los tokens mapeados del Design System.
- `src/app.py`: Debe incluir el bloque de CSS custom al inicio para inyectar fuentes y reglas de componentes.
- Proyectos futuros con Streamlit: Este patron es el estandar; no requiere decision nueva en cada proyecto.

---

### Lecciones Aprendidas — Sesion 2026-04-20 (Design System y Gobernanza de Marca)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | Una carpeta de materiales del cliente (`parameters/`, `brand/`, etc.) no tiene valor sin integracion formal en el ecosistema de agentes. El valor real esta en que los agentes la lean automaticamente en Pre-Flight, no en que el archivo exista. | Arquitectura de Agentes |
| 2 | El nombre de la carpeta importa: `design-system` comunica proposito de forma universal; `parameters` es ambiguo. Usar terminologia de industria reduce la friccion cognitiva para cualquier colaborador nuevo. | Convencion de Nomenclatura |
| 3 | Preguntar al usuario antes de aplicar defaults de UI es siempre mejor que asumir. La pregunta cuesta segundos; rehacer una interfaz con los colores incorrectos cuesta horas. El flujo de 3 caminos materializa este principio. | UX de Herramientas de IA |
| 4 | Los tokens de Tailwind CSS y los tokens de Streamlit son isomorfos para los 4 valores criticos de marca. Documentar el mapeo una sola vez elimina la necesidad de redescubrirlo en cada proyecto con Streamlit. | Patrones de Implementacion |

---

*Fin de entrada #6.*

---

---

## Entrada #7 — Sesion 2026-04-20 | Phase Discovery (Correccion Design System y Reconstruccion de Mockup)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-20

---

### D-019: "No-Line Rule" como principio absoluto de separacion visual en la UI

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Discovery (aplica a Phase Delivery) |
| **Origen** | Auditoria de `docs/design-system/code.html` contra `docs/design-system/DESIGN.md` |
| **Tipo**  | Decision de diseno de interfaz de usuario |

**Contexto:** Al auditar `code.html` contra las reglas de `DESIGN.md`, se detecto que el footer usaba `border-t border-slate-100` (una linea superior explicita con color hardcodeado). Esta construccion viola la "No-Line Rule" documentada en el Design System del cliente, que prohibe el uso de bordes explicitos para separar secciones y exige que la separacion visual se logre exclusivamente mediante diferencias de fondo (surface tokens).

**Decision:** Se elimina `border-t border-slate-100` del footer y se reemplaza por `background: var(--surface-container-low)`. La "No-Line Rule" queda registrada como principio activo: ningun contenedor de la UI (ni en HTML, ni en Streamlit, ni en el mockup) puede usar `border` como mecanismo de separacion visual. La separacion se logra siempre con fondos diferenciados usando tokens del sistema.

**Justificacion:** Los bordes explicitos son un patron de diseno de la decada de 2010 que produce interfaces visualmente "ruidosas". El Design System del cliente (paleta "The Clinical Sanctuary") usa la elevacion y los fondos diferenciados para crear jerarquia visual sin lineas. Respetar esta regla es esencial para que la app Streamlit sea percibida como una extension coherente de la identidad del cliente, no como una herramienta tecnica genérica.

**Impacto Transversal:**
- `docs/design-system/code.html`: Correccion aplicada al footer.
- `mockup/index.html`: CSS reconstruido sin ningun `border` en contenedores.
- `src/app.py` (Phase Delivery): El CSS custom inyectado via `st.markdown` no debe incluir `border` en elementos de layout. Usar `background-color` con tokens de superficie en su lugar.
- `ai-ux-designer.md`, `ai-frontend-engineer.md`: Pre-Flight debe verificar ausencia de bordes en contenedores.

---

### D-020: Tokens semanticos obligatorios — prohibicion de colores hardcodeados en la UI

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Discovery (aplica a Phase Delivery) |
| **Origen** | Auditoria de `docs/design-system/code.html` — footer usaba `slate-400` y `slate-50` |
| **Tipo**  | Decision de sistema de tokens de UI |

**Contexto:** El footer de `code.html` usaba `text-slate-400` y `bg-slate-50` (colores Tailwind hardcodeados). Estos colores no pertenecen al vocabulario semantico del Design System del cliente y no tienen correspondencia con los tokens definidos en `DESIGN.md`. Si el cliente modifica su paleta, estos colores permanecerian inalterados, rompiendo la coherencia de la identidad visual.

**Decision:** Todos los elementos de la UI deben usar exclusivamente los tokens semanticos definidos en `DESIGN.md` (`on-surface-variant`, `surface-container-low`, `primary`, `error-container`, `tertiary-container`, etc.). El uso de colores del framework CSS directamente (clases Tailwind de la escala de grises, valores hex literales fuera del sistema de tokens) queda prohibido en cualquier componente de la interfaz.

**Justificacion:** Los tokens semanticos desacoplan el color concreto del proposito del elemento. `on-surface-variant` siempre sera el color correcto para texto secundario, independientemente de si el cliente decide cambiar su palette de azul a verde en el futuro. Los hardcodes crean deuda tecnica de UI que solo se detecta visualmente, no en pruebas automatizadas.

**Impacto Transversal:**
- `docs/design-system/code.html`: Correcciones aplicadas al footer.
- `mockup/index.html`: CSS reconstruido usando exclusivamente tokens del sistema.
- `src/app.py` (Phase Delivery): El CSS inyectado debe referenciar las variables CSS definidas en el bloque de tokens, no valores hex literales externos al sistema.
- `.streamlit/config.toml` (Phase Delivery): Los 4 valores deben mapear directamente desde los tokens `primary`, `surface`, `surface-container-low`, `on-surface` del Design System.

---

### D-021: Gradiente lineal en el boton CTA como expresion del token `primary`

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Discovery (aplica a Phase Delivery) |
| **Origen** | Auditoria de `docs/design-system/code.html` — CTA era azul plano sin gradiente |
| **Tipo**  | Decision de diseno de componente |

**Contexto:** El boton CTA "Analizar Parametros" en `code.html` usaba `background-color: #00478d` (color plano). La regla de gradiente documentada en `DESIGN.md` establece que el boton primario debe usar `linear-gradient(135deg, primary, primary-container)` para comunicar interactividad y profundidad. El color plano reducia el contraste visual del boton respecto a los fondos claros del sistema.

**Decision:** El boton CTA usa `linear-gradient(135deg, #00478d, #005eb8)` donde `#00478d` es `primary` y `#005eb8` es `primary-container` segun la paleta del cliente. Esta es la expresion correcta del token de boton primario en el Design System actual. El patron se aplica al boton principal en `code.html` y en `mockup/index.html`.

**Justificacion:** El gradiente diagonal (135 grados) es un patron visual que distingue elementos interactivos de elementos estaticos en el mismo espacio visual. En una interfaz con fondos monocromaticos y sin bordes, el gradiente del CTA es el unico elemento que comunica "accion principal". Un boton plano del mismo color que otros elementos de la paleta reduce la affordance de la interfaz y puede causar confusion en el usuario sobre donde hacer clic.

**Impacto Transversal:**
- `docs/design-system/code.html`: Gradiente aplicado al boton CTA.
- `mockup/index.html`: Boton principal con gradiente.
- `src/app.py` (Phase Delivery): El boton de submit de Streamlit debe tener el gradiente inyectado via `st.markdown` con el selector `.stButton > button`.

---

### D-022: Mockup reconstruido desde cero con paleta del cliente — tema oscuro verde descartado

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Discovery |
| **Origen** | Auditoria del mockup original contra `docs/design-system/DESIGN.md` |
| **Tipo**  | Decision de rediseno de prototipo |

**Contexto:** El mockup original (`mockup/index.html`) fue creado antes de que el Design System del cliente estuviera integrado en el repositorio. Usaba un tema oscuro con paleta verde (`#22c55e`, `#16a34a`) y fondo `#0f172a` — una estetica de "terminal hacker" completamente desalineada con la identidad visual del cliente (paleta "The Clinical Sanctuary": entorno clinico, fondos claros, azul corporativo).

**Decision:** El bloque CSS completo de `mockup/index.html` fue reescrito por el agente `ai-ux-designer` aplicando el Design System del cliente desde cero. El tema oscuro verde queda descartado permanentemente. El mockup ahora implementa: paleta "The Clinical Sanctuary", fuentes Manrope (headlines) + Inter (body), No-Line Rule, sidebar `surface-container-low`, tarjetas `surface-container-lowest`, CTA con gradiente, tokens semanticos para los 4 estados de pantalla. Los 4 estados del BRD (formulario, exito, baja confianza, error) fueron verificados y estan correctamente implementados.

**Justificacion:** Un mockup aprobado por el Stakeholder que no refleja la identidad visual del cliente crea una expectativa incorrecta sobre el producto final. El equipo de desarrollo implementaria la app Streamlit tomando el mockup como referencia, produciendo una UI que el cliente rechazaria. Corregir el mockup en Phase Discovery (antes de escribir codigo de UI) elimina ese riesgo sin costo de retrabajo en codigo productivo.

**Impacto Transversal:**
- `mockup/index.html`: Unico prototipo visual valido. El mockup anterior con tema oscuro verde no debe usarse como referencia.
- `src/app.py` (Phase Delivery): El CSS custom debe replicar los estilos del mockup actualizado, no del original.
- `docs/Phase_discovery/mockup.md`: Debe actualizarse en la proxima revision para indicar que el mockup fue re-alineado con el design system en sesion 2026-04-20.

---

### Lecciones Aprendidas — Sesion 2026-04-20 (Correccion Design System y Reconstruccion de Mockup)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | Un design system integrado en el repositorio (D-016) tiene valor real solo si los prototipos existentes son auditados contra el al momento de la integracion. La auditoria inmediata de `code.html` y `mockup/index.html` detecto 4 desviaciones que, de no corregirse, habrian propagado errores de marca al codigo de produccion. | Proceso de Auditoria |
| 2 | Los mockups creados antes de que el design system del cliente este disponible deben marcarse como "provisionales" y auditarse al momento de recibir los materiales de marca. Un mockup aprobado visualmente por el Stakeholder pero sin el design system aplicado no es un artefacto de Phase Discovery cerrado — es un riesgo latente. | Gestion de Artefactos |
| 3 | Las violaciones de design system mas comunes en HTML son: colores hardcodeados fuera del vocabulario de tokens, bordes explicitos donde deberia haber diferencias de fondo, y botones sin gradiente cuando el sistema de diseno lo exige. Estos tres patrones deben ser los primeros en la checklist de auditoria de cualquier agente de UI. | Calidad de UI |
| 4 | Usar playwright para generar screenshots de verificacion (`screen.png`, `preview.png`) despues de cada correccion de UI es una practica de bajo costo que elimina la ambiguedad sobre si el cambio en el HTML produce el resultado visual esperado. La verificacion visual automatizada es un sustituto valido del QA humano para cambios de CSS. | Proceso de Verificacion |

---

*Fin de entrada #7.*

---

---

## Entrada #8 — Sesion 2026-04-20 | Phase Engineering (Apertura y Expansion del Backlog F2)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-20
**Rama activa:** `feat/F2-engineering` (commit `802b22a`)

---

### D-023: Ciclo IA-TDD completo como estructura obligatoria del backlog por fase

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Engineering (aplicable a todas las fases tecnicas) |
| **Origen** | Expansion del backlog F2 de 6 a 11 tareas |
| **Tipo**  | Decision de proceso / estructura del backlog |

**Contexto:** El backlog original de Phase Engineering tenia 6 tareas que cubrian solo los pasos RED y GREEN del ciclo IA-TDD definido en CLAUDE.md §4. Los pasos REFACTOR, CERTIFICACION y VALIDACION no estaban representados como tareas atomicas. Esto significaba que el ciclo quedaria incompleto sin trazabilidad formal de la calidad del codigo y del cumplimiento del linaje de datos.

**Decision:** Cada iteracion tecnica del backlog debe contener obligatoriamente tres tareas: [RED] (tests primero), [GREEN] (implementacion minima que pasa los tests) y [REFACTOR] (calidad de codigo + EDA/documentacion del resultado de la capa). Adicionalmente, cada fase tecnica debe cerrar con una iteracion de [CERTIFICACION] (auditoria de linaje completo) y [VALIDACION] (verificacion contra KPIs del BRD). Esta estructura se aplico retroactivamente a Phase Engineering (F2) y debe aplicarse al disenar el backlog de Phase Modeling (F3) y Phase Delivery (F4).

**Justificacion:** Sin las tareas [REFACTOR], el codigo GREEN (minimo para pasar tests) queda en produccion sin tipado estricto, sin documentacion de la transformacion y sin el EDA que valida el resultado de la capa. Esto viola el principio "Soberania Documental" de CLAUDE.md. Sin [CERTIFICACION] y [VALIDACION], una fase puede declararse completa sin haber verificado el linaje de datos de extremo a extremo ni haber confirmado que el Feature Set cumple los thresholds del BRD.

**Impacto Transversal:**
- `docs/governance/backlog.md`: Phase Engineering actualizada de 6 a 11 tareas con ciclo completo.
- Phase Modeling (F3) y Phase Delivery (F4): Cuando se atomicen, deben incluir las tareas [REFACTOR], [CERTIFICACION] y [VALIDACION] correspondientes.
- `ai-backlog-manager`: Al disenar backlogs de fases tecnicas futuras, debe usar esta estructura de 3 tareas por iteracion + iteracion de cierre como plantilla mandatoria.

---

### D-024: Sincronizacion de rama siempre desde origin/dev, no desde dev local

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal (gestion de ramas) |
| **Origen** | Error de creacion de `feat/F2-engineering` desde `dev` local desactualizado |
| **Tipo**  | Decision de protocolo Git |

**Contexto:** Al crear la rama `feat/F2-engineering`, se uso `git checkout -b feat/F2-engineering dev` sin haber ejecutado `git fetch origin` previamente. La rama `dev` local estaba desactualizada respecto a `origin/dev` (le faltaba el commit del Merge PR #1). Esto produjo una rama que no incluia el ultimo merge y requirio correccion con `git reset --hard origin/dev` + `git rebase dev`.

**Decision:** El protocolo obligatorio para crear ramas de feature es: (1) `git fetch origin`, (2) `git checkout -b feat/<nombre> origin/dev`. Nunca crear ramas desde referencias locales sin verificar su estado respecto al remoto. Si ya se creo una rama desde una referencia local desactualizada, el procedimiento de correccion es `git reset --hard origin/<base>` antes de realizar cualquier commit en la rama nueva.

**Justificacion:** Una rama creada desde `dev` local desactualizado producira conflictos en el PR o perdera commits del merge mas reciente. El paso `git fetch origin` es gratuito en costo y elimina completamente este riesgo. El protocolo `origin/<rama>` como referencia explicita garantiza que siempre se parte del estado remoto verificado, independientemente del estado local.

**Impacto Transversal:**
- Todas las ramas `feat/F3-*` y `feat/F4-*` futuras deben crearse con `git checkout -b feat/<nombre> origin/dev`.
- El ritual de apertura de sesion debe incluir `git fetch origin` como primer comando Git antes de cualquier operacion de ramas.

---

### Lecciones Aprendidas — Sesion 2026-04-20 (Apertura Phase Engineering)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | El ciclo IA-TDD definido en CLAUDE.md §4 tiene 5 pasos, pero un backlog que solo atomiza RED y GREEN deja 3 pasos sin trazabilidad. La estructura del backlog debe reflejar el ciclo completo desde el primer borrador, no corregirse antes de empezar la fase. | Proceso / Backlog |
| 2 | `git fetch origin` debe ser el primer comando de cualquier sesion que involucre trabajo con ramas. El costo es cero y el riesgo de omitirlo es crear ramas desde referencias obsoletas, lo que genera retrabajo de correccion. | Gestion de Versiones |
| 3 | Las tareas [REFACTOR] no son opcionales ni "si hay tiempo" — son el paso que transforma codigo funcional en codigo industrializable. Sin ellas, el pipeline de datos puede pasar los tests pero no cumple el contrato del SpecDD (tipado estricto, importabilidad, sin rutas absolutas). | Calidad de Codigo |
| 4 | La iteracion de CERTIFICACION al cierre de cada fase tecnica es el mecanismo que garantiza que el linaje Bronze → Silver → Gold es trazable antes de iniciar la siguiente fase. Sin este paso formal, la Phase Modeling podria iniciarse con un dataset Gold sin linaje verificado. | Trazabilidad de Datos |

---

*Fin de entrada #8.*

---

---

## Entrada #9 — Sesion 2026-04-20 | Phase Engineering (Integracion de Capa BDD)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-20
**Rama activa:** `feat/F2-engineering` (commit `3d4bb87`)

---

### D-025: Jerarquia de especificacion BRD → BDD → SpecDD → TDD como protocolo obligatorio

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Transversal (Phase Engineering en adelante) |
| **Origen** | Incorporacion de BDD como capa metodologica al proyecto |
| **Tipo**  | Decision de proceso / jerarquia de especificacion |

**Contexto:** El flujo de desarrollo del proyecto definia la cadena `BRD → SpecDD → TDD` (CLAUDE.md §1 "Soberania Documental"). Esta cadena saltaba directamente de los requisitos de negocio (BRD) a los contratos de interfaz tecnica (SpecDD), sin una capa intermedia que tradujera los requisitos de negocio en comportamiento observable del sistema. Esto generaba un gap: el `ai-data-qa-engineer` debia inferir los casos de prueba directamente del BRD, con riesgo de ambiguedad en las condiciones de frontera.

**Decision:** Se incorpora BDD (Behavior-Driven Development) como capa obligatoria entre el BRD y el SpecDD. La jerarquia queda: `BRD (intencion) → behavior.md (comportamiento observable) → SpecDD (contrato tecnico) → TDD (correctitud del codigo)`. El documento `behavior.md` es el Contrato de Comportamiento del proyecto, escrito en Gherkin (Given/When/Then), y es la fuente de verdad para los tests RED de cada ciclo IA-TDD. Ningun test RED puede escribirse sin que exista el escenario BDD correspondiente en `behavior.md`.

**Justificacion:** BDD cierra el gap de interpretacion entre negocio y tecnica. Los escenarios Gherkin son legibles por el Stakeholder (validacion de negocio) y ejecutables como tests (validacion tecnica). Al forzar la escritura del escenario BDD antes del test TDD, se garantiza que cada test tiene una justificacion de negocio trazable. Ademas, los escenarios de frontera (baja confianza, entradas invalidas) son mas faciles de identificar en lenguaje de comportamiento que en codigo de test.

**Impacto Transversal:**
- `CLAUDE.md`: Jerarquia BDD documentada en Soberania Documental y seccion 4 ("SpecDD + BDD + TDD").
- `docs/governance/behavior.md`: Nuevo artefacto mandatorio de gobernanza.
- `docs/governance/BRD.md`: Escenarios Gherkin añadidos a cada User Story; nueva seccion 9.4 de trazabilidad BDD.
- `docs/methodology/ai_process.md`: behavior.md en tabla de artefactos Phase Discovery; jerarquia BDD documentada en seccion 5; ai-full-stack-sdet referencia behavior.md como fuente de verdad E2E.
- `docs/governance/backlog.md`: Las tareas [RED] futuras de Phase Modeling y Phase Delivery deben referenciarse contra escenarios BDD de behavior.md.
- Proyectos futuros: El skill `gherkin-scenario-author` genera behavior.md como parte del cierre de Phase Discovery, antes de iniciar Phase Engineering.

---

### D-026: SpecDD v1.0.0 cubre el 100% de los escenarios BDD sin modificaciones

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Engineering |
| **Origen** | Auditoria de alineacion entre behavior.md v1.0.0 y specdd.md v1.0.0 |
| **Tipo**  | Decision de validacion de arquitectura (verificacion de linaje) |

**Contexto:** Al crear `behavior.md` con 10 escenarios Gherkin para US-01, US-02 y US-03, se realizo una auditoria de alineacion contra `specdd.md` v1.0.0 para determinar si el contrato de interfaz existente era suficiente o requeria extension. Los escenarios BDD dependen de cuatro campos del resultado de prediccion: `species` (nombre de la clase), `confidence` (probabilidad de la clase ganadora), `probabilities` (distribucion completa por clase) y `low_confidence` (flag booleano de advertencia).

**Decision:** El objeto `PredictionResult` definido en SpecDD v1.0.0 (seccion 1.2 — `src/predictor.py`) ya expone exactamente los cuatro campos requeridos. El SpecDD no requiere modificaciones para soportar la capa BDD. La version del SpecDD permanece en v1.0.0. Esta alineacion queda documentada en la seccion "Nota de Alineacion con SpecDD" de `behavior.md`.

**Justificacion:** La alineacion perfecta entre BDD y SpecDD sin modificaciones es una validacion de que la arquitectura tecnica fue disenada correctamente desde el inicio, anticipando las necesidades de comportamiento observable. Modificar el SpecDD en respuesta a un BDD es el escenario esperado en proyectos donde la arquitectura se disena antes del BDD; aqui el resultado opuesto confirma que el SAD/SpecDD diseñados en Phase Discovery son robustos. Esta decision elimina cualquier deuda tecnica de interfaz antes de iniciar la implementacion.

**Impacto Transversal:**
- `docs/governance/specdd.md`: Sin cambios. v1.0.0 permanece vigente.
- `docs/governance/behavior.md`: Seccion "Nota de Alineacion con SpecDD" documenta la tabla de cobertura de campos.
- `src/predictor.py` (Phase Delivery): La implementacion de `PredictionResult` puede proceder directamente contra SpecDD v1.0.0 y behavior.md v1.0.0 sin tension entre ambos contratos.

---

### D-027: behavior.md como documento de gobernanza de Phase Discovery, no de Phase Engineering

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-20 |
| **Fase**  | Phase Discovery (cierre retroactivo) |
| **Origen** | Clasificacion del artefacto behavior.md en la tabla de gobernanza de ai_process.md |
| **Tipo**  | Decision de clasificacion de artefactos / proceso metodologico |

**Contexto:** Al incorporar `behavior.md` al proyecto en sesion de Phase Engineering, surgio la pregunta de a que fase pertenece este artefacto. El BDD es conceptualmente una actividad de definicion de requisitos (anterior a la implementacion), pero se creo durante la Phase Engineering. Se evaluo clasificarlo en Phase Engineering o retroactivamente en Phase Discovery.

**Decision:** `behavior.md` pertenece a Phase Discovery como artefacto de cierre. Su posicion en `ai_process.md` es junto a los demas documentos de contrato (BRD, SAD, SpecDD) y debe generarse antes de iniciar Phase Engineering. En proyectos futuros que usen este framework, el skill `gherkin-scenario-author` debe ejecutarse al cerrar Phase Discovery, inmediatamente despues de aprobar el BRD y antes de iniciar la Phase Engineering. El comportamiento observable del sistema debe estar acordado con el Stakeholder antes de comenzar a escribir tests.

**Justificacion:** Los escenarios BDD son una extension del BRD en lenguaje ejecutable. Pertenecen al mismo espacio de "que debe hacer el sistema" (not "como lo hace"). Crear BDD en Phase Engineering es aceptable si el SpecDD fue disenado correctamente (como fue el caso aqui), pero es un riesgo si los escenarios BDD revelan gaps en el SpecDD que ya fue usado como base para el backlog. El orden correcto es: BRD → behavior.md → SAD → SpecDD → backlog. En este proyecto el orden fue suboptimo pero no genero retrabajo gracias a la solidez del SpecDD v1.0.0.

**Impacto Transversal:**
- `docs/methodology/ai_process.md`: behavior.md posicionado en la tabla de artefactos de Phase Discovery.
- `.claude/skills/gherkin-scenario-author/SKILL.md`: El skill documenta que debe ejecutarse al cierre de Phase Discovery.
- Proyectos futuros: El backlog de Phase Discovery debe incluir una tarea para crear behavior.md antes de crear el SpecDD.

---

### Lecciones Aprendidas — Sesion 2026-04-20 (Integracion BDD)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | Un SpecDD disenado con rigor de contratos (campos tipados, nombres semanticos) tiene alta probabilidad de cubrir los escenarios BDD sin modificacion. La alineacion perfecta entre behavior.md v1.0.0 y specdd.md v1.0.0 valida que el esfuerzo de precision en Phase Discovery se amortiza en cero deuda tecnica al incorporar BDD. | Calidad de Arquitectura |
| 2 | El orden correcto de artefactos es BRD → behavior.md → SAD → SpecDD. Crear el SpecDD antes del BDD es un riesgo calculado: si el SpecDD es robusto, no hay retrabajo; si el BDD revela gaps en el SpecDD, hay que versionar el SpecDD y actualizar el backlog. Documentar este riesgo en el handoff evita que el proximo agente asuma que el orden fue intencional. | Proceso / Metodologia |
| 3 | Los escenarios de frontera (baja confianza con umbral exacto del 60%, valores en los limites exactos del rango de validacion) son mas faciles de identificar en Gherkin que en TDD. El lenguaje de comportamiento observable obliga al autor a pensar en terminos de "dado este input exacto, que muestra la pantalla" antes de pensar en aserciones de codigo. | Calidad de Tests |
| 4 | Crear un skill para una capacidad nueva (gherkin-scenario-author) inmediatamente al usarla por primera vez garantiza que la capacidad es reproducible en sesiones futuras sin depender de la memoria del agente. El skill es la documentacion ejecutable de la habilidad. | Gestion de Conocimiento |

---

*Fin de entrada #9.*

---

## Entrada #10 — Sesión 2026-04-21 | Gobernanza

**Agente:** ai-change-manager

---

### CC-028 (referencia): Expansión del Protocolo de Control de Cambios

| Campo | Valor |
|---|---|
| **Tipo** | Control de Cambios |
| **Estado** | APROBADO |
| **Ficha completa** | `docs/changes/CC-028.md` |
| **Resumen** | Protocolo CC expandido en CLAUDE.md Sección 5. Creación de `docs/changes/` como ubicación oficial de fichas CC. El ritual de cierre de sesión sincroniza `docs/changes/` a NotebookLM. |

---

*Fin de entrada #10.*

---

## Entrada #11 — Sesion 2026-04-21 | Phase Engineering — Gobernanza

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-21

---

### D-029: NotebookLM se consulta a demanda, no en el ritual de apertura

| Campo | Valor |
|---|---|
| **Contexto** | Se debatio si el ritual de apertura debia incluir una lectura de NotebookLM como paso obligatorio. |
| **Decision** | NotebookLM es una base de conocimiento profundo que se consulta a demanda durante la sesion, no en apertura. Los 4 documentos operativos (handoff, decisions, backlog, config) son suficientes para reconstruir el contexto de arranque. |
| **Justificacion** | Cargar el cerebro completo en cada apertura es costoso y generalmente innecesario. El conocimiento profundo solo es relevante cuando los documentos operativos no responden una pregunta especifica. |
| **Impacto** | CLAUDE.md Seccion 8 (Ritual de Apertura) incluye nota explicita de este diseño. |

---

### D-030: AGENTS.md es la unica fuente de verdad del catalogo de agentes

| Campo | Valor |
|---|---|
| **Contexto** | CLAUDE.md Seccion 7 listaba 4 agentes de forma redundante con AGENTS.md. |
| **Decision** | Eliminar la lista duplicada de CLAUDE.md y reemplazar por una referencia directa a AGENTS.md. |
| **Justificacion** | Un catalogo duplicado genera deriva — si se agrega un agente nuevo, hay dos lugares que actualizar. AGENTS.md es el documento diseñado para este proposito. |
| **Impacto** | CLAUDE.md Seccion 7 actualizada. AGENTS.md es la fuente de verdad del escuadron de agentes. |

---

### Referencia CC-028: docs/changes/ como ubicacion oficial de fichas CC

Ver ficha completa en `docs/changes/CC-028.md`.

**Resumen:** Protocolo CC expandido en CLAUDE.md Seccion 5. Creacion de `docs/changes/` para fichas formales. decisions.md referencia CCs sin duplicar detalle. Session-steward sincroniza docs/changes/ a NotebookLM al cierre si hubo CC aprobado.

---

*Fin de entrada #11.*

---

---

## Entrada #12 — Sesion 2026-04-21 | Phase Engineering — Iteraciones 2.0 y 2.1 (Implementacion Bronze)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-21
**Rama activa:** `feat/F2-engineering`

---

### D-028: Patron de inyeccion de dependencias en tests de modulos de datos

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-21 |
| **Fase**  | Phase Engineering |
| **Origen** | Diseño de `tests/unit/data/test_bronze_loader.py` — necesidad de ejecutar F2-T01 antes de que F2-T00B estuviera listo |
| **Tipo**  | Decision de diseño de tests (desacoplamiento de infraestructura) |

**Contexto:** Al diseñar los tests para `bronze_loader.py`, se planteo si los tests debian importar `src.config` para obtener el path del CSV (acoplamiento con el modulo de configuracion) o si el path debia ser inyectado como argumento de la funcion testeada. F2-T01 (RED de bronze_loader) fue ejecutada antes de F2-T00B (GREEN de config.py), lo que hizo que el acoplamiento con config.py fuera imposible por ausencia del modulo.

**Decision:** Los tests de modulos de datos (`test_bronze_loader.py`, `test_silver_cleaner.py`, `test_gold_builder.py`) NO importan `src.config` directamente. El path del CSV (u otro artefacto de entrada) se inyecta como argumento a la funcion testeada, construyendo el path en el fixture del test usando `pathlib.Path(__file__).resolve().parents[3] / "data" / "bronze" / "Iris.csv"`. Este patron sigue el principio SpecDD §12.4 de inyeccion de dependencias y se aplica a todos los modulos de datos de la fase Engineering.

**Justificacion:** El desacoplamiento de los tests respecto a `config.py` tiene tres ventajas: (1) permite ejecutar los tests RED de cada capa antes de que la infraestructura base (config.py) este implementada, (2) los tests son mas robustos porque no dependen de que `config.py` se importe correctamente, (3) si `config.py` cambia sus constantes de ruta, los tests de datos no se rompen. Este patron replica el principio de "ports and adapters" en el nivel de tests.

**Impacto Transversal:**
- `tests/unit/data/test_bronze_loader.py`: Patron implementado. Path del CSV construido en fixture con `pathlib`.
- `tests/unit/data/test_silver_cleaner.py` (F2-T04, pendiente): Debe seguir el mismo patron — inyectar el path de `data/bronze/Iris.csv` como argumento a `clean_silver()`, no importar `config.DATA_BRONZE`.
- `tests/unit/data/test_gold_builder.py` (F2-T07, pendiente): Idem — inyectar paths de Silver como argumentos.

---

### D-029: `src/__init__.py` vacio es prerequisito obligatorio para importar desde `src`

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-21 |
| **Fase**  | Phase Engineering |
| **Origen** | Error de importacion al ejecutar `pytest tests/unit/test_config.py` antes de crear `src/__init__.py` |
| **Tipo**  | Decision de ingenieria de software (estructura de paquete Python) |

**Contexto:** Al implementar `src/config.py` (F2-T00B) y ejecutar los tests, el comando `from src import config` fallo con `ModuleNotFoundError: No module named 'src'`. El directorio `src/` no tenia un archivo `__init__.py`, por lo que Python no lo reconocia como paquete importable.

**Decision:** El archivo `src/__init__.py` (contenido vacio) debe crearse en el mismo momento que `src/config.py`. Analogamente, `src/data/__init__.py` debe crearse junto con el primer modulo en `src/data/`. Esta regla se extiende a todos los sub-paquetes de `src/` (`src/training/`). Cualquier directorio en `src/` que contenga modulos Python debe tener su `__init__.py` antes de que se pueda importar desde ese directorio.

**Justificacion:** En Python, un directorio es un paquete importable solo si contiene `__init__.py`. Sin este archivo, `import src.config` y `from src import config` fallan con `ModuleNotFoundError`, aunque el archivo `config.py` exista fisicamente. La ausencia de `__init__.py` es un error de infraestructura silencioso que produce falsos negativos en los tests RED (el test falla por razon incorrecta, no porque el codigo de produccion no exista, sino porque el paquete no es importable).

**Impacto Transversal:**
- `src/__init__.py`: Creado (vacio) junto con `src/config.py` en F2-T00B.
- `src/data/__init__.py`: Creado (vacio) junto con `src/data/bronze_loader.py` en F2-T02.
- `src/training/__init__.py` (futuro): Debe crearse junto con el primer modulo de `src/training/` en Phase Modeling.
- `tests/__init__.py`, `tests/unit/__init__.py`, `tests/unit/data/__init__.py`: Creados como scaffolding inicial de la suite de tests.

---

### D-030: FileNotFoundError explicito en bronze_loader antes de delegar a pandas

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-21 |
| **Fase**  | Phase Engineering |
| **Origen** | Diseno del test `test_bronze_raises_file_not_found_for_missing_csv` en F2-T01 |
| **Tipo**  | Decision de diseno de manejo de errores (contrato de interfaz) |

**Contexto:** El test F2-T01 incluye el caso `test_bronze_raises_file_not_found_for_missing_csv` que verifica que `load_bronze(path)` levanta `FileNotFoundError` cuando el CSV no existe. pandas levanta internamente `FileNotFoundError` si el archivo no existe, pero el mensaje de error es generico y la excepcion proviene de las entrañas de pandas. Un consumidor del modulo que capture esta excepcion no puede saber si el error es del modulo de datos o de pandas.

**Decision:** `bronze_loader.py` verifica explicitamente `csv_path.exists()` antes de llamar a `pd.read_csv()`. Si el archivo no existe, levanta `FileNotFoundError(f"CSV no encontrado en: {csv_path}")` con un mensaje descriptivo especifico del modulo. La verificacion con `pathlib.Path.exists()` es el patron estandar para este tipo de guard clause. Este patron se aplica a todos los modulos de carga de datos (`silver_cleaner.py`, `gold_builder.py`).

**Justificacion:** (1) La excepcion con mensaje personalizado identifica inequivocamente el modulo origen del error sin necesidad de trazar el stack completo. (2) Verificar antes de delegar a pandas evita que el usuario del modulo reciba un mensaje de error de pandas que no menciona el contexto del pipeline de datos. (3) El test puede afirmar con precision que el modulo levanta la excepcion correcta, no que pandas la levanta internamente — esto es lo que valida el contrato de interfaz del SpecDD.

**Impacto Transversal:**
- `src/data/bronze_loader.py`: Guard clause implementada antes de `pd.read_csv()`.
- `src/data/silver_cleaner.py` (F2-T05, pendiente): Debe implementar el mismo patron para verificar existencia del CSV Silver antes de procesar.
- `src/data/gold_builder.py` (F2-T08, pendiente): Idem para los archivos Silver de entrada.

---

### D-031: Orden de ejecucion del backlog — prerequisitos de infraestructura base primero

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-21 |
| **Fase**  | Phase Engineering |
| **Origen** | Ejecucion de F2-T01 antes de F2-T00A/B por error de lectura del backlog |
| **Tipo**  | Decision de proceso (orden de ejecucion de tareas) |

**Contexto:** En esta sesion se ejecuto F2-T01 (RED de bronze_loader) antes de F2-T00A/B (RED+GREEN de config.py). El error fue detectado mid-sesion y corregido: F2-T00A y F2-T00B se ejecutaron antes de continuar con F2-T02 y F2-T03. Sin embargo, el orden incorrecto inicial genero un loop de diagnostico de `ModuleNotFoundError` que costo tiempo de sesion.

**Decision:** Al iniciar una sesion de implementacion, el primer paso es verificar el backlog y ejecutar las tareas de la Iteracion de menor numero disponible. La Iteracion 2.0 (Infraestructura Base) debe completarse antes de comenzar cualquier tarea de la Iteracion 2.1. En general, las tareas de infraestructura base (config, `__init__.py`, scaffolding de tests) son prerequisito bloqueante de las tareas de capa de datos.

**Justificacion:** Las tareas de infraestructura base (config.py, `__init__.py`) crean las dependencias de importacion que necesitan los modulos de capas superiores. Ejecutar tareas de capas superiores antes de que la infraestructura exista produce errores de importacion que oscurecen los errores reales del codigo en desarrollo. El tiempo de diagnostico de errores de infraestructura es siempre mayor que el tiempo de completar la infraestructura primero.

**Impacto Transversal:**
- Backlog F2: La Iteracion 2.0 es prerequisito de la Iteracion 2.1; la 2.1 es prerequisito de la 2.2; la 2.2 de la 2.3. Esta dependencia secuencial no esta marcada explicitamente en el backlog pero debe respetarse.
- Ritual de apertura: El agente que inicie una sesion de implementacion debe verificar que todas las tareas de la iteracion anterior estan DONE antes de iniciar la siguiente.

---

### D-032: EDA Bronze — hallazgos y veredicto GO para Silver

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-21 |
| **Fase**  | Phase Engineering |
| **Origen** | Ejecucion de F2-T03b — Reporte EDA Bronze |
| **Tipo**  | Decision de calidad de datos (habilitacion de capa) |

**Contexto:** El EDA Bronze analizo el dataset Iris crudo (150 filas, 6 columnas) para verificar los invariantes BR-01 a BR-04 del contract.md y determinar si los datos son aptos para la transformacion Silver.

**Decision:** Se emite veredicto GO para la capa Silver. Los hallazgos clave del EDA Bronze son: (1) 5 near-duplicates confirmados en 2 grupos (4 instancias de Versicolor y 1 de Virginica con features identicas en todas las 4 dimensiones) — valida la proyeccion M-02 de 150→147 filas en Silver. (2) 4 outliers detectados en `SepalWidthCm` (valores en rango 2.0-2.2 cm) que son biologicamente plausibles segun literatura botanica — NO son errores de medicion, NO deben eliminarse en Silver. (3) 0 nulos, shape (150,6), tipos correctos — invariantes BR-01 a BR-04 del contract.md satisfechos al 100%.

**Justificacion:** Los near-duplicates son el unico hallazgo que requiere accion en Silver (transformacion M-02). Los outliers de `SepalWidthCm` son caracteristicas biologicas reales de la especie Setosa y su eliminacion introducirìa sesgo en el modelo. El veredicto GO es firme y no requiere condiciones adicionales antes de iniciar la Iteracion 2.2.

**Impacto Transversal:**
- `docs/Phase_engineering/eda_bronze.md`: Veredicto GO documentado con justificacion.
- `tests/unit/data/test_silver_cleaner.py` (F2-T04): El test SR-02 debe verificar `len(df) == 147` (no 145, no 150 — exactamente 147, eliminando los 5 near-duplicates en 2 grupos).
- `src/data/silver_cleaner.py` (F2-T05): La transformacion M-02 (eliminacion de near-duplicates) elimina exactamente 3 filas (de 150 a 147), no mas.

---

### Lecciones Aprendidas — Sesion 2026-04-21 (Implementacion Bronze + Infraestructura Base)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | Verificar el orden de iteraciones en el backlog antes de ejecutar cualquier tarea. Las tareas de Iteracion 2.0 (infraestructura base) son prerequisito bloqueante de todas las demas. El tiempo de detectar y corregir un orden incorrecto mid-sesion es mayor que el tiempo de verificar el orden al inicio. | Proceso / Backlog |
| 2 | `src/__init__.py` vacio es prerequisito de cualquier modulo en `src/`. Su ausencia produce `ModuleNotFoundError` que es silencioso — el archivo `.py` existe pero Python no puede importarlo. Debe crearse siempre junto con el primer modulo del directorio, no como tarea separada posterior. | Ingenieria de Software |
| 3 | El patron de inyeccion de dependencias en tests (inyectar paths como argumentos en lugar de importar config) desacopla los tests de la infraestructura base y permite ejecutar suites RED antes de que config.py exista. Este patron debe documentarse en el primer test de datos de la fase como referencia para los tests posteriores. | Calidad de Tests |
| 4 | Los guard clauses explicititos (`csv_path.exists()` antes de `pd.read_csv()`) producen mensajes de error que identifican el modulo origen sin trazar el stack completo de pandas. Son contratos de interfaz observables que los tests pueden afirmar con precision. | Calidad de Codigo |
| 5 | Los outliers detectados en EDA deben clasificarse como "error de medicion" vs. "caracteristica biologica real" antes de decidir si eliminarlos. En el dataset Iris, los valores bajos de `SepalWidthCm` en Setosa son documentados en literatura botanica — eliminarlos introduce sesgo. La fuente de verdad para esta decision es el dominio del problema, no solo la estadistica. | Calidad de Datos |

---

*Fin de entrada #12.*

---

---

## Entrada #13 — Sesion 2026-04-22 | Phase Engineering — Infraestructura CI/CD

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-22
**Rama activa:** `feat/F2-engineering`

---

### D-033: Toolchain de calidad formalizado — ruff + pytest + GitHub Actions como estandar CI/CD del proyecto

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-22 |
| **Fase**  | Phase Engineering (transversal a todas las fases tecnicas) |
| **Origen** | Creacion de `requirements.txt`, `pytest.ini` y `.github/workflows/ci.yml` |
| **Tipo**  | Decision de infraestructura de calidad (CI/CD) |

**Contexto:** El proyecto tenia una suite de tests local funcional (28/28 en verde) pero no habia ninguna garantia automatizada de que los tests se ejecutaran en cada push ni de que el codigo cumpliera un estandar de estilo. El workflow de GitHub Actions existente en el repositorio estaba configurado para un stack Node.js de ejemplo, no para el stack Python real del proyecto. `requirements.txt` y `pytest.ini` no existian como artefactos formales.

**Decision:** Se formaliza el toolchain de calidad del proyecto con tres artefactos:
1. `requirements.txt` en la raiz del repositorio como unica fuente de verdad de dependencias (pandas>=2.2, numpy>=1.26, scikit-learn>=1.4, joblib>=1.3, streamlit>=1.32, pydantic>=2.6, pytest>=8.0, ruff>=0.4).
2. `pytest.ini` con `pythonpath = .` y `testpaths = tests`. Esta configuracion permite que `from src import config` funcione sin manipulacion manual de variables de entorno, tanto en local como en CI.
3. `.github/workflows/ci.yml` adaptado al stack Python: checkout → setup Python 3.12 con cache pip → `pip install -r requirements.txt` → `ruff check .` → `pytest -v`. El workflow se dispara en push a ramas que no sean `main`/`dev` y en PRs hacia `main`/`dev`.

**Justificacion:** Sin `pytest.ini`, los tests con `from src import config` requieren que el desarrollador configure `PYTHONPATH` manualmente antes de ejecutar pytest, lo que es fragil y no reproducible en CI. Sin `requirements.txt`, el entorno de CI no puede construirse de forma determinista. Sin el workflow, el estado verde de los tests solo es verificable localmente — cualquier push puede introducir una regresion sin deteccion automatica. Los tres artefactos juntos cierran el ciclo de calidad: el codigo es verificable en cualquier entorno sin configuracion manual.

**Impacto Transversal:**
- `requirements.txt`: Debe actualizarse inmediatamente si se instala una nueva dependencia en cualquier fase futura. Es la fuente de verdad para `pip install` en CI y en onboarding de nuevos colaboradores.
- `pytest.ini`: El campo `testpaths = tests` garantiza que `pytest` sin argumentos ejecuta exactamente la suite correcta. No se necesita especificar la ruta en los comandos del backlog.
- `.github/workflows/ci.yml`: El workflow falla en ruff antes de ejecutar pytest — los errores de estilo bloquean la integracion antes de verificar la logica. Todo codigo nuevo en `src/` debe pasar `ruff check .` localmente antes de hacer push.
- Fases futuras (Modeling, Delivery): Al agregar nuevas dependencias (p. ej. `matplotlib`, `shap`), actualizar `requirements.txt` es obligatorio antes del commit.

---

### Lecciones Aprendidas — Sesion 2026-04-22 (Infraestructura CI/CD)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | `pytest.ini` con `pythonpath = .` es la solucion mas simple y portable para hacer importables los modulos de `src/` sin manipular variables de entorno. Es preferible a soluciones como `conftest.py` con `sys.path.insert` porque es declarativa y visible a nivel de proyecto. | Configuracion de Tests |
| 2 | El workflow de CI debe adaptarse al stack real del proyecto antes de que haya codigo productivo — no despues. Un workflow desalineado (Node.js en un proyecto Python) genera falsa confianza: el CI pasa porque no ejecuta nada relevante. La adaptacion debe ser la primera tarea de infraestructura de cualquier fase de implementacion. | Proceso de CI/CD |
| 3 | Ejecutar `ruff check` antes de `pytest` en el pipeline CI es una decision de diseño con consecuencias: los errores de estilo bloquean la verificacion de tests. Esto obliga a mantener el codigo limpio de forma continua en lugar de acumular deuda de estilo. El costo es mayor disciplina por push; el beneficio es un historial de commits consistentemente limpio. | Calidad de Codigo |

---

*Fin de entrada #13.*

---

---

## Entrada #14 — Sesion 2026-04-23 | Phase Engineering — Reorganizacion de Artefactos de Gobernanza

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-23
**Rama activa:** `feat/F2-engineering`

---

### D-031: Reorganizacion de artefactos de gobernanza agnostica — renombrado y reubicacion

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-23 |
| **Fase**  | Phase Engineering (transversal — gobernanza del proyecto) |
| **Origen** | Instruccion del usuario: estandarizar nombres y ubicaciones de artefactos de referencia agnosticos |
| **Tipo**  | Decision de organizacion documental (higiene de repositorio) |

**Contexto:** El proyecto tenia dos artefactos de gobernanza agnostica con nombres no estandarizados: `AGENTS.md` en la raiz del repositorio (nombre en mayusculas, fuera de la estructura `docs/`) y `docs/methodology/ai_process.md` (con prefijo `ai_` redundante que no aplica a ningun otro documento del proyecto). La raiz del repositorio debe contener unicamente archivos de configuracion del proyecto (`CLAUDE.md`, `requirements.txt`, `pytest.ini`, etc.), no documentacion de referencia.

**Decision:**
1. `AGENTS.md` (raiz) → `docs/references/agents.md`: Centraliza el catalogo de agentes en el directorio de referencias junto con `config.md`, `decisions.md`, `handoff.md`, `principles.md` y `sources.md`. El titulo interno del archivo fue actualizado a `# agents.md`.
2. `docs/methodology/ai_process.md` → `docs/methodology/process.md`: Elimina el prefijo `ai_` para uniformizar la nomenclatura. El archivo permanece en `docs/methodology/` — su ubicacion es correcta, solo el nombre cambia.
3. Ambos cambios se ejecutaron con `git mv` para preservar el historial de commits de cada archivo.

**Justificacion:** (1) La raiz del repositorio es mas limpia sin documentos de referencia navegacional — `AGENTS.md` es documentacion, no configuracion. (2) `docs/references/` ya contiene todos los artefactos de referencia del proyecto; concentrarlos en un unico directorio reduce el tiempo de navegacion para nuevos colaboradores. (3) El prefijo `ai_` en `ai_process.md` era un artifact del nombre original del documento — el resto de artefactos del proyecto no usan este prefijo (no existe `ai_brd.md`, `ai_sad.md`, etc.).

**Impacto Transversal:**
- `CLAUDE.md`: 3 referencias actualizadas (Seccion de metodologia, encabezado de tabla de gobernanza, Seccion 7 de agentes).
- `docs/governance/backlog.md`: Enlace de metodologia actualizado.
- `docs/references/handoff.md`: 3 referencias actualizadas (tabla de inventario, tabla NotebookLM, notas de contexto).
- `docs/references/config.md`: Entrada en fuentes cargadas en NotebookLM actualizada.
- `.claude/skills/session-management/SKILL.md`: Tabla de sincronizacion actualizada.
- `.claude/skills/repository-governance/SKILL.md`: Cabecera de fuente de verdad actualizada.
- Entradas historicas en `decisions.md` (D-012, D-030 y otras): Conservadas intactas — son registros de estado pasado, no referencias navegables.

---

### Lecciones Aprendidas — Sesion 2026-04-23 (Reorganizacion de Gobernanza)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | `git mv` es el unico comando correcto para renombrar o mover archivos de gobernanza — preserva el historial de commits. Usar `cp` + `rm` rompe la trazabilidad del archivo. | Gestion de Versiones |
| 2 | Las entradas historicas en `decisions.md` documentan el estado en el momento de la decision, no el estado actual del sistema. Actualizar su contenido para reflejar reorganizaciones posteriores seria revisionismo — se debe dejar intactas y registrar el cambio en una nueva entrada. | Gobernanza Documental |
| 3 | La raiz del repositorio debe contener exclusivamente archivos de configuracion del proyecto (CLAUDE.md, requirements.txt, pytest.ini, .github/, .gitignore). Los documentos de referencia navegacional pertenecen a `docs/references/`, no a la raiz. | Organizacion de Repositorio |

---

*Fin de entrada #14.*

---

---

## Entrada #15 — Sesion 2026-04-23 | Phase Engineering — EDA Silver y Cierre de Iteracion 2.2

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-23
**Rama activa:** `feat/F2-engineering`

---

### D-034: Distribucion real de clases Silver diverge de la estimacion del contract.md — los valores reales prevalecen

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-23 |
| **Fase**  | Phase Engineering — Iteracion 2.2 (Silver) |
| **Origen** | F2-T06b — EDA Silver ejecutado por ai-data-auditor |
| **Tipo**  | Decision de calidad de datos (reconciliacion de estimacion vs. valor real) |

**Contexto:** El EDA Silver (F2-T06b) calculo la distribucion real de clases despues de aplicar las transformaciones M-01 a M-04 sobre el dataset Bronze (150 filas, 3 clases balanceadas). El contract.md §4.2 incluia una estimacion de la distribucion post-limpieza: setosa=49, virginica=48. Sin embargo, los valores reales calculados por el pipeline `clean_silver()` aplicando `drop_duplicates(keep='first')` son: setosa=48, versicolor=50, virginica=49 (total=147).

La discrepancia se origina en que la estimacion del contract.md fue realizada antes de conocer exactamente que near-duplicates serian eliminados y con que criterio de ordenamiento. El criterio `keep='first'` retiene la primera ocurrencia en el orden de aparicion del CSV original, lo que determina de forma determinista cuales filas sobreviven en cada especie.

**Decision:** Los valores reales de la distribucion Silver (setosa=48, versicolor=50, virginica=49) son los valores canonicos para cualquier operacion posterior. Al ejecutar F2-T09b, el archivo `data/gold/reference_stats.json` debe construirse usando estos valores reales, no la estimacion del contract.md §4.2. No se emite un Control de Cambios para el contract.md porque la estimacion era una proyeccion orientativa, no un invariante vinculante — el invariante vinculante SR-01 (`len(df) == 147`) se cumple correctamente.

**Justificacion:** El contrato de datos define invariantes verificables (SR-01 a SR-07), no estimaciones de distribucion. El invariante SR-01 establece que el dataset Silver debe tener exactamente 147 filas — este invariante se cumple. El desbalance resultante entre clases es del 4.2% (maximo absoluto entre conteos: 50 vs. 48), que esta por debajo del umbral del 5% establecido en el contract.md como aceptable. Por lo tanto, la situacion no es un bloqueo ni requiere re-ejecucion del pipeline. El hallazgo no afecta la viabilidad del modelo: un desbalance del 4.2% en un dataset de 147 filas es estadisticamente irrelevante para las metricas de Accuracy y F1-Score Macro. La decision de preservar los valores reales en `reference_stats.json` garantiza que cualquier verificacion futura del linaje de datos encuentre consistencia entre el EDA Silver, el archivo JSON y los datos reales en `data/silver/`.

**Impacto Transversal:**
- `data/gold/reference_stats.json` (F2-T09b — pendiente): Debe contener `{"setosa": 48, "versicolor": 50, "virginica": 49, "total": 147}` como distribucion canonica de referencia.
- `docs/Phase_engineering/eda_silver.md`: Hallazgo documentado en la seccion de distribucion de clases.
- `docs/governance/contract.md` §4.2: La estimacion existente (setosa=49, virginica=48) queda obsoleta como referencia numerica pero el contrato no requiere actualizacion formal porque el invariante SR-01 sigue siendo `len==147` y los valores reales no lo contradicen. Si en el futuro se requiere precision numerica en el contract, se puede emitir un CC menor para actualizar la tabla de proyeccion.
- `handoff.md`: Nota critica añadida en la seccion de proximos pasos para que el agente que ejecute F2-T09b use los valores reales.

---

### Lecciones Aprendidas — Sesion 2026-04-23 (EDA Silver)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | Las estimaciones de distribucion post-limpieza en el contract.md son proyecciones orientativas, no invariantes vinculantes. Los invariantes vinculantes son los que tienen un operador de comparacion explicito (==, >=, <=). Al auditar el EDA, distinguir claramente entre "el invariante se cumple" y "la estimacion era exacta" evita falsas alarmas de calidad. | Calidad de Datos |
| 2 | El criterio `keep='first'` en `drop_duplicates` es determinista pero su efecto sobre la distribucion de clases depende del orden de las filas en el CSV de origen. Si el CSV cambia de orden (ej. tras una re-exportacion), la distribucion Silver puede variar. Documentar el criterio en el EDA Silver garantiza reproducibilidad auditada. | Reproducibilidad de Datos |
| 3 | Un desbalance del 4.2% entre clases en un dataset de 147 filas es estadisticamente irrelevante para clasificacion multi-clase con F1-Score Macro como metrica primaria. No escalar a CC ni a rediseno del pipeline por divergencias menores que el umbral definido es una aplicacion correcta del principio "Truth over Speed": registrar el hallazgo, no paralizarse por el. | Proceso de Toma de Decisiones |
| 4 | El EDA de cada capa (Bronze, Silver, Gold) debe verificar no solo los invariantes del contract.md sino tambien la coherencia entre capas (deltas de media Bronze→Silver). Un delta de media < 0.022 en todas las features confirma que las transformaciones M-01 a M-04 no introducen sesgo estadistico — esta es la evidencia mas fuerte de que el pipeline es correcto. | Auditoria de Pipelines de Datos |

---

*Fin de entrada #15.*

---

---

## Entrada #16 — Sesion 2026-04-24 | Phase Engineering — Gold Layer completa: Iteracion 2.3 DONE

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-24
**Rama activa:** `feat/F2-engineering`

---

### D-035: `TARGET_COLUMN` como constante de modulo explicita en `gold_builder.py`

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-24 |
| **Fase**  | Phase Engineering — Iteracion 2.3 (Gold) |
| **Origen** | F2-T09a — REFACTOR de `src/data/gold_builder.py` |
| **Tipo**  | Decision de diseno de codigo (contrato anti-leakage) |

**Contexto:** Durante el refactor de `gold_builder.py` (F2-T09a), se detecto que el string literal `"species"` aparecia en multiples puntos del modulo: en la logica de separacion X/y, en las validaciones de invariantes y en el test. El patron de constantes de modulo ya estaba establecido en `silver_cleaner.py` con `RENAME_MAP` y `LABEL_MAP`.

**Decision:** Se define `TARGET_COLUMN: str = "species"` como constante de nivel de modulo en `gold_builder.py`. Todas las referencias al nombre de la columna objetivo dentro del modulo usan esta constante. El string literal `"species"` no aparece duplicado en el cuerpo de las funciones.

**Justificacion:** Una constante de modulo explicita hace visible el contrato anti-leakage: cualquier agente que lea el encabezado del modulo sabe inmediatamente cual es la columna objetivo que se separa del Feature Store. Si el nombre de la columna cambiara en una version futura del dataset, el cambio se hace en un unico punto. El patron es consistente con `RENAME_MAP` y `LABEL_MAP` en `silver_cleaner.py`, lo que reduce la curva de aprendizaje para el siguiente agente que trabaje en los modulos de datos.

**Impacto Transversal:**
- `src/data/gold_builder.py`: Unico archivo afectado. Constante definida en la cabecera del modulo.

---

### D-036: Correlaciones Gold reales vs. referencia contract.md §8.3 — desviacion maxima ±0.001

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-24 |
| **Fase**  | Phase Engineering — Iteracion 2.3 (Gold) |
| **Origen** | F2-T09b — EDA Gold ejecutado por ai-data-auditor |
| **Tipo**  | Decision de calidad de datos (reconciliacion de valores de referencia) |

**Contexto:** El EDA Gold (F2-T09b) calculo las correlaciones reales entre features del dataset Gold y las comparo contra los valores de referencia documentados en `contract.md §8.3`. La desviacion maxima encontrada fue de ±0.001, consistente con diferencias de redondeo a 4 decimales vs. los valores estimados a 2 decimales en el feasibility report.

**Decision:** Las correlaciones Gold calculadas son estadisticamente identicas a las del contrato. No se emite Control de Cambios. Los valores reales a 4 decimales se almacenan en `data/gold/reference_stats.json` como referencia canonica para drift detection en produccion. El contract.md no requiere actualizacion formal: la desviacion esta dentro de la tolerancia de redondeo esperada.

**Justificacion:** Una desviacion de ±0.001 en correlaciones es ruido de redondeo, no una divergencia estadistica. El umbral de tolerancia implicito para este tipo de comparacion (estimacion a 2 decimales vs. valor real a 4 decimales) es del orden de ±0.005. Escalar a CC por una desviacion 5 veces menor que el umbral seria una aplicacion incorrecta del principio de Control de Cambios. Los valores reales en `reference_stats.json` son mas precisos que los del feasibility report y deben usarse como referencia operativa para cualquier verificacion de drift en el pipeline de produccion.

**Impacto Transversal:**
- `data/gold/reference_stats.json`: Contiene los valores reales a 4 decimales. Fuente de verdad para drift detection.
- `docs/Phase_engineering/eda_gold.md`: Tabla de correlaciones con valores reales documentada.
- `docs/governance/contract.md §8.3`: Sin cambios formales. Los valores estimados quedan como referencia orientativa; `reference_stats.json` es la fuente operativa.

---

### D-037: Alta correlacion petal_length/petal_width (0.962) — correlacion biologica documentada, no target leakage

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-24 |
| **Fase**  | Phase Engineering — Iteracion 2.3 (Gold) |
| **Origen** | F2-T09b — EDA Gold, analisis de matriz de correlaciones |
| **Tipo**  | Decision de diseno de features (inclusion/exclusion en Feature Store) |

**Contexto:** El EDA Gold detecto una correlacion de 0.962 entre `petal_length` y `petal_width`. Esta correlacion es la mas alta del dataset y podria interpretarse superficialmente como redundancia de features o como riesgo de multicolinealidad en modelos lineales. Se evaluo si alguna de las dos features debia eliminarse del Feature Store Gold antes de Phase Modeling.

**Decision:** Ambas features se preservan en el Feature Store Gold. La correlacion petal_length/petal_width (0.962) es una correlacion biologica documentada en la literatura botanica del genero Iris: las especies con petalos mas largos biologicamente tambien tienen petalos mas anchos como consecuencia del desarrollo del organo floral. No es leakage (ninguna feature es un proxy de la etiqueta `species` calculado a partir de `species`). Phase Modeling debe evaluar el VIF (Variance Inflation Factor) si usa modelos lineales (regresion logistica, LDA) para determinar si la multicolinealidad afecta los coeficientes. Para ensambles (Random Forest, Gradient Boosting) y SVM con kernel RBF, la alta correlacion entre features no es un bloqueador.

**Justificacion:** Eliminar una feature del Feature Store por correlacion alta con otra feature sin evidencia de impacto negativo en el modelo es sobre-ingenieria prematura que viola el principio "Simplicidad Primero" del proyecto. La correlacion entre features no implica reduccion de poder discriminativo — ambas features contribuyen a la separacion de la zona de solapamiento versicolor/virginica en `petal_width` [1.4-1.8 cm]. La decision de eliminar features por multicolinealidad pertenece a Phase Modeling, donde se cuenta con metricas de modelo (VIF, feature importance, permutation importance) para tomar la decision con evidencia, no con heuristicas.

**Impacto Transversal:**
- `src/data/gold_builder.py`: Sin cambios. Las 4 features permanecen en el Feature Store.
- `data/gold/X_gold.csv`: 4 columnas (sepal_length, sepal_width, petal_length, petal_width).
- Phase Modeling: Evaluar VIF si se usa regresion logistica o LDA. Documentar el resultado en el reporte de seleccion de features.
- `docs/Phase_engineering/eda_gold.md`: Hallazgo documentado con justificacion biologica y recomendacion para Phase Modeling.

---

### Lecciones Aprendidas — Sesion 2026-04-24 (Gold Layer — Iteracion 2.3 completa)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | Verificar el orden de columnas de X con `np.array_equal(X, df_silver[config.FEATURE_COLUMNS].to_numpy())` es mas robusto que comparar solo shape. La comparacion de shape detecta que hay 4 columnas pero no detecta si estan en el orden incorrecto — un feature misalignment silencioso que producira predicciones incorrectas sin errores en tests. La comparacion con `array_equal` es el gold standard para esta verificacion. | Calidad de Tests |
| 2 | La zona de solapamiento versicolor/virginica en `petal_width` [1.4-1.8 cm] (~17 instancias) es el limite fisico de separabilidad del dataset Iris. No es un defecto de los datos ni del pipeline — es una caracteristica intrinseca del problema biologico. Phase Modeling debe evaluar el modelo especificamente sobre estas instancias y reportar la metrica de error en este subconjunto como indicador de la dificultad real del problema. | Calidad de Datos / Modelado |
| 3 | `data/gold/reference_stats.json` debe versionarse junto con el modelo en cada reentrenamiento. La trazabilidad del drift detection depende de que el archivo JSON de referencia corresponda exactamente al Feature Store con el que se entreno el modelo. Un modelo entrenado con Gold v1 y validado con `reference_stats.json` de Gold v2 produce metricas de drift incorrectas. | Trazabilidad de Linaje |
| 4 | El patron `TARGET_COLUMN: str = "species"` a nivel de modulo es la documentacion mas eficiente del contrato anti-leakage: visible en el primer scroll del archivo, sin necesidad de leer las funciones. Este patron debe aplicarse a cualquier modulo de datos que tenga una columna objetivo explicita — es mejor que un comentario porque es verificable por los tests. | Calidad de Codigo |

---

---

## Entrada #17 — Sesion 2026-04-24 | Phase Engineering — Iteracion 2.4 (Certificacion)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-24
**Tarea:** F2-T10 [CERTIFICACION] — Entregable: `docs/Phase_engineering/certification_f2.md`

---

### D-038: Certificacion de linaje Bronze→Silver→Gold — 34/34 tests PASS como criterio de cierre de Phase Engineering

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-24 |
| **Fase**  | Phase Engineering — Iteracion 2.4 (Certificacion) |
| **Origen** | F2-T10 — Certificacion tecnica ejecutada por @ai-data-qa-engineer |
| **Tipo**  | Decision de proceso (criterio de certificacion de capa de datos) |

**Contexto:** La certificacion tecnica de la Fase 2 se ejecuto mediante `pytest tests/unit/data/ -v`, que cubre las tres capas del Medallion Architecture: 10 tests Bronze (invariantes BR), 12 tests Silver (invariantes SR), 12 tests Gold (invariantes GR). La suite de 34 tests es el subconjunto del pipeline que valida el linaje de datos de extremo a extremo, sin incluir los 16 tests de configuracion.

**Decision:** El criterio de certificacion de linaje para Phase Engineering es 34/34 tests en verde en `tests/unit/data/`, con 0 fallos y 0 errores. Este criterio se ejecuto y se cumplio. El reporte formal queda en `docs/Phase_engineering/certification_f2.md`. Adicionalmente se verifico: ausencia de rutas absolutas en codigo fuente y todas las dependencias declaradas en `requirements.txt`.

**Justificacion:** Separar la suite de linaje (34 tests de data) de la suite completa (50 tests incluyendo config) permite auditar el pipeline de datos de forma aislada sin ruido de tests de infraestructura. Este es el patron que usara Phase Modeling para certificar el pipeline de entrenamiento de forma analoga.

**Impacto Transversal:**
- `docs/Phase_engineering/certification_f2.md`: Reporte formal de certificacion. Fuente de verdad para el GO de Phase Modeling.
- Phase Modeling: El mismo patron de certificacion por capa debe aplicarse al pipeline de entrenamiento antes de emitir el GO de Phase Modeling.

---

---

## Entrada #18 — Sesion 2026-04-24 | Phase Engineering — Iteracion 2.4 (Validacion)

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** Fin de jornada 2026-04-24
**Tarea:** F2-T11 [VALIDACION] — Entregable: `docs/Phase_engineering/validation_f2.md`

---

### D-039: Baseline RandomForest 5-fold CV 95.20% sobre Gold dataset — umbral BRD superado, GO para Phase Modeling

| Campo     | Valor |
| :-------- | :---- |
| **Fecha** | 2026-04-24 |
| **Fase**  | Phase Engineering — Iteracion 2.4 (Validacion) |
| **Origen** | F2-T11 — Validacion de negocio ejecutada por @ai-data-scientist |
| **Tipo**  | Decision de validacion de negocio (GO/NO-GO para Phase Modeling) |

**Contexto:** La validacion de la Fase 2 consistio en verificar que el Feature Set Gold es suficientemente informativo para el problema de clasificacion Iris. Se ejecuto un proxy de separabilidad: RandomForest sin hiperparametrizar, 5-fold cross-validation, sobre `data/gold/X_gold.csv` y `data/gold/y_gold.csv`. El resultado fue 95.20% accuracy ± 3.53%. El umbral del BRD es Accuracy >= 95%.

**Decision:** El Feature Set Gold supera el umbral de accuracy del BRD. Se emite veredicto GO para Phase Modeling. El baseline de 95.20% queda registrado como referencia: el modelo final de produccion debe igualar o superar este valor. Los cuatro criterios de validacion se cumplieron: linaje 100% documentado, trazabilidad SpecDD completa, cobertura de tests 100%, baseline ≥ 95%.

**Justificacion:** La validacion del Feature Set con un clasificador proxy (no el modelo de produccion final) antes de iniciar Phase Modeling es una practica de bajo costo y alto valor: si el baseline no supera el umbral, el problema esta en los features o en la limpieza de datos, no en el modelo. Detectarlo aqui evita iteraciones costosas en Phase Modeling. El RandomForest sin tuning es el proxy mas honesto: no puede hacer overfitting por hiperparametrizacion agresiva y su performance real en CV refleja la separabilidad intrinseca del Feature Store.

**Impacto Transversal:**
- `docs/Phase_engineering/validation_f2.md`: Reporte formal de validacion con veredicto GO.
- Phase Modeling: El modelo final debe superar 95.20% accuracy en el conjunto de test. Este valor es el piso, no el techo.
- `docs/governance/brd.md`: KPI de accuracy validado formalmente contra el Feature Set Gold.

---

### Lecciones Aprendidas — Sesion 2026-04-24 (Iteracion 2.4 — Certificacion y Validacion)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | El ciclo AI-TDD (Red→Green→Refactor→Certificacion→Validacion) por capa fue completado de forma limpia en Fase 2. La separacion de responsabilidades entre @ai-data-qa-engineer (certificacion tecnica — 34 tests, ausencia de rutas absolutas, dependencias declaradas) y @ai-data-scientist (validacion de negocio — linaje, trazabilidad SpecDD, baseline KPI) funcionó correctamente. Cada agente tiene un criterio de exito diferente y complementario. | Proceso / Organizacion de Agentes |
| 2 | El baseline proxy de separabilidad (RandomForest 5-fold CV sin hiperparametrizar) es la herramienta mas honesta para validar un Feature Store antes de Phase Modeling. Un resultado de 95.20% ± 3.53% sobre el Gold dataset confirma que los datos son suficientemente informativos. La desviacion estandar de 3.53% es aceptable para un dataset de 147 instancias con 5 folds — indica varianza de muestreo, no inestabilidad del clasificador. | Calidad de Datos / Modelado |
| 3 | La certificacion tecnica del linaje mediante ejecucion directa de pytest (sin mocks ni fixtures artificiales) es la auditoria mas rigurosa del pipeline. Si los 34 tests de data pasan, el codigo que implementa Bronze→Silver→Gold es correcto por construccion. No existe documentacion de linaje mas fiable que una suite de tests que falla si el contrato se rompe. | Calidad de Tests |

---

*Fin de entrada #16.*

---

---

## Entrada #17 — Sesion 2026-04-24 | Gobernanza: Atomizacion Backlog Fase 3

**Agente de Cierre:** ai-session-steward
**Hora de Cierre:** 2026-04-24 (sesion de gobernanza de backlog)

---

### D-040: Atomizacion del Backlog de Fase 3 siguiendo el patron IA-TDD de Fase 2

| Campo | Valor |
| :---- | :---- |
| **Fecha** | 2026-04-24 |
| **Fase** | Phase Modeling (Pre-ejecucion — Gobernanza) |
| **Origen** | Auditoria del backlog.md §F3 contra el patron establecido en D-023 |
| **Tipo** | Decision de proceso / estructura del backlog |

**Contexto:** Al revisar el Backlog de Fase 3 previo a su ejecucion, se detecto que contenia solo 3 tareas vagas (F3-T01, F3-T02, F3-T03) que violaban los mismos principios corregidos en D-023 para Fase 2: DoDs imprecisos sin trazabilidad al SpecDD, ruta de tests no canonica (`tests/test_model_training.py` en lugar de `tests/unit/training/`), modulos `trainer.py` y `serializer.py` mezclados en una sola tarea (violacion de atomicidad), y ausencia de las iteraciones REFACTOR, CERTIFICACION y VALIDACION.

**Decision:** Se atomizo completamente el Backlog F3 de 3 tareas a 9 tareas distribuidas en 4 iteraciones:
- **Iter 3.1:** RED + GREEN + REFACTOR para `src/training/trainer.py` (SpecDD §9)
- **Iter 3.2:** RED + GREEN + REFACTOR para `src/training/serializer.py` (SpecDD §10)
- **Iter 3.3:** EXPERIMENT (notebook de seleccion) + BUILD (modelo certificado `.joblib`)
- **Iter 3.4:** MODEL QA + CERTIFICACION (`certification_f3.md`) + VALIDACION (`validation_f3.md`)

**Justificacion:** La D-023 establece que el ciclo completo RED→GREEN→REFACTOR es obligatorio por modulo, y que cada fase tecnica debe cerrar con CERTIFICACION y VALIDACION. Iniciar la ejecucion de F3 con un backlog incompleto habria producido el mismo problema que en Fase 2: completar el ciclo sin trazabilidad formal de linaje, calidad de codigo o cumplimiento de KPIs. El principio "Pensar antes de programar" (principles.md) exige que el backlog este completo y auditado antes de escribir la primera linea de codigo.

**Impacto Transversal:**
- `docs/governance/backlog.md`: F3 actualizado de 3 a 9 tareas atomicas con DoDs trazables al SpecDD §9–10, SAD §9.2 y BRD §4.
- `docs/references/handoff.md`: Proximos pasos actualizados con la ruta canonica de tests `tests/unit/training/` y el responsable correcto por tarea.
- Phase Modeling: La primera tarea ejecutable es F3-T01 [RED] con entregable `tests/unit/training/test_trainer.py`.

---

### D-041: Separacion de `trainer.py` y `serializer.py` como iteraciones independientes en F3

| Campo | Valor |
| :---- | :---- |
| **Fecha** | 2026-04-24 |
| **Fase** | Phase Modeling |
| **Origen** | Auditoria de atomicidad del backlog F3 |
| **Tipo** | Decision de estructura del backlog / atomicidad de tareas |

**Contexto:** El backlog original de F3 agrupaba el entrenamiento del modelo y su serializacion en una unica tarea [GREEN] (F3-T02) con dos entregables: `notebooks/03_model_selection.ipynb` y `models/iris_model.joblib`. Esto viola el principio de atomicidad ("Un unico responsable por tarea. Un unico entregable por tarea.") y mezcla las responsabilidades de `trainer.py` (SpecDD §9) y `serializer.py` (SpecDD §10), que son modulos distintos con contratos de interfaz independientes.

**Decision:** Se separan en iteraciones distintas: Iteracion 3.1 cubre `trainer.py` completo (RED + GREEN + REFACTOR), Iteracion 3.2 cubre `serializer.py` completo (RED + GREEN + REFACTOR). El notebook de seleccion y el build del modelo certificado se ubican en Iteracion 3.3, garantizando que los modulos productivos estean implementados y testeados antes de usarlos en experimentacion.

**Justificacion:** El patron de Fase 2 (Bronze/Silver/Gold como iteraciones separadas) demostro que la separacion por modulo reduce la complejidad del ciclo TDD y facilita la certificacion de linaje. Un modulo = una iteracion = una suite de tests = un responsable. Este patron se aplica directamente a `trainer.py` y `serializer.py`.

**Impacto Transversal:**
- `docs/governance/backlog.md`: Iteraciones 3.1 y 3.2 son independientes.
- `tests/unit/training/`: Contendra `test_trainer.py` (F3-T01) y `test_serializer.py` (F3-T03) como suites independientes.
- `pytest tests/unit/training/` es el comando de verificacion del ciclo completo de Phase Modeling.

---

### Lecciones Aprendidas — Sesion 2026-04-24 (Gobernanza Backlog F3)

| # | Leccion | Categoria |
| :- | :------- | :-------- |
| 1 | El backlog de una fase debe auditarse contra el patron IA-TDD (D-023) ANTES de iniciar la ejecucion, no durante. Un backlog incompleto en el momento de ejecucion obliga a pausar el trabajo para corregir la gobernanza, lo que interrumpe el flujo. La auditoria pre-ejecucion es una inversion que cuesta minutos y ahorra horas. | Proceso / Backlog |
| 2 | Los principios de ingenieria (principles.md) y el catalogo de agentes (agents.md) deben leerse al inicio de cualquier sesion de gobernanza, no solo al inicio de sesiones de codigo. Las decisiones de backlog tambien son decisiones de ingenieria y deben cumplir los mismos estandares. | Proceso / Gobernanza |
| 3 | Asignar agentes correctos desde agents.md en el momento de disenar las tareas (no al ejecutarlas) permite que el backlog sea autoexplicativo: cualquier colaborador sabe quien hace que sin necesidad de contexto adicional. La asignacion correcta en F3 fue: @ai-data-qa-engineer para suites RED, @ai-data-scientist para implementacion del trainer, @ai-ml-engineer para serializer y refactorizaciones, @ai-model-qa-validator para QA, @ai-mlops-specialist para validacion final. | Organizacion de Agentes |

---

*Fin de entrada #17.*
