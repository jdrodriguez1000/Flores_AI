---
name: ux-feedback-loop-designer
description: Protocolo para la gestión del estado de la aplicación y la captura de feedback del usuario para la mejora continua del modelo.
user-invocable: false
agent: ai-frontend-engineer
allowed-tools: [Read, Write, Edit, Python-Interpreter]
---

## 🏗️ I. Captura de "Ground Truth" Humano
El agente debe diseñar los mecanismos para que el usuario aprenda del modelo y viceversa:
1. **Botón de Reporte de Error:** Implementar un flujo para que el usuario marque una predicción como incorrecta, enviando la metadata al MLOps.
2. **Formulario de Corrección:** Permitir que el usuario edite los datos sugeridos por el modelo (ej: corregir una categoría mal imputada).
3. **Encuestas de Utilidad:** Capturar si la predicción fue útil para la toma de decisiones del negocio.

## 📐 II. Gestión de Estado Global (App State)
1. **Persistencia Local:** Guardar preferencias del usuario y resultados recientes para agilizar la navegación.
2. **Sincronización con el Backend:** Asegurar que los cambios realizados por el usuario se guarden correctamente en la base de datos de auditoría.

## 🚀 III. Notificaciones de Eventos Predicitivos
1. **Alertas en Tiempo Real:** Implementar notificaciones (Push/Toast) cuando un proceso asíncrono finaliza o cuando el modelo detecta un caso crítico.

---

> **Check de Certificación de Feedback:**
> - [ ] ¿Existe un mecanismo claro para reportar discrepancias en el modelo?
> - [ ] ¿El feedback del usuario se está enviando al backend con el contexto completo?
> - [ ] ¿La navegación entre estados de la aplicación es fluida y coherente?
