from pathlib import Path
import json,re,html,os,shutil,unicodedata
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs';OUT.mkdir(exist_ok=True)
E=json.loads((ROOT/'data/entries.json').read_text());V=json.loads((ROOT/'data/genesis.json').read_text());B=json.loads((ROOT/'data/bibliography.json').read_text())
# Las revisiones aprobadas de Materiales se aplican sobre el catálogo de origen
# antes de generar las páginas y el índice de búsqueda.
MATERIAL_REVISION=json.loads((ROOT/'data/materiales_revision.json').read_text(encoding='utf-8'))
OBJECT_REVISION=json.loads((ROOT/'data/objetos_revision.json').read_text(encoding='utf-8'))
INSTRUMENT_REVISION=json.loads((ROOT/'data/instrumentos_revision.json').read_text(encoding='utf-8'))
for _entry in E:
 _eid=_entry['id']
 if _eid in MATERIAL_REVISION['titles']:
  _entry['title']=MATERIAL_REVISION['titles'][_eid]
 if _eid in MATERIAL_REVISION['revised']:
  _entry.update(MATERIAL_REVISION['revised'][_eid])
  _entry['text']=_entry['title']+'. '+_entry['body']
 if _eid in OBJECT_REVISION['titles']:
  _entry['title']=OBJECT_REVISION['titles'][_eid]
 if _eid in OBJECT_REVISION['revised']:
  _entry.update(OBJECT_REVISION['revised'][_eid])
  _entry['text']=_entry['title']+'. '+_entry['body']
 if _eid in INSTRUMENT_REVISION['titles']:
  _entry['title']=INSTRUMENT_REVISION['titles'][_eid]
 if _eid in INSTRUMENT_REVISION['revised']:
  _entry.update(INSTRUMENT_REVISION['revised'][_eid])
  _entry['text']=_entry['title']+'. '+_entry['body']
H=html.escape
GENEALOGY_LINKS=json.loads((ROOT/'assets/genealogias/enlaces.json').read_text(encoding='utf-8'))
MAPS=json.loads((ROOT/'assets/mapas/catalogo.json').read_text(encoding='utf-8'))
ENTRY_TO_PERSON=GENEALOGY_LINKS['entry_to_person']
PERSON_TO_SHEETS=GENEALOGY_LINKS.get('person_to_sheets', {})
C={'onomastico':('Onomástico','Personas y relaciones familiares'),'lugares':('Lugares','La geografía del relato'),'animales':('Seres Vivos','Animales, plantas y criaturas celestiales'),'materiales':('Materiales','Materias primas, metales y minerales'),'tribus':('Tribus','Pueblos de la Antigüedad'),'objetos':('Objetos y símbolos','Objetos, construcciones y señales especiales'),'instrumentos':('Instrumentos musicales','La música y sus instrumentos en la Biblia'),'medidas':('Pesos, medidas y monedas','Unidades, equivalencias y valores bíblicos')}
byid={e['id']:e for e in E};links={}
# Selección contextual para Génesis 1–3. No se enlazan homónimos automáticamente.
for cat,names in {'onomastico':['Adán','Eva','Varona'],'materiales':['Oro','Bedelio','Ónice'],'objetos':['Espada encendida'],'lugares':['Edén','Pisón','Havila','Gihón','Cus','Hidekel','Asiria','Eúfrates'],'animales':['Higuera','Querubín','Serpiente','Cardo','Árbol de la Vida','Árbol de la Ciencia del Bien y del Mal']}.items():
 for name in names:
  found=next((e for e in E if e['category']==cat and e['name'].lower()==name.lower()),None)
  if found:links[name.lower()]=found['id']
links.update({'éufrates':'lugares/eufrates','querubines':'animales/querubin','cardos':'animales/cardo','árbol de vida':'animales/arbol-de-la-vida','árbol de la vida':'animales/arbol-de-la-vida','serpiente':'animales/serpiente'})
links.update({'abram':'onomastico/abram','abraham':'onomastico/abraham','sarai':'onomastico/sarai','sara':'onomastico/sara','agar':'onomastico/agar','ismael':'onomastico/ismael','isaac':'onomastico/isaac','shur':'lugares/shur','cades':'lugares/cades','bered':'lugares/bered','canaán':'lugares/canaan','ángel de jehová':'animales/angel-de-jehova','pozo del viviente-que-me-ve':'lugares/pozo-del-viviente-que-me-ve'})
links.update({'lot':'onomastico/lot','moab':'onomastico/moab','ben-ammi':'onomastico/ben-ammi','mamre':'lugares/mamre','sodoma':'lugares/sodoma','gomorra':'lugares/gomorra','zoar':'lugares/zoar','ángeles':'animales/angeles','moabitas':'tribus/moabitas','amonitas':'tribus/amonitas'})
links.update({'abimelec':'onomastico/abimelec','ficol':'onomastico/ficol','efrón':'onomastico/efron','zohar':'onomastico/zohar','gerar':'lugares/gerar','beerseba':'lugares/beerseba','parán':'lugares/paran','moriah':'lugares/moriah','hebrón':'lugares/hebron','quiriat-arba':'lugares/quiriat-arba','macpela':'lugares/macpela','filisteos':'tribus/filisteos','heteos':'tribus/heteo','carnero':'animales/carnero','tamarisco':'animales/tamarisco','siclo':'medidas/siclo','siclos':'medidas/siclo'})
links={k:v for k,v in links.items() if v in byid}
# Las palabras de Dios prevalecen sobre los enlaces de categorías.
aftercolon={(1,n) for n in [3,6,9,11,14,20,22,24,26,28,29]}|{(2,n) for n in [16,18]}|{(3,n) for n in [1,3,9,11,13,14,16,17,22]}
full={(1,15),(1,30),(2,17),(3,15),(3,18),(3,19)}
def mark(text,pre,divine=False):
 if divine:return '<span class="divine">'+H(text)+'</span>'
 pat=r'\b(?:Jehová(?: Dios)?|Dios|'+ '|'.join(re.escape(x) for x in sorted(links,key=len,reverse=True))+r')\b'
 def sub(m):
  word=m[0]
  if re.fullmatch(r'Jehová(?: Dios)?|Dios',word,re.I):return '<span class="divine">'+H(word)+'</span>'
  eid=links[word.lower()];cat=eid.split('/')[0]
  return f'<a class="term {cat}" data-entry="{eid}" href="{pre}apendices/{eid}/index.html">{H(word)}</a>'
 return re.sub(pat,sub,text,flags=re.I)
