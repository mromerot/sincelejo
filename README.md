# EVA · Sincelejo

Libro MyST sobre amenazas y riesgos de desastres y climáticos de Sincelejo, Sucre. [Leer el libro](https://mromerot.github.io/sincelejo/).

Conserva la estructura y el diseño EVA de Leticia. Aplica el marco del libro de teoría y contrasta evidencia institucional y científica. Incluye ocho amenazas, 28 cuadernos con salidas, 35 años diarios de NASA POWER y un registro de evidencia. **Diagnóstico exploratorio:** no es una evaluación predial ni una estimación de pérdidas económicas.

## Reproducir

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[libro]'
python scripts/calcular.py
python scripts/ejecutar_cuadernos.py
python scripts/validar_ideam.py   # contraste con la estación IDEAM (datos ya incluidos)
python -m unittest discover -s tests
python scripts/validar_libro.py
npm ci
npm run build
```

Para vista previa: `npm run start`. Para Pages: `BASE_URL=/sincelejo npm run build`.

`scripts/descargar_ideam.py` actualiza la estación IDEAM (descarga explícita). Los cuadernos usan la instantánea original de `data/raw/`; el hash y los metadatos están en `data/manifest.json`. `data/entorno.json` registra el entorno de cálculo. El flujo de Actions **no ejecuta los cuadernos**: valida que sus salidas guardadas existan y no tengan errores, y publica esas salidas en GitHub Pages. Por eso, tras cambiar datos o código hay que correr `scripts/ejecutar_cuadernos.py` y subir los cuadernos actualizados.

## Estructura

- `book/01_conceptos/`: conceptos, contexto, evidencia y revisión.
- `book/02_datos/`: fuentes, exposición y escala de análisis.
- `book/03_analisis/`: inundación, sequía, erosión/laderas, calor, incendios, tormentas, dengue, sismo y síntesis.
- `src/sincelejo/`: indicadores, validación y preparación común de cuadernos (`nb.py`).
- `data/`: datos, trazabilidad y resultados tabulares.
- `scripts/`: descarga explícita, cálculo, ejecución y validación.
- `recursos_web/eva/`: diseño heredado de Leticia.

Consulta documental: 2026-11-01. Serie climática: 1991–2025; referencia: 1991–2020. Contenido propio CC BY 4.0; código MIT. Los datos de terceros conservan sus condiciones y atribuciones.
