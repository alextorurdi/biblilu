"""Validate the map catalogue and scene/place deep links against actual SVG labels."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, parse_qs
import json, re, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
M=json.loads((R/'assets/mapas/catalogo.json').read_text())
E={e['id'] for e in json.loads((R/'data/entries.json').read_text())}
byid={m['id']:m for m in M}
assert len(byid)==len(M)==15
for m in M:
 asset=R/'assets'/m['asset']
 assert asset.read_bytes()==(R/'docs/assets'/m['asset']).read_bytes()
 labels=list(ET.parse(asset).getroot().iter('{http://www.w3.org/2000/svg}text'))
 for l in m['labels']:
  assert ''.join(labels[l['index']].itertext())==l['label']
  assert set(l['entries'])<=E
class Links(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='a':self.links.append(d.get('href',''))
count=0
for p in (R/'docs').rglob('*.html'):
 for href in Links(p.read_text()).links:
  u=urlsplit(href)
  if not u.fragment.startswith('mapa='):continue
  assert (p.parent/u.path).resolve()==(R/'docs/apendices/mapas/index.html').resolve()
  q=parse_qs(u.fragment);m=byid[q['mapa'][0]]
  if 'lugar' in q:assert any(q['lugar'][0] in l['entries'] for l in m['labels'])
  count+=1
for m in M:
 scene=R/'docs/genesis'/m['scene']/'index.html'
 assert '#mapa='+m['id']+'"' in scene.read_text()
 # El generador restaura la fuente aprobada y luego inserta vínculos a Puerta/Codo/Sea.
 # Comparar tras retirar SOLO esas inserciones; cualquier otra divergencia falla.
 rendered=scene.read_text(encoding='utf-8')
 approved=(R/'editorial/approved-pages/genesis'/m['scene']/'index.html').read_text(encoding='utf-8')
 without_links=re.sub(r'<a class="term (?:objetos|medidas)" data-entry="(?:objetos/puerta|medidas/(?:codo|sea))" href="../../apendices/[^\"]+">([^<]*)</a>',r'\1',rendered)
 assert without_links==approved,(m['id'],'contenido cartográfico divergente de la fuente aprobada')
for eid in {eid for m in M for l in m['labels'] for eid in l['entries']}:
 text=(R/'docs/apendices'/eid/'index.html').read_text()
 expected={m['id'] for m in M if any(eid in l['entries'] for l in m['labels'])}
 actual={parse_qs(urlsplit(h).fragment)['mapa'][0] for h in Links(text).links if urlsplit(h).fragment.startswith('mapa=')}
 assert actual==expected,(eid,actual,expected)
print(f'OK: {len(M)} mapas; {count} enlaces; todas las fichas incluyen todos sus mapas; SVG originales intactos.')
