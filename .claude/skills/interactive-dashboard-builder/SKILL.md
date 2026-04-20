---
name: interactive-dashboard-builder
description: Protocolo para el desarrollo de interfaces de usuario (Streamlit, React, Next.js) que permitan la interacción fluida con modelos de IA y visualización de datos.
user-invocable: false
agent: ai-frontend-engineer
allowed-tools: [Read, Write, Edit, Bash, Python-Interpreter]
---

## 🏗️ I. Diseño de la Arquitectura de UI
El agente debe construir el punto de entrada para el usuario final:
1. **Flujo de Carga de Datos:** Implementar componentes para subir archivos (CSV/Excel) o formularios de entrada manual con validación visual inmediata.
2. **Visualización de Resultados:** Diseñar paneles que presenten las predicciones de forma clara, priorizando la información crítica (ej: Predict Score).
3. **Responsive Design:** Asegurar que el dashboard sea utilizable en diferentes dispositivos (Desktop/Tablet) según el requisito del cliente.

## 📐 II. Integración con el Backend
1. **Consumo de API:** Implementar la lógica para llamar a los endpoints de la Fase 4, manejando estados de carga (`loading`) y errores técnicos de forma elegante.
2. **Visualización de Logs de Proceso:** Mostrar al usuario el progreso de las tareas asíncronas (ej: "Limpiando datos...", "Calculando predicción...").

## 🚀 III. Prototipado Rápido vs. Producción
1. **Streamlit (Discovery):** Uso de componentes estándar para validación rápida con stakeholders.
2. **Next.js / Tailwind (Producción):** Implementación de interfaces de alta fidelidad, con micro-animaciones y diseño premium según el manual de marca.

---

> **Check de Certificación de UI:**
> - [ ] ¿La interfaz permite completar el flujo de predicción de punta a punta?
> - [ ] ¿Se manejan correctamente los errores de red y de validación del backend?
> - [ ] ¿El diseño es intuitivo para un usuario que no conoce de ciencia de datos?
