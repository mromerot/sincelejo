"""Valida índice, referencias internas, citas y salidas de cuadernos."""
from pathlib import Path
import re, json, yaml, nbformat
ROOT=Path(__file__).resolve().parents[1]
config=yaml.safe_load((ROOT/'myst.yml').read_text()); paths=[]
def walk(nodes):
    for n in nodes:
        if 'file' in n: paths.append(ROOT/n['file'])
        walk(n.get('children',[]))
walk(config['project']['toc'])
assert len(paths)==len(set(paths)), 'Índice duplicado'
keys=set(re.findall(r'@\w+\{([^,]+),',(ROOT/'references.bib').read_text()))
for p in paths:
    assert p.exists(),f'Falta {p}'
    if p.suffix=='.ipynb':
        nb=nbformat.read(p,as_version=4); nbformat.validate(nb)
        text='\n'.join(c.source for c in nb.cells if c.cell_type=='markdown')
        for c in nb.cells:
            if c.cell_type=='code':
                assert c.execution_count is not None,f'No ejecutado: {p}'
                assert all(o.output_type!='error' for o in c.outputs),f'Error en {p}'
    else:text=p.read_text()
    for key in re.findall(r'(?<!\w)@([A-Za-z][\w-]*)',text):
        assert key in keys,f'Cita {key} no definida en {p}'
    for url in re.findall(r'\]\(([^\s)]+)\)',text):
        if '://' in url or url.startswith(('#','mailto:')):continue
        target=(p.parent/url.split('#')[0]).resolve()
        assert target.exists(),f'Enlace roto en {p}: {url}'
raw=ROOT/'data/raw/power_1991_2025.json'
import hashlib
assert hashlib.sha256(raw.read_bytes()).hexdigest()==json.loads((ROOT/'data/manifest.json').read_text())['sha256']
print(f'OK: {len(paths)} páginas; {sum(p.suffix==".ipynb" for p in paths)} cuadernos ejecutados; citas, enlaces y hash verificados.')
