---
title: Software, métodos y versiones
---

El paquete `eva-sincelejo` contiene carga y validación de datos, indicadores, sensibilidades y una función general de PAE por catálogo. Python, NumPy y pandas realizan los cálculos; Matplotlib crea las figuras; nbformat y nbclient gestionan y ejecutan cuadernos; MyST genera el sitio.

**MyST se fija en 1.10.1** en `package.json` y se instala con el archivo de bloqueo. El entorno de cálculo utilizado se registra en `data/entorno.json`. El rango de dependencias Python se declara en `pyproject.toml`; para reproducir bit a bit use también las versiones registradas y el commit de esta edición.

No se ejecutaron CLIMADA, OpenQuake ni un modelo hidráulico local. Se emplean como referencias de método o rutas futuras; no se presentan sus salidas como si hubieran sido calculadas.

Las pruebas comprueban rachas y faltantes, tasas de PAE, consistencia del producto climático y monotonía de la sensibilidad térmica. La validación editorial comprueba el índice, enlaces internos, citas y ejecución de cuadernos.
