# CLAUDE.md: Protocolos de Ingeniería de IA y Ciencia de Datos

Este archivo define las convenciones y protocolos agnósticos para Claude Code en proyectos de **Ciencia de Datos, Machine Learning e Ingeniería de IA**, siguiendo las metodologías **SpecDD** (Specification-Driven Development) y **TDD** (Test-Driven Development).

Para configuración específica del proyecto actual (nombre, stack, IDs), consulta siempre **[docs/references/config.md](docs/references/config.md)**.

Seguir la metodologia de trabajo para proyectos de ciencia de datos y machine learning, qeu se encuentra en el archivo **[ai_process.md](docs/methodology/ai_process.md)**.
---

## 🎯 1. Directivas Fundamentales

### Mentalidad de Auditor (Devil's Advocate)
Cuestiona proactivamente la factibilidad de los datos, la lógica de los KPIs y la arquitectura del modelo. **Rechaza tareas sin criterios de aceptación técnicos (Thresholds) definidos.** 

### Soberanía Documental (SpecDD)
El código productivo (`.py`) es un reflejo estricto de la especificación técnica. **Cada línea de código traza a: TAREA → SpecDD → SAD (Arquitectura) → BRD.** Se prohíbe la improvisación de lógica de limpieza o modelado fuera del flujo documentado.

### Separación de Entornos (Notebook vs. Production)
*   **Notebooks (`notebooks/`):** Espacio de R&D, descubrimiento y descarte de hipótesis algorítmicas. No requieren código "grado producción" pero deben ser legibles y estar documentados.
*   **Módulos (`src/`):** Código industrializado, modular, con tipado estricto y siguiendo los contratos del SpecDD. **Solo el código en `src/` entra en el pipeline de despliegue.**

### Cadena de Confianza y Linaje
Toda transformación de datos y entrenamiento de modelos debe ser reproducible. Se debe mantener el linaje: **VERSIÓN DE DATOS (Gold) → VERSIÓN DE CÓDIGO (src) → VERSIÓN DE MODELO (models).**

### Higiene del Entorno Técnico
*   **Versión:** Uso obligatorio de **Python 3.12+**.
*   **Aislamiento:** Todo desarrollo debe realizarse dentro de un **Ambiente Virtual** (`venv` o `conda`).
*   **Dependencias:** El archivo **`requirements.txt`** es la única fuente de verdad para librerías. Debe actualizarse inmediatamente al instalar nuevas dependencias.
*   **Portabilidad:** Se prohíbe el uso de rutas absolutas. Todo enlace en documentos y toda referencia en el código debe utilizar **rutas relativas** respecto a la raíz del proyecto para garantizar la movilidad total del repositorio.

---

## 📂 2. Estándar de Almacenamiento y Gobernanza

Para garantizar la organización y trazabilidad, se sigue esta jerarquía de carpetas obligatoria:

| Directorio   | Propósito                                   | Regla de Oro                                                 |
| :----------- | :------------------------------------------ | :----------------------------------------------------------- |
| `docs/`             | Documentación técnica y de negocio oficial. | Segmentado por fases (`Phase_discovery` a `Phase_delivery`).                  |
| `docs/design-system/` | Sistema de diseño del cliente (Brand).    | **Fuente de verdad de UI.** Obligatorio leer antes de generar cualquier interfaz. Contiene tokens de color, tipografía, reglas de componentes y referencia visual. |
| `src/`              | Código fuente productivo (.py).             | Modularizado según el SAD (Ingesta, Modelado, API).          |
| `data/`             | Almacenamiento de datos.                    | Estructura Bronze (crudo), Silver (limpio), Gold (features). |
| `models/`           | Artefactos de modelos serializados.         | Solo modelos certificados (ONNX, Pickle, Joblib).            |
| `notebooks/`        | Investigación y experimentación.            | Archivos `.ipynb` documentados y numerados.                  |
| `tests/`            | Suite de pruebas técnicas.                  | Unit, Integration, E2E y Model QA.                           |
| `infra/`            | Infraestructura como Código (IaC).          | Scripts de Docker, Terraform o K8s.                          |

---

## 📝 3. Documentos de Gobernanza (Alineados con ai_process.md)

