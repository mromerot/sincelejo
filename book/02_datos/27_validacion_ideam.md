---
title: 2.7 Contraste con estaciones IDEAM
short_title: 2.7 Contraste con IDEAM
---

## Qué se comparó

El reanálisis NASA POWER es una rejilla de 0,5° × 0,625°, no una medición local. Se contrastó su precipitación diaria con **cuatro estaciones automáticas del IDEAM** cuyos datos abiertos de 10 minutos están en datos.gov.co [@ideamdatos]. Se agregaron a totales diarios y se usaron solo los días con al menos 140 de 144 registros. El origen repite bloques de fechas con valores idénticos (por ejemplo, 18 días de 2019 en Puerta Roja); se eliminan antes de sumar, porque sumarlos multiplicaría la lluvia. Las otras estaciones activas o históricas de la zona (Aeropuerto Rafael Barvo, Libra Arriba, La Pastora y la pluviométrica convencional Sincelejo) no tienen datos en este conjunto. Los resultados están en `data/processed/validacion_ideam.json` y se regeneran con `scripts/descargar_ideam.py` y `scripts/validar_ideam.py`.

| Estación | Distancia al punto NASA | Periodo | Días comparados | r diaria | r mensual (meses) | Lluvia estación / reanálisis* | Meses sospechosos |
|---|---:|---|---:|---:|---:|---:|---:|
| Puerta Roja – AUT (Sincelejo) | 1,7 km | 2017-01 a 2021-10 | 1231 | 0,03 | 0,07 (34) | 0,69 | 11 |
| El Tesoro – AUT (Morroa) | 13,3 km | 2017-01 a 2025-12 | 1609 | 0,11 | 0,43 (47) | 0,87 | 1 |
| Unisucre AUT (Sampués) | 10,4 km | 2023-11 a 2025-12 | 643 | 0,09 | 0,25 (17) | 1,07 | 0 |
| San Pedro – AUT (San Pedro) | 43,2 km | 2019-08 a 2025-12 | 1664 | 0,06 | 0,13 (40) | 0,42 | 0 |

\* Razón de lluvia acumulada en los meses comparables, sin los meses «sospechosos» (estación con menos del 5 % de lo que calcula el reanálisis cuando este supera 50 mm). Es un criterio práctico mío, no un estándar.

## Resultado

**1. La coincidencia día a día es muy baja en las cuatro estaciones** (correlación diaria 0,03 a 0,11). Es esperable: la lluvia convectiva tropical es muy local, las estaciones están a 2–43 km del punto y el reanálisis es un promedio de rejilla. Los extremos tampoco coinciden: los máximos diarios de las estaciones (78,6 mm en El Tesoro el 9 de enero de 2023; 67,6 mm en Unisucre el 27 de mayo de 2025) corresponden a días en que el reanálisis calcula 1 mm o menos. En sentido contrario, el máximo del reanálisis, 177,3 mm el 3 de octubre de 2023, **no pudo verificarse**: ese día El Tesoro y Unisucre no tienen registros, y San Pedro (a 43 km) midió 0,1 mm.

**2. Los totales mensuales concuerdan solo parcialmente y la razón estación/reanálisis varía mucho** (0,42 a 1,07). Unisucre registra totales muy parecidos a los del reanálisis en sus dos años completos (1087 frente a 1012 mm en 2024 y 1543 frente a 1389 mm en 2025, con 297 y 314 días válidos). San Pedro registra menos de la mitad, y puede deberse a distancia, a fallas o a ambas. No hay un sesgo único que se pueda corregir con un factor.

**3. Las estaciones fallan por tramos.** Puerta Roja marca menos de 1 mm de septiembre de 2018 a enero de 2019, cuando el reanálisis calcula 130 a 180 mm mensuales en septiembre–noviembre. Un sensor sin lluvia durante tres meses de temporada húmeda es inverosímil, aunque los datos no lo demuestran. Cuando funciona, el acuerdo mejora: en septiembre y octubre de 2017 midió 178 y 86 mm frente a 182 y 89 mm del reanálisis.

**4. El reanálisis tiene más días débilmente húmedos.** En Puerta Roja, 526 días con al menos 1 mm frente a 151 en la estación. Parte de esa diferencia puede deberse a los tramos fallidos de la estación.

## Consecuencias para los indicadores

- **CDD (racha seca, <1 mm/día):** si el reanálisis tiene más días débilmente húmedos, las rachas calculadas son probablemente **más cortas** que las observadas. El valor de 90 días (2016) debe leerse como límite inferior del reanálisis, no como una medición.
- **Rx1day, R20 y 177 mm de 2023:** ninguna estación corrobora los extremos diarios del reanálisis, y los extremos de las estaciones tampoco aparecen en él. Son contexto regional, no frecuencia ni intensidad de eventos locales.
- **Año 2020:** el reanálisis y El Tesoro coinciden en un año muy seco (11 mm de la estación frente a 52 mm del reanálisis en sus 135 días válidos), con pocos días de registro.
- **Año 2021:** el reanálisis da **508 mm** en todo el año, la cifra más baja de la serie. El Tesoro, a 13 km, midió **733 mm solo en 176 días válidos de 2021**, mientras el reanálisis calculó 301 mm en esos mismos días. Es una sola estación y la diferencia puede deberse a lluvia local, pero indica que **el valor de 2021 podría estar subestimado**. No debe usarse como magnitud de sequía sin validación adicional.

## Qué no se concluye

No se concluye que NASA POWER sea inadecuado ni que las estaciones sean fiables. Con cuatro estaciones automáticas, series con huecos y sin pluviómetros convencionales, solo se sostiene que **el reanálisis sirve como contexto de totales y estacionalidad, no para fechar o dimensionar eventos locales**. Un siguiente paso útil es solicitar al IDEAM las series de las estaciones convencionales cercanas (Sincelejo 25020130, 1958–2010; Libra Arriba; La Pastora; Aeropuerto Rafael Barvo) y, si se quiere cuantificar extremos, corregir el sesgo del reanálisis contra todas ellas.
