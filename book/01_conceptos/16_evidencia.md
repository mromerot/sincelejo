---
title: 1.6 Calidad y alcance de la evidencia
short_title: 1.6 Calidad y alcance de la evidencia
---

## Cuatro etiquetas de lectura

| Etiqueta | Significado | Ejemplo |
|---|---|---|
| Calculado | Sale de una entrada preservada y código ejecutado | Máxima lluvia diaria del reanálisis |
| Documentado | Una fuente identificada reporta el hecho | Corte municipal de dengue de 2024 |
| Sensibilidad | Resultado condicionado a una perturbación elegida | Días calurosos al sumar 2 °C |
| Por completar | Requiere nuevas entradas o validación | PAE y población dentro de manchas hidráulicas |

**No disponible no significa cero.** Los reportes de prensa institucional muestran hechos o acciones; no son un catálogo completo de desastres. La frecuencia de menciones tampoco mide la frecuencia física. La ausencia de datos de una amenaza no justifica reducir su prioridad de investigación.

## Registro y reproducibilidad

`data/evidencia.json` conserva siete hechos con lugar, fecha, fuente, tipo y límite de interpretación. `data/fuentes.csv` distingue documentos leídos, documentación y fuentes localizadas para uso posterior. `data/manifest.json` registra la consulta de NASA, versión de API y hash SHA-256. Los datos climáticos se congelaron para permitir reproducir el análisis sin depender de futuras revisiones del proveedor.

## Sesgos que afectan las decisiones

La cobertura mediática privilegia daños visibles; el subregistro puede ser mayor en zonas rurales. Un caso notificado en un municipio no necesariamente coincide con residencia o lugar de contagio. Las series de reanálisis pueden suavizar lluvia convectiva y máximas térmicas. Los cambios de infraestructura pueden modificar el riesgo incluso si el clima se mantiene.

La edición es un diagnóstico exploratorio con análisis meteorológico reproducible. No asigna legalmente zonas de riesgo ni presenta inventarios de personas expuestas que no hayan sido levantados.