| Documento       | Ubicación          | Propósito                                                 |
| :-------------- | :----------------- | :-------------------------------------------------------- |
| **BACKLOG**     | `docs/governance/` | Orquestación de tareas (Fases > Iteraciones > Tareas).    |
| **BRD**         | `docs/governance/` | Business Requirements Document: Objetivos y KPIs.         |
| **SAD**         | `docs/governance/` | Software Architecture Document: Stack y Diseño técnico.   |
| **SpecDD**      | `docs/governance/` | Especificación de Interfaces: Contratos y firmas `.py`.   |
| **CONTRACT**    | `docs/governance/` | Contrato de Datos: Validaciones matemáticas de variables. |
| **FEASIBILITY** | `docs/Phase_discovery/`     | Reporte de Factibilidad: Diagnóstico de salud de datos.   |
| **EDAs**        | `docs/Phase_engineering/`     | Reportes de Ingesta, Limpieza y Análisis Estadístico.     |
| **MODEL QA**    | `docs/Phase_modeling/`     | Validación de Modelos: Benchmarking y Sesgo.              |
| **QA SYSTEM**   | `docs/Phase_delivery/`     | Certificados E2E y Stress Testing.                        |
| **HANDOFF**     | `docs/references/` | Estado Operativo diario (sobrescribible).                 |
| **DECISIONS**   | `docs/references/` | Log histórico de decisiones y lecciones.                  |

---

## 🧪 4. Ciclo de Desarrollo: IA-TDD

Todo desarrollo sigue el ciclo **Red-Green-Refactor-Certificación-Validación**:

1.  **RED (Test Fallido):** Escribir el test (código o datos) antes de la lógica.
2.  **GREEN (Funcionalidad):** Escribir código mínimo para pasar el test.
3.  **REFACTOR (Calidad):** Optimización técnica y cumplimiento del linaje.
4.  **CERTIFICACIÓN (Técnica):** Validación contra SAD & SpecDD.
5.  **VALIDACIÓN (Negocio):** Verificación final contra el BRD y KPIs.

---

## 🏗️ 5. Protocolo de Control de Cambios (CC)

Obligatorio cuando se detecta una desviación de los documentos de gobernanza.

1.  **Detección:** Parada inmediata del código ante lógica no documentada.
2.  **Ficha de CC:** Generar ID, Justificación e Impacto Transversal.
3.  **Autorización:** Esperar "APROBADO" explícito del usuario.
4.  **Efecto Cascada:** Actualizar Gobernanza -> Modificar Código.

---

## 🌳 6. Protocolo de Gestión de Versiones (Git)

### Soberanía de Ramas
*   `main` / `dev` protegidas. PR obligatorio.
*   `feat/F[1-4]-<nombre>`: Nuevas funcionalidades.
*   `fix/F[1-4]-<nombre>`: Correcciones técnicos/datos.

### Commits Semánticos (Foco DS/ML)
*   `feat(data):` Transformaciones en Bronze/Silver/Gold.
*   `feat(model):` Ajustes en entrenamiento o arquitectura.
*   `test(qa):` Validaciones de datos y tests unitarios.
*   `docs(f-X):` Cambios en documentación de la fase X.

---

## ⚙️ 7. Escuadrón de Agentes Especializados

*   **ai-repository-governor:** Auditor de higiene del repo y Git.
*   **ai-session-steward:** Gestor de continuidad y Handoff.
*   **ai-change-manager:** Juez de integridad y Control de Cambios.
*   **ai-backlog-manager:** Orquestador de Tareas, Iteraciones y DoD.

---

## 🕒 8. Rituales de Sesión

### Ritual de Apertura (Session Kickoff)
1.  **Sincronización:** Ejecutar `ai-session-steward.start_session`.
2.  **Lectura Obligatoria:** `handoff.md`, `decisions.md`, `backlog.md` y `config.md`.
3.  **Priorización:** Seleccionar la siguiente tarea atómica del Backlog.

### Ritual de Cierre (Session Wrap-up)
1.  **Commit:** Versionar el progreso con mensaje semántico.
2.  **Validación:** Asegurar que los tests sean verdes.
3.  **Handoff:** Actualizar `handoff.md` (Logros, Pendientes, Bloqueos).
4.  **Memoria:** Registrar en `decisions.md` (Decisiones, Lecciones).
