# mockup.md — Visual Prototype v1.0
## Proyecto: Flores AI - Iris

> **Documento:** Visual Mockup & UX Design Rationale
> **Version:** 1.0.0
> **Estado:** Entregado — Pendiente aprobacion UAT
> **Fecha:** 2026-04-19
> **Autor:** ai-ux-designer
> **Stakeholder:** jdrodriguez1000@gmail.com
> **Archivo del prototipo:** `docs/Fase_1/mockup/index.html`

---

## 1. Localizacion del Artefacto

| Artefacto | Ruta relativa |
|:----------|:--------------|
| Prototipo interactivo (HTML) | `docs/Fase_1/mockup/index.html` |
| Este documento | `docs/Fase_1/mockup.md` |

Para visualizar el prototipo, abrir `docs/Fase_1/mockup/index.html` directamente en cualquier navegador web moderno (Chrome, Edge, Firefox). No requiere servidor ni dependencias externas.

---

## 2. Resumen del Prototipo

El prototipo es un archivo HTML autocontenido de alta fidelidad que simula la aplicacion Streamlit completa con cuatro estados de pantalla navegables. Todos los datos son estaticos (hardcoded). No existe conexion a backend, modelo, ni archivos externos. Todo es una ilusión visual controlada.

### Estados cubiertos

| # | ID de pantalla | Descripcion | User Story relacionada |
|:--|:--------------|:------------|:----------------------|
| 1 | `s-initial` | Estado inicial — formulario de entrada con 4 sliders | US-03 (validacion de rangos visible) |
| 2 | `s-success` | Resultado exitoso — especie predicha con alta confianza (97.3%) | US-01, US-02 |
| 3 | `s-lowconf` | Resultado de baja confianza — advertencia prominente (52.4%) | US-01 (criterio de confianza < 60%) |
| 4 | `s-error` | Error de validacion — campos invalidos con mensajes descriptivos | US-03 |

---

## 3. Descripcion Detallada de Cada Pantalla

### Pantalla 1 — Estado Inicial

El usuario llega a la aplicacion y ve un formulario limpio con los cuatro controles deslizantes (sliders), uno por cada medida de la flor. El diseno prioriza la claridad: cada slider muestra el valor actual en grande, el rango valido como hint, y las etiquetas extremas del eje.

Componentes presentes:
- Barra lateral con logo, guia de medicion ilustrada (SVG botanico), y rangos de referencia.
- Cuatro controles de entrada (sepal_length, sepal_width, petal_length, petal_width).
- Boton principal "Predecir Especie".
- Pie de pagina con metadatos del modelo.

Dato hardcoded de ejemplo: Setosa tipica (5.1, 3.5, 1.4, 0.2 cm).

### Pantalla 2 — Resultado Exitoso

Se muestra luego de una prediccion con alta confianza (>= 60%). El resultado es prominente, legible a un vistazo, sin necesidad de conocimiento tecnico.

Componentes presentes:
- Badge "Alta confianza" en el encabezado.
- Tarjeta de resultado con: ilustracion SVG de la especie (Iris setosa en tonos verdes), nombre en italica, clasificacion taxonomica, barra de confianza al 97.3%.
- Grafico de probabilidades por clase (barras horizontales con colores diferenciados: verde Setosa, azul Versicolor, violeta Virginica).
- Boton "Nueva prediccion" para reiniciar.
- Boton "Esta prediccion es incorrecta" para feedback (BRD seccion 12.1).
- Panel lateral con resumen de las entradas usadas.

Dato hardcoded: Setosa con 97.3% / Versicolor 2.1% / Virginica 0.6%.

### Pantalla 3 — Baja Confianza

Misma estructura que el resultado exitoso, pero el sistema detecta que la confianza maxima < 60% y activa el estado de advertencia. El tono visual cambia a ambar/dorado para comunicar incertidumbre sin bloquear al usuario.

Componentes presentes:
- Badge "Baja confianza" en color ambar.
- Alerta de advertencia encima del resultado: texto "Resultado de baja confianza. Verifique las medidas ingresadas."
- Tarjeta de resultado con barra de confianza en degradado ambar (52.4%).
- Ilustracion SVG de Iris versicolor en tonos azules.
- Grafico de probabilidades mostrando la ambiguedad: Versicolor 52.4%, Virginica 42.6%, Setosa 5.0%.
- Nota explicativa debajo del grafico sobre la superposicion Versicolor/Virginica.
- Boton "Reingresar medidas" como CTA principal.

