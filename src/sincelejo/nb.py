"""Preparación común de los cuadernos: datos, indicadores y estilo de figuras.

Se usa con ``from sincelejo.nb import *`` tras ubicar ``src/`` en ``sys.path``.
"""
import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from .analisis import cargar, indicadores, deficit_trimestral, sensibilidad_calor, resumen

ROOT = Path(__file__).resolve().parents[2]
clima = cargar(ROOT / 'data/raw/power_1991_2025.json')
anual = indicadores(clima)
evidencia = pd.read_json(ROOT / 'data/evidencia.json')
plt.rcParams.update({'figure.figsize': (9, 4), 'axes.spines.top': False, 'axes.spines.right': False})
