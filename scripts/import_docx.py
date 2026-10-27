"""Importación literal de documentos BIBLILU. Uso: python scripts/import_docx.py ../upload"""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import re,json,sys,unicodedata
ROOT=Path(__file__).resolve().parents[1]; SRC=Path(sys.argv[1]); W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
def paragraphs(name):
 with ZipFile(SRC/name) as z:
  root=ET.fromstring(z.read('word/document.xml'))
  return [''.join(p.itertext()) for p in []] or [''.join(t.text or '' for t in p.iter(W+'t')) for p in root.find(W+'body').findall(W+'p')]
def slug(t):return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()).strip('-')
def save(name,obj):(ROOT/'data'/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
ps=paragraphs('Genesis.docx');active=False;parts=[]
for t in ps:
 if t.startswith('1-1 '):active=True
 if t.startswith('4-1 '):break
 if active and t.strip() and not t.isupper() and t not in ['Paraíso','Crueldad','Creación']:parts.append(t)
text='\n'.join(parts);matches=list(re.finditer(r'(?<!\d)([1-3])-(\d+)\s+',text));verses=[];counts={}
for i,m in enumerate(matches):
 c=int(m[1]);counts[c]=counts.get(c,0)+1
 verses.append({'chapter':c,'verse':counts[c],'source_label':m[0].strip(),'text':text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)].strip()})
assert [counts.get(i) for i in [1,2,3]]==[31,25,24],counts
save('genesis.json',verses)
entries=[]
for cat,file in [('onomastico','PERSONAJES'),('materiales','MATERIALES'),('animales','ANIMALES'),('lugares','LUGARES'),('tribus','TRIBUS')]:
 seen={}
 for t in paragraphs('Genesis - '+file+'.docx'):
  t=t.strip()
  if not t or t.startswith('GLOSARIO'):continue
  title=re.split(r'\.|:',t,maxsplit=1)[0].strip(); name=title.split(' (')[0].strip();key=slug(name);seen[key]=seen.get(key,0)+1
  if seen[key]>1:key+='-'+str(seen[key])
  entries.append({'id':cat+'/'+key,'category':cat,'name':name,'title':title,'text':t,'body':t[len(title):].lstrip('.: ')})
save('entries.json',entries)
save('bibliography.json',[t.strip() for t in paragraphs('Genesis - BIBLIOGRAFÍA.docx') if t.strip() and t.strip()!='BIBLIOGRAFÍA'])
with ZipFile(SRC/'Genesis.docx') as z:
 for a,b in [('image5.jpeg','creacion.jpg'),('image6.jpeg','eden.jpg'),('image8.jpeg','espada.jpg')]:
  (ROOT/'assets'/b).write_bytes(z.read('word/media/'+a))
# La ilustración aprobada de La Caída se conserva como PNG independiente.
# No sobrescribirla con la imagen WebP incrustada en el Word.
fall_image=ROOT/'assets'/'tentación.png'
if not fall_image.is_file():
 raise FileNotFoundError(f'Falta la ilustración aprobada: {fall_image}')
print(f'{len(verses)} versículos, {len(entries)} fichas importadas; imágenes sin el marco independiente.')
