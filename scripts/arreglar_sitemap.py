"""Sustituye el host local que MyST escribe en sitemap.xml y robots.txt por la URL pública.
Se ejecuta tras `myst build --html`; SITE_URL permite cambiarla."""
from pathlib import Path
import os, re
SITE = os.environ.get('SITE_URL', 'https://mromerot.github.io/sincelejo').rstrip('/')
html = Path(__file__).resolve().parents[1] / '_build/html'
for nombre in ('sitemap.xml', 'robots.txt'):
    f = html / nombre
    if not f.exists():
        raise SystemExit(f'Falta {f}: ejecute primero myst build --html')
    s = f.read_text()
    nuevo = re.sub(r'http://localhost:\d+', SITE, s)
    if 'localhost' in nuevo:
        raise SystemExit(f'Quedan referencias locales en {nombre}')
    f.write_text(nuevo)
    print(f'{nombre}: {s.count("localhost")} referencias locales -> {SITE}')