def verse(v,pre):
 t=v['text'];key=(v['chapter'],v['verse']);start=end=None
 if key in full:start=0;end=len(t)
 elif key in aftercolon:
  start=t.find(':')+1;end=len(t)
  if key==(3,1):start=t.find('No comáis') # cita atribuida a Dios dentro de la pregunta
  if key==(3,13):end=t.find('Y dijo la mujer:')
 if start is not None:
  if key[0]==1:
   for ending in ['; y fue la luz.',' Y fue así.']:
    match=re.search(r'\s+Y fue así\.',t[start:]) if ending==' Y fue así.' else re.search(re.escape(ending),t[start:])
    if match:end=min(end,start+match.start())
  rendered=mark(t[:start],pre)+mark(t[start:end],pre,True)+mark(t[end:],pre)
 else:rendered=mark(t,pre)
 label=v['source_label'].split('-')[1]
 note=' <span class="note" title="Numeración conservada del documento original; revisión pendiente.">†</span>' if key==(2,2) else ''
 return f'<p class="verse" id="v{v["verse"]}"><a class="verse-num" href="#v{v["verse"]}" aria-label="Enlace a Génesis {key[0]}:{key[1]}">{label}</a>{note} {rendered}</p>'
def rel(path):return '../'*len(Path(path).parent.parts) if str(Path(path).parent)!='.' else ''
def page(path,title,body,kind=''):
 pre=rel(path);p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True)
 # Versionado del CSS para evitar estilos antiguos cacheados en el índice de Seres Vivos.
 css_version='?v=seres-vivos-index-20261118-2' if str(path)=='apendices/animales/index.html' else '?v=materiales-lingotes-20261118' if str(path)=='apendices/materiales/index.html' else '?v=objetos-revision-20261119' if str(path).startswith('apendices/objetos/') else ''
 p.write_text(f'''<!doctype html><html lang="es-ES"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="BIBLILU: una Biblia ilustrada para leer, descubrir y explorar. Génesis y sus apéndices."><title>{H(title)} · BIBLILU</title><link rel="icon" href="{pre}assets/favicon.svg"><link rel="stylesheet" href="{pre}assets/style.css{css_version}"><script src="{pre}assets/app.js" defer></script></head><body data-base="{pre}" class="{kind}"><a class="skip" href="#contenido">Saltar al contenido</a><header class="header"><a class="brand" href="{pre}index.html">BIBLILU<span>LA BIBLIA ILUSTRADA</span></a><nav aria-label="Principal"><a href="{pre}index.html#libros">Los libros</a><a href="{pre}apendices/index.html">Apéndices</a><a href="{pre}bibliografia/index.html">Bibliografía</a></nav></header><main id="contenido">{body}</main><footer><a class="brand" href="{pre}index.html">BIBLILU</a><p>Una lectura que también se contempla.</p><a href="{pre}sobre/index.html">Sobre el proyecto y créditos</a><span>Español · RVR 1960</span></footer><dialog id="entry-dialog" aria-labelledby="dialog-title"><button class="close" aria-label="Cerrar ficha">×</button><div id="dialog-content"></div></dialog></body></html>''',encoding='utf-8')
def onomastic_card(pre):
 return f'<div class="appendix-card onomastico appendix-card-family"><a class="appendix-card-main" href="{pre}apendices/onomastico/index.html"><span class="dot"></span><h3>Onomástico</h3><p>Personas y relaciones familiares</p><span aria-hidden="true">↗</span></a><a class="appendix-tree-link" href="{pre}apendices/genealogias/index.html">Árboles genealógicos <span aria-hidden="true">↗</span></a></div>'
def places_card(pre):
 return f'<div class="appendix-card lugares appendix-card-family"><a class="appendix-card-main" href="{pre}apendices/lugares/index.html"><span class="dot"></span><h3>Lugares</h3><p>La geografía del relato</p><span aria-hidden="true">↗</span></a><a class="appendix-tree-link" href="{pre}apendices/mapas/index.html">Mapas <span aria-hidden="true">↗</span></a></div>'
def map_links(e,pre):
 matches=[(m,l) for m in MAPS for l in m['labels'] if e['id'] in l['entries']]
 if not matches:return ''
 seen=set(); links=[]
 for m,l in matches:
  if m['id'] in seen:continue
  seen.add(m['id'])
  links.append(f'<a href="{pre}apendices/mapas/index.html#mapa={m["id"]}&amp;lugar={e["id"]}">{H(m["title"])} ↗</a>')
 return '<div class="map-links"><strong>En los mapas</strong>'+''.join(links)+'</div>'
def cards(pre, appendix_index=False):
 result=[]
 for cat,(name,desc) in C.items():
  if cat=='onomastico':
   result.append(onomastic_card(pre))
  elif cat=='lugares':
   result.append(places_card(pre))
  else:
   label=name
   result.append(f'<a class="appendix-card {cat}" href="{pre}apendices/{cat}/index.html"><span class="dot"></span><h3>{label}</h3><p>{desc}</p><span aria-hidden="true">↗</span></a>')
 return ''.join(result)
