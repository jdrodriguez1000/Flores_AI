# HANDOFF.md: Estado Operativo del Proyecto

> **Definicion del Documento**
> Este archivo es la foto nítida y actual del proyecto. Es sobrescribible al cierre de cada sesion.
> Un nuevo agente debe poder retomar el trabajo leyendo unicamente este archivo.
>
> **Ultima actualizacion:** 2026-04-19
> **Responsable de cierre:** ai-session-steward
> **Fase activa:** Fase 1 - Discovery (cierre de fase en progreso)

---

## 1. Resumen de Estado

| Campo               | Valor                                                                    |
| :------------------ | :----------------------------------------------------------------------- |
| **Proyecto**        | Flores AI - Iris                                                         |
| **Fase Actual**     | Fase 1 - Discovery                                                       |
| **Iteracion**       | Sesion de arquitectura y diseno — cierre de Fase 1                      |
| **Estado General**  | Fase 1 al 85% completada. Unico pendiente: BACKLOG.                     |
| **Progreso Fase 1** | 85% (BRD + FEASIBILITY + MOCKUP + SAD + SpecDD + DATA_CONTRACT entregados) |

---

## 2. Logros de la Sesion (2026-04-19)

| # | Entregable                        | Archivo                                              | Estado      | Responsable         |
| :-- | :-------------------------------- | :--------------------------------------------------- | :---------- | :------------------ |
| 1 | Visual Mockup (HTML + documento)  | `docs/governance/MOCKUP/index.html` + `docs/governance/MOCKUP.md` | Completado y aprobado por Stakeholder | ai-ux-designer |
| 2 | Software Architecture Document    | `docs/governance/SAD.md`                             | Completado  | ai-solutions-architect |
| 3 | SpecDD (Especificacion de Interfaces) | `docs/governance/SpecDD.md`                      | Completado  | ai-solutions-architect |
| 4 | Data Contract                     | `docs/governance/DATA_CONTRACT.md`                   | Completado  | ai-solutions-architect |

### Detalle de Logros

**Entregable 1 — Visual Mockup**
Prototipo interactivo HTML de alta fidelidad que cubre 4 estados de pantalla: estado inicial (formulario con sliders), resultado exitoso (alta confianza, 97.3%), resultado de baja confianza (advertencia prominente, 52.4%) y error de validacion (campos invalidos con mensajes descriptivos). El Stakeholder reviso y aprobo el diseno en sesion. La UI de Streamlit debe seguir este mockup como especificacion visual vinculante.

**Entregable 2 — SAD**
Arquitectura Monolito Modular con Medallion Architecture (Bronze / Silver / Gold). Define la estructura completa de `src/` en 5 modulos: `config.py`, `validators.py`, `predictor.py`, `feedback.py`, `app.py`, mas los sub-paquetes `src/data/` y `src/training/`. Cuatro ADRs registrados: Streamlit como UI, Joblib para serializacion, StandardScaler dentro de sklearn.Pipeline, y pathlib para gestion de rutas. El principio "Decoupling is King" garantiza que `app.py` solo invoca `predictor.predict()` sin importar nada de los pipelines de datos o entrenamiento.

**Entregable 3 — SpecDD**
Define las firmas exactas (tipos de entrada, tipos de retorno, excepciones) de todos los modulos `.py` de `src/`. Ninguna implementacion en Fase 2 o Fase 3 puede desviarse de estas firmas sin un Control de Cambios aprobado. Incluye tipos Pydantic v2 compartidos (`IrisInput`, `PredictionResult`, `FeedbackRecord`) y el protocolo de Mock para desarrollo paralelo.

**Entregable 4 — DATA_CONTRACT**
Invariantes rigidos para las tres capas Medallion. Prohibicion explícita de la columna `Id` como feature valida. Define esquemas de Bronze (CSV crudo con 6 columnas incluyendo `Id`), Silver (150 filas, 5 columnas sin `Id`, sin nulos, sin near-duplicates) y Gold (arrays NumPy normalizados con StandardScaler). Incluye reglas de validacion matematica, politica de nulos, deteccion de data drift y mensajes de error estandarizados.

