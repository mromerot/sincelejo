"""Contrasta NASA POWER con las estaciones IDEAM descargadas y guarda data/processed/validacion_ideam.json."""
from pathlib import Path
import sys, json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from sincelejo.analisis import cargar, comparar_estacion
from sincelejo.estaciones import ESTACIONES, PUNTO_NASA, distancia_km
nasa=cargar(ROOT/'data/raw/power_1991_2025.json').PRECTOTCORR
salida={}
for codigo,e in ESTACIONES.items():
    f=ROOT/f'data/raw/ideam_{codigo}_diario.csv'
    if not f.exists(): continue
    dia=pd.read_csv(f,index_col='fecha',parse_dates=True)
    res=comparar_estacion(dia,nasa)
    res['estacion']={'codigo':codigo,**e,'distancia_al_punto_nasa_km':round(distancia_km(*PUNTO_NASA,e['lat'],e['lon']),1),
                     'fuente':'IDEAM vía datos.gov.co, dataset s54a-sgyg'}
    salida[codigo]=res
(ROOT/'data/processed/validacion_ideam.json').write_text(json.dumps(salida,indent=2,ensure_ascii=False)+'\n')
for c,r in salida.items():
    print(c,r['estacion']['nombre'],r['estacion']['distancia_al_punto_nasa_km'],'km | días',r['dias_comparados'],r['primer_dia'],r['ultimo_dia'],
          '| r diaria %.2f | r mensual %.2f | sospechosos %d/%d | r mensual sin sosp. %.2f | razón %.2f' % (
          r['r_pearson_diaria'],r['r_pearson_mensual'],len(r['meses_sospechosos']),r['meses_comparables'],
          r['r_pearson_mensual_sin_sospechosos'],r['razon_estacion_reanalisis_sin_sospechosos']))
