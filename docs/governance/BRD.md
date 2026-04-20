# Business Requirements Document (BRD)
## Proyecto: Flores AI - Iris

> **Documento:** Business Requirements Document (BRD)
> **Version:** 1.0.0
> **Estado:** Aprobado - Fase 1 Discovery
> **Fecha de creacion:** 2026-04-19
> **Ultima actualizacion:** 2026-04-19
> **Autor:** ai-business-strategist
> **Stakeholder Principal:** jdrodriguez1000@gmail.com
> **Repositorio:** https://github.com/jdrodriguez1000/Flores_AI.git

---

## Indice

1. [Contexto y Problema de Negocio](#1-contexto-y-problema-de-negocio)
2. [Objetivo de Negocio](#2-objetivo-de-negocio)
3. [Objetivo de ML (Traduccion Tecnica)](#3-objetivo-de-ml-traduccion-tecnica)
4. [KPIs y Thresholds de Exito](#4-kpis-y-thresholds-de-exito)
5. [Stakeholders](#5-stakeholders)
6. [Alcance del Proyecto](#6-alcance-del-proyecto)
7. [Restricciones y Supuestos](#7-restricciones-y-supuestos)
8. [User Stories de IA](#8-user-stories-de-ia)
9. [Criterios de Aceptacion (DoD)](#9-criterios-de-aceptacion-dod)
10. [Riesgos Identificados](#10-riesgos-identificados)
11. [Analisis de Viabilidad y Baseline](#11-analisis-de-viabilidad-y-baseline)
12. [Ciclo de Feedback y Aprendizaje Continuo](#12-ciclo-de-feedback-y-aprendizaje-continuo)
13. [Firmas y Certificacion](#13-firmas-y-certificacion)

---

## 1. Contexto y Problema de Negocio

### 1.1 Descripcion del Dominio

El dataset Iris es el problema de clasificacion botanica mas estudiado en la historia del Machine Learning, introducido por el biologo Ronald Fisher en 1936. Contiene 150 registros de flores Iris medidas fisicamente en cuatro dimensiones (longitud y ancho del sepalo y petalo) distribuidas en tres especies: *Iris setosa*, *Iris versicolor* e *Iris virginica*.

### 1.2 Problema que Resuelve

Sin un sistema automatizado, la clasificacion de una especie de Iris requiere la intervencion de un experto botanico que examine visualmente la flor y consulte tablas de referencia. Este proceso es:

- **Lento:** Requiere disponibilidad del experto.
- **No escalable:** Imposible de aplicar en tiempo real a volumenes grandes de muestras.
- **Propenso a error humano:** La variabilidad entre Versicolor y Virginica es baja y puede generar confusion.

### 1.3 Propuesta de Valor

Construir un sistema de clasificacion automatica que, a partir de cuatro medidas fisicas de entrada (en centimetros), determine instantaneamente la especie de Iris con alta confianza. El sistema se expone como una aplicacion web interactiva construida con Streamlit, accesible sin conocimiento tecnico.

### 1.4 Contexto del Proyecto

Este proyecto opera como un **proyecto de portafolio academico-profesional**. Su valor de negocio no es directamente monetario sino de demostración de competencia tecnica en el ciclo completo de un proyecto de Machine Learning: desde la definicion del problema hasta el despliegue de una aplicacion funcional. El ROI se mide en credibilidad tecnica, empleabilidad y calidad del portafolio.

---

## 2. Objetivo de Negocio

### 2.1 Meta Principal

> **"Construir y desplegar un clasificador de especies Iris de alta precision accesible via aplicacion web, que demuestre el ciclo completo de ingenieria de ML desde los datos crudos hasta la interfaz de usuario, completado en tiempo y forma dentro de la Fase 4."**

### 2.2 Objetivos Secundarios

| ID  | Objetivo Secundario                                                                            | Indicador de Exito                              |
| :-- | :--------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| OS1 | Demostrar dominio de la metodologia SpecDD y TDD aplicada a proyectos de ML.                  | 100% de los modulos `.py` trazables al SpecDD.  |
| OS2 | Construir una aplicacion web funcional que no requiera conocimiento tecnico para ser utilizada.| UAT aprobada por el Stakeholder Principal.      |
| OS3 | Mantener trazabilidad completa de datos (Bronze -> Silver -> Gold -> Modelo -> UI).            | Linaje documentado sin gaps en el DECISIONS_LOG.|
| OS4 | Generar un repositorio Git limpio, versionado y publico que pueda ser presentado en entrevistas.| Repo publico en GitHub con historial semantico. |

---

## 3. Objetivo de ML (Traduccion Tecnica)

### 3.1 Taxonomia del Problema

Aplicando el protocolo `business-to-ml-translator`:

| Campo                      | Definicion                                                    |
| :------------------------- | :------------------------------------------------------------ |
| **Tipo de Aprendizaje**    | Supervisado                                                   |
| **Tipo de Tarea**          | Clasificacion Multi-clase (3 clases)                          |
| **Variable Objetivo (y)**  | `species` (categorica: Setosa, Versicolor, Virginica)         |
| **Variables de Entrada (X)** | `sepal_length`, `sepal_width`, `petal_length`, `petal_width` (todas en cm, tipo float) |
| **Origen del Label**       | Pre-etiquetado. No requiere construccion de etiqueta (Labeling). |
| **Balanceo de Clases**     | Balanceado: 50 registros por clase (33.3% cada una).          |

### 3.2 Formulacion Matematica

El modelo debe aprender una funcion $f$ tal que:

$$f(\text{sepal\_length}, \text{sepal\_width}, \text{petal\_length}, \text{petal\_width}) \rightarrow \{Setosa, Versicolor, Virginica\}$$

### 3.3 Analisis del Costo del Error (Error Cost Analysis)

Este es el componente critico que define la penalizacion durante el entrenamiento:

| Tipo de Error            | Descripcion                                          | Impacto en Portafolio           | Penalizacion |
| :----------------------- | :--------------------------------------------------- | :------------------------------ | :----------- |
| **Falso Positivo (FP)**  | Predecir Setosa cuando es Versicolor (o similar)     | Demuestra imprecision del modelo| Media        |
| **Falso Negativo (FN)**  | No detectar la especie correcta                      | Equivalente al FP en este dominio| Media       |
| **Confusion Versicolor/Virginica** | El error mas probable dado que su separacion es parcialmente lineal | Mas critico que confundir Setosa | Alta  |

**Conclusion del Costo del Error:** En este dominio de portafolio, los errores de clasificacion entre Versicolor y Virginica son los mas costosos (desde la perspectiva de demostracion tecnica) porque son los que evidencian la capacidad discriminativa del modelo. No existe asimetria entre FP y FN, por lo que la metrica primaria es **Accuracy** global con **F1-Score Macro-Weighted** como metrica de control para detectar degradacion por clase.

**Regla de Negocio vs. IA:** Se ha evaluado si una regla IF-ELSE es suficiente. La respuesta es parcial: Setosa es linealmente separable del resto (regla simple posible). Sin embargo, Versicolor y Virginica requieren un modelo no lineal para superar el 95% de precision. Por tanto, el modelo de ML esta justificado.

---

## 4. KPIs y Thresholds de Exito

### 4.1 Metricas del Modelo (Fase 3)

| KPI                        | Descripcion                                                         | Umbral Minimo (RED)  | Umbral Objetivo (GREEN) | Umbral Excelencia   |
| :------------------------- | :------------------------------------------------------------------ | :------------------- | :---------------------- | :------------------ |
| **Accuracy Global**        | Porcentaje de clasificaciones correctas sobre el conjunto de test.  | >= 92%               | >= 95%                  | >= 98%              |
| **F1-Score Macro**         | Media armonica de Precision y Recall por clase, sin ponderar.      | >= 0.92              | >= 0.95                 | >= 0.98             |
| **F1-Score por Clase**     | F1 individual para Setosa, Versicolor y Virginica.                  | >= 0.90 (cada una)   | >= 0.95 (cada una)      | >= 0.98 (cada una)  |
| **Precision Macro**        | Exactitud cuando el modelo predice una clase.                       | >= 0.92              | >= 0.95                 | >= 0.98             |
| **Recall Macro**           | Capacidad de encontrar todos los casos de cada clase.               | >= 0.92              | >= 0.95                 | >= 0.98             |

**Justificacion de Umbrales:** El dataset Iris es un benchmark maduro y bien estructurado. La literatura establece que modelos simples (Logistic Regression, KNN, SVM) alcanzan entre 95-98% de accuracy. Un umbral minimo de 92% indica que el modelo esta funcionando, pero no ha sido optimizado. El umbral objetivo de 95% es el estandar de la industria para este dataset.

### 4.2 Metricas de la Aplicacion Web (Fase 4)

| KPI                        | Descripcion                                                                  | Umbral Minimo        | Umbral Objetivo         |
| :------------------------- | :--------------------------------------------------------------------------- | :------------------- | :---------------------- |
| **Latencia de Prediccion** | Tiempo desde que el usuario hace clic en "Predecir" hasta ver el resultado.  | <= 3,000 ms          | <= 1,000 ms             |
| **Disponibilidad (Uptime)**| Porcentaje de tiempo que la aplicacion esta operativa.                        | >= 95%               | >= 99%                  |
| **Tasa de Error de UI**    | Porcentaje de interacciones que generan un error no manejado en la interfaz.  | <= 5%                | <= 1%                   |

### 4.3 Metricas de Calidad de Ingenieria (Global)

| KPI                        | Descripcion                                                                  | Umbral              |
| :------------------------- | :--------------------------------------------------------------------------- | :------------------ |
| **Cobertura de Tests**     | Porcentaje de codigo en `src/` cubierto por tests unitarios.                 | >= 80%              |
| **Linaje de Datos**        | 100% de las transformaciones Bronze->Silver->Gold documentadas.              | 100% (binario)      |
| **Trazabilidad SpecDD**    | Cada funcion en `src/` tiene su contrato definido en el SpecDD.              | 100% (binario)      |

---

## 5. Stakeholders

### 5.1 Mapa de Stakeholders

| Rol                        | Nombre / Contacto                  | Tipo         | Nivel de Influencia | Expectativa Principal                                  |
| :------------------------- | :--------------------------------- | :----------- | :------------------ | :----------------------------------------------------- |
| **Propietario / Sponsor**  | Empresa Flores AI / jdrodriguez1000@gmail.com | Primario | Alta | Portafolio tecnico de calidad industrial.        |
| **Usuario Final**          | Personas sin conocimiento tecnico que interactuan con la app web | Primario | Media | Interfaz simple: ingresar medidas, ver resultado. |
| **Evaluador Tecnico**      | Reclutadores, ingenieros de entrevistas, profesores | Secundario | Alta | Codigo limpio, documentacion robusta, metodologia SpecDD/TDD. |
| **Agentes de IA**          | ai-data-auditor, ai-solutions-architect, etc. | Interno | Media | BRD claro para operar sobre base solida.          |

### 5.2 Interaccion de los Usuarios con la IA

El usuario final interactua con el sistema de la siguiente forma:

1. Accede a la aplicacion web Streamlit (URL local o desplegada).
2. Ingresa manualmente los cuatro valores numericos de las dimensiones de la flor.
3. Hace clic en el boton "Predecir Especie".
4. El sistema muestra: (a) el nombre de la especie predicha, (b) la probabilidad de confianza de la prediccion, (c) una visualizacion referencial de la especie.

---

## 6. Alcance del Proyecto

### 6.1 IN SCOPE (Dentro del Alcance)

| ID  | Item                                                                                           |
| :-- | :--------------------------------------------------------------------------------------------- |
| IS1 | Ingesta, limpieza y transformacion del dataset Iris (sklearn.datasets o CSV publico).          |
| IS2 | Analisis exploratorio de datos (EDA) completo en las tres capas (Bronze, Silver, Gold).        |
| IS3 | Entrenamiento y comparacion de al menos dos algoritmos de clasificacion.                       |
| IS4 | Seleccion del modelo final con justificacion tecnica documentada en el SAD.                    |
| IS5 | Serializacion del modelo final en formato Pickle o Joblib.                                     |
| IS6 | Construccion de la aplicacion web con Streamlit (entrada manual de features, salida de clase). |
| IS7 | Visualizacion de la probabilidad de prediccion por clase en la interfaz web.                   |
| IS8 | Suite de tests unitarios para los modulos de `src/` (Pytest).                                 |
| IS9 | Documentacion completa: BRD, SAD, SpecDD, CONTRACT, BACKLOG.                                   |
| IS10| Repositorio Git publico con historial de commits semanticos.                                   |

### 6.2 OUT OF SCOPE (Fuera del Alcance)

| ID  | Item                                                                                           | Razon de Exclusion                                                          |
| :-- | :--------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| OS1 | Integracion con bases de datos externas (SQL, NoSQL).                                         | El dataset es estatico y publico. No hay fuente de datos operacional.       |
| OS2 | Autenticacion y gestion de usuarios en la aplicacion web.                                     | Proyecto academico; no requiere multi-tenancy ni seguridad de acceso.       |
| OS3 | Despliegue en infraestructura cloud de produccion (AWS, GCP, Azure).                          | Fuera del alcance de portafolio; despliegue local es suficiente.            |
| OS4 | Reentrenamiento automatico del modelo con datos nuevos (MLOps avanzado).                      | Dataset estatico; no hay flujo de nuevos datos en produccion.               |
| OS5 | Soporte para otras especies de flores o datasets distintos al Iris.                           | El dominio esta acotado al dataset Iris original de tres especies.          |
| OS6 | Explicabilidad avanzada (SHAP, LIME) en la interfaz web.                                      | Se priorizara la prediccion y confianza. XAI es una mejora futura opcional. |
| OS7 | API REST separada del frontend Streamlit.                                                     | Streamlit maneja el backend y frontend de forma integrada en esta version.  |

---

## 7. Restricciones y Supuestos

### 7.1 Restricciones Tecnicas

| ID  | Restriccion                                                                                          | Impacto                                             |
| :-- | :--------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| RT1 | **Lenguaje:** Python 3.12+ obligatorio (segun CLAUDE.md).                                           | Define la version del interprete y compatibilidad.  |
| RT2 | **Framework UI:** Streamlit es el unico framework de interfaz web permitido.                        | Limita las opciones de personalizacion visual.      |
| RT3 | **Ambiente:** Todo el desarrollo debe realizarse dentro de un ambiente virtual (`venv` o `conda`).  | No se permite instalacion global de dependencias.   |
| RT4 | **Serializacion:** Solo se permiten formatos ONNX, Pickle o Joblib para el modelo final.            | Limita el uso de formatos propietarios.             |
| RT5 | **Rutas:** Prohibido el uso de rutas absolutas en el codigo. Solo rutas relativas.                  | Garantiza portabilidad del repositorio.             |

### 7.2 Restricciones de Datos

| ID  | Restriccion                                                                                          | Impacto                                             |
| :-- | :--------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| RD1 | **Fuente de datos:** Solo el dataset Iris original (150 registros, 4 features, 3 clases).           | No hay posibilidad de aumentar el dataset con datos propios. |
| RD2 | **Volumen:** 150 registros en total. Es un dataset pequeno.                                         | Tecnicas de Deep Learning no son aplicables ni justificadas. |
| RD3 | **Sin datos nuevos en produccion:** No existe un flujo de nuevas muestras de flores.                | El modelo no requiere reentrenamiento periodico.    |

### 7.3 Supuestos del Proyecto

| ID  | Supuesto                                                                                             | Consecuencia si es Falso                           |
| :-- | :--------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| SA1 | El dataset Iris original (Fisher, 1936) esta libre de errores criticos de medicion.                 | Se requerira limpieza de outliers en Fase 2.        |
| SA2 | El dataset es suficientemente representativo de las tres especies para generalizar bien.             | El modelo fallaria en datos del mundo real (fuera de distribucion). |
| SA3 | El usuario final entiende como medir las dimensiones fisicas de una flor en centimetros.            | La UI debe incluir instrucciones o ilustraciones de referencia. |
| SA4 | El entorno de ejecucion local del Stakeholder es compatible con Python 3.12+ y Streamlit.           | Se requeriria soporte de despliegue en contenedor Docker. |

---

## 8. User Stories de IA

Aplicando el protocolo `value-driven-product-mapper` con estructura de IA-UX:

### US-01: Clasificacion de Especie

> **Como** usuario sin conocimiento botanico especializado,
> **quiero** ingresar las cuatro medidas fisicas de una flor Iris (sepal length, sepal width, petal length, petal width en cm)
> **y recibir** la especie predicha con su probabilidad de confianza (en porcentaje),
> **para poder** identificar la especie de la flor sin necesidad de un experto,
> **visible en** la interfaz web de Streamlit con una respuesta instantanea.

**Criterio de Confianza:** Si la probabilidad maxima de la clase predicha es menor al 60%, la UI debe mostrar una advertencia: "Resultado de baja confianza. Verifique las medidas ingresadas."

**Explicabilidad Requerida (XAI):** No obligatoria en v1.0. La prediccion de la clase y su probabilidad es suficiente para el usuario final.

### US-02: Visualizacion de Probabilidades por Clase

> **Como** usuario curioso o evaluador tecnico,
> **quiero** ver las probabilidades de prediccion para las tres especies (no solo la ganadora),
> **y recibir** un grafico de barras o similar que muestre la distribucion de confianza,
> **para poder** entender el grado de certeza del modelo y detectar casos ambiguos,
> **visible en** la interfaz web de Streamlit como un componente visual secundario.

### US-03: Validacion de Entradas Invalidas

> **Como** usuario que comete errores de tipeo,
> **quiero** que el sistema me informe claramente si ingreso valores fuera de rango o invalidos,
> **y recibir** un mensaje de error descriptivo (no un stack trace de Python),
> **para poder** corregir mis datos y volver a intentar sin frustrarme,
> **visible en** la interfaz web como un mensaje de alerta de color rojo.

**Rangos de validacion (del dataset de referencia, con margen del 20%):**

| Feature         | Minimo Aceptable | Maximo Aceptable | Unidad |
| :-------------- | :--------------- | :--------------- | :----- |
| sepal_length    | 3.0              | 9.0              | cm     |
| sepal_width     | 1.5              | 5.5              | cm     |
| petal_length    | 0.5              | 8.0              | cm     |
| petal_width     | 0.0              | 3.5              | cm     |

---

## 9. Criterios de Aceptacion (DoD)

La Fase 4 se considera exitosa y el proyecto es aprobado por el ai-business-strategist cuando se cumplan TODOS los siguientes criterios de forma binaria (SI/NO):

### 9.1 Criterios del Modelo (Fase 3)

| ID   | Criterio                                                                                               | Verificacion                              |
| :--- | :----------------------------------------------------------------------------------------------------- | :---------------------------------------- |
| CA01 | El modelo alcanza Accuracy >= 95% en el conjunto de test (hold-out set no visto durante entrenamiento).| Reporte de MODEL QA en `docs/Fase_3/`.   |
| CA02 | El F1-Score Macro es >= 0.95 sobre el conjunto de test.                                               | Reporte de MODEL QA en `docs/Fase_3/`.   |
| CA03 | Ninguna clase individual tiene F1-Score < 0.90.                                                       | Reporte de MODEL QA en `docs/Fase_3/`.   |
| CA04 | El modelo esta serializado en formato Pickle o Joblib y almacenado en `models/`.                      | Existencia del archivo serializado.       |
| CA05 | El modelo fue evaluado con validacion cruzada (k-fold, k >= 5) ademas del hold-out set.               | Reporte de MODEL QA en `docs/Fase_3/`.   |

### 9.2 Criterios de la Aplicacion Web (Fase 4)

| ID   | Criterio                                                                                               | Verificacion                              |
| :--- | :----------------------------------------------------------------------------------------------------- | :---------------------------------------- |
| CA06 | La aplicacion Streamlit responde una prediccion en <= 3,000 ms en hardware local estandar.            | Test de latencia en `docs/Fase_4/`.       |
| CA07 | La UI valida los rangos de entrada y muestra mensajes de error sin exponer trazas de Python.          | Test E2E en `tests/` y revision manual.  |
| CA08 | La UI muestra la especie predicha y las probabilidades de las tres clases.                            | Validacion visual UAT por Stakeholder.    |
| CA09 | La aplicacion arranca correctamente con `streamlit run src/app.py` sin errores.                      | Prueba de arranque documentada.           |

### 9.3 Criterios de Ingenieria y Gobernanza

| ID   | Criterio                                                                                               | Verificacion                              |
| :--- | :----------------------------------------------------------------------------------------------------- | :---------------------------------------- |
| CA10 | El linaje Bronze->Silver->Gold->Modelo esta documentado sin gaps.                                     | Revision del DECISIONS_LOG.               |
| CA11 | Todos los modulos en `src/` tienen su contrato en el SpecDD.                                          | Revision cruzada SpecDD vs. `src/`.       |
| CA12 | La cobertura de tests unitarios en `src/` es >= 80%.                                                  | Reporte de Pytest coverage.               |
| CA13 | El `requirements.txt` refleja exactamente las dependencias instaladas en el venv.                     | Comparacion `pip freeze` vs. `requirements.txt`. |
| CA14 | El repositorio Git tiene historial semantico limpio sin commits de "fix typo" consecutivos.           | Revision del `git log`.                   |

### 9.4 Criterio Final de Validacion (UAT)

| ID   | Criterio                                                                                               | Autoridad                                 |
| :--- | :----------------------------------------------------------------------------------------------------- | :---------------------------------------- |
| CA15 | El Stakeholder Principal (jdrodriguez1000@gmail.com) valida que la aplicacion resuelve la necesidad descrita en la Seccion 1.3 de este BRD. | ai-business-strategist (firma de UAT). |

---

## 10. Riesgos Identificados

### 10.1 Riesgos Tecnicos

| ID  | Riesgo                                                                 | Probabilidad | Impacto | Mitigacion                                                                 |
| :-- | :--------------------------------------------------------------------- | :----------- | :------ | :------------------------------------------------------------------------- |
| RT1 | **Overfitting:** El modelo memoriza los 150 registros y no generaliza. | Media        | Alto    | Usar validacion cruzada k-fold y hold-out set. Reportar ambas metricas.    |
| RT2 | **Confusion Versicolor/Virginica:** El modelo no discrimina bien estas dos clases. | Alta  | Medio | Analizar la matriz de confusion por clase y priorizar modelos con fronteras no lineales (SVM, Random Forest). |
| RT3 | **Data Leakage:** El scaler o encoder se ajusta con datos de test.    | Media        | Alto    | Implementar el pipeline de preprocesamiento estrictamente dentro del `fit` de entrenamiento. Usar `Pipeline` de scikit-learn. |
| RT4 | **Latencia alta en Streamlit:** La carga del modelo en cada request es lenta. | Baja   | Medio   | Cargar el modelo una sola vez al inicio de la sesion usando `st.cache_resource`. |

### 10.2 Riesgos de Negocio / Portafolio

| ID  | Riesgo                                                                 | Probabilidad | Impacto | Mitigacion                                                                 |
| :-- | :--------------------------------------------------------------------- | :----------- | :------ | :------------------------------------------------------------------------- |
| RN1 | **Proyecto percibido como trivial:** El evaluador tecnico considera el dataset Iris demasiado simple. | Alta | Medio | El valor esta en la **metodologia** (SpecDD, TDD, Medallion Architecture), no en la complejidad del dataset. El BRD y el BACKLOG deben ser de calidad industrial. |
| RN2 | **Documentacion incompleta:** Los documentos de gobernanza quedan sin completar. | Media | Alto | El BACKLOG debe incluir tareas especificas de documentacion con Definition of Done. |
| RN3 | **Deuda tecnica en `src/`:** El codigo de notebooks se migra sin refactorizacion a produccion. | Media | Alto | Protocolo obligatorio: ningun `.ipynb` entra a `src/` sin pasar por el ciclo Red-Green-Refactor. |

---

## 11. Analisis de Viabilidad y Baseline

### 11.1 Baseline del Proceso Actual

Sin ningun modelo, el clasificador mas simple posible (clasificador por clase mayoritaria o "dummy") tendria:

- **Accuracy Baseline (Dummy):** 33.3% (dataset balanceado, predice siempre la misma clase).
- **F1-Score Baseline (Dummy):** ~0.17 (penalizado por las clases no predichas).

### 11.2 Benchmark Conocido de la Literatura

| Algoritmo                  | Accuracy Tipico (Literatura) | Observacion                                    |
| :------------------------- | :--------------------------- | :--------------------------------------------- |
| Logistic Regression        | 97%                          | Funciona bien por la separabilidad del dataset. |
| K-Nearest Neighbors (KNN)  | 96-98%                       | Muy efectivo en datasets pequenos.              |
| Support Vector Machine (SVM)| 97-98%                      | Excelente separacion de fronteras.              |
| Random Forest              | 96-97%                       | Robusto ante outliers.                          |
| Decision Tree              | 95-97%                       | Interpretable pero propenso a overfitting.      |

### 11.3 Evaluacion de Regla de Negocio (No-ML)

Una regla IF-ELSE puede clasificar Setosa con ~100% de precision (petal_length < 2.5 cm => Setosa). Sin embargo, la distincion Versicolor/Virginica requiere una frontera no lineal que una regla simple no puede capturar con suficiente precision. Conclusion: **el modelo de ML esta plenamente justificado**.

### 11.4 ROI del Proyecto

| Inversion Estimada                 | Retorno Esperado                                                      |
| :--------------------------------- | :-------------------------------------------------------------------- |
| 4-6 semanas de desarrollo (Fases 1-4) | Portafolio demostrable de nivel junior-mid con metodologia industrial. |
| Costo operativo: $0 (local)        | Credibilidad tecnica en entrevistas y evaluaciones academicas.        |

---

## 12. Ciclo de Feedback y Aprendizaje Continuo

Aplicando el protocolo `value-driven-product-mapper` - Seccion III:

### 12.1 Captura de Ground Truth en Produccion

Dado que el proyecto opera con un dataset estatico y no hay flujo de nuevas flores en produccion, no existe mecanismo automatico de captura de Ground Truth real. Sin embargo, se implementara:

- Un boton en la UI: **"Esta prediccion es incorrecta"** que registra en un log local (`logs/feedback.log`) la entrada del usuario y la prediccion rechazada.
- Este log podria, en una iteracion futura (v2.0), alimentar un proceso de reentrenamiento.

### 12.2 Mecanismo de Correccion

| Accion del Usuario                 | Respuesta del Sistema                                                 |
| :--------------------------------- | :-------------------------------------------------------------------- |
| Clic en "Esta prediccion es incorrecta" | Se registra `{timestamp, input_features, predicted_class}` en `logs/feedback.log`. |
| El log tiene >= 20 entradas        | El BACKLOG de v2.0 considerara un ciclo de reentrenamiento semi-supervisado. |

---

## 13. Firmas y Certificacion

### 13.1 Checklist de Certificacion del BRD

Aplicando el check de certificacion del protocolo `business-to-ml-translator`:

| Criterio de Certificacion                                                              | Estado   |
| :------------------------------------------------------------------------------------- | :------- |
| La tarea de ML seleccionada (clasificacion multi-clase) cubre el 100% del caso de uso. | Aprobado |
| Se ha definido la metrica tecnica para el ciclo RED de los agentes de QA (Accuracy >= 95%, F1 >= 0.95). | Aprobado |
| Se ha cuantificado el costo de un error del modelo (confusion Versicolor/Virginica como error primario). | Aprobado |
| Se han definido las User Stories con el componente de incertidumbre de la IA (umbral de baja confianza). | Aprobado |
| Se han establecido umbrales de decision claros para el backend (rangos de validacion de entrada). | Aprobado |
| El diseno incluye visualizaciones interpretables sin conocimiento de ciencias de datos. | Aprobado |

### 13.2 Autoridades del Documento

| Rol                          | Responsable                          | Firma           | Fecha       |
| :--------------------------- | :----------------------------------- | :-------------- | :---------- |
| **Autor del BRD**            | ai-business-strategist               | Emitido         | 2026-04-19  |
| **Validacion de Negocio (UAT)** | Stakeholder Principal (jdrodriguez1000@gmail.com) | Pendiente Fase 4 | Por definir |

---

> **Nota de Gobernanza:** Este documento es la fuente de verdad para todos los agentes del proyecto Flores AI - Iris. Cualquier desviacion de los objetivos, KPIs o criterios de aceptacion aqui definidos debe pasar por el Protocolo de Control de Cambios (CC) antes de ser implementada. El ai-business-strategist es el unico agente con autoridad para modificar este documento.
