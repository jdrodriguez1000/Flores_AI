# Backlog del Proyecto: Flores AI - Iris

> **Fuente de verdad:** [CLAUDE.md](../../CLAUDE.md) | **Metodología:** [ai_process.md](../methodology/ai_process.md)
> **Proyecto:** Flores AI — Clasificación de especies Iris
> **Última actualización:** 2026-04-19
> **Responsable del backlog:** @ai-backlog-manager

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
**Estado de Fase:** TODO — pendiente inicio tras Phase Discovery completada.

> Tareas pendientes de atomización desde SpecDD y Contract. Se poblará al iniciar Phase Engineering.

### Iteración 2.1: Ingesta y Capa Bronze

#### [F2-T01] [RED] Desarrollar suite de pruebas para ingesta Bronze
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 2.1
- **Entregable:** `tests/test_bronze_ingestion.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada (sin código productivo). Cubre: schema, tipos, rangos del Contract.
- **Estado:** TODO

#### [F2-T02] [GREEN] Implementar pipeline de ingesta Bronze
- **Responsable:** @ai-data-engineer
- **Iteración:** 2.1
- **Entregable:** `src/ingestion/bronze_loader.py`
- **Acción:** Coding
- **DoD:** Pasa la suite F2-T01. Carga el dataset Iris crudo a `data/bronze/`. Trazable al SpecDD §2.1.
- **Estado:** TODO

### Iteración 2.2: Limpieza y Capa Silver

#### [F2-T03] [RED] Desarrollar suite de pruebas para transformación Silver
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 2.2
- **Entregable:** `tests/test_silver_transform.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada. Cubre: imputación, outliers, tipos del Contract.
- **Estado:** TODO

#### [F2-T04] [GREEN] Implementar pipeline de transformación Silver
- **Responsable:** @ai-analytics-engineer
- **Iteración:** 2.2
- **Entregable:** `src/processing/silver_transformer.py`
- **Acción:** Coding
- **DoD:** Pasa la suite F2-T03. Genera dataset limpio en `data/silver/`. Trazable al SpecDD §2.2.
- **Estado:** TODO

### Iteración 2.3: Feature Engineering y Capa Gold

#### [F2-T05] [RED] Desarrollar suite de pruebas para capa Gold
- **Responsable:** @ai-data-qa-engineer
- **Iteración:** 2.3
- **Entregable:** `tests/test_gold_features.py`
- **Acción:** Testing
- **DoD:** Suite falla de forma controlada. Valida ausencia de target leakage y distribución de features.
- **Estado:** TODO

#### [F2-T06] [GREEN] Implementar Feature Store (Gold Layer)
- **Responsable:** @ai-feature-store-architect
- **Iteración:** 2.3
- **Entregable:** `src/features/gold_builder.py`
- **Acción:** Coding
- **DoD:** Pasa la suite F2-T05. Genera dataset en `data/gold/`. Trazable al SpecDD §2.3.
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
