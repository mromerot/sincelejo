"""Descarga explícita de estaciones automáticas del IDEAM desde datos.gov.co (dataset s54a-sgyg,
precipitación cada 10 min) y guarda el total diario en data/raw/ideam_<código>_diario.csv.
Uso: python scripts/descargar_ideam.py [código ...]   (sin argumentos, todas). No se ejecuta en el despliegue."""
from pathlib import Path
import json, sys, time, urllib.parse, urllib.request
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from sincelejo.analisis import diario_estacion
from sincelejo.estaciones import ESTACIONES
def pagina(codigo, off):
    q={'$where':f"codigoestacion='{codigo}'",'$select':'fechaobservacion,valorobservado','$order':'fechaobservacion','$limit':50000,'$offset':off}
    u='https://www.datos.gov.co/resource/s54a-sgyg.json?'+urllib.parse.urlencode(q)
    for _ in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=180))
        except Exception as e: print('reintento',codigo,off,e,flush=True); time.sleep(5)
    raise SystemExit('Descarga fallida')
for codigo in (sys.argv[1:] or ESTACIONES):
    filas=[]; off=0
    while True:
        r=pagina(codigo,off); filas+=r
        if len(r)<50000: break
        off+=50000
    d10=pd.DataFrame(filas).rename(columns={'fechaobservacion':'fecha','valorobservado':'mm'})
    dia=diario_estacion(d10)
    dia.to_csv(ROOT/f'data/raw/ideam_{codigo}_diario.csv',float_format='%.2f')
    print(codigo,ESTACIONES[codigo]['nombre'],len(d10),'registros ->',len(dia),'días',dia.index.min().date(),dia.index.max().date(),flush=True)
