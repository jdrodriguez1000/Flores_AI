---
name: xai-visualizer-specialist
description: Protocolo para la visualización de la explicabilidad del modelo (XAI) mediante componentes gráficos que faciliten la interpretación de predicciones.
user-invocable: false
agent: ai-frontend-engineer
allowed-tools: [Read, Write, Edit, Python-Interpreter]
---

## 🏗️ I. Representación Visual de SHAP/Importance
El agente debe traducir los números del Data Scientist en gráficos comprensibles:
1. **Barras de Contribución:** Mostrar qué variables empujaron la predicción hacia arriba o hacia abajo (ej: Rojo para negativo, Verde para positivo).
2. **Semáforos de Confianza:** Implementar indicadores visuales basados en la probabilidad del modelo (ej: Verde > 80%, Amarillo 50-80%, Rojo < 50%).
3. **Tooltips de Explicación:** Traducir nombres técnicos de variables (ej: `feat_income_log`) a lenguaje de negocio (ej: "Nivel de Ingresos Mensuales").

## 📐 II. Narrativa Predictiva
1. **Compresión de Complejidad:** Ocultar variables de baja importancia para evitar la sobrecarga cognitiva del usuario.
2. **Comparativa Local vs. Global:** Mostrar cómo se compara el caso actual con el promedio del historial del modelo.

## 🚀 III. Interactividad en la Explicación
1. **Análisis What-if:** Permitir que el usuario cambie un valor en la UI (ej: aumentar el precio) y ver en tiempo real cómo cambia la explicación del modelo.

---

> **Check de Certificación de XAI:**
> - [ ] ¿Los gráficos de explicabilidad coinciden con los datos entregados por el backend?
> - [ ] ¿El usuario final puede entender por qué el modelo tomó una decisión específica?
> - [ ] ¿Se han traducido los términos técnicos a conceptos de negocio?
