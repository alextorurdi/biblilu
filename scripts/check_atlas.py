"""Integridad del Atlas de Pueblos y de sus vínculos con las fichas generadas."""
from pathlib import Path
from urllib.parse import quote
import json
R=Path(__file__).resolve().parents[1]
catalog=json.loads((R/'assets/atlas/pentateuco.geojson').read_text(encoding='utf-8'))
assert catalog['type']=='FeatureCollection'
features=catalog['features']
ids=[f['properties']['id'] for f in features]
assert len(ids)==len(set(ids))==27, 'El atlas debe contener 27 pueblos únicos'
for feature in features:
    p=feature['properties']
    assert all(p.get(k) for k in ['id','name','kind','note','refs','era'])
    assert p['id'].startswith('tribus/')
    geom=feature['geometry']
    if p['kind']=='desconocida':
        assert geom is None, p['name']
    else:
        assert geom is not None, p['name']
        assert geom['type'] in ['Point','MultiPoint','Polygon','MultiPolygon']
    assert p['kind'] in ['aproximada','difusa','nucleo','nucleos','desconocida']
base=json.loads((R/'data/entries.json').read_text(encoding='utf-8'))
new=json.loads((R/'data/tribus_nuevas.json').read_text(encoding='utf-8'))['new_entries']
expected={e['id'] for e in base if e['category']=='tribus' and e['id']!='tribus/amorreo'}
expected|={e['id'] for e in new}
assert set(ids)==expected, 'El atlas y el apéndice no contienen los mismos pueblos'
site=R/'docs/apendices/atlas-pueblos/index.html'
assert site.exists() and 'atlas-pueblos' in site.read_text(encoding='utf-8')
assert (R/'docs/assets/atlas/pentateuco.geojson').read_bytes()==(R/'assets/atlas/pentateuco.geojson').read_bytes()
for p in ['visor.js','atlas.css']:
    assert (R/'docs/assets/atlas'/p).read_bytes()==(R/'assets/atlas'/p).read_bytes()
for eid in ids:
    file=R/'docs/apendices'/eid/'index.html'
    assert file.exists(), eid
    h=file.read_text(encoding='utf-8')
    assert '#pueblo='+quote(eid,safe='') in h, f'Sin enlace al atlas: {eid}'
assert 'Atlas de Pueblos' in (R/'docs/apendices/tribus/index.html').read_text(encoding='utf-8')
assert 'atlas-pueblos/index.html' in (R/'docs/apendices/index.html').read_text(encoding='utf-8')
assert 'atlas-pueblos/index.html' in (R/'docs/apendices/mapas/index.html').read_text(encoding='utf-8')
print('OK: Atlas de Pueblos, 27 fichas enlazadas, geometrías y recursos publicados.')
