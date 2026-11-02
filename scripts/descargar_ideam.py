"""Descarga explícita de la estación IDEAM 'Puerta Roja - AUT' (Sincelejo) desde datos.gov.co
(dataset s54a-sgyg, precipitación cada 10 min) y guarda el total diario. No se ejecuta en el despliegue."""
from pathlib import Path
import json, sys, time, urllib.parse, urllib.request
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from sincelejo.analisis import diario_estacion
ESTACION='0025025350'
def pagina(off):
    q={'$where':f"codigoestacion='{ESTACION}'",'$select':'fechaobservacion,valorobservado','$order':'fechaobservacion','$limit':50000,'$offset':off}
    u='https://www.datos.gov.co/resource/s54a-sgyg.json?'+urllib.parse.urlencode(q)
    for _ in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=180))
        except Exception as e: print('reintento',off,e,flush=True); time.sleep(5)
    raise SystemExit('Descarga fallida')
filas=[]; off=0
while True:
    r=pagina(off); filas+=r
    if len(r)<50000: break
    off+=50000
d10=pd.DataFrame(filas).rename(columns={'fechaobservacion':'fecha','valorobservado':'mm'})
dia=diario_estacion(d10)
dia.to_csv(ROOT/'data/raw/ideam_puerta_roja_diario.csv',float_format='%.2f')
print(len(d10),'registros de 10 min ->',len(dia),'días',dia.index.min().date(),dia.index.max().date())
