import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from sincelejo.analisis import cargar, indicadores, racha_max, pae_catalogo, sensibilidad_calor
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
if __name__=='__main__': unittest.main()
