"""Ejecuta los cuadernos (todos, o solo las rutas dadas como argumentos) y guarda solo resultados obtenidos correctamente."""
from pathlib import Path
import json, os, sys, platform, importlib.metadata
os.environ.setdefault('MPLCONFIGDIR','/tmp/mpl-sincelejo')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/cache-sincelejo')
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
ROOT=Path(__file__).resolve().parents[1]
rutas=[Path(a).resolve() for a in sys.argv[1:]] or sorted((ROOT/'book').rglob('*.ipynb'))
for p in rutas:
    nb=nbformat.read(p,as_version=4)
    km=KernelManager(kernel_name='python3')
    km.kernel_spec.argv=[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
    try:
        NotebookClient(nb,timeout=180,km=km,resources={'metadata':{'path':str(ROOT)}}).execute()
    finally:
        if km.has_kernel:
            km.shutdown_kernel(now=True)
    nbformat.write(nb,p)
    print('OK',p.relative_to(ROOT),flush=True)
packages=['numpy','pandas','matplotlib','nbformat','nbclient','ipykernel','PyYAML']
(ROOT/'data/entorno.json').write_text(json.dumps({'python':sys.version,'platform':platform.platform(),'packages':{m:importlib.metadata.version(m) for m in packages}},indent=2)+'\n')