old='Génesis|Éxodo|Levítico|Números|Deuteronomio|Josué|Jueces|Rut|1 Samuel|2 Samuel|1 Reyes|2 Reyes|1 Crónicas|2 Crónicas|Esdras|Nehemías|Ester|Job|Salmos|Proverbios|Eclesiastés|Cantares|Isaías|Jeremías|Lamentaciones|Ezequiel|Daniel|Oseas|Joel|Amós|Abdías|Jonás|Miqueas|Nahúm|Habacuc|Sofonías|Hageo|Zacarías|Malaquías'.split('|')
new='Mateo|Marcos|Lucas|Juan|Hechos|Romanos|1 Corintios|2 Corintios|Gálatas|Efesios|Filipenses|Colosenses|1 Tesalonicenses|2 Tesalonicenses|1 Timoteo|2 Timoteo|Tito|Filemón|Hebreos|Santiago|1 Pedro|2 Pedro|1 Juan|2 Juan|3 Juan|Judas|Apocalipsis'.split('|')
def books(items):return ''.join('<a class="book available" href="genesis/index.html"><span>01</span><strong>Génesis</strong><small>Capítulos 1–24 disponibles ↗</small></a>' if b=='Génesis' else f'<div class="book pending"><strong>{b}</strong><small>Próximamente</small></div>' for b in items)
page('index.html','La Biblia ilustrada',f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">UN LIBRO. MUCHAS FORMAS DE DESCUBRIRLO.</p><h1>Las palabras.<br>Las imágenes.<br><em>El principio.</em></h1><p class="intro">Recorre la Biblia a través de sus relatos, sus imágenes y el mundo que habita en cada palabra.</p><a class="button" href="genesis/1/index.html">Comenzar la lectura <span>↗</span></a><a class="quiet" href="#libros">Explorar los libros ↓</a><p class="edition">PRIMERA ENTREGA &nbsp; / &nbsp; GÉNESIS 1–10</p></div><figure class="hero-art"><img src="assets/creacion.jpg" alt="Ilustración de la creación: luz, astros, animales y naturaleza"><figcaption>01 / La creación</figcaption></figure></section><section id="libros" class="section"><p class="eyebrow">LA BIBLIOTECA</p><h2>Un recorrido, libro a libro.</h2><p>Los capítulos se incorporan a medida que están preparados.</p><h3 class="testament">Antiguo Testamento <span>39 libros</span></h3><div class="books">{books(old)}</div><details class="new-testament"><summary>Nuevo Testamento <span>27 libros</span></summary><div class="books">{books(new)}</div></details></section><section class="section tinted"><p class="eyebrow">MÁS ALLÁ DEL VERSÍCULO</p><h2>Cada palabra abre un mundo.</h2><p>Consulta los nombres, los lugares y los elementos del relato en nuestros cinco apéndices.</p><div class="appendix-grid">{cards('')}</div></section>''')
page('genesis/index.html','Génesis','''<section class="book-hero"><div><p class="eyebrow">ANTIGUO TESTAMENTO / LIBRO 01</p><h1>Génesis</h1><p class="intro">Los comienzos: el mundo, la vida y los primeros pasos de la humanidad.</p><a class="button" href="1/index.html">Leer el primer capítulo ↗</a><p>8 de 50 capítulos disponibles</p></div><img src="../assets/eden.jpg" alt="El jardín de Edén"></section><section class="section"><h2>Índice de capítulos</h2><div class="chapter-grid">'''+''.join(f'<a href="{i}/index.html"><b>{i:02}</b><span>{["La creación","El huerto de Edén","Fuera del paraíso"][i-1]}</span>↗</a>' if i<=3 else f'<div class="pending"><b>{i:02}</b><span>Próximamente</span></div>' for i in range(1,51))+'''</div></section>''')
art={1:('creacion.jpg','La creación'),2:('eden.jpg','El huerto de Edén'),3:('tentación.png','La serpiente y el fruto')};titles={1:'La creación',2:'El huerto de Edén',3:'Fuera del paraíso'}
for c in [1,2,3]:
 pre='../../';vs=[v for v in V if v['chapter']==c]
 toolbar='''<div class="reader-tools"><label>Capítulo <select id="chapter-select">'''+''.join(f'<option value="../{i}/index.html" {"selected" if i==c else ""}>{i}</option>' for i in [1,2,3])+'''</select></label><button id="font-minus" aria-label="Reducir tamaño de letra">A−</button><button id="font-plus" aria-label="Aumentar tamaño de letra">A+</button><button id="toggle-images" aria-pressed="false">Ocultar imágenes</button><button id="toggle-colors" aria-pressed="false">Ocultar colores</button></div>'''
 legend='<div class="legend">'+''.join(f'<span class="{cat}">● {n}</span>' for cat,(n,_) in C.items())+'<span class="divine">● Dios y sus palabras</span></div>'
 note='<p class="source-note">† Se conserva la numeración del original: el segundo pasaje aparece también como «2-1».</p>' if c==2 else ''
 im,alt=art[c]
 reading=''
 for v in vs:
  reading+=verse(v,pre)
  if v['verse']=={1:13,2:14,3:7}[c]:reading+=f'<figure class="mobile-art"><img loading="lazy" src="{pre}assets/{im}" alt="{alt}"><figcaption>{alt} · Génesis {c}</figcaption></figure>'
  if c==3 and v['verse']==24:reading+=f'<figure class="mobile-art sword"><img loading="lazy" src="{pre}assets/espada.jpg" alt="Una espada rodeada de llamas"><figcaption>La espada encendida · Génesis 3:24</figcaption></figure>'
 body=f'<div class="reader-heading"><p class="crumb"><a href="../../index.html">Biblia</a> / <a href="../index.html">Génesis</a> / {c}</p><p class="eyebrow">GÉNESIS · CAPÍTULO {c:02}</p><h1>{titles[c]}</h1><p class="subtitle">Reina-Valera 1960 · Edición ilustrada</p>{toolbar}{legend}</div><div class="reading-layout"><article class="verses">'+reading+note+f'</article><aside class="reading-art"><figure><img src="{pre}assets/{im}" alt="{alt}"><figcaption>{alt} · Génesis {c}</figcaption></figure>'+(f'<figure class="sword"><img loading="lazy" src="{pre}assets/espada.jpg" alt="Una espada rodeada de llamas"><figcaption>La espada encendida · Génesis 3:24</figcaption></figure>' if c==3 else '')+'</aside></div>'
 body+='<nav class="chapter-nav" aria-label="Navegación de capítulos">'+(f'<a href="../{c-1}/index.html">← Capítulo {c-1}</a>' if c>1 else '<a href="../index.html">← Índice de Génesis</a>')+(f'<a href="../{c+1}/index.html">Capítulo {c+1} →</a>' if c<3 else '<span>Capítulo 4 · Próximamente</span>')+'</nav>'
 page(f'genesis/{c}/index.html',f'Génesis {c}',body,'reader')
headings=['Relaciones familiares','Hechos bíblicos','Identificación','Ubicación e identificación','Etimología','Referencias','Descripción','Simbolismo cultural','Simbolismo','Apariciones','Especie','Estado actual','Estado de conservación','Cultura','Controversia','Ubicación']
def heading_title(e):
 title=H(e['title'])
 return re.sub(r'\*([^*]+)\*',r'<em>\1</em>',title) if e['category']=='animales' else title

def living_index_title(e):
 title=heading_title(e)
 if e['category'] in ('materiales','objetos','instrumentos'):
  if ' (' in title and title.endswith(')'):
   name,term=title.rsplit(' (',1)
   css={'materiales':'material-index-original','objetos':'object-index-original','instrumentos':'instrument-index-original'}[e['category']]
   return name+' <small class="'+css+'"><em>'+term[:-1]+'</em></small>'
 # El subtítulo "ser sobrenatural" es editorial, no una forma hebrea.
 if e['category']!='animales' or e['id']=='animales/serpiente':
  return title
 parts=re.fullmatch(r'(.+?)\s+(\(.*\))',title)
 if not parts:
  return title
 return parts.group(1)+' <small class="living-index-original">'+parts.group(2)+'</small>'

def entry_heading_title(e):
 title=heading_title(e)
 if e['category'] in ('materiales','objetos','instrumentos'):
  if ' (' in title and title.endswith(')'):
   name,term=title.rsplit(' (',1)
   css={'materiales':'material-title-secondary','objetos':'object-title-secondary','instrumentos':'instrument-title-secondary'}[e['category']]
   return name+'<span class="'+css+'">'+term[:-1]+'</span>'
 if e['category']!='animales':
  return title
 parts=re.fullmatch(r'(.+?)\s+(\(.*\))',title)
 if not parts:
  return title
 return parts.group(1)+'<span class="living-title-secondary">'+parts.group(2)+'</span>'

def species_figure(e):
 photo=e.get('image') if e['category']=='animales' else None
 if not photo:return ''
 image_url='https://commons.wikimedia.org/wiki/Special:FilePath/'+quote(photo['file'])
 author=photo.get('author') or 'Autor en la ficha original'
 caption='<em>'+H(photo['scientific'])+'</em> · '+H(author)+' · '+H(photo['license'])
 return '<figure class="species-photo"><a href="'+H(image_url)+'" target="_blank" rel="noopener noreferrer" aria-label="Ampliar fotografía de '+H(photo['scientific'])+'"><img src="'+H(image_url)+'" alt="Fotografía natural: '+H(photo['scientific'])+'" loading="lazy" decoding="async"></a><figcaption>'+caption+' · <a href="'+H(photo['source'])+'" target="_blank" rel="noopener noreferrer">Fuente y licencia</a></figcaption></figure>'

def material_figure(e):
 if e['category']!='materiales':return ''
 photo=MATERIAL_REVISION.get('images',{}).get(e['id'])
 if not photo:return ''
 image_url='https://commons.wikimedia.org/wiki/Special:FilePath/'+quote(photo['file'])
 source_url=photo['source']
 caption=H(photo['caption'])+' · '+H(photo['author'])+' · '+H(photo['license'])
 return (
  '<figure class="material-photo">'
  +'<a class="material-photo-view" href="'+H(source_url)+'" target="_blank" rel="noopener noreferrer" aria-label="Ver fotografía y licencia de '+H(e['name'])+'">'
  +'<img src="'+H(image_url)+'" alt="'+H(photo['alt'])+'" loading="lazy" decoding="async">'
  +'</a><figcaption>'+caption+' · <a href="'+H(source_url)+'" target="_blank" rel="noopener noreferrer">Fuente y licencia</a></figcaption></figure>'
 )

def object_figure(e):
 if e['category']!='objetos':return ''
 photo=OBJECT_REVISION.get('images',{}).get(e['id'])
 if not photo:return ''
 image_url='../../../assets/'+quote(photo['local']) if 'local' in photo else 'https://commons.wikimedia.org/wiki/Special:FilePath/'+quote(photo['file'])
 source_url=photo['source']
 caption=H(photo['caption'])+' · '+H(photo['author'])+' · '+H(photo['license'])
 return (
  '<figure class="object-photo">'
  +'<a class="object-photo-view" href="'+H(source_url)+'" aria-label="Ver fuente y licencia de '+H(e['name'])+'"' + (' target="_blank" rel="noopener noreferrer"' if source_url.startswith('http') else '') + '>'
  +'<img src="'+H(image_url)+'" alt="'+H(photo['alt'])+'" loading="lazy" decoding="async">'
  +'</a><figcaption>'+caption+' · <a href="'+H(source_url)+'"'+(' target="_blank" rel="noopener noreferrer"' if source_url.startswith('http') else '')+'>Fuente y licencia</a></figcaption></figure>'
 )

def instrument_figure(e):
 if e['category']!='instrumentos':return ''
 photo=INSTRUMENT_REVISION.get('images',{}).get(e['id'])
 if not photo:return ''
 image_url='../../../assets/'+quote(photo['local'])
 source_url=photo['source']
 caption=H(photo['caption'])+' · '+H(photo['author'])+' · '+H(photo['license'])
 return (
  '<figure class="instrument-photo"><a class="instrument-photo-view" href="'+H(image_url)+'" target="_blank" rel="noopener noreferrer" aria-label="Ampliar ilustración de '+H(e['name'])+'">'
  +'<img src="'+H(image_url)+'" alt="'+H(photo['alt'])+'" loading="lazy" decoding="async"></a>'
  +'<figcaption>'+caption+' · <a href="'+H(source_url)+'">Ver en la escena Crueldad</a></figcaption></figure>'
 )

def entrybody(e,pre):
 raw=e['body']
 if e['category'] in ('animales','materiales','objetos','instrumentos') and (raw.startswith('Ver ') or '\n### ' in raw):
  def inline(v):
   v=H(v)
   v=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',v)
   return re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)',r'<em>\1</em>',v)
  chunks=[]
  for block in re.split(r'\n\s*\n',raw.strip()):
   if block.startswith('### '):
    chunks.append('<h2>'+H(block[4:].strip())+'</h2>')
   elif block.startswith('- '):
    chunks.append('<ul>'+''.join('<li>'+inline(line[2:].strip())+'</li>' for line in block.splitlines() if line.startswith('- '))+'</ul>')
   else:
    chunks.append('<p>'+inline(block.replace('\n',' '))+'</p>')
  out=''.join(chunks)
 else:
  pats='|'.join(map(re.escape,headings));pieces=re.split(r'(?<!\w)('+pats+r')[.:]\s*',raw)
  out='<p>'+H(pieces[0])+'</p>' if pieces[0].strip() else ''
  for i in range(1,len(pieces),2):
   fragment=H(pieces[i+1]);fragment=re.sub(r'\*([^*]+)\*',r'<em>\1</em>',fragment)
   out+=f'<h2>{H(pieces[i])}</h2><p>{fragment}</p>'
 # Referencias a pasajes disponibles, sin alterar el texto visible.
 def ref(m):
  c=int(m[1]);v=int(m[2]);return f'<a href="{pre}genesis/{scene_path_for({"chapter":c,"verse":v})}/index.html#gn-{c}-{v}">{m[0]}</a>' if any(x['chapter']==c and x['verse']==v for x in V) else m[0]
 out=re.sub(r'\b(?:Gn|Gen|Génesis)\s+(\d+):(\d+)(?:-\d+)?',ref,out)
 def cite(m):
  s=html.unescape(m[1]);first=s.split(',')[0].strip().lower();first='day' if first=='john day' else first;year=re.search(r'\d{4}',s);candidates=[i for i,b in enumerate(B) if first in b.lower() and (not year or year[0] in b)]
  target=f'#ref-{candidates[0]+1}' if len(candidates)==1 else ''
  return f'<a href="{pre}bibliografia/index.html{target}">{m[0]}</a>'
 # Internal cross-links in approved geographical entries: [[category/slug|label]]
 def internal(m):
  target,label=m[1],html.unescape(m[2])
  assert target in {x['id'] for x in E}, ('invalid internal link',target)
  return f'<a href="{pre}apendices/{target}/index.html">{H(label)}</a>'
 out=re.sub(r'\[\[([a-z]+/[a-z0-9-]+)\|([^\]\n]+)\]\]',internal,out)
 out=re.sub(r'(?<!\[)\[([^\[\]]+)\](?!\])',cite,out)
 if raw.startswith('Ver '):
  target=raw[4:].rstrip('.');dest=next((x for x in E if x['category']==e['category'] and x['name']==target),None)
  if dest:out=f'<p>Ver <a href="{pre}apendices/{dest["id"]}/index.html">{H(target)}</a>.</p>'
 return out
