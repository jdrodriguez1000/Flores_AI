# DECISIONS_LOG.md: Registro Historico de Decisiones

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
| **Origen**              | DATA_FEASIBILITY_REPORT — Analisis de data leakage                                        |
| **Tipo**                | Decision de preprocesamiento de datos                                                     |

**Contexto:** Durante el analisis de factibilidad del dataset Iris se detecto que la columna `Id` es un identificador secuencial correlacionado con el orden de recoleccion de las muestras. Las filas estan ordenadas por especie (primeras 50: Setosa, siguientes 50: Versicolor, ultimas 50: Virginica), lo que genera una correlacion espuria entre el `Id` y la variable objetivo.

**Decision:** La columna `Id` debe ser eliminada del dataset como paso obligatorio (accion M-01) antes de cualquier operacion de entrenamiento, validacion o inferencia. Esta eliminacion debe implementarse en el pipeline de preprocesamiento Silver.

**Justificacion:** Si el modelo aprende a usar el `Id` como feature, obtendra artificialmente metricas de rendimiento infladas en entrenamiento que no se replicaran en produccion real (donde el `Id` no tiene valor predictivo). Mantener el `Id` constituye data leakage clasico.

**Impacto Transversal:**
- `docs/governance/SpecDD.md`: La firma del modulo de preprocesamiento debe incluir explicitamente la exclusion de `Id`.
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
- `docs/governance/SAD.md`: Los experimentos de benchmarking deben reportar ambas metricas.
- `docs/Fase_3/MODEL_QA.md`: El modelo candidato no puede ser certificado si no supera ambos thresholds.
- `tests/`: Los tests de Model QA deben incluir assertions sobre ambas metricas.

---

### D-003: Stack tecnologico confirmado — Python 3.12+ y Streamlit

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | PROJECT_config.md — Definicion de stack                                                   |
| **Tipo**                | Decision de arquitectura tecnologica                                                      |

**Contexto:** El proyecto requiere un lenguaje de ML y una interfaz web para la demostracion de predicciones. Se evaluaron las opciones disponibles segun el protocolo CLAUDE.md (Python 3.12+ obligatorio) y los requisitos del stakeholder.

**Decision:** El stack tecnologico queda confirmado con Python 3.12+ como lenguaje base y Streamlit como framework de la aplicacion web de prediccion. Las librerias especificas de ML (scikit-learn, pandas, etc.) y serializacion (ONNX/Pickle/Joblib) quedaran definidas en la Fase 2 una vez que el SAD este completo.

**Justificacion:** Python 3.12+ es mandatorio segun CLAUDE.md. Streamlit fue elegido sobre Flask/FastAPI por su velocidad de desarrollo para prototipos de ML con interfaces de prediccion simples, su integracion nativa con pandas y su capacidad de despliegue rapido. Para un problema de clasificacion multi-clase con cuatro inputs numericos, Streamlit provee la interfaz optima sin overhead de desarrollo de frontend.

**Impacto Transversal:**
- `docs/governance/SAD.md`: Debe documentar la justificacion arquitectonica de Streamlit.
- `requirements.txt`: Primera dependencia a registrar sera streamlit.
- `infra/`: La containerizacion (Docker) debe basarse en imagen Python 3.12.

---

### D-004: Veredicto de Factibilidad — GO con confianza Alta (9.2/10)

| Campo                   | Valor                                                                                     |
| :---------------------- | :---------------------------------------------------------------------------------------- |
| **Fecha**               | 2026-04-19                                                                                |
| **Fase**                | Fase 1 - Discovery                                                                        |
| **Origen**              | DATA_FEASIBILITY_REPORT — Veredicto final                                                 |
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
| 1 | El orden correcto de documentacion es: PROJECT_config -> estructura de carpetas -> BRD -> FEASIBILITY -> SAD -> SpecDD. Saltarse pasos genera retrabajo. | Proceso / Metodologia  |
| 2 | El data leakage por columnas de ID es el riesgo mas comun y menos visible en datasets tabulares clasicos. Siempre revisar columnas de identificadores primero. | Calidad de Datos       |
| 3 | Un dataset balanceado no garantiza ausencia de near-duplicates. La inspeccion de duplicados debe hacerse sobre el vector de features, no sobre el ID. | Calidad de Datos       |
| 4 | Documentar la hipotesis de confusion entre clases (Versicolor/Virginica) en el BRD desde el inicio obliga al equipo a disenar el modelo con ese riesgo en mente desde la arquitectura. | Diseño de Modelos      |

---

*Fin de entrada #1. La proxima entrada se agregara al cierre de la siguiente sesion.*
