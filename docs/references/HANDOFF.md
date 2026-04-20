# handoff.md: Estado Operativo del Proyecto

> **Definicion del Documento**
> Este archivo es la foto nitida y actual del proyecto. Es sobrescribible al cierre de cada sesion.
> Un nuevo agente debe poder retomar el trabajo leyendo unicamente este archivo.
>
> **Ultima actualizacion:** 2026-04-20
> **Responsable de cierre:** ai-session-steward
> **Fase activa:** Phase Discovery — CERRADA | Proxima: Phase Engineering - Data & EDA

---

## 1. Resumen de Estado

| Campo               | Valor                                                                              |
| :------------------ | :--------------------------------------------------------------------------------- |
| **Proyecto**        | Flores AI - Iris                                                                   |
| **Fase Actual**     | Phase Discovery — COMPLETADA AL 100%                                               |
| **Iteracion**       | Sesion de integracion NotebookLM y auditoria de agnosticismo (2026-04-20)          |
| **Estado General**  | Gobernanza normalizada. NotebookLM integrado. Todos los agentes y skills auditados como 100% agnosticos. |
| **Progreso Global** | 40% — Phase Engineering pendiente de inicio                                        |

---

## 2. Logros de la Sesion (2026-04-20 — Integracion NotebookLM y Auditoria de Agnosticismo)

| # | Entregable / Accion | Archivos Afectados | Estado |
| :- | :------------------ | :----------------- | :----- |
| 1 | Creacion del notebook NotebookLM "Flores AI — Cerebro del Proyecto" (ID: `35c8760b-4797-4df2-8c91-cbf5b2df0240`) con 7 documentos de gobernanza cargados como fuentes | Externo (NotebookLM) | Completado |
| 2 | `config.md` actualizado: NotebookLM ID registrado en seccion 4.2, listado de 7 fuentes cargadas y nota de re-sincronizacion | `docs/references/config.md` | Completado |
| 3 | `session-management/SKILL.md` actualizado: paso de sincronizacion NotebookLM añadido al ritual de cierre, con tabla de documentos sincronizables y patron de actualizacion | `.claude/skills/session-management/SKILL.md` | Completado |
| 4 | `session-management/SKILL.md` refactorizado a 100% agnostico: NOTEBOOK_ID hardcodeado eliminado; el skill ahora lee el ID desde `config.md` (seccion 4.2) | `.claude/skills/session-management/SKILL.md` | Completado |
| 5 | Auditoria de agnosticismo de 63+ archivos (agentes, skills, CLAUDE.md, ai_process.md): resultado 100% agnostico tras la correccion del skill de session-management | Todos los `.md` del proyecto | Completado |

---

## 3. Estado Actual de Entregables de Gobernanza (Phase Discovery — COMPLETA)

| Documento      | Ruta                                              | Estado                                   |
| :------------- | :------------------------------------------------ | :--------------------------------------- |
| config.md      | `docs/references/config.md`                       | DONE — 2026-04-20 (actualizado con NotebookLM ID) |
| brd.md         | `docs/governance/brd.md`                          | DONE — 2026-04-19                        |
| feasibility.md | `docs/Phase_discovery/feasibility.md`             | DONE — 2026-04-19                        |
| mockup         | `mockup/index.html` + `docs/Phase_discovery/mockup.md` | DONE — 2026-04-19 (aprobado Stakeholder) |
| sad.md         | `docs/governance/sad.md`                          | DONE — 2026-04-19 (v1.0.0)              |
| specdd.md      | `docs/governance/specdd.md`                       | DONE — 2026-04-19 (v1.0.0)              |
| contract.md    | `docs/governance/contract.md`                     | DONE — 2026-04-19 (v1.0.0)              |
| AGENTS.md      | `AGENTS.md` (raiz)                                | DONE — 2026-04-20                        |
| session-management/SKILL.md | `.claude/skills/session-management/SKILL.md` | DONE — 2026-04-20 (actualizado y agnostico) |

---

## 4. Fuentes en NotebookLM (Estado al Cierre)

**Notebook:** "Flores AI — Cerebro del Proyecto"
**ID:** `35c8760b-4797-4df2-8c91-cbf5b2df0240`

