# Backlog del Proyecto: Flores AI - Iris

> **Fuente de verdad:** [CLAUDE.md](../../CLAUDE.md) | **Metodología:** [process.md](../methodology/process.md)
> **Proyecto:** Flores AI — Clasificación de especies Iris
> **Última actualización:** 2026-04-21
> **Responsable del backlog:** @ai-backlog-manager
> **Auditoría aplicada:** 2026-04-21 — correcciones de rutas (SAD §5), tarea config.py añadida, tareas REFACTOR atomizadas, citas SpecDD corregidas (§6–8), reference_stats.json añadido al DoD.

---

## FASE 1: Discovery — Línea Base Documental

**Entregable Principal:** Documentación de Gobernanza completa (config + BRD + Factibilidad + Mockup + SAD + SpecDD + Contract).
**Estado de Fase:** DONE ✅ — 2026-04-19

### Iteración 1.1: Configuración e Identidad del Proyecto

#### [F1-T01] Crear config.md
- **Responsable:** @config-manager
- **Iteración:** 1.1
- **Entregable:** `docs/references/config.md`
- **Acción:** Documentation
- **DoD:** El archivo existe con las 4 secciones mandatorias (Definición, Identidad, Estado, Fuentes). Todos los campos obligatorios tienen valor real (no placeholder).
- **Estado:** DONE ✅ — 2026-04-19

### Iteración 1.2: Documentación de Negocio

#### [F1-T02] Crear BRD (Business Requirements Document)
- **Responsable:** @ai-business-strategist
- **Iteración:** 1.2
- **Entregable:** `docs/governance/brd.md`
- **Acción:** Documentation
- **DoD:** BRD contiene objetivos de negocio, KPIs con thresholds definidos y criterios de aceptación verificables.
- **Estado:** DONE ✅ — 2026-04-19

### Iteración 1.3: Factibilidad y Diseño de Experiencia

#### [F1-T03] Ejecutar Análisis de Factibilidad
- **Responsable:** @ai-data-auditor
- **Iteración:** 1.3
- **Entregable:** `docs/Phase_discovery/feasibility.md`
- **Acción:** Documentation
- **DoD:** Reporte incluye diagnóstico de calidad de datos (completitud, distribución, outliers) y veredicto GO/NO-GO para continuar a Phase Engineering.
- **Estado:** DONE ✅ — 2026-04-19

#### [F1-T04] Crear Mockup de Interfaz
- **Responsable:** @ai-ux-designer
- **Iteración:** 1.3
- **Entregable:** `docs/Phase_discovery/mockup.md`
- **Acción:** Documentation
- **DoD:** Mockup aprobado por el Stakeholder principal. Cubre flujos principales de la aplicación.
- **Estado:** DONE ✅ — 2026-04-19 (aprobado por Stakeholder)

### Iteración 1.4: Arquitectura y Especificaciones Técnicas

#### [F1-T05] Crear SAD (Software Architecture Document)
- **Responsable:** @ai-solutions-architect
- **Iteración:** 1.4
- **Entregable:** `docs/governance/sad.md`
- **Acción:** Documentation
- **DoD:** SAD define el stack tecnológico, diagrama de arquitectura de 4 capas (Bronze/Silver/Gold/Model) y las interfaces entre componentes.
- **Estado:** DONE ✅ — 2026-04-19 (v1.0.0)

#### [F1-T06] Crear SpecDD (Specification-Driven Development)
- **Responsable:** @ai-solutions-architect
- **Iteración:** 1.4
- **Entregable:** `docs/governance/specdd.md`
- **Acción:** Documentation
- **DoD:** SpecDD contiene las firmas de todas las funciones `.py` del pipeline, contratos de entrada/salida y criterios de aceptación técnicos por módulo.
- **Estado:** DONE ✅ — 2026-04-19 (v1.0.0)

### Iteración 1.5: Contrato de Datos

#### [F1-T07] Crear Data Contract
- **Responsable:** @ai-data-auditor
- **Iteración:** 1.5
- **Entregable:** `docs/governance/contract.md`
- **Acción:** Documentation
- **DoD:** Contract define esquema de variables (tipo, rango, cardinalidad), reglas de validación matemáticas y criterios de rechazo de datos.
- **Estado:** DONE ✅ — 2026-04-19 (v1.0.0)

---

## FASE 2: Data & EDA — Feature Set Certificado

**Entregable Principal:** Dataset Gold certificado con features validadas estadísticamente.
**Estado de Fase:** IN PROGRESS — inicio 2026-04-20.