---

## 3. Pendientes y Proximos Pasos

| Prioridad | Tarea                          | Documento Destino              | Responsable              | Fase   |
| :-------- | :----------------------------- | :----------------------------- | :----------------------- | :----- |
| 1 (CRITICA) | BACKLOG detallado (unico pendiente de Fase 1) | `docs/governance/BACKLOG.md` | ai-backlog-manager | Fase 1 |
| 2         | Inicio de Fase 2: pipeline Bronze → Silver → Gold | `src/data/`, `data/bronze/`, `data/silver/`, `data/gold/` | ai-data-engineer | Fase 2 |
| 3         | EDA (Ingesta, Limpieza, Analisis Estadistico) | `docs/Fase_2/`          | ai-data-analyst          | Fase 2 |

**Nota critica sobre la Tarea 1:** El BACKLOG debe descomponer las Fases 2, 3 y 4 en iteraciones atomicas con Definition of Done (DoD) por tarea. No puede iniciarse Fase 2 sin BACKLOG aprobado.

---

## 4. Bloqueos Activos

**Ninguno.** Los seis entregables de arquitectura y diseno de Fase 1 estan completos. El unico paso restante de Fase 1 es la generacion del BACKLOG por el `ai-backlog-manager`.

---

## 5. Decisiones Criticas Activas (Consultar DECISIONS_LOG.md para contexto completo)

| ID    | Decision                                                              | Impacto                                                    |
| :---- | :-------------------------------------------------------------------- | :--------------------------------------------------------- |
| D-001 | Eliminar columna `Id` antes de cualquier entrenamiento                | Previene data leakage — mandatorio en pipeline Silver      |
| D-002 | Metrica primaria: Accuracy Global + F1-Score Macro >= 0.95            | Define criterio de exito del modelo                        |
| D-003 | Stack confirmado: Python 3.12+ y Streamlit                            | Condiciona SAD y SpecDD                                    |
| D-004 | Veredicto GO con confianza Alta (9.2/10)                              | Habilita continuacion a Fase 2                             |
| D-005 | Mockup aprobado por el Stakeholder                                    | La UI de Streamlit debe seguir el diseno del mockup        |
| D-006 | Patron arquitectonico: Monolito Modular + Medallion Architecture      | Define la estructura completa de `src/`                    |
| D-007 | Serializacion: Joblib (no Pickle)                                     | `models/iris_model.joblib` es el unico punto de acoplamiento offline/online |
| D-008 | StandardScaler dentro de sklearn.Pipeline                             | Elimina completamente el riesgo de Data Leakage (RT3 BRD) |
| D-009 | pathlib.Path en `src/config.py` como unico gestor de rutas            | Cero strings hardcodeados en el codigo                     |
| D-010 | Pipeline offline y online completamente desacoplados                  | `app.py` nunca importa modulos de ingesta o entrenamiento  |

---

## 6. Contexto para el Siguiente Agente

La Fase 1 tiene seis de sus siete entregables listos. El unico documento faltante es el **BACKLOG** (`docs/governance/BACKLOG.md`), responsabilidad del `ai-backlog-manager`. Una vez entregado el BACKLOG, la Fase 1 queda formalmente cerrada y el proyecto puede iniciar la Fase 2 con plena trazabilidad.

Los documentos de arquitectura (SAD, SpecDD, DATA_CONTRACT) estan interconectados y deben leerse en ese orden antes de implementar cualquier modulo en `src/`. La firma de `predictor.predict()` en el SpecDD es el contrato mas critico del sistema: todas las demas capas se adaptan a ella.

El prototipo en `docs/governance/MOCKUP/index.html` es la referencia visual oficial aprobada por el Stakeholder. Cualquier desviacion en la implementacion de `src/app.py` respecto al mockup requiere un Control de Cambios.
