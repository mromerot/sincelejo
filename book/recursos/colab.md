---
title: Ejecutar y reproducir
---

## Entorno local

```bash
git clone https://github.com/mromerot/sincelejo.git
cd sincelejo
python -m venv .venv
source .venv/bin/activate
pip install -e '.[libro]'
python scripts/calcular.py
python scripts/ejecutar_cuadernos.py
python -m unittest discover -s tests
npm install
npm run build
```

El cálculo usa la instantánea original incluida; no necesita descargar nuevos datos. Los cuadernos buscan la raíz del proyecto desde su directorio. Para Colab use el botón de cada cuaderno: el arranque clona el repositorio e instala el paquete. Colab requiere acceso a internet para ese arranque, pero no credenciales de NASA.

## Actualizar datos

Ejecute `python scripts/descargar_clima.py` solo cuando quiera una nueva consulta. Se valida la respuesta antes de reemplazar el archivo. Después regenere tablas, figuras y cuadernos. Revise cambios de metadatos y resultados y actualice explícitamente el texto de portada y la fecha de edición; la publicación no modifica los datos por su cuenta.

Para repetir exactamente una edición, use su commit de Git. La ejecución en Colab desde `main` usa la versión más reciente del repositorio; cambie a un commit concreto si necesita fijarla.

## Publicación

El flujo de GitHub Actions valida código y estructura, construye MyST con `BASE_URL=/sincelejo` y publica en GitHub Pages. Usa las salidas guardadas; las fuentes remotas de datos no intervienen durante la publicación. El workflow puede ejecutarse manualmente y vuelve a publicarse con cada cambio en `main`.