> Ciclo completo IA-TDD por capa: RED → GREEN → REFACTOR por iteración. CERTIFICACIÓN y VALIDACIÓN consolidan la fase antes de avanzar a Modeling.
> **Tarea atómica:** Un único responsable por tarea. Un único entregable por tarea.

### Iteración 2.0: Infraestructura Base

#### [F2-T00A] [RED] Suite de pruebas para `src/config.py`
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 2.0
- **Entregable:** `tests/unit/test_config.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada. Valida que las constantes del SpecDD §2 existen: `DATA_BRONZE`, `DATA_SILVER`, `DATA_GOLD_X`, `DATA_GOLD_Y`, `MODEL_PATH`, `FEEDBACK_LOG`, `RANDOM_STATE=42`, `TEST_SIZE=0.20`, `CV_FOLDS=5`, `CONFIDENCE_THRESHOLD=0.60`, `FEATURE_COLUMNS` (4 elementos), `CLASS_NAMES` (3 elementos). Ninguna constante de ruta es absoluta. Trazable al SpecDD §2 y SAD §5.
- **Estado:** DONE ✅ — 2026-04-21

#### [F2-T00B] [GREEN] Implementar `src/config.py`
- **Responsable:** @ai-data-engineer
- **Iteración:** 2.0
- **Entregable:** `src/config.py`
- **Acción:** Coding
- **DoD:** Pasa la suite F2-T00A. Expone todas las constantes definidas en el SpecDD §2. `PROJECT_ROOT` calculado con `pathlib.Path(__file__).resolve().parent.parent`. Sin importar pandas, sklearn, streamlit ni pydantic. Trazable al SpecDD §2 y SAD §5 (ADR-004).
- **Estado:** DONE ✅ — 2026-04-21

### Iteración 2.1: Ingesta y Capa Bronze

#### [F2-T01] [RED] Suite de pruebas para ingesta Bronze
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 2.1
- **Entregable:** `tests/unit/data/test_bronze_loader.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada (sin código productivo). Cubre los invariantes BR-01 a BR-04 del contract.md §10.2: shape `(150, 6)`, columnas exactas, tipos `int64`/`float64`/`object`, cero nulos, tres clases válidas en `Species`. Trazable al SpecDD §6 y contract.md §2.
- **Estado:** DONE ✅ — 2026-04-21

#### [F2-T02] [GREEN] Implementar pipeline de ingesta Bronze
- **Responsable:** @ai-data-engineer
- **Iteración:** 2.1
- **Entregable:** `src/data/bronze_loader.py`
- **Acción:** Coding
- **DoD:** Pasa la suite F2-T01. Carga el dataset Iris crudo retornando `pd.DataFrame (150, 6)`. Sin transformaciones sobre los datos. Trazable al SpecDD §6.
- **Estado:** DONE ✅ — 2026-04-21

#### [F2-T03a] [REFACTOR] Refactorizar `src/data/bronze_loader.py`
- **Responsable:** @ai-data-engineer
- **Iteración:** 2.1
- **Entregable:** `src/data/bronze_loader.py` (refactored)
- **Acción:** Refactoring
- **DoD:** Código con tipado estricto (type hints en todas las firmas), sin rutas absolutas (usa `config.DATA_BRONZE`), módulo importable sin efectos secundarios. Sin importar sklearn, streamlit ni pydantic. Todos los tests F2-T01 siguen en verde. Trazable al SpecDD §6 y SAD §5.1.
- **Estado:** DONE ✅ — 2026-04-21

#### [F2-T03b] [EDA] Reporte EDA Bronze
- **Responsable:** @ai-data-auditor
- **Iteración:** 2.1
- **Entregable:** `docs/Phase_engineering/eda_bronze.md`
- **Acción:** Documentation
- **DoD:** Reporte documenta completitud (0 nulos confirmados), distribución por feature (histogramas + estadísticas descriptivas) y outliers del dato crudo Bronze. Verifica los invariantes BR-01 a BR-04 del contract.md §2.2. Emite veredicto sobre la calidad del dato crudo.
- **Estado:** DONE ✅ — 2026-04-21

### Iteración 2.2: Limpieza y Capa Silver