page('apendices/index.html','Apéndices','<section class="section"><p class="eyebrow">GUÍAS DE LECTURA</p><h1>El mundo de la Biblia.</h1><p class="intro">Ocho caminos para explorar lo que aparece en el relato.</p><div class="appendix-grid">'+cards('../')+'</div></section>')
def spanish_alphabetical_key(label):
 normalized=unicodedata.normalize('NFD',label.casefold()).replace('n\u0303','n~')
 return ''.join(char for char in normalized if not unicodedata.combining(char))

SERES_VIVOS_TYPES = {
 "animales/arbol-de-la-ciencia-del-bien-y-del-mal": "vegetal",
 "animales/arbol-de-la-vida": "vegetal",
 "animales/cardo": "vegetal",
 "animales/centaurea": "vegetal",
 "animales/higuera": "vegetal",
 "animales/lentejas": "vegetal",
 "animales/matorral": "vegetal",
 "animales/olivo": "vegetal",
 "animales/tamarisco": "vegetal",
 "animales/vid": "vegetal",
 "animales/vina": "vegetal",
 "animales/zarzal": "vegetal",
 "animales/asno": "animal",
 "animales/asno-montes": "animal",
 "animales/aves-de-rapina": "animal",
 "animales/becerro": "animal",
 "animales/burro": "animal",
 "animales/cabra": "animal",
 "animales/camello": "animal",
 "animales/carnero": "animal",
 "animales/cordero": "animal",
 "animales/cuervo": "animal",
 "animales/ganado-bovino": "animal",
 "animales/onagro": "animal",
 "animales/oveja": "animal",
 "animales/paloma": "animal",
 "animales/palomino": "animal",
 "animales/serpiente-natural": "animal",
 "animales/tortola": "animal",
 "animales/vaca": "animal",
 "animales/angel-de-jehova": "sobrenatural",
 "animales/angeles": "sobrenatural",
 "animales/nefilim": "sobrenatural",
 "animales/querubin": "sobrenatural",
 "animales/serpiente": "sobrenatural",
}
SERES_VIVOS_ICONS = {
 "vegetal": "<svg viewBox=\"0 0 24 24\" width=\"18\" height=\"18\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 21V11\"/><path d=\"M12 14C6 14 4 10 4 5c6 0 9 3 8 9Z\"/><path d=\"M12 11c0-6 3-9 9-9 0 6-3 9-9 9Z\"/></svg>",
 "animal": "<svg viewBox=\"0 0 24 24\" width=\"18\" height=\"18\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.45\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M7 8a3 3 0 0 1 5-2 3 3 0 0 1 4 2 3 3 0 0 1 2 5 3 3 0 0 1-3 4H7a3 3 0 0 1-3-4 3 3 0 0 1 3-5Z\"/><path d=\"M7 17v3h3v-3M14 17v3h3v-4\"/><path d=\"M16 9c2-3 5-2 5 1v4c0 2-1 3-3 3h-1\"/><path d=\"M19 10l2-1M19 13h.01\"/><path d=\"M4 11 2 10\"/></svg>",
 "sobrenatural": "<svg viewBox=\"0 0 24 24\" width=\"18\" height=\"18\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><ellipse cx=\"12\" cy=\"3.5\" rx=\"4.2\" ry=\"1.5\"/><circle cx=\"12\" cy=\"9\" r=\"3\"/><path d=\"M7 14c-3-3-6-2-5 2l5 5 2-3M17 14c3-3 6-2 5 2l-5 5-2-3M9 14h6l2 8H7l2-8Z\"/></svg>",
}
SERES_VIVOS_LABELS = {"vegetal":"Vegetal","animal":"Animal","sobrenatural":"Ser sobrenatural"}

