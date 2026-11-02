---
title: 2.7 Contraste con una estación IDEAM
short_title: 2.7 Contraste con IDEAM
---

## Qué se comparó

El reanálisis NASA POWER es una rejilla de 0,5° × 0,625° y no una medición local. Para probar su utilidad se contrastó con la estación automática **Puerta Roja – AUT** del IDEAM (código 0025025350, a unos 1,7 km del punto de consulta), cuyos datos abiertos de precipitación cada 10 minutos se publican en datos.gov.co [@ideamdatos]. La estación tiene registros entre 2017 y el 29 de octubre de 2021; no cubre 2023 ni 2024. Se agregaron a totales diarios y se usaron solo los **1231 días** con al menos 140 de 144 registros. El origen repite bloques de fechas con valores idénticos (18 días de agosto y septiembre de 2019); se eliminaron antes de sumar, porque sumarlos multiplicaría la lluvia. Los resultados están en `data/processed/validacion_ideam.json` y se regeneran con `scripts/validar_ideam.py`.

## Resultado

| Medida (días comunes, 2017–2021) | Estación | NASA POWER |
|---|---:|---:|
| Lluvia acumulada | 1457 mm | 3294 mm |
| Días con ≥1 mm | 151 | 526 |
| Máximo diario | 50,3 mm | 129,0 mm |
| Correlación diaria (Pearson / Spearman) | 0,03 / 0,22 | |
| Correlación mensual (34 meses) | 0,07 | |

El acuerdo es **bajo** en conjunto. Dos hechos explican buena parte:

1. **La estación parece fallar por tramos.** Registra menos de 1 mm de septiembre de 2018 a enero de 2019, mientras que en septiembre–noviembre el reanálisis calcula entre 130 y 180 mm mensuales. En 11 de 34 meses comparables la estación mide menos del 5 % del reanálisis cuando este supera 50 mm. No hay forma de demostrar la falla desde los datos, pero un sensor sin lluvia durante tres meses de temporada húmeda es inverosímil. Cuando la estación funciona, el contraste mejora: en septiembre y octubre de 2017 midió 178 y 86 mm frente a 182 y 89 mm del reanálisis.
2. **El reanálisis llueve con más frecuencia y menos intensidad.** Excluidos los meses sospechosos, quedan 23 meses con correlación mensual de **0,52** y la estación registra alrededor del **69 %** de la lluvia del reanálisis. En todo el periodo común, el reanálisis tiene 3,5 veces más días con ≥1 mm (526 frente a 151), aunque parte de esa diferencia puede deberse a los tramos fallidos de la estación.

## Consecuencias para los indicadores

- **CDD (racha seca, <1 mm/día):** si el reanálisis tiene más días débilmente húmedos, las rachas secas calculadas son probablemente **más cortas** que las observadas. El valor de 90 días (2016) debe leerse como un límite inferior del reanálisis, no como una medición.
- **Rx1day y R20:** el máximo diario del reanálisis es mayor que el observado en la estación en el periodo común, pero es un solo punto y una estación con fallas. No permite afirmar que 177 mm en 2023 sea correcto ni excesivo; ese año queda fuera de la estación.
- **Lluvia anual de 2020 (608 mm) y 2021 (508 mm):** son las más bajas de la serie. La estación tiene datos de esos años, pero con huecos y tramos sospechosos (251 días registrados en 2021), así que **no confirma ni refuta** la sequía. Se mantiene como señal pendiente de validar con estaciones pluviométricas convencionales o CHIRPS.

## Qué no se concluye

No se concluye que NASA POWER sea inadecuado ni que la estación sea fiable. Con una estación, cinco años y fallas probables, el contraste muestra que **los indicadores de lluvia diaria deben tratarse como contexto regional** y que el siguiente paso útil es consolidar varias estaciones del IDEAM, depurar sus series y, si se pretende cuantificar frecuencia de extremos, corregir sesgo del reanálisis contra ellas.
