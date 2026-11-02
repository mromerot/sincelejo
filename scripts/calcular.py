"""Regenera tablas y figuras desde la instantánea de NASA; no requiere red."""
from pathlib import Path
import sys, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sincelejo.analisis import cargar, indicadores, deficit_trimestral, resumen, sensibilidad_calor
raw=ROOT/'data/raw/power_1991_2025.json'
df=cargar(raw); a=indicadores(df); z=deficit_trimestral(df); s=resumen(df)
out=ROOT/'data/processed'; out.mkdir(exist_ok=True)
fig=ROOT/'book/figuras'; fig.mkdir(parents=True,exist_ok=True)
a.to_csv(out/'indicadores_anuales.csv',float_format='%.6f')
z.to_csv(out/'deficit_trimestral.csv',float_format='%.6f')
sensibilidad_calor(df).to_csv(out/'sensibilidad_calor.csv',index=False,float_format='%.6f')
(out/'resumen.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
meta={'fuente':'NASA POWER Daily API','consulta':'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS10M&community=AG&longitude=-75.3978&latitude=9.3047&start=19910101&end=20251231&format=JSON',
 'fecha_consulta':'2026-11-01','sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
 'coordenadas_solicitadas':[-75.3978,9.3047], 'header':json.loads(raw.read_text())['header'],
 'alcance':'Punto de reanálisis regional; no representa el promedio del polígono municipal.',
 'baseline':'1991-2020','control_calidad':{'dias':len(df),'faltantes':int(df.isna().sum().sum()),'duplicados':int(df.index.duplicated().sum())}}
(ROOT/'data/manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'#0b2545','text.color':'#0b2545','figure.facecolor':'white'})
def save(f,name):
 f.savefig(fig/(name+'.png'),dpi=170,bbox_inches='tight'); plt.close(f)
b=df.loc['1991':'2020']; m=b.groupby(b.index.month).mean(); mp=b.PRECTOTCORR.resample('MS').sum().groupby(lambda x:x.month).mean()
f,axs=plt.subplots(1,2,figsize=(11,4),layout='constrained')
axs[0].bar(mp.index,mp,color='#1a6fa3'); axs[0].set(title='Estacionalidad de la lluvia',ylabel='mm/mes',xlabel='Mes')
axs[1].plot(m.index,m.T2M_MAX,label='Máxima diaria media',color='#c8811a'); axs[1].plot(m.index,m.T2M_MIN,label='Mínima diaria media',color='#1a6fa3'); axs[1].legend(fontsize=8); axs[1].set(title='Ciclo térmico',ylabel='°C',xlabel='Mes')
for ax in axs: ax.set_xticks(range(1,13)); ax.grid(axis='y',alpha=.15)
f.suptitle('Sincelejo · NASA POWER · referencia 1991–2020'); save(f,'climatologia')
f,axs=plt.subplots(2,2,figsize=(11,7),layout='constrained')
for ax,col,title,unit,color in zip(axs.flat,['tmedia','tx35','rx1day','cdd'],['Temperatura media anual','Días con máxima ≥ 35 °C','Máxima lluvia diaria de cada año','Mayor racha seca dentro del año'],['°C','días/año','mm/día','días'],['#c8811a','#c2410c','#1a6fa3','#2e7d32']):
 ax.plot(a.index,a[col],color=color,lw=1.5); ax.axvspan(2021,2025,color='#e3e8ee',alpha=.5); ax.set(title=title,ylabel=unit); ax.grid(alpha=.15)
f.suptitle('Contexto regional de amenaza · 1991–2025 · no son daños observados'); save(f,'indicadores')
f,ax=plt.subplots(figsize=(11,3.5),layout='constrained'); ax.fill_between(z.index,0,z.z_p3,where=z.z_p3<0,color='#c8811a'); ax.fill_between(z.index,0,z.z_p3,where=z.z_p3>=0,color='#1a6fa3'); ax.axhline(-1,color='#c2410c',ls='--',lw=1); ax.set(title='Anomalía estandarizada de lluvia acumulada en tres meses',ylabel='Z por mes final (no SPI/SPEI)'); save(f,'deficit')
h=sensibilidad_calor(df); f,ax=plt.subplots(figsize=(8,4),layout='constrained'); ax.plot(h.delta_C,h.dias_tx35_anio,'o-',label='Días Tmax ≥ 35 °C',color='#c2410c'); ax.plot(h.delta_C,h.noches_tn25_anio,'o-',label='Noches Tmin ≥ 25 °C',color='#1a6fa3'); ax.set(xlabel='Incremento uniforme aplicado a la serie base (°C)',ylabel='Días o noches por año',title='Prueba de sensibilidad · sin fecha ni probabilidad asignadas'); ax.legend(); ax.grid(alpha=.15); save(f,'sensibilidad_calor')
print(json.dumps(s,indent=2,ensure_ascii=False))