for cat,(name,desc) in C.items():
 entries=[e for e in E if e['category']==cat]
 if cat in ('animales','materiales','objetos','instrumentos','medidas'):
  entries.sort(key=lambda e: spanish_alphabetical_key(e['name']))
 family_link='<a class="button genealogy-directory-link" href="../genealogias/index.html">Explorar los árboles genealógicos ↗</a>' if cat=='onomastico' else '<a class="button genealogy-directory-link" href="../mapas/index.html">Explorar los mapas ↗</a>' if cat=='lugares' else ''
 def render_index_row(e):
  slug=e['id'].split('/')[1]
  person=ENTRY_TO_PERSON.get(slug) if cat=='onomastico' else None
  has_map=(cat=='lugares' and any(e['id'] in label['entries'] for m in MAPS for label in m['labels']))
  tree_glyph='<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 6v5M5 17v-6h14v6"/><rect x="9" y="2" width="6" height="4" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/></svg>'
  map_glyph='<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/></svg>'
  if person:
   suffix='<span class="entry-row-tail"><span class="genealogy-index-mark" role="img" aria-label="Incluido en los árboles genealógicos" title="Representado en los árboles genealógicos">'+tree_glyph+'</span><span>↗</span></span>'
  elif has_map:
   suffix='<span class="entry-row-tail"><span class="map-index-mark" role="img" aria-label="Representado en los mapas" title="Representado en los mapas">'+map_glyph+'</span><span>↗</span></span>'
  elif cat=='materiales' and e['id'] in MATERIAL_REVISION.get('images',{}):
   # Tres lingotes en pirámide (uno arriba, dos abajo), con el color del apéndice.
   ingots='<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="M10 3.5h4l2.5 6.5h-9L10 3.5Z"/><path d="M4.5 12.5h4l2.5 7h-9l2.5-7Z"/><path d="M15.5 12.5h4l2.5 7h-9l2.5-7Z"/></svg>'
   suffix='<span class="entry-row-tail"><span class="material-index-mark" role="img" aria-label="Ficha con fotografía" title="Ficha con fotografía">'+ingots+'</span><span>↗</span></span>'
  elif cat=='objetos' and e['id'] in OBJECT_REVISION.get('images',{}):
   # Tienda estilizada: marca común de las fichas ilustradas de Objetos y símbolos.
   glyph='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 2.5 20h19L12 3Z"/><path d="M12 3v11"/><path d="m8.5 20 3.5-6 3.5 6"/></svg>'
   suffix='<span class="entry-row-tail"><span class="object-index-mark" role="img" aria-label="Ficha ilustrada" title="Ficha con imagen">'+glyph+'</span><span>↗</span></span>'
  elif cat=='animales':
   kind=SERES_VIVOS_TYPES[e['id']]
   glyph=SERES_VIVOS_ICONS[kind]
   kind_label=SERES_VIVOS_LABELS[kind]
   suffix=f'<span class="entry-row-tail"><span class="living-index-mark living-index-mark--{kind}" role="img" aria-label="{kind_label}" title="{kind_label}">{glyph}</span><span>↗</span></span>'
  else:
   suffix='<span>↗</span>'
  extras={'onomastico/jacob':'Israel','onomastico/jose':'Zafnat-panea','onomastico/eliezer':'siervo de Abraham siervo de Abram mayordomo','onomastico/abraham':'Abram','onomastico/sara':'Sarai','onomastico/benjamin':'Benoni'}
  family=re.search(r'Relaciones familiares[.:]\s*(.*?)(?=Hechos bíblicos[.:]|Identificación[.:]|Etimología[.:]|$)',e['body'])
  query=' '.join([e['title'], e['name'], extras.get(e['id'],''), family.group(1)[:200] if family else '']).lower()
  return f'<a class="entry-row {cat}" data-search="{H(query)}" href="{slug}/index.html"><strong>{living_index_title(e)}</strong>{suffix}</a>'
 listing=''.join(render_index_row(e) for e in entries)
 count_label='entrada' if len(entries)==1 else 'entradas'
 intro=desc
 if cat=='animales':
  intro=(
   f'<span class="living-legend-part">Animales{SERES_VIVOS_ICONS["animal"]}</span>, '
   f'<span class="living-legend-part">plantas{SERES_VIVOS_ICONS["vegetal"]}</span> y criaturas '
   f'<span class="living-legend-part">celestiales{SERES_VIVOS_ICONS["sobrenatural"]}</span>'
  )
 page(f'apendices/{cat}/index.html',name,f'<section class="section directory"><p class="crumb"><a href="../index.html">Apéndices</a> / {name}</p><p class="eyebrow">{len(entries)} {count_label.upper()}</p><h1 class="{cat}">{name}</h1><p class="intro">{intro}</p>{family_link}<label class="search-label" for="entry-search">Buscar en este apéndice</label><input id="entry-search" type="search" placeholder="Escribe un nombre o término…"><p id="result-count" role="status">{len(entries)} {count_label}</p><div class="entry-list">{listing}</div></section>')
