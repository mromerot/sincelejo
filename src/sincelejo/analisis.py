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

def diario_estacion(d10, columna_fecha='fecha', columna_valor='mm'):
    """Agrega precipitación de 10 min a total diario. Elimina fechas repetidas (el origen
    publica bloques duplicados con valores idénticos; sumarlos multiplicaría la lluvia)."""
    d = d10[[columna_fecha, columna_valor]].copy()
    d[columna_fecha] = pd.to_datetime(d[columna_fecha])
    d[columna_valor] = pd.to_numeric(d[columna_valor], errors='raise')
    if (d[columna_valor] < 0).any():
        raise ValueError('Precipitación negativa')
    d = d.drop_duplicates(columna_fecha)
    g = d.groupby(d[columna_fecha].dt.normalize())[columna_valor].agg(['size', 'sum'])
    g.index.name = 'fecha'
    return g.rename(columns={'size': 'n_registros', 'sum': 'mm'})

def comparar_estacion(diario, nasa_precip, min_registros=140, min_dias_mes=25):
    """Contrasta lluvia de estación y reanálisis en días con >=min_registros de 144.
    Devuelve métricas diarias y mensuales y los meses con posible falla del sensor
    (estación <5 % del reanálisis cuando éste supera 50 mm)."""
    ok = diario[diario.n_registros >= min_registros]
    j = ok.join(nasa_precip.rename('nasa'), how='inner')
    if j.empty: raise ValueError('Sin días comunes')
    m = j.groupby(j.index.to_period('M')).agg(dias=('mm', 'size'), estacion=('mm', 'sum'), nasa=('nasa', 'sum'))
    m = m[m.dias >= min_dias_mes]
    sospechoso = m[(m.nasa > 50) & (m.estacion < .05 * m.nasa)]
    mm = m.drop(sospechoso.index)
    def r(x, y, method='pearson'):
        if len(x) <= 2: return float('nan')
        if method == 'spearman': x, y = x.rank(), y.rank()   # evita depender de scipy
        return float(x.corr(y))
    return {
        'dias_comparados': int(len(j)), 'primer_dia': str(j.index.min().date()), 'ultimo_dia': str(j.index.max().date()),
        'suma_estacion_mm': float(j.mm.sum()), 'suma_reanalisis_mm': float(j.nasa.sum()),
        'dias_lluvia_ge1_estacion': int((j.mm >= 1).sum()), 'dias_lluvia_ge1_reanalisis': int((j.nasa >= 1).sum()),
        'dias_lluvia_ge1_ambos': int(((j.mm >= 1) & (j.nasa >= 1)).sum()),
        'max_diario_estacion_mm': float(j.mm.max()), 'max_diario_reanalisis_mm': float(j.nasa.max()),
        'r_pearson_diaria': r(j.mm, j.nasa), 'r_spearman_diaria': r(j.mm, j.nasa, 'spearman'),
        'meses_comparables': int(len(m)), 'r_pearson_mensual': r(m.estacion, m.nasa),
        'meses_sospechosos': [str(p) for p in sospechoso.index],
        'meses_sin_sospechosos': int(len(mm)), 'r_pearson_mensual_sin_sospechosos': r(mm.estacion, mm.nasa),
        'razon_estacion_reanalisis_sin_sospechosos': float(mm.estacion.sum() / mm.nasa.sum()) if len(mm) else float('nan'),
    }
