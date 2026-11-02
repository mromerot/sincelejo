"""Pruebas de los scripts: se ejecutan sobre una copia temporal del proyecto."""
import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]

def copiar(destino, extra=()):
    for d in ('src', 'scripts', 'data', 'book/figuras', *extra):
        origen = ROOT / d
        if origen.is_dir(): shutil.copytree(origen, destino / d, dirs_exist_ok=True,
                                            ignore=shutil.ignore_patterns('__pycache__'))
        else:
            (destino / d).parent.mkdir(parents=True, exist_ok=True); shutil.copy(origen, destino / d)

def correr(tmp, *args):
    return subprocess.run([sys.executable, *args], cwd=tmp, capture_output=True, text=True, timeout=600)

class Scripts(unittest.TestCase):
    def test_calcular_regenera_las_tablas_publicadas(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t); copiar(t)
            for f in (t / 'data/processed').glob('*'): f.unlink()
            r = correr(t, 'scripts/calcular.py'); self.assertEqual(r.returncode, 0, r.stderr)
            for nombre in ('indicadores_anuales.csv', 'deficit_trimestral.csv', 'sensibilidad_calor.csv'):
                self.assertEqual((t / 'data/processed' / nombre).read_text(), (ROOT / 'data/processed' / nombre).read_text(), nombre)
            a = json.loads((t / 'data/processed/resumen.json').read_text()); b = json.loads((ROOT / 'data/processed/resumen.json').read_text())
            self.assertEqual(a.keys(), b.keys())
            for k in a: self.assertAlmostEqual(a[k], b[k]) if isinstance(a[k], float) else self.assertEqual(a[k], b[k])
            self.assertEqual(json.loads((t / 'data/manifest.json').read_text()), json.loads((ROOT / 'data/manifest.json').read_text()))

    def test_validar_ideam_regenera_el_json_publicado(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t); copiar(t)
            r = correr(t, 'scripts/validar_ideam.py'); self.assertEqual(r.returncode, 0, r.stderr)
            a = json.loads((t / 'data/processed/validacion_ideam.json').read_text()); b = json.loads((ROOT / 'data/processed/validacion_ideam.json').read_text())
            self.assertEqual(a, b)

    def test_arreglar_sitemap(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t); copiar(t); h = t / '_build/html'; h.mkdir(parents=True)
            (h / 'sitemap.xml').write_text('<loc>http://localhost:3001/book</loc><?xml-stylesheet href="http://localhost:3001/x.xsl"?>')
            (h / 'robots.txt').write_text('Sitemap: http://localhost:3000/sitemap.xml')
            r = correr(t, 'scripts/arreglar_sitemap.py'); self.assertEqual(r.returncode, 0, r.stderr)
            self.assertNotIn('localhost', (h / 'sitemap.xml').read_text() + (h / 'robots.txt').read_text())
            self.assertIn('https://mromerot.github.io/sincelejo/book', (h / 'sitemap.xml').read_text())
            (h / 'robots.txt').unlink()   # falta un archivo: debe fallar, no publicar a medias
            self.assertNotEqual(correr(t, 'scripts/arreglar_sitemap.py').returncode, 0)

    @unittest.skipUnless(all(__import__('importlib').util.find_spec(m) for m in ('nbclient', 'ipykernel')), 'requiere extras [libro]')
    def test_ejecutar_cuadernos_ejecuta_y_guarda_salidas(self):
        rel = 'book/03_analisis/38_sismo/b_amenaza.ipynb'
        with tempfile.TemporaryDirectory() as t:
            t = Path(t); copiar(t, extra=(rel,))
            import nbformat
            nb = nbformat.read(t / rel, 4)
            for c in nb.cells:
                if c.cell_type == 'code': c.outputs = []; c.execution_count = None
            nbformat.write(nb, t / rel)
            r = correr(t, 'scripts/ejecutar_cuadernos.py', str(t / rel)); self.assertEqual(r.returncode, 0, r.stderr)
            nb = nbformat.read(t / rel, 4)
            codigo = [c for c in nb.cells if c.cell_type == 'code']
            self.assertTrue(all(c.execution_count is not None for c in codigo))
            self.assertTrue(any(c.outputs for c in codigo))
            self.assertTrue((t / 'data/entorno.json').exists())

    @unittest.skipUnless(all(__import__('importlib').util.find_spec(m) for m in ('nbclient', 'ipykernel')), 'requiere extras [libro]')
    def test_ejecutar_cuadernos_falla_si_el_cuaderno_tiene_error(self):
        rel = 'book/03_analisis/38_sismo/b_amenaza.ipynb'
        with tempfile.TemporaryDirectory() as t:
            t = Path(t); copiar(t, extra=(rel,))
            import nbformat
            nb = nbformat.read(t / rel, 4); nb.cells.append(nbformat.v4.new_code_cell('raise RuntimeError("falla de prueba")'))
            nbformat.write(nb, t / rel)
            antes = (t / rel).read_text()
            self.assertNotEqual(correr(t, 'scripts/ejecutar_cuadernos.py', str(t / rel)).returncode, 0)
            self.assertEqual((t / rel).read_text(), antes)   # no guarda resultados fallidos

if __name__ == '__main__': unittest.main()
