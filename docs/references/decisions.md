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
