"""Actualización explícita de la fuente; no se ejecuta en el despliegue."""
from pathlib import Path
import json, urllib.request, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from sincelejo.analisis import cargar
url=json.loads((ROOT/'data/manifest.json').read_text())['consulta']
raw=urllib.request.urlopen(url,timeout=180).read()
with tempfile.NamedTemporaryFile(suffix='.json') as f:
    f.write(raw); f.flush(); df=cargar(f.name)
    if len(df)!=12784: raise ValueError('Cobertura distinta de la edición: revisar fechas')
(ROOT/'data/raw/power_1991_2025.json').write_bytes(raw)
print('Fuente actualizada. Regenere resultados, revise fecha de consulta y texto editorial.')
