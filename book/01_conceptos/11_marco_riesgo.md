---
title: 1.1 Marco del riesgo
short_title: 1.1 Marco del riesgo
---

## Amenaza, exposición y vulnerabilidad

La Ley 1523 organiza la gestión en conocimiento, reducción y manejo de desastres [@ley1523]. En este libro se usan tres preguntas operativas:

| Componente | Pregunta | Ejemplo de aplicación |
|---|---|---|
| Amenaza | ¿Qué intensidad puede presentarse y con qué frecuencia? | Profundidad y velocidad del agua en una vivienda |
| Exposición | ¿Qué personas, bienes o servicios coinciden con el evento? | Viviendas, escuelas y pasos viales dentro de la mancha |
| Vulnerabilidad | ¿Cómo se transforma la intensidad en daño o interrupción? | Material, altura del piso, movilidad y acceso a ayuda |

Un barrio mencionado en un reporte no queda automáticamente clasificado como de riesgo alto. Una lluvia extrema tampoco indica cuántas personas se inundan. El cálculo necesita conectar los tres componentes en el mismo espacio y tiempo.

## Riesgo por evento y pérdida anual esperada

La separación modular procede del libro local de teoría y es compatible con CLIMADA [@climada2019]. Para un evento $e$ y activos $j$:

$$L_e=\sum_j V_j\,f_j(I_{ej}),\qquad \mathrm{PAE}=\sum_e\lambda_e\,\mathbb{E}[L_e].$$

$V_j$ es el valor de reposición, $f_j$ una fracción de daño y $\lambda_e$ una tasa de ocurrencia anual de un catálogo coherente. Las tasas de eventos pueden sumar más de uno cuando caben varios eventos por año. El módulo `pae_catalogo` implementa esta identidad, pero **esta edición no publica una PAE de Sincelejo**: faltan intensidades locales, inventario valorado y funciones de daño verificadas.

Los mapas de retorno 10, 50 y 100 años son escenarios de excedencia anidados. Sus probabilidades $1/T$ no pueden usarse como si fueran tasas de eventos independientes. Se requiere integrar una curva de excedencia o construir intervalos con probabilidades incrementales, declarando las colas. Además, la probabilidad anual de superar el máximo no es idéntica a la tasa de excedencia de todos los eventos; bajo Poisson se relacionan mediante $p=1-\exp(-\lambda)$.

## Qué sí se mide aquí

Se calculan indicadores meteorológicos y pruebas de sensibilidad; se construye un registro de evidencia y una agenda de reducción del riesgo. Se evita convertir días calurosos en fallecimientos, déficit de lluvia en pérdida de agua del acuífero, o puntos de fuego en viviendas quemadas. La incertidumbre se registra como parte del resultado, no como un valor cero.
