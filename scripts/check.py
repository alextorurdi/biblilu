from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit, unquote
import json,re

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'docs'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__()
  self.ids=set()
  self.urls=[]
  self.feed(text)
 def handle_starttag(self,tag,attrs):
  data=dict(attrs)
  if 'id' in data:
   assert data['id'] not in self.ids,('duplicate',data['id'])
   self.ids.add(data['id'])
  for key in ('href','src'):
   if data.get(key):self.urls.append(data[key])
parsed={p.resolve():Page(p.read_text(encoding='utf-8')) for p in SITE.rglob('*.html')}
for p,doc in parsed.items():
 for address in doc.urls:
  url=urlsplit(address)
  if url.scheme or url.netloc:continue
  dest=(p.parent/unquote(url.path)).resolve() if url.path else p
  if dest.is_dir():dest=dest/'index.html'
  assert dest.exists(),(p,address,'missing file')
  if url.fragment and dest in parsed:
   fragment=unquote(url.fragment)
   if fragment not in parsed[dest].ids:
    # Enlaces de fichas preexistentes: la ruta de Génesis 3 redirige
    # conservando el versículo; Gn 2:1–3 pertenece a «Creación».
    old_ch3=dest== (SITE/'genesis/3/index.html').resolve() and re.fullmatch(r'v[1-9]\d*',fragment)
    assert old_ch3,(p,address,'missing anchor')

V=json.loads((ROOT/'data/genesis.json').read_text(encoding='utf-8'))
assert len(V)==235
normalize=lambda x:re.sub(r'\s+',' ',x).strip()
all_text=''
for verse in V:
 c,v=verse['chapter'],verse['verse']
 unit=6 if c in (6,7,8,9) else (5 if c==5 or (c==4 and v>=25) else (4 if c==4 else (1 if c==1 or (c==2 and v<=3) else 2)))
 path=SITE/f'genesis/{unit}/index.html'
 html=path.read_text(encoding='utf-8')
 match=re.search(r'<p class="verse(?: poetry)?" id="gn-'+str(c)+'-'+str(v)+r'">(.*?)</p>',html,re.S)
 assert match,(c,v,'missing canonical verse')
 text=re.sub(r'<sup class="fn-marker">[\s\S]*?</sup>','',match[1])
 text=re.sub(r'<a class="verse-num"[\s\S]*?</a>','',text)
 text=unescape(re.sub(r'<[^>]+>','',text))
 assert normalize(text)==normalize(verse['text']),(c,v,'verse text changed')
 for speech in re.findall(r'<span class="divine">([\s\S]*?)</span>',match[1]):
  assert not re.search(r'<a(?![^>]*class="fn-link")',speech),(c,v,'divine text has hyperlink')
 all_text+=match[1]
for unit,min_n,max_n in [(1,1,8),(2,9,22),(4,23,39),(5,40,53),(6,54,67)]:
 html=(SITE/f'genesis/{unit}/index.html').read_text(encoding='utf-8')
 a=[int(x) for x in re.findall(r'id="fnref-(\d+)"',html)]
 b=[int(x) for x in re.findall(r'<li id="fn-(\d+)"',html)]
 assert a==list(range(min_n,max_n+1)),(unit,a)
 assert b==list(range(min_n,max_n+1)),(unit,b)
assert '<span class="divine">No moriréis' not in all_text
assert 'id="infographic-title"' in (SITE/'genesis/1/index.html').read_text(encoding='utf-8')
assert 'id="gn-3-24"' in (SITE/'genesis/2/index.html').read_text(encoding='utf-8')
assert 'location.replace' in (SITE/'genesis/3/index.html').read_text(encoding='utf-8')
assert 'Escenas del manuscrito' in (SITE/'genesis/index.html').read_text(encoding='utf-8')
assert 'Génesis 4' in (SITE/'genesis/index.html').read_text(encoding='utf-8')
assert 'data-scene="crueldad"' in (SITE/'genesis/4/index.html').read_text(encoding='utf-8')
assert 'data-illustration="music"' in (SITE/'genesis/4/index.html').read_text(encoding='utf-8')
assert 'id="fnref-27"' in (SITE/'genesis/4/index.html').read_text(encoding='utf-8')
assert '“dadora de vida”' in (SITE/'genesis/2/index.html').read_text(encoding='utf-8')
print(f'OK: {len(parsed)} páginas; 235 versículos, 67 notas, dos índices, anclas canónicas y marcado divino.')

# La escena 4 abarca Gn 4:25–5:32; el árbol 02 cambia a cronología en Gn 5:25.
scene_4=(SITE/'genesis/5/index.html').read_text(encoding='utf-8')
assert 'id="gn-4-25"' in scene_4 and 'id="gn-5-32"' in scene_4
assert 'data-panel="chronology"' in scene_4 and 'id="gn-5-25"' in scene_4
assert 'src="../../assets/genealogias/02.svg"' in scene_4
assert scene_4.count('id="v25"')==1 and scene_4.count('id="v26"')==1

# La escena 5 incluye Génesis 6–9, cinco ilustraciones y la cronología final.
scene_5=(SITE/'genesis/6/index.html').read_text(encoding='utf-8')
assert 'id="gn-6-1"' in scene_5 and 'id="gn-8-22"' in scene_5
assert scene_5.count('class="flood-mobile-art"')==5
assert scene_5.count('data-flood-panel=')==5
assert 'id="cronologia-diluvio"' in scene_5
assert 'href="../6/index.html"' in (SITE/'genesis/5/index.html').read_text(encoding='utf-8')

# Restauración de Génesis 9, después del arcoíris y antes de la cronología.
assert all(f'id="gn-9-{n}"' in scene_5 for n in range(1,30))
assert scene_5.index('diluvio-arcoiris.webp') < scene_5.index('id="gn-9-1"') < scene_5.index('id="gn-9-29"') < scene_5.index('id="cronologia-diluvio"')
assert 'id="fn-66"' in scene_5 and 'id="fn-67"' in scene_5
assert '<a href="6/index.html#gn-9-1">' in (SITE/'genesis/index.html').read_text(encoding='utf-8')

# Bibliografía de Génesis 9:25: correspondencia entre la nota 67 y las fuentes.
_bib=json.loads((ROOT/'data/bibliography.json').read_text(encoding='utf-8'))
assert len(_bib)==55
for _n,_name in ((53,'Embry'),(54,'Bergsma'),(55,'Alexander')):
 assert _name in _bib[_n-1]
 assert f'href="../../bibliografia/index.html#ref-{_n}"' in scene_5
 assert f'id="ref-{_n}"' in (SITE/'bibliografia/index.html').read_text(encoding='utf-8')
assert 'id="fn-67"' in scene_5
