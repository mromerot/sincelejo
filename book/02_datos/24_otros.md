---
title: 2.4 Datos complementarios y registro de eventos
short_title: 2.4 Datos complementarios y registro de eventos
---

La próxima integración debe comenzar por los registros de emergencia del CMGRD y UNGRD, las estaciones del IDEAM, los inventarios ambientales de CARSUCRE y los datos operativos de agua y salud. Cada registro debe conservar fecha de ocurrencia y de reporte, localización, tipo de fenómeno, unidades de daño y nivel de verificación.

## Reglas de depuración

Un mismo episodio puede aparecer como inundación, vendaval y caída de árboles. Guardar un identificador de episodio, mantener sus mecanismos y evitar sumar dos veces las mismas viviendas. Separar afectados acumulados de personas únicas; viviendas destruidas de averiadas; alertas de emergencias observadas. Un dato ausente no se reemplaza por cero.

Para dengue, especificar residencia, procedencia o notificación, semana epidemiológica y revisiones posteriores. El proyecto HARMONIZE reúne herramientas abiertas para integrar salud, clima y datos socioeconómicos [@harmonize]; su módulo data4health (paquete de R) limpia y agrega listados de casos por espacio y tiempo, y lee archivos DBF como los de vigilancia [@data4health]. Su licencia es AGPL ≥3: conviene usarlo como herramienta externa, sin copiar su código a este repositorio, que usa MIT. Requiere el listado de casos individuales de SIVIGILA para Sincelejo, que no está en datos abiertos y debe solicitarse al INS o a la Secretaría de Salud de Sucre. Esta edición no lo ejecutó. Para incendios, agrupar detecciones del mismo episodio y contrastar con perímetros: FIRMS advierte que una detección no significa que el píxel completo se haya quemado [@firms].

Se propone un archivo de eventos con: `evento_id, fecha_inicio, fecha_fin, amenaza, latitud, longitud, precision_m, fuente, personas_unicas, viviendas_danadas, perdida_COP, anio_precios, validacion`. La edición actual no rellena ese inventario con datos ficticios.