#### [F2-T04] [RED] Suite de pruebas para transformación Silver
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 2.2
- **Entregable:** `tests/unit/data/test_silver_cleaner.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada. Cubre los invariantes SR-01 a SR-05 del contract.md §10.3: `len(df)==147`, columna `Id` ausente, nombres en snake_case, etiquetas sin prefijo `Iris-`, cero duplicados, cero nulos. Trazable al SpecDD §7 y contract.md §3.
- **Estado:** TODO

#### [F2-T05] [GREEN] Implementar pipeline de transformación Silver
- **Responsable:** @ai-analytics-engineer
- **Iteración:** 2.2
- **Entregable:** `src/data/silver_cleaner.py`
- **Acción:** Coding
- **DoD:** Pasa la suite F2-T04. Aplica las transformaciones M-01 a M-04 en orden. Genera dataset limpio `(147, 5)` en `data/silver/iris_silver.csv`. Trazable al SpecDD §7.
- **Estado:** TODO

#### [F2-T06a] [REFACTOR] Refactorizar `src/data/silver_cleaner.py`
- **Responsable:** @ai-analytics-engineer
- **Iteración:** 2.2
- **Entregable:** `src/data/silver_cleaner.py` (refactored)
- **Acción:** Refactoring
- **DoD:** Código modular con `RENAME_MAP` y `LABEL_MAP` como constantes de módulo (SpecDD §7). Sin rutas absolutas. Sin importar sklearn, streamlit ni pydantic. Todos los tests F2-T04 siguen en verde. Trazable al SpecDD §7 y SAD §5.1.
- **Estado:** TODO

#### [F2-T06b] [EDA] Reporte EDA Silver
- **Responsable:** @ai-data-auditor
- **Iteración:** 2.2
- **Entregable:** `docs/Phase_engineering/eda_silver.md`
- **Acción:** Documentation
- **DoD:** Reporte certifica ausencia de sesgo introducido por la limpieza. Incluye comparativa de distribución Bronze → Silver por feature. Verifica los invariantes SR-01 a SR-05 del contract.md §3.2. Confirma que las 3 transformaciones M-01 a M-04 no alteran la distribución estadística de las features.
- **Estado:** TODO

### Iteración 2.3: Feature Engineering y Capa Gold

#### [F2-T07] [RED] Suite de pruebas para capa Gold
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 2.3
- **Entregable:** `tests/unit/data/test_gold_builder.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada. Valida los invariantes GR-01 a GR-06 del contract.md §10.4: `X.shape==(147,4)`, `y.shape==(147,)`, `X.dtype==float64`, `np.isnan(X).sum()==0`, `np.isinf(X).sum()==0`, clases válidas en `y`. Verifica orden de columnas según `config.FEATURE_COLUMNS`. Trazable al SpecDD §8 y contract.md §4.
- **Estado:** TODO

#### [F2-T08] [GREEN] Implementar Feature Store (Gold Layer)
- **Responsable:** @ai-feature-store-architect
- **Iteración:** 2.3
- **Entregable:** `src/data/gold_builder.py`
- **Acción:** Coding
- **DoD:** Pasa la suite F2-T07. Genera `data/gold/X_gold.csv` y `data/gold/y_gold.csv`. Orden de columnas en `X` sigue `config.FEATURE_COLUMNS`. Trazable al SpecDD §8.
- **Estado:** TODO

#### [F2-T09a] [REFACTOR] Refactorizar `src/data/gold_builder.py`
- **Responsable:** @ai-feature-store-architect
- **Iteración:** 2.3
- **Entregable:** `src/data/gold_builder.py` (refactored)
- **Acción:** Refactoring
- **DoD:** Código con transformaciones deterministas. Sin target leakage: `species` no puede figurar en `X`. Orden de columnas explícito vía `config.FEATURE_COLUMNS`. Sin rutas absolutas. Todos los tests F2-T07 siguen en verde. Trazable al SpecDD §8 y SAD §5.1.
- **Estado:** TODO

#### [F2-T09b] [EDA] Reporte EDA Gold + `reference_stats.json`
- **Responsable:** @ai-data-auditor
- **Iteración:** 2.3
- **Entregables:** `docs/Phase_engineering/eda_gold.md`, `data/gold/reference_stats.json`
- **Acción:** Documentation
- **DoD:** Reporte valida correlaciones (matriz de correlación vs. referencia del contract.md §8.3), varianza por feature y separabilidad de clases. Confirma ausencia de target leakage en `X`. Verifica invariantes GR-01 a GR-06. Genera `data/gold/reference_stats.json` con estadísticas de referencia (contract.md §11.1) para uso futuro en drift detection.
- **Estado:** TODO

### Iteración 2.4: Certificación y Validación de Fase

