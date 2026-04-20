---
name: session-management
description: Protocolo para la gestión sincronizada de apertura y cierre de sesiones de trabajo mediante Handoffs y Logs de Decisiones.
user-invocable: false
agent: ai-session-steward
allowed-tools: [Read, Write, Edit, Bash]
---

# Skill: Gestión de Sesión (Session Management)

Esta habilidad instrumenta los rituales definidos en **CLAUDE.md** para garantizar que la transición entre estados de desarrollo sea fluida, auditable y sin pérdida de contexto.

## Funciones

### 1. Ritual de Apertura (Session Kickoff)
**Acción:** `start_session`
- Lee `docs/references/HANDOFF.md` para recuperar el estado operativo.
- Lee `docs/references/DECISIONS_LOG.md` para asimilar el historial de decisiones y lecciones aprendidas.
- Lee `docs/references/PROJECT_config.md` para verificar la fase activa y los IDs de fuentes externas.
- Genera un **Briefing de Inicio** que resuma: "Dónde nos quedamos", "Lecciones clave para hoy", "Qué bloqueos tenemos" y "Cuál es la Tarea #1".

### 2. Ritual de Cierre (Session Wrap-up)
**Acción:** `close_session`
- **Generación de Handoff Operativo:** Sobrescribe `docs/references/HANDOFF.md` con:
    - **Logros:** Entregables terminados en la sesión.
    - **Pendientes:** Tareas en curso o no iniciadas.
    - **Bloqueadores:** Falta de acceso, dudas de negocio o fallas técnicas.
    - **Próximos Pasos:** Hoja de ruta para la sesión inmediata.
- **Actualización de Memoria Histórica:** Añade una entrada (Appended) en `docs/references/DECISIONS_LOG.md` con:
    - **Fecha:** Timestamp de la sesión.
    - **Fase:** Fase activa según el config.
    - **Decisiones:** Justificación de cambios estructurales o lógicos.
    - **Learnings:** Lecciones aprendidas (técnicas de datos, errores resueltos, etc.).

## Criterios de Éxito
✅ **Continuidad Cognitiva:** Un nuevo agente debe ser capaz de retomar el trabajo leyendo únicamente el `HANDOFF.md`.
✅ **Trazabilidad de Decisiones:** Cualquier cambio en el SAD o SpecDD debe tener una entrada correspondiente en el `DECISIONS_LOG.md`.
✅ **Higiene de Archivos:** Las carpetas `docs/references/` contienen archivos actualizados y sin inconsistencias.

## Reglas Técnicas
- **Formato Mandatorio:** Los archivos deben usar Markdown con tablas o listas para máxima legibilidad.
- **Append strictly:** El `DECISIONS_LOG.md` nunca se sobrescribe; los nuevos registros se agregan al final con separadores claros.
- **Validation:** Antes de cerrar, el agente debe preguntar al usuario si hay algún "Insight" adicional que desee capturar para las lecciones aprendidas.
