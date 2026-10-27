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
assert len(V)==80
normalize=lambda x:re.sub(r'\s+',' ',x).strip()
all_text=''
for verse in V:
 c,v=verse['chapter'],verse['verse']
 unit=1 if c==1 or (c==2 and v<=3) else 2
 path=SITE/f'genesis/{unit}/index.html'
 html=path.read_text(encoding='utf-8')
 match=re.search(r'<p class="verse" id="gn-'+str(c)+'-'+str(v)+r'">(.*?)</p>',html,re.S)
 assert match,(c,v,'missing canonical verse')
 text=re.sub(r'<sup class="fn-marker">[\s\S]*?</sup>','',match[1])
 text=re.sub(r'<a class="verse-num"[\s\S]*?</a>','',text)
 text=unescape(re.sub(r'<[^>]+>','',text))
 assert normalize(text)==normalize(verse['text']),(c,v,'verse text changed')
 for speech in re.findall(r'<span class="divine">([\s\S]*?)</span>',match[1]):
  assert '<a ' not in speech,(c,v,'divine text has hyperlink')
 all_text+=match[1]
for unit,min_n,max_n in [(1,1,8),(2,9,22)]:
 html=(SITE/f'genesis/{unit}/index.html').read_text(encoding='utf-8')
 a=[int(x) for x in re.findall(r'id="fnref-(\d+)"',html)]
 b=[int(x) for x in re.findall(r'<li id="fn-(\d+)"',html)]
 assert a==list(range(min_n,max_n+1)),(unit,a)
 assert b==list(range(min_n,max_n+1)),(unit,b)
assert '<span class="divine">No moriréis' not in all_text
assert 'id="infographic-title"' in (SITE/'genesis/1/index.html').read_text(encoding='utf-8')
assert 'id="gn-3-24"' in (SITE/'genesis/2/index.html').read_text(encoding='utf-8')
assert 'location.replace' in (SITE/'genesis/3/index.html').read_text(encoding='utf-8')
assert 'Capítulos del manuscrito' in (SITE/'genesis/index.html').read_text(encoding='utf-8')
print(f'OK: {len(parsed)} páginas; 80 versículos, 22 notas, dos índices, anclas canónicas y marcado divino.')