Dato hardcoded: medidas en zona de superposicion (5.8, 2.7, 4.1, 1.0 cm).

### Pantalla 4 — Error de Validacion

El usuario ha ingresado valores fuera de rango. El sistema no ejecuta la prediccion: bloquea el boton y senala exactamente que campos estan mal y por que, sin exponer ningun stack trace de Python.

Componentes presentes:
- Badge "Entradas invalidas" en rojo.
- Alerta de error en la parte superior: "2 campos con valores invalidos" con instruccion clara.
- Cuatro sliders: dos en estado normal (verde), dos en estado de error (rojo) con hint de error especifico debajo de cada uno.
  - Sepal width: 0.8 cm < minimo 1.5 cm.
  - Petal length: 9.5 cm > maximo 8.0 cm.
- Boton "Predecir Especie" deshabilitado (opacidad 40%, cursor not-allowed) con texto explicativo.
- Panel lateral con rangos de referencia para ayudar al usuario a corregir.

---

## 4. Justificacion de Decisiones de UX

### 4.1 Dark Mode como base

El modo oscuro fue seleccionado como predeterminado por tres razones:
1. Streamlit soporta natively dark mode y es la preferencia comun en aplicaciones tecnicas/cientificas.
2. Mejora la legibilidad de graficos de colores (verde/azul/violeta) sobre fondo oscuro con mayor contraste.
3. Reduce la fatiga visual en sesiones de analisis prolongadas.

### 4.2 Paleta botanica restringida

