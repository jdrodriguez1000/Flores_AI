# handoff.md: Estado Operativo del Proyecto

> **Definicion del Documento**
> Este archivo es la foto nítida y actual del proyecto. Es sobrescribible al cierre de cada sesion.
> Un nuevo agente debe poder retomar el trabajo leyendo unicamente este archivo.
>
> **Ultima actualizacion:** 2026-04-20
> **Responsable de cierre:** ai-session-steward
> **Fase activa:** Phase Discovery — CERRADA | Proxima: Phase Engineering - Data & EDA

---

## 1. Resumen de Estado

| Campo               | Valor                                                                    |
| :------------------ | :----------------------------------------------------------------------- |
| **Proyecto**        | Flores AI - Iris                                                         |
| **Fase Actual**     | Phase Discovery — COMPLETADA AL 100%                                     |
| **Iteracion**       | Sesion de ajustes de gobernanza y nomenclatura (2026-04-20)              |
| **Estado General**  | Gobernanza normalizada. Nomenclatura de fases y carpetas estandarizada.  |
| **Progreso Global** | 40% — Phase Engineering pendiente de inicio                              |

---

## 2. Logros de la Sesion (2026-04-20 — Ajustes de Gobernanza)

| # | Entregable / Accion | Archivos Afectados | Estado |
| :- | :------------------ | :----------------- | :----- |
| 1 | Renombrado de carpetas de fases: `Fase_1→Phase_discovery`, `Fase_2→Phase_engineering`, `Fase_3→Phase_modeling`, `Fase_4→Phase_delivery` | `docs/Phase_discovery/`, `docs/Phase_engineering/`, `docs/Phase_modeling/`, `docs/Phase_delivery/` | Completado |
| 2 | Actualizacion masiva de referencias en 52 archivos (agentes, skills, governance, metodologia, CLAUDE.md) | Todos los `.md` del proyecto | Completado |
| 3 | Carpeta `mockup/` movida a la raiz del proyecto (desde `docs/Phase_discovery/mockup/`) | `mockup/index.html` | Completado |
| 4 | Referencias al mockup actualizadas en 5 archivos | `mockup.md`, `handoff.md`, `config.md`, `ui-ux-prototyping/SKILL.md`, `repository-governance/SKILL.md` | Completado |
| 5 | `ai_process.md` actualizado: agente `ai-ux-designer` añadido a Phase Discovery (seccion 2), ruta de mockup corregida en tabla de artefactos, entrada `mockup/` añadida a Regla de Oro | `docs/methodology/ai_process.md` | Completado |
| 6 | `AGENTS.md` creado en la raiz del proyecto: catalogo agnostico con 21 agentes, organizados por fase, con descripcion de cuando usarlos y skills asociados | `AGENTS.md` | Completado |

---

## 3. Estado Actual de Entregables de Gobernanza (Phase Discovery — COMPLETA)

| Documento      | Ruta                                              | Estado                                   |
| :------------- | :------------------------------------------------ | :--------------------------------------- |
| config.md      | `docs/references/config.md`                       | DONE — 2026-04-19                        |
| brd.md         | `docs/governance/brd.md`                          | DONE — 2026-04-19                        |
| feasibility.md | `docs/Phase_discovery/feasibility.md`             | DONE — 2026-04-19                        |
| mockup         | `mockup/index.html` + `docs/Phase_discovery/mockup.md` | DONE — 2026-04-19 (aprobado Stakeholder) |
| sad.md         | `docs/governance/sad.md`                          | DONE — 2026-04-19 (v1.0.0)              |
| specdd.md      | `docs/governance/specdd.md`                       | DONE — 2026-04-19 (v1.0.0)              |
| contract.md    | `docs/governance/contract.md`                     | DONE — 2026-04-19 (v1.0.0)              |
| AGENTS.md      | `AGENTS.md` (raiz)                                | DONE — 2026-04-20 (nuevo)               |

---

## 4. Estructura de Carpetas Vigente (Post-Ajuste)

```
Flores_AI/
├── AGENTS.md                        ← NUEVO: catalogo maestro de agentes
├── CLAUDE.md
├── mockup/                          ← MOVIDO: prototipo visual (antes en docs/Phase_discovery/)
│   └── index.html
├── docs/
│   ├── governance/                  (BRD, SAD, SpecDD, contract, backlog)
│   ├── methodology/                 (ai_process.md — actualizado)
│   ├── Phase_discovery/             ← RENOMBRADO (antes Fase_1)
│   ├── Phase_engineering/           ← RENOMBRADO (antes Fase_2)
│   ├── Phase_modeling/              ← RENOMBRADO (antes Fase_3)
│   ├── Phase_delivery/              ← RENOMBRADO (antes Fase_4)
│   └── references/                  (config, handoff, decisions)
└── .claude/
    ├── agents/                      (21 agentes actualizados)
    └── skills/                      (skills actualizados)
```

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

**Ninguno.** La Phase Discovery esta formalmente cerrada y la gobernanza esta completamente normalizada. El proyecto puede iniciar Phase Engineering sin dependencias externas pendientes.

**Pendiente menor (tarea 9):** Enlazar documentos con NotebookLM (ajuste #9 de `ajustes.txt`) quedó pendiente para la proxima sesion.

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

La Phase Discovery esta completamente cerrada y la gobernanza fue normalizada en esta sesion. Puntos clave:

- **Nomenclatura de fases:** Las carpetas usan ahora `Phase_discovery`, `Phase_engineering`, `Phase_modeling`, `Phase_delivery`. Todos los documentos estan actualizados.
- **Mockup:** `mockup/index.html` en la raiz es la referencia visual oficial aprobada por el Stakeholder.
- **AGENTS.md:** Nuevo archivo en la raiz con el catalogo completo de 21 agentes.
- **`docs/governance/specdd.md`** contiene las firmas exactas de cada funcion en `src/`.
- **`docs/governance/contract.md`** define los invariantes por capa: Bronze (6 cols + `Id`), Silver (147 filas, 5 cols, sin nulos), Gold (arrays NumPy).
- **`docs/governance/sad.md`** define la estructura de modulos. No se pueden crear `.py` fuera de esa jerarquia.
- **`docs/Phase_discovery/feasibility.md`** documenta los 3 near-duplicates a eliminar en Silver.

El primer paso de la sesion siguiente es ejecutar `ai-session-steward.start_session`.
