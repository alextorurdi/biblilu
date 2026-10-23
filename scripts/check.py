from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'docs'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.urls=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:
   assert d['id'] not in self.ids,('duplicate',d['id']);self.ids.add(d['id'])
  for k in ['href','src']:
   if d.get(k):self.urls.append(d[k])
parsed={p.resolve():Page(p.read_text()) for p in SITE.rglob('*.html')}
for p,doc in parsed.items():
 for u in doc.urls:
  url=urlsplit(u)
  if url.scheme or url.netloc:continue
  dest=(p.parent/unquote(url.path)).resolve() if url.path else p
  if dest.is_dir():dest=dest/'index.html'
  assert dest.exists(),(p,u)
  if url.fragment and dest in parsed:assert unquote(url.fragment) in parsed[dest].ids,(p,u,'missing anchor')
from html import unescape
V=json.loads((ROOT/'data/genesis.json').read_text())
normalize=lambda t:re.sub(r'\s+',' ',t).strip()
for v in V:
 text=(SITE/f'genesis/{v["chapter"]}/index.html').read_text()
 p=re.search(r'<p class="verse" id="v'+str(v['verse'])+r'">(.*?)</p>',text,re.S)[1]
 p=re.sub(r'<a class="verse-num".*?</a>','',p);p=re.sub(r'<span class="note".*?</span>','',p)
 assert normalize(unescape(re.sub('<[^>]+>','',p)))==normalize(v['text']),(v['chapter'],v['verse'],'text changed')
 for divine in re.findall(r'<span class="divine">(.*?)</span>',p,re.S):assert '<a ' not in divine
 assert not re.search(r'<a [^>]*>\s*(Dios|Jehová)(?: Dios)?\s*</a>',p)
assert [sum(v['chapter']==c for v in V) for c in [1,2,3]]==[31,25,24]
g3=(SITE/'genesis/3/index.html').read_text()
assert '<span class="divine">¿Dónde estás tú?</span>' in g3 or '<span class="divine"> \n¿Dónde estás tú?</span>' in g3
assert '<span class="divine">No moriréis' not in g3
assert 'image2.jpeg' not in ''.join(p.read_text() for p in SITE.rglob('*.html'))
print(f'OK: {len(parsed)} páginas; enlaces y anclas válidos; 80 versículos sin cambios; marcado divino sin hipervínculos.')
