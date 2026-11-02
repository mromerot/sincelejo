"""Contrasta NASA POWER con la estación IDEAM de Puerta Roja y guarda data/processed/validacion_ideam.json."""
from pathlib import Path
import sys, json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from sincelejo.analisis import cargar, comparar_estacion
nasa=cargar(ROOT/'data/raw/power_1991_2025.json').PRECTOTCORR
dia=pd.read_csv(ROOT/'data/raw/ideam_puerta_roja_diario.csv',index_col='fecha',parse_dates=True)
res=comparar_estacion(dia,nasa)
res['estacion']={'codigo':'0025025350','nombre':'PUERTA ROJA - AUT','lat':9.316389,'lon':-75.3875,'fuente':'IDEAM vía datos.gov.co, dataset s54a-sgyg','distancia_aprox_al_punto_nasa_km':1.7}
(ROOT/'data/processed/validacion_ideam.json').write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(res,indent=2,ensure_ascii=False))