def body_with_genealogy(e):
 body=entrybody(e,'../../../')
 if e['category']=='instrumentos':
  related=[byid[i] for i in INSTRUMENT_REVISION.get('related',{}).get(e['id'],[]) if i in byid]
  if related:
   links=''.join('<a href="../../../apendices/'+H(item['id'])+'/index.html">'+H(item['name'])+'</a>' for item in related)
   body+='<nav class="instrument-related" aria-label="Fichas relacionadas"><strong>Fichas relacionadas</strong><div class="instrument-related-links">'+links+'</div></nav>'
  return body
 if e['category']=='objetos':
  # Insertar figuras documentadas en su posición editorial dentro del texto.
  for illustration in OBJECT_REVISION.get('inline_images',{}).get(e['id'],[]):
   anchor='<p>'+H(illustration['after'])+'</p>'
   if anchor not in body:raise RuntimeError('No se encontró párrafo para imagen en '+e['id'])
   image_url='../../../assets/'+quote(illustration['asset'])
   fig=(
    '<figure class="object-inline-figure"><a href="'+H(image_url)+'" target="_blank" rel="noopener noreferrer" aria-label="Ampliar esquema de '+H(e['name'])+'">'
    +'<img src="'+H(image_url)+'" alt="'+H(illustration['alt'])+'" loading="lazy" decoding="async"></a>'
    +'<figcaption>'+H(illustration['caption'])+'</figcaption></figure>'
   )
   body=body.replace(anchor,anchor+fig,1)
  related=[byid[i] for i in OBJECT_REVISION.get('related',{}).get(e['id'],[]) if i in byid]
  if related:
   links=''.join('<a href="../../../apendices/'+H(item['id'])+'/index.html">'+H(item['name'])+'</a>' for item in related)
   body+='<nav class="object-related" aria-label="Fichas relacionadas"><strong>Fichas relacionadas</strong><div class="object-related-links">'+links+'</div></nav>'
  return body
 if e['category']=='materiales':
  related=[byid[i] for i in MATERIAL_REVISION['related'].get(e['id'],[]) if i in byid]
  if related:
   links=''.join('<a href="../../../apendices/'+H(item['id'])+'/index.html">'+H(item['name'])+'</a>' for item in related)
   body+='<nav class="material-related" aria-label="Fichas relacionadas"><strong>Fichas relacionadas</strong><div class="material-related-links">'+links+'</div></nav>'
  return body
 if e['category']=='lugares':
   panel=map_links(e,'../../../')
   if e['id']=='lugares/egipto':return body+panel # Excepción editorial: no intervenir en Egipto.
   if not panel:return body
   found=re.search(r'(<h2>(?:Ubicación(?: e identificación)?|Identificación)</h2><p>.*?</p>)',body,flags=re.S)
   if not found:found=re.search(r'(<h2>Hechos bíblicos</h2><p>.*?</p>)',body,flags=re.S)
   if not found:found=re.search(r'(<p>.*?</p>)',body,flags=re.S)
   return body[:found.end()]+panel+body[found.end():] if found else body+panel
 if e['category']!='onomastico':return body
 person=ENTRY_TO_PERSON.get(e['id'].split('/')[1])
 if not person:return body
 sections=PERSON_TO_SHEETS.get(person, ['general'])
 links=''.join(
   f'<a class="genealogy-person-link" href="../../../apendices/genealogias/index.html#persona={H(person)}&amp;lamina={H(section)}">'
   +(f'Lámina {H(section)} ↗' if section!='general' else 'Árbol general ↗')+'</a>'
   for section in sections
 )
 panel='<div class="genealogy-person-links"><strong>Árboles genealógicos</strong>'+links+'</div>'
 pattern=r'(<h2>Relaciones familiares</h2><p>.*?</p>)'
 return re.sub(pattern,lambda m:m.group(1)+panel,body,count=1) if re.search(pattern,body) else body+panel