Se usaron tres colores semanticos asignados permanentemente a las tres especies:
- Verde (#4caf62) para Setosa: especie mas facil de identificar, asociada con naturaleza simple.
- Azul (#58a6ff) para Versicolor: color intermedio, frecuente en flores reales de esta especie.
- Violeta (#bc8cff) para Virginica: especie mas compleja, tono diferenciado que evita confusion visual con Setosa.

Esta asignacion es consistente en todas las pantallas y el grafico de barras, reduciendo la carga cognitiva del usuario.

### 4.3 Sidebar persistente

La barra lateral cumple dos funciones simultaneas:
1. Navegacion (acceso al clasificador e historial).
2. Referencia contextual: la guia de medicion ilustrada y los rangos validos estan siempre visibles, sin necesidad de que el usuario los busque. Esto atiende directamente el supuesto SA3 del BRD: "el usuario entiende como medir en cm".

### 4.4 Ilustraciones SVG inline

Se usaron ilustraciones SVG embebidas (no imagenes externas) para:
1. Funcionar sin conexion a internet (ambiente local).
2. Escalar sin perdida de calidad a cualquier resolucion.
3. Ser personalizables por codigo (color por especie).

Las ilustraciones son esquematicas y botanicamente aproximadas (3 petalos + 3 sepalos + centro), suficientes para que un usuario no botanico comprenda de que planta se trata.

### 4.5 Boton deshabilitado en estado de error

En lugar de mostrar un mensaje de error despues de hacer clic en "Predecir", el prototipo deshabilita el boton proactivamente mientras existan errores. Esto sigue el principio de "fail fast and visibly" y elimina un ciclo de frustracion del usuario.

### 4.6 Grafico de barras horizontales para probabilidades

El grafico de barras horizontales fue preferido sobre un grafico de pie por:
1. Mayor precision visual para comparar valores cercanos (ej. 52.4% vs 42.6%).
2. Las etiquetas de porcentaje son legibles en barras horizontales sin superposicion.
3. Es el componente mas natural en Streamlit (`st.bar_chart` o `st.altair_chart`).

### 4.7 Escala de colores para comunicar confianza

- Alta confianza: barra verde brillante, badge verde.
- Baja confianza: barra ambar, badge ambar, alerta visible.
- Error: rojo en sliders afectados, badge rojo, boton bloqueado.

Este sistema de semaforo (verde/ambar/rojo) es intuitivo para usuarios sin formacion tecnica.

---

## 5. Mapa de Componentes UI a User Stories

| Componente UI | Pantalla(s) | User Story | Requisito BRD |
|:--------------|:-----------|:-----------|:--------------|
| 4 sliders numericos con labels y rangos | 1, 4 | US-03 | Seccion 8, Tabla de rangos |
| Badge de estado en encabezado | 1, 2, 3, 4 | US-01, US-03 | Seccion 8 |
| Tarjeta de resultado con nombre de especie | 2, 3 | US-01 | Seccion 5.2, paso 4(a) |
| Barra de confianza (porcentaje grafico) | 2, 3 | US-01 | Seccion 8 US-01: "probabilidad de confianza (en porcentaje)" |
| Alerta de baja confianza (ambar) | 3 | US-01 | Criterio de confianza: "Si probabilidad < 60%, mostrar advertencia" |
| Grafico de barras de probabilidades 3 clases | 2, 3 | US-02 | Seccion 8 US-02: "grafico de barras o similar" |
| Ilustracion SVG de la especie predicha | 2, 3 | US-01 | Restriccion de diseno: "referencia visual de la especie predicha" |
| Alerta de error rojo con mensaje descriptivo | 4 | US-03 | Seccion 8 US-03: "mensaje de error descriptivo (no stack trace)" |
| Sliders en estado de error (rojo) con hint | 4 | US-03 | Seccion 8 US-03: "valores fuera de rango" |
| Boton deshabilitado al haber errores | 4 | US-03 | Seccion 8 US-03: proteccion proactiva |
| Boton "Esta prediccion es incorrecta" | 2, 3 | Feedback BRD | Seccion 12.1: registro en logs/feedback.log |
| Panel lateral con guia de medicion | 1, 4 | US-01 soporte | Supuesto SA3 del BRD |
| Panel lateral con rangos validos | 1, 4 | US-03 soporte | Seccion 8, Tabla de rangos |

---

## 6. Notificacion al Backlog Manager

Los siguientes elementos visuales del prototipo implican logica de implementacion no trivial en fases posteriores:

| Elemento visual | Complejidad de implementacion | Tarea futura sugerida |
|:----------------|:------------------------------|:----------------------|
| Barra de confianza dinamica | Media — depende de `predict_proba()` del modelo | Fase 3: conectar output del modelo a la UI |
| Grafico de probabilidades por clase | Media — usar `st.bar_chart` o Altair | Fase 4: implementar componente de visualizacion |
| Validacion de rangos en tiempo real | Baja-Media — logica if/else en Streamlit | Fase 4: implementar `validate_inputs()` en `src/app.py` |
| Ilustraciones SVG de especies | Baja — activos estaticos | Fase 4: incluir como archivos en `src/assets/` |
| Boton de feedback con log | Baja-Media — escribir a `logs/feedback.log` | Fase 4: implementar `record_feedback()` en `src/app.py` |
| Alerta de baja confianza (threshold 60%) | Baja — condicional simple | Fase 4: constante `CONFIDENCE_THRESHOLD = 0.60` en config |
| Sidebar con historial de predicciones | Media-Alta — requiere estado de sesion | Fuera de alcance v1.0 (OUT OF SCOPE) |

---

## 7. Instrucciones para el Stakeholder (UAT)

Para validar el prototipo:

1. Abrir el archivo `docs/Fase_1/mockup/index.html` en su navegador (doble clic o arrastrar al navegador).
2. Navegar entre los 4 estados usando los botones en la barra superior.
3. Verificar que cada pantalla representa correctamente el comportamiento esperado segun las User Stories del BRD.
4. Proporcionar feedback a jdrodriguez1000@gmail.com con aprobacion o cambios solicitados.

Criterio de aprobacion: el Stakeholder confirma por escrito que las 4 pantallas reflejan el comportamiento esperado descrito en las US-01, US-02 y US-03 del BRD v1.0.

---

## 8. Firmas

| Rol | Responsable | Estado | Fecha |
|:----|:-----------|:-------|:------|
| Autor del mockup | ai-ux-designer | Entregado | 2026-04-19 |
| Aprobacion de diseno | Stakeholder (jdrodriguez1000@gmail.com) | Pendiente UAT | Por definir |

---

> **Nota de Gobernanza:** Este artefacto es el entregable de la tarea de prototipado de la Fase 1. Su aprobacion por el Stakeholder es prerequisito para el inicio de la Fase 2 (EDA y preprocesamiento de datos). Cualquier cambio solicitado debe registrarse en el decisions.md antes de ser implementado.
