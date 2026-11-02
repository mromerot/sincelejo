"""Indicadores diarios de contexto. No es un modelo hidráulico ni epidemiológico."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

BASE = (1991, 2020)

def cargar(ruta):
    j = json.loads(Path(ruta).read_text())
    df = pd.DataFrame(j['properties']['parameter']).replace(j['header']['fill_value'], np.nan)
    df.index = pd.to_datetime(df.index, format='%Y%m%d')
    df = df.sort_index().rename_axis('fecha')
    if df.index.has_duplicates:
        raise ValueError('Fechas duplicadas')
    esperado = pd.date_range(df.index.min(), df.index.max(), freq='D')
    if not df.index.equals(esperado):
        raise ValueError('Calendario incompleto: no comprimir huecos')
    if df.isna().any().any():
        raise ValueError('Datos faltantes: revisar cobertura antes de calcular rachas')
    if (df.PRECTOTCORR < 0).any() or (df.T2M_MIN > df.T2M_MAX).any():
        raise ValueError('Valores físicamente inconsistentes')
    if not df.RH2M.between(0, 100).all() or (df.WS10M < 0).any():
        raise ValueError('Humedad o viento fuera de rango')
    return df

def racha_max(valores):
    """Mayor racha True; no acepta valores faltantes."""
    v = pd.Series(valores)
    if v.isna().any():
        raise ValueError('Racha con valores faltantes')
    n = mejor = 0
    for x in v:
        n = n + 1 if x else 0
        mejor = max(mejor, n)
    return mejor

def umbral_mensual(df, variable='T2M_MAX', q=.9):
    b = df.loc[f'{BASE[0]}':f'{BASE[1]}', variable]
    if b.empty: raise ValueError('Sin línea base')
    return b.groupby(b.index.month).quantile(q)

def indicadores(df):
    """Años completos. Rx5day y CDD se reinician el 1 de enero."""
    p90 = umbral_mensual(df)
    filas = []
    for year, g in df.groupby(df.index.year):
        esperado = len(pd.date_range(f'{year}-01-01', f'{year}-12-31'))
        if len(g) != esperado: raise ValueError(f'Año {year} incompleto')
        hot = g.T2M_MAX.to_numpy() > g.index.month.map(p90).to_numpy()
        dry = g.PRECTOTCORR < 1
        filas.append(dict(anio=year, tmedia=g.T2M.mean(), tmax_media=g.T2M_MAX.mean(),
            p_total=g.PRECTOTCORR.sum(), rx1day=g.PRECTOTCORR.max(),
            rx5day=g.PRECTOTCORR.rolling(5,min_periods=5).sum().max(),
            cdd=racha_max(dry), r20=int((g.PRECTOTCORR >= 20).sum()),
            tx35=int((g.T2M_MAX >= 35).sum()), noches25=int((g.T2M_MIN >= 25).sum()),
            tx90_mes=int(hot.sum()), compuesto=int((hot & dry.to_numpy()).sum()),
            viento_medio=g.WS10M.mean(), viento_dia_max=g.WS10M.max()))
    return pd.DataFrame(filas).set_index('anio')

def deficit_trimestral(df):
    """Z de acumulado móvil de 3 meses por mes final; NO es SPI ni SPEI."""
    mensual = df.PRECTOTCORR.resample('MS').sum(min_count=1)
    p3 = mensual.rolling(3,min_periods=3).sum()
    base = p3.loc[f'{BASE[0]}':f'{BASE[1]}']
    mean = base.groupby(base.index.month).mean()
    std = base.groupby(base.index.month).std(ddof=1)
    z = (p3-p3.index.month.map(mean).to_numpy())/p3.index.month.map(std).to_numpy()
    return pd.DataFrame({'p3_mm': p3, 'z_p3': z})

def sensibilidad_calor(df):
    b = df.loc[f'{BASE[0]}':f'{BASE[1]}']
    return pd.DataFrame([{'delta_C': d,
        'dias_tx35_anio': ((b.T2M_MAX+d)>=35).groupby(b.index.year).sum().mean(),
        'noches_tn25_anio': ((b.T2M_MIN+d)>=25).groupby(b.index.year).sum().mean()}
        for d in [0,1,2,3]])

def pae_catalogo(perdidas, frecuencias):
    """Pérdidas por evento y tasas anuales; NO usar 1/T de mapas anidados como tasas."""
    l, f = np.asarray(perdidas,float), np.asarray(frecuencias,float)
    if l.shape != f.shape or l.ndim != 1 or len(l)==0:
        raise ValueError('Vectores no vacíos del mismo tamaño')
    if not np.isfinite(l).all() or not np.isfinite(f).all() or (l<0).any() or (f<0).any():
        raise ValueError('Pérdidas y tasas finitas no negativas')
    return float(np.dot(l,f))

def resumen(df):
    a = indicadores(df); b=a.loc[1991:2020]
    return {'dias':len(df), 'inicio':str(df.index.min().date()), 'fin':str(df.index.max().date()),
        'tmedia_base_C':float(b.tmedia.mean()), 'lluvia_base_mm_anio':float(b.p_total.mean()),
        'tx35_base_dias_anio':float(b.tx35.mean()), 'tx35_reciente_dias_anio':float(a.loc[2021:2025].tx35.mean()),
        'cdd_max_dias':int(a.cdd.max()), 'cdd_max_anio':int(a.cdd.idxmax()),
        'rx1_max_mm':float(a.rx1day.max()), 'rx1_max_anio':int(a.rx1day.idxmax()),
        'tmedia_pendiente_C_decada':float(np.polyfit(a.index, a.tmedia,1)[0]*10)}
