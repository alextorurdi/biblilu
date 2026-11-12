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
    assert old_ch3 or fragment.startswith(('lamina=','persona=')),(p,address,'missing anchor')

V=json.loads((ROOT/'data/genesis.json').read_text(encoding='utf-8'))
assert len(V)==425
normalize=lambda x:re.sub(r'\s+',' ',x).strip()
all_text=''
def scene_path(c,v):
 if c in (16,17):return '16'
 if c==15:return '15'
 if c==14:return '14'
 if c in (12,13):return '12'
 if c==11:return '11' if v<=9 else '11-10'
 if c==10:return '10'
 if c in (6,7,8,9):return '6'
 if c==5 or (c==4 and v>=25):return '5'
 if c==4:return '4'
 if c==3:return '2'
 if c==2:return '1' if v<=3 else '2'
 return '1'

for verse in V:
 c,v=verse['chapter'],verse['verse']
 unit=scene_path(c,v)
 path=SITE/f'genesis/{unit}/index.html'
 html=path.read_text(encoding='utf-8')
 match=re.search(r'<p class="verse(?: poetry)?" id="gn-'+str(c)+'-'+str(v)+r'">(.*?)</p>',html,re.S)
 assert match,(c,v,'missing canonical verse')
 text=re.sub(r'<sup class="fn-marker">[\s\S]*?</sup>','',match[1])
 text=re.sub(r'<a class="verse-num"[\s\S]*?</a>','',text)
 text=unescape(re.sub(r'<[^>]+>','',text))
 assert normalize(text.replace('— ',''))==normalize(verse['text']),(c,v,'verse text changed')
 for speech in re.findall(r'<span class="divine">([\s\S]*?)</span>',match[1]):
  assert not re.search(r'<a(?![^>]*class="fn-link")',speech),(c,v,'divine text has hyperlink')
 all_text+=match[1]
for unit,min_n,max_n in [(1,1,8),(2,9,22),(4,23,39),(5,40,53),(6,54,67),(10,68,76),('11',77,78),('11-10',79,81),('12',82,93),('14',94,103),('15',104,110),('16',111,121)]:
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
print(f'OK: {len(parsed)} páginas; 425 versículos, 121 notas, dos índices, anclas canónicas y marcado divino.')

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
assert len(_bib)==60
for _n,_name in ((53,'Embry'),(54,'Bergsma'),(55,'Alexander')):
 assert _name in _bib[_n-1]
 assert f'href="../../bibliografia/index.html#ref-{_n}"' in scene_5
 assert f'id="ref-{_n}"' in (SITE/'bibliografia/index.html').read_text(encoding='utf-8')
assert 'id="fn-67"' in scene_5

# Escena 6: texto de Gn 10, notas consecutivas y cartografía con árboles genealógicos.
scene_6=(SITE/'genesis/10/index.html').read_text(encoding='utf-8')
assert all(f'id="gn-10-{n}"' in scene_6 for n in range(1,33))
assert len(re.findall(r'<li id="fn-(?:6[89]|7[0-6])"',scene_6))==9
assert scene_6.count('class="dispersion-map"')==3
assert scene_6.count('class="dispersion-tree-mobile"')==3
assert scene_6.count('data-dispersion-panel=')==3
assert '<a href="10/index.html#gn-10-1">' in (SITE/'genesis/index.html').read_text(encoding='utf-8')
assert '<a href="../10/index.html">Dispersión →</a>' in scene_5
for _name in ('jafet','cam','sem'):
 assert (SITE/f'assets/mapas/{_name}.svg').exists()
for _sheet in ('03','04','05'):
 assert (SITE/f'assets/genealogias/{_sheet}.svg').exists()
print('OK: Dispersión · 32 versículos, notas 68–76, tres mapas y tres árboles.')

# Dispersión móvil: cada árbol desplegable se sitúa justo después del último
# versículo de su sección y antes del mapa correspondiente, sin cambiar el lateral.
for _last, _label in ((5, 'Jafet'), (20, 'Cam'), (32, 'Sem')):
 _verse=scene_6.index(f'id="gn-10-{_last}"')
 _end=scene_6.index('</p>', _verse)+4
 _tree=scene_6.index('<details class="dispersion-tree-mobile">', _end)
 _map=scene_6.index('<figure class="dispersion-map">', _tree)
 assert scene_6[_end:_tree].strip() == '', (_label, 'tree not directly after section')
 assert scene_6[_tree:_map].endswith('</details>'), (_label, 'map not directly after tree')

# v0.5: las dos escenas de Gn 11 se distribuyen entre 11:1–9 y 11:10–32.
for _unit,_first,_last,_notes in [('11',1,9,(77,78)),('11-10',10,32,(79,80,81))]:
 _page=(SITE/f'genesis/{_unit}/index.html').read_text(encoding='utf-8')
 assert all(f'id="gn-11-{_n}"' in _page for _n in range(_first,_last+1))
 assert all(f'id="fn-{_n}"' in _page and f'id="fnref-{_n}"' in _page for _n in _notes)
assert 'babel-v05.svg' in (SITE/'genesis/11/index.html').read_text(encoding='utf-8')
_scene8=(SITE/'genesis/11-10/index.html').read_text(encoding='utf-8')
assert 'genealogias/06.svg' in _scene8 and 'ur-haran-map' in _scene8
assert 'href="11/index.html"' in (SITE/'genesis/index.html').read_text(encoding='utf-8')
assert 'href="11-10/index.html"' in (SITE/'genesis/index.html').read_text(encoding='utf-8')
print('OK: v0.5 · Génesis 11:1–32, notas 77–81, dos escenas, Babel, genealogía 06 y mapa.')

# Escena 12 · Legado: capítulos 16 y 17, once notas y tres inserciones visuales.
legado=(SITE/'genesis/16/index.html').read_text(encoding='utf-8')
assert all(f'id="gn-16-{n}"' in legado for n in range(1,17))
assert all(f'id="gn-17-{n}"' in legado for n in range(1,28))
assert legado.count('class="legado-mobile-art')==3
assert legado.count('class="legado-panel')==3
assert 'data-legado-side' in legado
assert 'id="gn-16-7"' in legado and 'id="gn-17-15"' in legado
assert '<a href="16/index.html#gn-16-1">' in (SITE/'genesis/index.html').read_text(encoding='utf-8')
assert '<a href="16/index.html#gn-17-1">' in (SITE/'genesis/index.html').read_text(encoding='utf-8')
for _asset in ('legado-mapa.svg','legado-agar-angel.webp','legado-instrumento.webp','legado.css','legado.js'):
 assert (SITE/'assets'/_asset).exists()
assert 'legado-agar-angel.webp' in legado and 'legado-instrumento.webp' in legado
assert 'legado-mapa.svg?v=20261112def' in legado
print('OK: Legado · 43 versículos, 11 notas (111–121), mapa e ilustraciones definitivas.')
