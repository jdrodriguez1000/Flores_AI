# handoff.md: Estado Operativo del Proyecto

> **Definicion del Documento**
> Este archivo es la foto nitida y actual del proyecto. Es sobrescribible al cierre de cada sesion.
> Un nuevo agente debe poder retomar el trabajo leyendo unicamente este archivo.
>
> **Ultima actualizacion:** 2026-04-20
> **Responsable de cierre:** ai-session-steward
> **Fase activa:** Phase Engineering — Data & EDA (IN PROGRESS)

---

## 1. Resumen de Estado

| Campo               | Valor                                                                              |
| :------------------ | :--------------------------------------------------------------------------------- |
| **Proyecto**        | Flores AI - Iris                                                                   |
| **Fase Actual**     | Phase Engineering — Data & EDA (iniciada 2026-04-20)                              |
| **Rama activa**     | `feat/F2-engineering`                                                              |
| **Iteracion**       | Integracion de capa BDD al ecosistema de gobernanza (2026-04-20)                  |
| **Estado General**  | BDD integrado al pipeline de gobernanza. Contrato de comportamiento (behavior.md) creado y alineado con SpecDD v1.0.0. Nuevo skill gherkin-scenario-author disponible. Backlog F2 listo para iniciar F2-T01. |
| **Progreso Global** | 42% — Phase Discovery cerrada al 100%. Phase Engineering en curso (gobernanza BDD completada, implementacion pendiente). |

---

## 2. Logros de la Sesion (2026-04-20 — Integracion BDD)

| # | Entregable / Accion | Archivos Afectados | Estado |
| :- | :------------------ | :----------------- | :----- |
| 1 | Creacion de `docs/governance/behavior.md` (BDD Contract v1.0.0) con 10 escenarios Gherkin para US-01 (Clasificacion), US-02 (Probabilidades) y US-03 (Validacion de entradas). | `docs/governance/behavior.md` | Completado |
| 2 | Creacion de `.claude/skills/gherkin-scenario-author/SKILL.md`: nueva habilidad para traducir User Stories en escenarios Gherkin (Given/When/Then). | `.claude/skills/gherkin-scenario-author/SKILL.md` | Completado |
| 3 | Actualizacion de `docs/methodology/ai_process.md`: Gherkin Authoring añadido al rol del `ai-business-strategist`, behavior.md en tabla de artefactos Phase Discovery, jerarquia BDD en seccion 5, referencia a behavior.md como fuente de verdad E2E en Phase Delivery. | `docs/methodology/ai_process.md` | Completado |
| 4 | Actualizacion de `docs/governance/BRD.md`: escenarios Gherkin añadidos a US-01, US-02 y US-03; nueva seccion 9.4 vinculando BDD con Criterios de Aceptacion. | `docs/governance/BRD.md` | Completado |
| 5 | Actualizacion de `CLAUDE.md`: jerarquia `BRD → BDD → SpecDD → TDD` documentada en Soberania Documental; fila BEHAVIOR en tabla de gobernanza; seccion 4 renombrada a "SpecDD + BDD + TDD" con tabla de 3 capas. | `CLAUDE.md` | Completado |
| 6 | Actualizacion de `.claude/agents/ai-business-strategist.md`: skill gherkin-scenario-author añadido; 4 nuevos triggers BDD; regla de oro #5 "BDD Before Code". | `.claude/agents/ai-business-strategist.md` | Completado |
| 7 | Commit semantico: `feat(f-2): integrate BDD layer with Gherkin contract and update governance artifacts` (`3d4bb87`). | Rama `feat/F2-engineering` | Completado |

---

## 3. Estado Actual de Entregables de Gobernanza

| Documento      | Ruta                                              | Estado                                   |
| :------------- | :------------------------------------------------ | :--------------------------------------- |
| config.md      | `docs/references/config.md`                       | DONE — 2026-04-20                        |
| brd.md         | `docs/governance/brd.md`                          | DONE — 2026-04-20 (v1.1: escenarios BDD añadidos) |
| behavior.md    | `docs/governance/behavior.md`                     | DONE — 2026-04-20 (v1.0.0 — NUEVO)      |
| feasibility.md | `docs/Phase_discovery/feasibility.md`             | DONE — 2026-04-19                        |
| mockup         | `mockup/index.html` + `docs/Phase_discovery/mockup.md` | DONE — 2026-04-20 (alineado con design system) |
| sad.md         | `docs/governance/sad.md`                          | DONE — 2026-04-19 (v1.0.0)              |
| specdd.md      | `docs/governance/specdd.md`                       | DONE — 2026-04-19 (v1.0.0) — SIN CAMBIOS BDD |
| contract.md    | `docs/governance/contract.md`                     | DONE — 2026-04-19 (v1.0.0)              |
| design-system  | `docs/design-system/`                             | DONE — 2026-04-20                       |
| backlog.md     | `docs/governance/backlog.md`                      | DONE — 2026-04-20 (F2 expandido a 11 tareas, ciclo IA-TDD completo) |
| AGENTS.md      | `AGENTS.md` (raiz)                                | DONE — 2026-04-20                        |

---

## 4. Fuentes en NotebookLM (Estado al Cierre)

**Notebook:** "Flores AI — Cerebro del Proyecto"
**ID:** `35c8760b-4797-4df2-8c91-cbf5b2df0240`

