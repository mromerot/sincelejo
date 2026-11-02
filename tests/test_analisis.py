import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pandas as pd
from sincelejo.estaciones import ESTACIONES, PUNTO_NASA, distancia_km
from sincelejo.analisis import cargar, indicadores, racha_max, pae_catalogo, sensibilidad_calor, diario_estacion, comparar_estacion, umbral_mensual, deficit_trimestral, resumen
RAW=Path(__file__).resolve().parents[1]/'data/raw/power_1991_2025.json'
class Metodos(unittest.TestCase):
 def test_rachas(self):
  self.assertEqual(racha_max([False,True,True,False,True]),2)
  self.assertEqual(racha_max([False,False]),0)
  with self.assertRaises(ValueError): racha_max([True,np.nan,True])
 def test_pae_tasas_no_probabilidades_acumuladas(self):
  self.assertAlmostEqual(pae_catalogo([100,1000],[.2,.01]),30)
  with self.assertRaises(ValueError): pae_catalogo([100],[-.1])
  with self.assertRaises(ValueError): pae_catalogo([100],[np.nan])
 def test_datos_y_sensibilidad(self):
  df=cargar(Path(__file__).resolve().parents[1]/'data/raw/power_1991_2025.json')
  self.assertEqual(len(df),12784)
  a=indicadores(df); self.assertEqual(len(a),35)
  self.assertTrue((a.rx5day>=a.rx1day).all())
  self.assertTrue(a.cdd.between(0,366).all())
  h=sensibilidad_calor(df)
  self.assertTrue((h.dias_tx35_anio.diff().dropna()>=0).all())
  self.assertAlmostEqual(h.iloc[0].dias_tx35_anio,a.loc[1991:2020].tx35.mean())
 def test_umbral_mensual_valores_de_referencia(self):
  df=cargar(RAW); u=umbral_mensual(df)
  self.assertEqual(list(u.index),list(range(1,13)))
  self.assertAlmostEqual(u[3],37.87,places=2)   # marzo, máximo del año
  self.assertAlmostEqual(u[10],32.833,places=3) # octubre, mínimo del año
  b=df.loc['1991':'2020']
  self.assertAlmostEqual(u[1],b[b.index.month==1].T2M_MAX.quantile(.9))  # cálculo independiente
 def test_deficit_trimestral(self):
  z=deficit_trimestral(cargar(RAW))
  self.assertEqual(int(z.z_p3.isna().sum()),2)  # enero y febrero de 1991 no tienen 3 meses
  self.assertAlmostEqual(z.loc['2020-12-01','p3_mm'],71.5,places=1)
  self.assertAlmostEqual(z.loc['2020-12-01','z_p3'],-2.0019,places=3)
  self.assertAlmostEqual(z.loc['1991-03-01','z_p3'],0.6138,places=3)
  base=z.loc['1991':'2020']   # por construcción: media 0 y desviación 1 en cada mes de cierre
  g=base.z_p3.dropna().groupby(base.dropna().index.month)
  for m in range(1,13):
   if m in (1,2): continue
   self.assertAlmostEqual(g.mean()[m],0,places=9); self.assertAlmostEqual(g.std(ddof=1)[m],1,places=9)
 def test_resumen_coherente_con_indicadores(self):
  df=cargar(RAW); r=resumen(df); a=indicadores(df)
  self.assertEqual(r['dias'],12784); self.assertEqual((r['inicio'],r['fin']),('1991-01-01','2025-12-31'))
  self.assertEqual((r['cdd_max_dias'],r['cdd_max_anio']),(90,2016))
  self.assertAlmostEqual(r['rx1_max_mm'],177.33); self.assertEqual(r['rx1_max_anio'],2023)
  self.assertAlmostEqual(r['tx35_reciente_dias_anio'],a.loc[2021:2025].tx35.mean())
  self.assertAlmostEqual(r['tmedia_pendiente_C_decada'],0.3021,places=4)
 def test_indicadores_rechaza_anio_incompleto(self):
  df=cargar(RAW).loc[:'2025-12-30']
  with self.assertRaises(ValueError): indicadores(df)
 def test_cargar_rechaza_huecos_y_valores_imposibles(self):
  import json,tempfile
  j=json.loads(RAW.read_text()); par=j['properties']['parameter']
  malo=json.loads(json.dumps(j)); del malo['properties']['parameter']['T2M']['19910102']
  malo2=json.loads(json.dumps(j)); malo2['properties']['parameter']['RH2M']['19910103']=140
  for m in (malo,malo2):
   with tempfile.NamedTemporaryFile('w',suffix='.json') as f:
    json.dump(m,f); f.flush()
    with self.assertRaises(ValueError): cargar(f.name)
 def test_diario_estacion_elimina_duplicados(self):
  idx=pd.date_range('2020-01-01',periods=144,freq='10min')
  d=pd.DataFrame({'fecha':idx,'mm':1.0})
  r=diario_estacion(pd.concat([d,d.iloc[:10]]))   # 10 filas repetidas con el mismo valor
  self.assertEqual(int(r.n_registros.iloc[0]),144); self.assertAlmostEqual(r.mm.iloc[0],144.0)
  with self.assertRaises(ValueError): diario_estacion(pd.DataFrame({'fecha':idx[:2],'mm':[1,-1]}))
 def test_comparar_estacion_detecta_sensor_sin_lluvia(self):
  dias=pd.date_range('2020-01-01','2020-04-30',freq='D')
  nasa=pd.Series(5.0,index=dias)   # 150 mm al mes
  est=pd.DataFrame({'n_registros':144,'mm':5.0},index=dias)
  est.loc['2020-03-01':'2020-03-31','mm']=0.0   # marzo sin registros de lluvia
  r=comparar_estacion(est,nasa)
  self.assertEqual(r['meses_sospechosos'],['2020-03']); self.assertEqual(r['meses_comparables'],4)
  self.assertAlmostEqual(r['razon_estacion_reanalisis_sin_sospechosos'],1.0)
  self.assertEqual(r['dias_comparados'],len(dias))
  est.loc[:, 'n_registros']=10   # días incompletos: no hay comparación posible
  with self.assertRaises(ValueError): comparar_estacion(est,nasa)
 def test_validacion_ideam_guardada_coincide(self):
  import json
  base=Path(__file__).resolve().parents[1]
  g=json.loads((base/'data/processed/validacion_ideam.json').read_text())
  self.assertGreaterEqual(len(g),4)
  nasa=cargar(RAW).PRECTOTCORR
  for codigo,esperado in g.items():
   dia=pd.read_csv(base/f'data/raw/ideam_{codigo}_diario.csv',index_col='fecha',parse_dates=True)
   r=comparar_estacion(dia,nasa)
   for k in ('dias_comparados','meses_sospechosos','suma_estacion_mm','r_pearson_mensual_sin_sospechosos'):
    self.assertEqual(r[k],esperado[k]) if not isinstance(r[k],float) else self.assertAlmostEqual(r[k],esperado[k],places=9)
 def test_distancia_km(self):
  self.assertAlmostEqual(distancia_km(0,0,0,1),111.19,places=1)       # un grado de ecuador
  self.assertAlmostEqual(distancia_km(*PUNTO_NASA,*PUNTO_NASA),0.0)
  e=ESTACIONES['0025025350']; self.assertTrue(1.0<distancia_km(*PUNTO_NASA,e['lat'],e['lon'])<2.5)
if __name__=='__main__': unittest.main()
