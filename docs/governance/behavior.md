# Behavior Specifications (BDD Contract)
## Proyecto: Flores AI - Iris

> **Documento:** Contrato de Comportamiento BDD
> **Version:** 1.0.0
> **Estado:** Aprobado - Phase Discovery
> **Fecha de creacion:** 2026-04-20
> **Ultima actualizacion:** 2026-04-20
> **Autor:** ai-business-strategist
> **Skill utilizado:** `gherkin-scenario-author`
> **Trazabilidad:** BRD v1.0.0 → behavior.md v1.0.0 → SpecDD v1.0.0
> **Fuente de verdad para:** ai-data-qa-engineer (Phase Engineering) · ai-full-stack-sdet (Phase Delivery)

---

## Jerarquia de Especificacion

```
BRD (Intencion) → BDD/Gherkin (Comportamiento) → TDD (Correccion del codigo)
```

Este documento define el comportamiento observable esperado del sistema Flores AI - Iris ante entradas especificas. Cada escenario es un contrato ejecutable: si el sistema no cumple un escenario, el ciclo TDD no puede declararse en verde para esa funcionalidad.

---

## Feature: Clasificacion Automatica de Especies Iris

### US-01: Clasificacion de Especie

El sistema clasifica correctamente la especie de una flor Iris a partir de cuatro medidas fisicas y advierte cuando la confianza es baja.

```gherkin
Escenario: Clasificacion exitosa de Iris Setosa
  Dado que el usuario ingresa sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2
  Cuando el usuario hace clic en "Predecir Especie"
  Entonces el sistema muestra "setosa" como especie predicha
  Y la confianza mostrada es mayor o igual al 60%
  Y no se muestra ninguna advertencia de baja confianza

Escenario: Clasificacion exitosa de Iris Versicolor
  Dado que el usuario ingresa sepal_length=6.0, sepal_width=2.7, petal_length=5.1, petal_width=1.6
  Cuando el usuario hace clic en "Predecir Especie"
  Entonces el sistema muestra "versicolor" como especie predicha
  Y la confianza mostrada es mayor o igual al 60%

Escenario: Clasificacion exitosa de Iris Virginica
  Dado que el usuario ingresa sepal_length=6.3, sepal_width=3.3, petal_length=6.0, petal_width=2.5
  Cuando el usuario hace clic en "Predecir Especie"
  Entonces el sistema muestra "virginica" como especie predicha
  Y la confianza mostrada es mayor o igual al 60%

Escenario: Advertencia de baja confianza en caso ambiguo
  Dado que el usuario ingresa sepal_length=5.9, sepal_width=3.0, petal_length=4.8, petal_width=1.8
  Cuando el usuario hace clic en "Predecir Especie"
  Y la confianza de la prediccion es menor al 60%
  Entonces el sistema muestra el mensaje "Resultado de baja confianza. Verifique las medidas ingresadas."
  Y el campo low_confidence del resultado es True
  Y el sistema muestra igualmente la especie predicha
```

---

### US-02: Visualizacion de Probabilidades por Clase

El sistema muestra la distribucion de probabilidad para las tres especies simultaneamente, no solo la clase ganadora.

```gherkin
Escenario: Visualizacion completa de probabilidades tras una prediccion
  Dado que el usuario ingresa sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2
  Cuando el usuario hace clic en "Predecir Especie"
  Entonces el sistema muestra un grafico con tres barras: setosa, versicolor y virginica
  Y la barra de mayor altura corresponde a la especie predicha
  Y la suma de las tres probabilidades mostradas es igual a 1.0 (tolerancia: 1e-6)

Escenario: Coherencia entre probabilidad maxima y especie predicha
  Dado que el modelo predice "setosa" con confidence=0.97
  Entonces la probabilidad mostrada para "setosa" es 0.97
  Y las probabilidades de "versicolor" y "virginica" suman 0.03
  Y la barra de "setosa" es la mas alta del grafico
```

---

### US-03: Validacion de Entradas Invalidas