| Documento        | Ruta Local                                      | Estado en NotebookLM |
| :--------------- | :---------------------------------------------- | :------------------- |
| ai_process.md    | `docs/methodology/ai_process.md`               | Pendiente re-sincronizacion (modificado en esta sesion) |
| brd.md           | `docs/governance/brd.md`                        | Pendiente re-sincronizacion (modificado en esta sesion) |
| behavior.md      | `docs/governance/behavior.md`                   | Pendiente carga inicial (archivo nuevo en esta sesion) |
| sad.md           | `docs/governance/sad.md`                        | Cargado — 2026-04-20 |
| specdd.md        | `docs/governance/specdd.md`                     | Cargado — 2026-04-20 |
| contract.md      | `docs/governance/contract.md`                   | Cargado — 2026-04-20 |
| feasibility.md   | `docs/Phase_discovery/feasibility.md`           | Cargado — 2026-04-20 |
| decisions.md     | `docs/references/decisions.md`                  | Pendiente re-sincronizacion (entrada #9 añadida en esta sesion) |

> **Accion requerida al inicio de la proxima sesion:** Sincronizar en NotebookLM los siguientes documentos modificados en esta sesion: `ai_process.md`, `brd.md`, `decisions.md` (re-sincronizar) y `behavior.md` (carga inicial). Ver patron de actualizacion en `.claude/skills/session-management/SKILL.md`.

---

## 5. Proximos Pasos — Phase Engineering: Iteracion 2.1 (Bronze)

| Prioridad | ID Tarea | Descripcion | Responsable | Entregable |
| :-------- | :------- | :---------- | :---------- | :--------- |
| 1 (CRITICA) | F2-T01 | [RED] Desarrollar suite de pruebas para ingesta Bronze | @ai-data-qa-engineer | `tests/test_bronze_ingestion.py` |
| 2 | F2-T02 | [GREEN] Implementar pipeline de ingesta Bronze | @ai-data-engineer | `src/ingestion/bronze_loader.py`, `data/bronze/` |
| 3 | F2-T03 | [REFACTOR] Refactorizar Bronze + EDA tecnico post-ingesta | @ai-data-engineer + @ai-data-auditor | `src/ingestion/bronze_loader.py` (refactored), `docs/Phase_engineering/eda_bronze.md` |

**Prerequisito de implementacion:** Antes de escribir cualquier codigo en `src/`, leer:
- `docs/governance/specdd.md` (firmas mandatorias de `bronze_loader.py`)
- `docs/governance/contract.md` (invariantes por capa: Bronze tiene 6 columnas incluyendo `Id`, 150 filas, sin nulos)
- `docs/governance/sad.md` (estructura de modulos `src/ingestion/`)
- `docs/governance/behavior.md` (escenarios BDD como contrato observable — fuente de verdad para tests RED)

---

## 6. Bloqueos Activos

**Ninguno.** La capa BDD esta completamente integrada en la gobernanza. El SpecDD v1.0.0 no requirio cambios (el objeto `PredictionResult` ya cubre el 100% de los escenarios BDD). La siguiente accion es ejecutar F2-T01 (RED): escribir la suite de tests para Bronze guiandose por `behavior.md` y `contract.md`.

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
| D-016 | `docs/design-system/` como convencion agnostica de marca del cliente  | Los agentes de UI leen esta carpeta antes de generar cualquier interfaz |
| D-019 | "No-Line Rule": bordes explicitos prohibidos en contenedores de la UI | El mockup y la app Streamlit no deben usar `border` en divs contenedores |
| D-020 | Tokens semanticos (no colores hardcodeados) en toda la UI             | Todos los estados de la app usan tokens del Design System               |
| D-025 | Jerarquia BDD: BRD → behavior.md → SpecDD → TDD                      | behavior.md es el contrato de comportamiento observable antes de escribir tests RED |
| D-026 | SpecDD v1.0.0 no requiere cambios post-BDD                            | PredictionResult cubre el 100% de los escenarios BDD — linaje garantizado desde Phase Discovery |

---

## 8. Contexto para el Siguiente Agente

La Phase Discovery esta completamente cerrada y mergeada a `dev` via PR #1. La Phase Engineering esta en curso con la capa BDD completamente integrada. Puntos clave:

- **Rama activa:** `feat/F2-engineering`. Ultimo commit: `3d4bb87` — integracion BDD.
- **Gobernanza BDD completa:** `docs/governance/behavior.md` define 10 escenarios ejecutables para las 3 User Stories. El `ai-data-qa-engineer` debe usarlo como entrada principal para los tests RED de F2-T01.
- **SpecDD sin cambios:** `PredictionResult` ya expone `species`, `confidence`, `probabilities` y `low_confidence`. Cero deuda tecnica de interfaz.
- **Nuevo skill disponible:** `.claude/skills/gherkin-scenario-author/SKILL.md` — para cualquier nueva User Story que se añada en el futuro.
- **NotebookLM pendiente:** Al inicio de la proxima sesion, sincronizar `ai_process.md`, `brd.md` y cargar `behavior.md` por primera vez. Re-sincronizar `decisions.md`.
- **Orden de lectura obligatorio antes de F2-T01:** `behavior.md` (contrato BDD) → `specdd.md` (firmas de `bronze_loader.py`) → `contract.md` (invariantes capa Bronze) → `sad.md` (estructura de modulos).

El primer paso de la sesion siguiente es ejecutar `ai-session-steward.start_session`.