#### [F2-T10] [CERTIFICACIÓN] Certificar linaje completo Bronze → Silver → Gold
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 2.4
- **Entregable:** `docs/Phase_engineering/certification_f2.md`
- **Acción:** Documentation
- **DoD:** Reporte certifica trazabilidad total de datos (Bronze → Silver → Gold), cumplimiento del SAD §5 y del SpecDD §6–8. Todos los tests de la fase (F2-T01, F2-T04, F2-T07) pasan en conjunto con `pytest tests/unit/data/`. Sin rutas absolutas ni dependencias no declaradas en `requirements.txt`.
- **Estado:** TODO

#### [F2-T11] [VALIDACIÓN] Validar dataset Gold contra KPIs del BRD
- **Responsable:** @ai-data-scientist
- **Iteración:** 2.4
- **Entregable:** `docs/Phase_engineering/validation_f2.md`
- **Acción:** Documentation
- **DoD:** Reporte verifica que el Feature Set Gold cumple los thresholds de calidad definidos en el BRD. Incluye veredicto GO/NO-GO explícito para avanzar a Fase 3 (Modeling).
- **Estado:** TODO

---

## FASE 3: Modeling — Modelo Predictivo Certificado

**Entregable Principal:** Modelo de clasificación Iris serializado, certificado y registrado.
**Estado de Fase:** TODO — pendiente Phase Engineering.

> Tareas pendientes de atomización desde SpecDD §3.x. Se poblará al completar Phase Engineering.

### Iteración 3.1: Entrenamiento y Selección de Modelo

#### [F3-T01] [RED] Desarrollar suite de pruebas para entrenamiento
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 3.1
- **Entregable:** `tests/test_model_training.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada. Valida shapes, tipos de salida y reproducibilidad.
- **Estado:** TODO

#### [F3-T02] [GREEN] Entrenar y serializar modelo baseline
- **Responsable:** @ai-data-scientist
- **Iteración:** 3.1
- **Entregable:** `notebooks/03_model_selection.ipynb`, `models/iris_model.joblib`
- **Acción:** Coding
- **DoD:** Pasa F3-T01. Accuracy ≥ threshold BRD. Modelo serializado con Joblib.
- **Estado:** TODO

### Iteración 3.2: Validación y Certificación del Modelo

#### [F3-T03] Ejecutar Model QA (Benchmarking + Sesgo)
- **Responsable:** @ai-model-qa-validator
- **Iteración:** 3.2
- **Entregable:** `docs/Phase_modeling/model_qa_report.md`
- **Acción:** Testing
- **DoD:** Reporte incluye métricas por clase, matriz de confusión, análisis de sesgo y veredicto GO/NO-GO.
- **Estado:** TODO

---

## FASE 4: Delivery — Sistema en Producción con Monitoreo

**Entregable Principal:** API + Aplicación Streamlit desplegada y monitoreada.
**Estado de Fase:** TODO — pendiente Phase Modeling.

> Tareas pendientes de atomización desde SpecDD §4.x. Se poblará al completar Phase Modeling.

### Iteración 4.1: API de Inferencia

#### [F4-T01] [RED] Desarrollar suite de pruebas para API
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 4.1
- **Entregable:** `tests/test_api.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada. Cubre contrato de entrada (Pydantic), latencia y manejo de errores.
- **Estado:** TODO

#### [F4-T02] [GREEN] Implementar API de inferencia (FastAPI/Streamlit)
- **Responsable:** @ai-backend-engineer
- **Iteración:** 4.1
- **Entregable:** `src/api/app.py`
- **Acción:** Coding
- **DoD:** Pasa F4-T01. Interfaz Streamlit operativa. Trazable al SpecDD §4.1.
- **Estado:** TODO

### Iteración 4.2: Contenedorización y Certificación E2E

#### [F4-T03] Contenedorizar sistema completo
- **Responsable:** @ai-mlops-cloud-architect
- **Iteración:** 4.2
- **Entregable:** `infra/Dockerfile`, `infra/docker-compose.yml`
- **Acción:** Coding
- **DoD:** Imagen Docker construye sin errores. Sistema arranca con `docker-compose up`.
- **Estado:** TODO

#### [F4-T04] Ejecutar pruebas E2E y certificar sistema
- **Responsable:** @ai-full-stack-sdet
- **Iteración:** 4.2
- **Entregable:** `docs/Phase_delivery/e2e_certification.md`
- **Acción:** Testing
- **DoD:** Reporte E2E con resultado PASS en todos los flujos críticos. Sistema certificado para producción.
- **Estado:** TODO