AVAILABLE_VERSES={(v['chapter'],v['verse']) for v in V}

def scene_path_for(v):
 c,n=v['chapter'],v['verse']
 if c==3:return '2'  # Génesis 3 está en la escena Paraíso.
 if c==24:return '24'
 if c in (20,21,22,23):return '20'
 if c in (18,19):return '18'
 if c in (16,17):return '16'
 if c in (12,13):return '12'
 if c==15:return '15'
 if c==14:return '14'
 if c==11:return '11' if n<=9 else '11-10'
 if c in (6,7,8,9):return '6'
 if c==5 or (c==4 and n>=25):return '5'
 return str(c)

for e in E:
 cat=e['category'];chron='<p class="source-note">Las fechas expresan años desde la Creación según la cronología del Génesis.</p>' if cat=='onomastico' and re.search(r'\(\d',e['title']) else ''
 body_html=body_with_genealogy(e)
 # Una sola relación de referencias por ficha:
 # - Fichas con «Referencias» propio: no añadir un segundo listado.
 # - Fichas con «Menciones bíblicas»: enlazar pasajes ya publicados; omitir
 #   «En la lectura disponible» para evitar cientos de enlaces redundantes.
 # - Sin ninguno de los anteriores: conservar los enlaces a la lectura.
 has_references=bool(re.search(r'<h[2-6]>\s*Referencias(?: bíblicas)?\s*</h[2-6]>',body_html,re.I))
 mention_labels=e.get('mentions',[])
 biblical_mentions=''
 if mention_labels and not has_references:
  def linked_mention(label):
   match=re.match(r'^(?:Gn|Gen|Génesis)\s+(\d+):(\d+)',label,re.I)
   if not match:return H(label)
   chapter,verse_no=map(int,match.groups())
   if (chapter,verse_no) not in AVAILABLE_VERSES:return H(label)
   dest=scene_path_for({'chapter':chapter,'verse':verse_no})
   return f'<a href="../../../genesis/{dest}/index.html#gn-{chapter}-{verse_no}">{H(label)}</a>'
  biblical_mentions='<div class="backlinks"><h2>Menciones bíblicas</h2><p>'+ ' · '.join(linked_mention(r) for r in mention_labels)+'</p></div>'
 backlinks=''
 if not has_references and not mention_labels:
  mentions=[]
  for v in V:
   rendered=verse(v,'../../../')
   if f'data-entry="{e["id"]}"' in rendered:mentions.append(f'<a href="../../../genesis/{scene_path_for(v)}/index.html#gn-{v["chapter"]}-{v["verse"]}">Gn {v["chapter"]}:{v["verse"]}</a>')
  backlinks='<div class="backlinks"><h2>En la lectura disponible</h2>'+ ' · '.join(mentions)+'</div>' if mentions else ''
 page(f'apendices/{e["id"]}/index.html',e['title'],f'<article class="section entry"><p class="crumb"><a href="../../index.html">Apéndices</a> / <a href="../index.html">{C[cat][0]}</a></p><p class="eyebrow {cat}">{C[cat][0]}</p><h1>{entry_heading_title(e)}</h1>{chron}<div class="entry-body {cat}">{species_figure(e)}{material_figure(e)}{object_figure(e)}{instrument_figure(e)}{body_html}</div>{backlinks}{biblical_mentions}</article>')
page('bibliografia/index.html','Bibliografía','<section class="section bibliography"><p class="eyebrow">LAS FUENTES</p><h1>Bibliografía</h1><p class="intro">Obras y recursos que acompañan los apéndices de BIBLILU.</p><ol>'+''.join(f'<li id="ref-{i+1}">{H(b)}</li>' for i,b in enumerate(B))+'</ol></section>')
page('sobre/index.html','Sobre BIBLILU','''<section class="section entry"><p class="eyebrow">EL PROYECTO</p><h1>Leer. Mirar. Descubrir.</h1><p class="intro">BIBLILU es una edición ilustrada de la Biblia que conecta cada relato con sus personajes, lugares y referencias.</p><h2>Una publicación en marcha</h2><p>Esta entrega contiene Génesis 1–15. Los demás capítulos y libros se incorporarán progresivamente.</p><h2>Texto e ilustraciones</h2><p>Texto base: Reina-Valera 1960, según los documentos aportados por el editor. Se conserva su redacción. Las ilustraciones fueron creadas con ChatGPT para el proyecto BIBLILU.</p><p>Reina-Valera 1960 ® © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.</p><h2>Cómo leer los colores</h2><p>Los enlaces coloreados abren los apéndices. Dios, Jehová y las palabras atribuidas a Dios aparecen en rojo, sin hipervínculos. Las criaturas celestiales se incluyen en Animales.</p><h2>La cronología de Génesis</h2><p>Las fechas de las fichas del Génesis se expresan en años desde la Creación según el propio relato; no son fechas antes de Cristo.</p></section>''')

page('apendices/genealogias/index.html','Árboles genealógicos', '''<section class="section genealogy-page"><p class="crumb"><a href="../index.html">Apéndices</a> / <a href="../onomastico/index.html">Onomástico</a> / Árboles genealógicos</p><p class="eyebrow onomastico">APÉNDICE GENEALÓGICO · GÉNESIS</p><h1>De Adán y Eva<br>a las últimas generaciones.</h1><p class="intro">Explora las filiaciones del Génesis en un árbol general y 19 láminas. Busca un nombre, amplía una rama o consulta las referencias y los casos ambiguos.</p><div class="genealogy-actions"><a class="button" href="../../assets/genealogias/visor.html" target="_blank" rel="noopener">Abrir visor en una pestaña ↗</a><a class="genealogy-return" href="../onomastico/index.html">Consultar el índice onomástico →</a></div><iframe class="genealogy-frame" src="../../assets/genealogias/visor.html" title="Árboles genealógicos del Génesis: buscador y 19 láminas" loading="eager"></iframe><p class="source-note">Pulsa un nombre para consultar sus relaciones y abrir su ficha del Onomástico. Los nombres conservan los colores del modelo: rojo para varones y violeta para mujeres. Las entradas colectivas y las filiaciones incompletas se identifican por separado. Las referencias y los criterios de inclusión se pueden consultar dentro del visor.</p></section>''', 'genealogy')

