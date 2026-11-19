"""Build a self-hosted geographical relief backdrop for the BIBLILU Atlas.

Source: Basemap shadedrelief.jpg (global shaded-relief raster), included in
mpl_toolkits.basemap_data. We crop in equirectangular lon/lat coordinates
matching the atlas' SVG projection, so clickable features remain aligned.
Run only if assets/atlas/relieve.webp is missing; it is checked into git.
"""
from pathlib import Path
import os
from PIL import Image
from mpl_toolkits import basemap_data

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/atlas/relieve.webp'
if OUT.is_file() and OUT.stat().st_size>10000:
    print('El relieve del atlas ya existe:', OUT)
    raise SystemExit(0)
SOURCE=Path(next(iter(basemap_data.__path__)))/'shadedrelief.jpg'
if not SOURCE.exists():raise RuntimeError('No se encontró el raster shadedrelief.jpg de basemap-data')
lon_w,lon_e,lat_s,lat_n=24,56,21,44
with Image.open(SOURCE) as raster:
    w,h=raster.size
    x1=round((lon_w+180)/360*w)
    x2=round((lon_e+180)/360*w)
    y1=round((90-lat_n)/180*h)
    y2=round((90-lat_s)/180*h)
    crop=raster.convert('RGB').crop((x1,y1,x2,y2))
    # Sharpening would artificially alter topography; use only resampling.
    crop=crop.resize((1600,1150),Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    crop.save(OUT,'WEBP',quality=85,method=6)
print(f'Generado relieve georreferenciado: {OUT} ({OUT.stat().st_size//1024} KB)')
