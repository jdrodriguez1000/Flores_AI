---
name: repository-governance
description: Protocolo técnico para la organización, limpieza y gestión de versiones de un repositorio de Ciencia de Datos e IA.
user-invocable: false
agent: ai-repository-governor
allowed-tools: [Read, Write, Edit, Bash]
---

# Skill: Gobernanza de Repositorio (Repository Governance)

Esta habilidad instrumenta las reglas de **CLAUDE.md** y la metodología de 4 fases para garantizar que el repositorio sea un activo técnico de alta calidad.

## Funciones Principales

### 1. Bootstrap de Estructura Industrial
**Acción:** `initialize_repo`
- Crea las carpetas raíz: `docs/Fase_1..4`, `src/`, `data/Bronze..Gold`, `models/`, `notebooks/`, `tests/`, `infra/`.
- Crea el `.gitignore` estándar para DS (excluyendo `.csv`, `.parquet`, `.pkl`, `.h5`, `.env`, `__pycache__`, etc.).
- Crea un `README.md` base con la ficha técnica del proyecto.

### 2. Auditoría de Higiene Git
**Acción:** `audit_git_health`
- **Check Large Files:** Escanea el área de *stage* buscando archivos > 10MB. Si existen, sugiere DVC o eliminación.
- **Check Notebooks:** Verifica si los `.ipynb` tienen la celda de output poblada. Si es así, ejecuta `nbstripout` o pide al usuario limpiar antes de commitear.
- **Check Branches:** Valida que la rama actual siga el patrón `feat/F[1-4]-<nombre>` o `fix/...`.

### 3. Orquestación de Commits y PRs
**Acción:** `semantic_commit_manager`
- Valida que el mensaje de commit empiece con: `feat(data):`, `feat(model):`, `feat(api):`, `test(qa):`, `docs(f-X):`.
- Genera el borrador del Pull Request vinculándolo a los documentos de la Fase activa (ej: "Resolves tasks defined in SAD.md").

### 4. Cumplimiento de Linaje (Fase 3)
**Acción:** `verify_lineage_link`
- Asegura que al commitear un cambio en `src/`, se reporte si hay un impacto en la versión del modelo certificada en `models/`.

## Criterios de Éxito
✅ **Zero-Binary Policy:** Git solo contiene código, documentación y configuraciones pequeñas.
✅ **Clean Diffs:** Los Notebooks no generan diffs ruidosos por metadatos o salidas de celdas.
✅ **Trazabilidad Fase-Rama:** Es posible saber a qué fase pertenece cada línea de código por el nombre de la rama de origen.

## Reglas Técnicas
- **Nbstripout:** El uso de herramientas de limpieza de notebooks es mandatorio antes de cualquier merge a `dev` o `main`.
- **Pre-commit Checks:** Todas las validaciones de esta habilidad deben reportarse como un checklist al usuario antes de proceder con el comando Git final.