El sistema rechaza entradas fuera de rango y comunica el error de forma clara sin exponer trazas tecnicas de Python.

```gherkin
Escenario: Rechazo de sepal_length por encima del rango maximo
  Dado que el usuario ingresa sepal_length=15.0, sepal_width=3.5, petal_length=1.4, petal_width=0.2
  Cuando el usuario hace clic en "Predecir Especie"
  Entonces el sistema muestra un mensaje de error en color rojo
  Y el mensaje indica que sepal_length esta fuera del rango permitido [3.0, 9.0] cm
  Y el mensaje no contiene las palabras "Traceback", "ValueError" ni rutas de archivo .py

Escenario: Rechazo de petal_width con valor negativo
  Dado que el usuario ingresa sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=-1.0
  Cuando el usuario hace clic en "Predecir Especie"
  Entonces el sistema muestra un mensaje de error en color rojo
  Y el mensaje indica que petal_width esta fuera del rango permitido [0.0, 3.5] cm
  Y el sistema no realiza ninguna llamada al modelo

Escenario: Aceptacion de valores en el limite inferior del rango
  Dado que el usuario ingresa sepal_length=3.0, sepal_width=1.5, petal_length=0.5, petal_width=0.0
  Cuando el usuario hace clic en "Predecir Especie"
  Entonces el sistema NO muestra ninguna advertencia de rango
  Y el sistema procesa la prediccion y muestra un resultado

Escenario: Aceptacion de valores en el limite superior del rango
  Dado que el usuario ingresa sepal_length=9.0, sepal_width=5.5, petal_length=8.0, petal_width=3.5
  Cuando el usuario hace clic en "Predecir Especie"
  Entonces el sistema NO muestra ninguna advertencia de rango
  Y el sistema procesa la prediccion y muestra un resultado
```

---

## Trazabilidad BDD → Criterios de Aceptacion

| Escenario | US Origen | CA Relacionados |
| :--- | :--- | :--- |
| Clasificacion exitosa de Iris Setosa | US-01 | CA01, CA02, CA08 |
| Clasificacion exitosa de Iris Versicolor | US-01 | CA01, CA02, CA08 |
| Clasificacion exitosa de Iris Virginica | US-01 | CA01, CA02, CA08 |
| Advertencia de baja confianza en caso ambiguo | US-01 | CA07, CA08 |
| Visualizacion completa de probabilidades | US-02 | CA08 |
| Coherencia entre probabilidad maxima y especie predicha | US-02 | CA08, CA11 |
| Rechazo de sepal_length por encima del rango maximo | US-03 | CA07 |
| Rechazo de petal_width con valor negativo | US-03 | CA07 |
| Aceptacion de valores en el limite inferior del rango | US-03 | CA07 |
| Aceptacion de valores en el limite superior del rango | US-03 | CA07 |

---

## Nota de Alineacion con SpecDD

El objeto `PredictionResult` en `src/predictor.py` (SpecDD v1.0.0, Seccion 1.2) cubre todos los estados requeridos por este contrato. No se requieren cambios al SpecDD v1.0.0.

| Campo de PredictionResult | Escenarios BDD que lo requieren |
| :--- | :--- |
| `species: str` | Todos los escenarios de US-01 y US-02 |
| `confidence: float` | Escenario de baja confianza (US-01), Coherencia de probabilidades (US-02) |
| `probabilities: dict[str, float]` | Ambos escenarios de US-02 |
| `low_confidence: bool` | Escenario de advertencia de baja confianza (US-01) |

---

> **Nota de Gobernanza:** Este documento es el Contrato de Comportamiento del proyecto Flores AI - Iris. El `ai-data-qa-engineer` usa este contrato como entrada para disenar los tests RED en la Phase Engineering. El `ai-full-stack-sdet` usa este contrato para validar los tests E2E en la Phase Delivery. Cualquier nueva User Story debe pasar por el protocolo `gherkin-scenario-author` antes de ser implementada. El `ai-business-strategist` es el unico agente con autoridad para modificar este documento.