| Documento        | Ruta Local                                      | Estado en NotebookLM |
| :--------------- | :---------------------------------------------- | :------------------- |
| ai_process.md    | `docs/methodology/ai_process.md`               | Cargado — 2026-04-20 |
| brd.md           | `docs/governance/brd.md`                        | Cargado — 2026-04-20 |
| sad.md           | `docs/governance/sad.md`                        | Cargado — 2026-04-20 |
| specdd.md        | `docs/governance/specdd.md`                     | Cargado — 2026-04-20 |
| contract.md      | `docs/governance/contract.md`                   | Cargado — 2026-04-20 |
| feasibility.md   | `docs/Phase_discovery/feasibility.md`           | Cargado — 2026-04-20 |
| decisions.md     | `docs/references/decisions.md`                  | Pendiente re-sincronizacion (entrada #5 añadida hoy) |

> **Accion requerida al inicio de la proxima sesion:** Re-sincronizar `decisions.md` en NotebookLM (entrada #5 fue añadida en esta sesion). Ver patron de actualizacion en `.claude/skills/session-management/SKILL.md`.

---

## 5. Proximos Pasos — Phase Engineering: Data & EDA

| Prioridad | ID Tarea | Descripcion | Responsable | Entregable |
| :-------- | :------- | :---------- | :---------- | :--------- |
| 1 (CRITICA) | F2-T01 | Implementar pipeline Bronze: ingesta y validacion del CSV crudo | ai-data-engineer | `src/data/ingestion.py`, `data/bronze/` |
| 2 | F2-T02 | Implementar pipeline Silver: limpieza, eliminacion de `Id` y near-duplicates | ai-analytics-engineer | `src/data/cleaner.py`, `data/silver/` |
| 3 | F2-T03 | Implementar pipeline Gold: normalizacion y generacion de features | ai-feature-store-architect | `src/data/feature_builder.py`, `data/gold/` |
| 4 | F2-T04 | EDA de Ingesta: Reporte estadistico de la capa Bronze | ai-data-engineer | `docs/Phase_engineering/eda_ingestion.md` |
| 5 | F2-T05 | EDA de Limpieza: Reporte de transformaciones Silver | ai-analytics-engineer | `docs/Phase_engineering/eda_cleaning.md` |
| 6 | F2-T06 | EDA Estadistico: Analisis de distribucion y correlacion Gold | ai-feature-store-architect | `docs/Phase_engineering/eda_statistical.md` |

**Prerequisito de implementacion:** Antes de escribir cualquier codigo en `src/`, leer `docs/governance/specdd.md` (firmas mandatorias), `docs/governance/contract.md` (invariantes por capa) y `docs/governance/sad.md` (estructura de modulos).

---

## 6. Bloqueos Activos

**Ninguno.** La Phase Discovery esta formalmente cerrada, la gobernanza esta completamente normalizada y el notebook de NotebookLM esta activo. El proyecto puede iniciar Phase Engineering sin dependencias externas pendientes.

---

## 7. Decisiones Criticas Activas (Consultar decisions.md para contexto completo)

| ID    | Decision                                                              | Impacto en Phase Engineering                                            |
| :---- | :-------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| D-001 | Eliminar columna `Id` antes de cualquier entrenamiento                | Accion M-01 obligatoria en pipeline Silver — no negociable              |
| D-002 | Metrica primaria: Accuracy Global + F1-Score Macro >= 0.95            | Define el criterio de exito al que sirve el pipeline de datos           |
| D-003 | Stack confirmado: Python 3.12+ y Streamlit                            | Todos los modulos de `src/data/` deben seguir este stack                |
| D-006 | Monolito Modular + Medallion Architecture (Bronze/Silver/Gold)        | Las tres carpetas `data/` son el contrato fisico de las capas           |
| D-008 | StandardScaler dentro de sklearn.Pipeline                             | El pipeline Gold NO normaliza; la normalizacion va en trainer.py        |
| D-009 | pathlib.Path en `src/config.py` como unico gestor de rutas            | Todos los paths en `src/data/` se importan desde `config.py`           |

---

## 8. Contexto para el Siguiente Agente

La Phase Discovery esta completamente cerrada. En esta sesion se establecio la integracion con NotebookLM como parte del ritual de cierre. Puntos clave:

- **NotebookLM:** El notebook "Flores AI — Cerebro del Proyecto" (ID: `35c8760b-4797-4df2-8c91-cbf5b2df0240`) es la herramienta de consulta de gobernanza. El ID vive en `docs/references/config.md` seccion 4.2 como unica fuente de verdad.
- **Sincronizacion:** `decisions.md` debe re-sincronizarse al iniciar la proxima sesion (se modifico hoy). Los demas documentos en NotebookLM estan vigentes.
- **Agnosticismo:** Todos los agentes (21) y skills del proyecto son 100% agnosticos. Ninguno tiene IDs de proyecto hardcodeados. El skill `session-management/SKILL.md` lee el NOTEBOOK_ID desde `config.md`.
- **`docs/governance/specdd.md`** contiene las firmas exactas de cada funcion en `src/`.
- **`docs/governance/contract.md`** define los invariantes por capa: Bronze (6 cols + `Id`), Silver (147 filas, 5 cols, sin nulos), Gold (arrays NumPy).
- **`docs/governance/sad.md`** define la estructura de modulos. No se pueden crear `.py` fuera de esa jerarquia.
- **`docs/Phase_discovery/feasibility.md`** documenta los 3 near-duplicates a eliminar en Silver.

El primer paso de la sesion siguiente es ejecutar `ai-session-steward.start_session`.
