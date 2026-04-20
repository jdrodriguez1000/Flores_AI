# config.md: Cédula de Identidad del Proyecto

> **Definición del Documento**
> Este archivo es la instancia local del protocolo general definido en [CLAUDE.md](../../CLAUDE.md).
> Contiene los metadatos específicos del proyecto actual y actúa como fuente de verdad para
> todos los agentes especializados. Ningún agente debe operar sin leer este archivo primero.
>
> **Fecha de creación:** 2026-04-19
> **Última actualización:** 2026-04-19

---

## 1. Identidad del Proyecto

| Campo                    | Valor                                                                 |
| :----------------------- | :-------------------------------------------------------------------- |
| **Nombre Oficial**       | Flores AI - Iris                                                      |
| **Alias / Nombre Corto** | Flores_ai                                                             |
| **Propietario**          | Empresa Flores AI                                                     |
| **Stakeholder Principal**| jdrodriguez1000@gmail.com                                             |
| **Fecha de Inicio**      | 2026-04-19                                                            |

### Descripcion del Proyecto

Construir un modelo de machine learning que, dadas cuatro dimensiones fisicas de una flor Iris
(sepal length, sepal width, petal length, petal width), prediga con exactitud a cual de las tres
especies pertenece (Setosa, Versicolor, Virginica). Ademas, construir una aplicacion web que dadas
las cuatro dimensiones muestre el tipo de especie predicha.

---

## 2. Estado del Proyecto

| Campo                  | Valor                          |
| :--------------------- | :----------------------------- |
| **Fase Actual**        | Fase 1 - Discovery             |
| **Hito Activo**        | Fase 1 completada — todos los entregables de gobernanza entregados. Próximo: iniciar Fase 2 |
| **Progreso Estimado**  | 40% (Fase 1 al 100%) |
| **Estado**             | En curso                       |

### Mapa de Fases

| Fase   | Nombre          | Estado      | Notas                          |
| :----- | :-------------- | :---------- | :----------------------------- |
| Fase 1 | Discovery       | Completada (100%) | Todos los entregables completados — 2026-04-19 |
| Fase 2 | Data & EDA      | Pendiente   |                                |
| Fase 3 | Modeling        | Pendiente   |                                |
| Fase 4 | Deployment      | Pendiente   |                                |

---

## 3. Stack Tecnologico

| Componente              | Tecnologia                    | Estado          | Notas                               |
| :---------------------- | :---------------------------- | :-------------- | :---------------------------------- |
| **Lenguaje**            | Python 3.12+                  | Confirmado      | Segun protocolo CLAUDE.md           |
| **Aplicacion Web**      | Streamlit                     | Confirmado      | Interfaz de prediccion de especies  |
| **Librerias ML**        | scikit-learn (Pipeline, StandardScaler, clasificadores) | Confirmado (SAD ADR-001) | Se implementara en Fase 2 |
| **Librerias de Datos**  | pandas, NumPy                 | Confirmado (SAD)| Se implementara en Fase 2           |
| **Validacion**          | Pydantic v2                   | Confirmado (SpecDD) | Contratos de frontera entre modulos |
| **Testing**             | Por definir                   | Pendiente       | Se definira segun necesidades       |
| **Serializacion**       | Joblib                        | Confirmado (SAD ADR-002) | `models/iris_model.joblib` |

> **Nota:** El archivo `requirements.txt` es la unica fuente de verdad para librerias instaladas.
> Se actualizara cada vez que se incorpore una nueva dependencia.

---

## 4. Fuentes de Verdad

### 4.1 Repositorio de Codigo

| Campo           | Valor                                            |
| :-------------- | :----------------------------------------------- |
| **Plataforma**  | GitHub                                           |
| **URL**         | https://github.com/jdrodriguez1000/Flores_AI.git |
| **Rama Main**   | main                                             |
| **Rama Dev**    | dev                                             |

### 4.2 Fuentes Externas Adicionales

| Tipo                 | ID / URL       | Descripcion                     | Estado    |
| :------------------- | :------------- | :------------------------------ | :-------- |
| NotebookLM           | No definido    | Sin fuente externa por definir  | Pendiente |
| Documentacion externa| No definida    | Sin fuente externa por definir  | Pendiente |

> **Nota:** Esta tabla se actualizara cuando se incorporen nuevas fuentes externas al proyecto.

---

## 5. Estructura del Repositorio

Estructura de carpetas mandatoria segun CLAUDE.md:

```
Flores_AI/
├── CLAUDE.md                      # Constitución del proyecto
├── docs/
│   ├── Fase_1/                    # Reporte de Factibilidad (FEASIBILITY)
│   ├── Fase_2/                    # EDAs: Ingesta, Limpieza, Analisis
│   ├── Fase_3/                    # Validacion de Modelos (MODEL QA)
│   ├── Fase_4/                    # Certificados E2E y Stress Testing
│   ├── governance/                # BACKLOG, BRD, SAD, SpecDD, CONTRACT
│   └── references/                # handoff, decisions, config
├── src/                           # Codigo fuente productivo (.py)
├── data/
│   ├── bronze/                    # Datos crudos (raw)
│   ├── silver/                    # Datos limpios
│   └── gold/                      # Features para modelado
├── models/                        # Artefactos de modelos certificados
├── notebooks/                     # Investigacion y experimentacion (.ipynb)
├── tests/                         # Suite de pruebas (Unit, Integration, E2E, QA)
└── infra/                         # Infraestructura como Codigo (Docker, etc.)
```

---

## 6. Documentos de Gobernanza

| Documento       | Ruta de Destino              | Estado      |
| :-------------- | :--------------------------- | :---------- |
| BACKLOG         | docs/governance/             | Completado - 2026-04-19 |
| BRD             | docs/governance/             | Completado - 2026-04-19 |
| SAD             | docs/governance/             | Completado - 2026-04-19 (v1.0.0) |
| SpecDD          | docs/governance/             | Completado - 2026-04-19 (v1.0.0) |
| contract        | docs/governance/             | Completado - 2026-04-19 (v1.0.0) |
| mockup          | docs/Fase_1/                 | Completado y aprobado por Stakeholder - 2026-04-19 (v1.0.0) |
| FEASIBILITY     | docs/Fase_1/                 | Completado - 2026-04-19 |
| handoff         | docs/references/             | Completado - 2026-04-19 |
| decisions       | docs/references/             | Completado - 2026-04-19 |

---

## 7. Historial de Actualizaciones

| Fecha       | Accion                              | Responsable        |
| :---------- | :---------------------------------- | :----------------- |
| 2026-04-19  | Creacion inicial del archivo        | project-config     |
| 2026-04-19  | BRD completado y estado actualizado | ai-business-strategist |
| 2026-04-19  | FEASIBILITY completado y estado actualizado | ai-data-auditor |
| 2026-04-19  | handoff y decisions creados; progreso actualizado a 25% | ai-session-steward |
| 2026-04-19  | sad, specdd y contract completados; progreso actualizado a 30% | ai-solutions-architect |
| 2026-04-19  | mockup aprobado por Stakeholder; progreso actualizado a 35%; stack tecnologico ampliado con Joblib y Pydantic v2 | ai-session-steward |
| 2026-04-19  | backlog.md creado (F1-T08 DONE); Fase 1 completada al 100%; progreso global actualizado a 40% | ai-backlog-manager |
