"""Estaciones automáticas IDEAM usadas para contrastar el reanálisis (catálogo hp9r-jxuu de datos.gov.co)."""
import numpy as np
PUNTO_NASA = (9.3047, -75.3978)  # lat, lon de la consulta NASA POWER
ESTACIONES = {
    '0025025350': {'nombre': 'PUERTA ROJA - AUT', 'municipio': 'Sincelejo', 'lat': 9.316389, 'lon': -75.3875},
    '0025025270': {'nombre': 'UNISUCRE AUT', 'municipio': 'Sampués', 'lat': 9.211607, 'lon': -75.401011},
    '0025025280': {'nombre': 'EL TESORO IDEAM - AUT', 'municipio': 'Morroa', 'lat': 9.357083, 'lon': -75.28925},
    '0025020440': {'nombre': 'SAN PEDRO - AUT', 'municipio': 'San Pedro', 'lat': 9.401597, 'lon': -75.016434},
}
def distancia_km(lat1, lon1, lat2, lon2):
    """Distancia de círculo máximo (haversine)."""
    p1, p2 = np.radians(lat1), np.radians(lat2)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(np.radians(lon2 - lon1) / 2) ** 2
    return float(6371.0 * 2 * np.arcsin(np.sqrt(a)))