# Mantener los enlaces históricos al trasladar fichas a sus nuevos apéndices.
MOVED_FROM_MATERIALES = {"altar":"objetos","arca-de-noe":"objetos","arco-iris":"objetos","espada-encendida":"objetos","tienda":"objetos","torre-de-babel":"objetos","kinnor":"instrumentos","ugab":"instrumentos","siclo":"medidas"}
for old_slug,new_category in MOVED_FROM_MATERIALES.items():
 redirect=f'../../{new_category}/{old_slug}/index.html'
 legacy=OUT/f'apendices/materiales/{old_slug}/index.html'
 legacy.parent.mkdir(parents=True,exist_ok=True)
 legacy.write_text('<!doctype html><html lang="es-ES"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0; url='+redirect+'"><link rel="canonical" href="'+redirect+'"><title>Ficha trasladada · BIBLILU</title></head><body><p>Esta ficha se encuentra en otro apéndice: <a href="'+redirect+'">Abrir la ficha</a>.</p></body></html>',encoding='utf-8')

page('apendices/mapas/index.html','Mapas','<section class="section"><p class="crumb"><a href="../index.html">Apéndices</a> / <a href="../lugares/index.html">Lugares</a> / Mapas</p><p class="eyebrow lugares">CARTOGRAFÍA · GÉNESIS</p><h1>Los lugares del relato.</h1><p class="intro">Explora los 15 mapas de las escenas. Elige un mapa o busca un lugar para encontrar todas sus apariciones.</p><div id="map-viewer" class="map-viewer"><div class="map-controls"><label for="map-select">Mapa<select id="map-select"></select></label><label for="map-search">Buscar un lugar o mapa<input type="search" id="map-search" placeholder="Harán, Canaán, Familia…" autocomplete="off" aria-controls="map-results"></label></div><div id="map-results" class="map-results" aria-live="polite" hidden></div><div class="map-buttons"><button id="map-in" aria-label="Ampliar mapa">+</button><button id="map-out" aria-label="Reducir mapa">−</button><button id="map-reset">Ver mapa completo</button><button id="map-full">Pantalla completa</button></div><p id="map-status" class="map-status" role="status">Cargando catálogo…</p><div id="map-canvas" class="map-canvas" tabindex="0" role="region" aria-label="Mapa interactivo. Usa las flechas para desplazar y más o menos para ampliar."></div><div id="map-caption" class="map-caption"></div></div><p class="source-note">Los resaltados señalan los rótulos del mapa. Las áreas, rutas e identificaciones aproximadas conservan las advertencias del original; un resaltado no implica una ubicación arqueológica segura.</p><details><summary>Índice de mapas y archivos originales</summary><ul>'+''.join(f'<li><a href="../../assets/{m["asset"]}">{H(m["title"])}</a></li>' for m in MAPS)+'</ul></details><p><a href="../lugares/index.html">Consultar el Apéndice de Lugares →</a></p></section><script src="../../assets/mapas/visor.js" defer></script>')

shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'assets/genealogias/familiares.json').write_text(json.dumps({e['name']:e['id'].split('/')[1] for e in E if e['category']=='onomastico'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'assets/entries.json').write_text(json.dumps({e['id']:{'title':e['title'],'category':C[e['category']][0],'body':e['body'],'mentions':e.get('mentions',[])} for e in E},ensure_ascii=False))
(OUT/'.nojekyll').touch()
print('Generadas',len(list(OUT.rglob('*.html'))),'páginas estáticas.')

# Restaurar las páginas temáticas que cuentan con revisión editorial aprobada.
# No regenerarlas según la división bíblica convencional ni perder sus notas.
for _relative in ('index.html','genesis/index.html','genesis/1/index.html','genesis/2/index.html','genesis/3/index.html','genesis/4/index.html','genesis/5/index.html','genesis/6/index.html','genesis/10/index.html','genesis/11/index.html','genesis/11-10/index.html','genesis/12/index.html','genesis/14/index.html','genesis/15/index.html','genesis/16/index.html','genesis/17/index.html','genesis/18/index.html','genesis/19/index.html','genesis/20/index.html','genesis/21/index.html','genesis/22/index.html','genesis/23/index.html','genesis/24/index.html','articulos/concepto-dia-genesis/index.html','articulos/cosmologia-hebrea/index.html'):
 _source=ROOT/'editorial'/'approved-pages'/_relative
 if _source.exists():
  _dest=OUT/_relative
  _dest.parent.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(_source,_dest)
# Enlazar las menciones aprobadas de «puerta» en las escenas temáticas,
# después de restaurar sus originales editoriales y sin reescribir sus notas.
_SCENE_PUERTA_REFS={
 '4':{(4,7)},
 '6':{(6,16),(7,16)},
 '18':{(18,1),(18,2),(18,10),(19,1),(19,6),(19,9),(19,10),(19,11)},
 '20':{(22,17),(23,10),(23,18)},
 '24':{(24,60)}
}
_PUERTA_LINK='<a class="term objetos" data-entry="objetos/puerta" href="../../apendices/objetos/puerta/index.html">'
for _scene,_target_verses in _SCENE_PUERTA_REFS.items():
 _file=OUT/'genesis'/_scene/'index.html'
 if not _file.exists():continue
 _html=_file.read_text(encoding='utf-8')
 _seen=set()
 def _wrap_puerta(_match):
  _key=(int(_match[1]),int(_match[2]))
  if _key not in _target_verses:return _match[0]
  _seen.add(_key)
  _tokens=re.split(r'(<[^>]+>)',_match[0])
  for _k in range(0,len(_tokens),2):
   _tokens[_k]=re.sub(r'\bpuertas?\b',lambda _w:_PUERTA_LINK+_w[0]+'</a>',_tokens[_k],flags=re.I)
  return ''.join(_tokens)
 _html=re.sub(r'<p class="verse" id="gn-(\d+)-(\d+)"[^>]*>.*?</p>',_wrap_puerta,_html,flags=re.S)
 if _seen!=_target_verses:raise RuntimeError(f'Menciones a puerta sin encontrar en escena {_scene}: {_target_verses-_seen}')
 if _scene=='24':
  _note=re.search(r'<li id="fn-150">.*?</li>',_html,flags=re.S)
  if not _note or 'La «puerta»' not in _note[0]:raise RuntimeError('Nota 150 no localizada para enlazar Puerta')
  _html=_html[:_note.start()]+_note[0].replace('La «puerta»','La «'+_PUERTA_LINK+'puerta</a>»',1)+_html[_note.end():]
 _file.write_text(_html,encoding='utf-8')

print('Plantillas temáticas BIBLILU v. 0.1 restauradas.')
