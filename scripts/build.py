from pathlib import Path
import json,re,html,os,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs';OUT.mkdir(exist_ok=True)
E=json.loads((ROOT/'data/entries.json').read_text());V=json.loads((ROOT/'data/genesis.json').read_text());B=json.loads((ROOT/'data/bibliography.json').read_text())
H=html.escape
C={'onomastico':('Onomástico','Personas y relaciones familiares'),'materiales':('Materiales','Objetos, minerales y símbolos'),'animales':('Animales','Animales, plantas y criaturas celestiales'),'lugares':('Lugares','La geografía del relato'),'tribus':('Tribus','Pueblos de la Antigüedad')}
byid={e['id']:e for e in E};links={}
# Selección contextual para Génesis 1–3. No se enlazan homónimos automáticamente.
for cat,names in {'onomastico':['Adán','Eva','Varona'],'materiales':['Oro','Bedelio','Ónice','Espada encendida'],'lugares':['Edén','Pisón','Havila','Gihón','Cus','Hidekel','Asiria','Eúfrates'],'animales':['Higuera','Querubín','Serpiente','Cardo','Árbol de la Vida','Árbol de la Ciencia del Bien y del Mal']}.items():
 for name in names:
  found=next((e for e in E if e['category']==cat and e['name'].lower()==name.lower()),None)
  if found:links[name.lower()]=found['id']
links.update({'éufrates':'lugares/eufrates','querubines':'animales/querubin','cardos':'animales/cardo','árbol de vida':'animales/arbol-de-la-vida','árbol de la vida':'animales/arbol-de-la-vida','serpiente':'animales/serpiente'})
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
 p.write_text(f'''<!doctype html><html lang="es-ES"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="BIBLILU: una Biblia ilustrada para leer, descubrir y explorar. Génesis y sus apéndices."><title>{H(title)} · BIBLILU</title><link rel="icon" href="{pre}assets/favicon.svg"><link rel="stylesheet" href="{pre}assets/style.css"><script src="{pre}assets/app.js" defer></script></head><body data-base="{pre}" class="{kind}"><a class="skip" href="#contenido">Saltar al contenido</a><header class="header"><a class="brand" href="{pre}index.html">BIBLILU<span>LA BIBLIA ILUSTRADA</span></a><nav aria-label="Principal"><a href="{pre}index.html#libros">Los libros</a><a href="{pre}apendices/index.html">Apéndices</a><a href="{pre}bibliografia/index.html">Bibliografía</a></nav></header><main id="contenido">{body}</main><footer><a class="brand" href="{pre}index.html">BIBLILU</a><p>Una lectura que también se contempla.</p><a href="{pre}sobre/index.html">Sobre el proyecto y créditos</a><span>Español · RVR 1960</span></footer><dialog id="entry-dialog" aria-labelledby="dialog-title"><button class="close" aria-label="Cerrar ficha">×</button><div id="dialog-content"></div></dialog></body></html>''',encoding='utf-8')
def cards(pre):return ''.join(f'<a class="appendix-card {cat}" href="{pre}apendices/{cat}/index.html"><span class="dot"></span><h3>{name}</h3><p>{desc}</p><span aria-hidden="true">↗</span></a>' for cat,(name,desc) in C.items())
old='Génesis|Éxodo|Levítico|Números|Deuteronomio|Josué|Jueces|Rut|1 Samuel|2 Samuel|1 Reyes|2 Reyes|1 Crónicas|2 Crónicas|Esdras|Nehemías|Ester|Job|Salmos|Proverbios|Eclesiastés|Cantares|Isaías|Jeremías|Lamentaciones|Ezequiel|Daniel|Oseas|Joel|Amós|Abdías|Jonás|Miqueas|Nahúm|Habacuc|Sofonías|Hageo|Zacarías|Malaquías'.split('|')
new='Mateo|Marcos|Lucas|Juan|Hechos|Romanos|1 Corintios|2 Corintios|Gálatas|Efesios|Filipenses|Colosenses|1 Tesalonicenses|2 Tesalonicenses|1 Timoteo|2 Timoteo|Tito|Filemón|Hebreos|Santiago|1 Pedro|2 Pedro|1 Juan|2 Juan|3 Juan|Judas|Apocalipsis'.split('|')
def books(items):return ''.join('<a class="book available" href="genesis/index.html"><span>01</span><strong>Génesis</strong><small>Capítulos 1–3 disponibles ↗</small></a>' if b=='Génesis' else f'<div class="book pending"><strong>{b}</strong><small>Próximamente</small></div>' for b in items)
page('index.html','La Biblia ilustrada',f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">UN LIBRO. MUCHAS FORMAS DE DESCUBRIRLO.</p><h1>Las palabras.<br>Las imágenes.<br><em>El principio.</em></h1><p class="intro">Recorre la Biblia a través de sus relatos, sus imágenes y el mundo que habita en cada palabra.</p><a class="button" href="genesis/1/index.html">Comenzar la lectura <span>↗</span></a><a class="quiet" href="#libros">Explorar los libros ↓</a><p class="edition">PRIMERA ENTREGA &nbsp; / &nbsp; GÉNESIS 1–3</p></div><figure class="hero-art"><img src="assets/creacion.jpg" alt="Ilustración de la creación: luz, astros, animales y naturaleza"><figcaption>01 / La creación</figcaption></figure></section><section id="libros" class="section"><p class="eyebrow">LA BIBLIOTECA</p><h2>Un recorrido, libro a libro.</h2><p>Los capítulos se incorporan a medida que están preparados.</p><h3 class="testament">Antiguo Testamento <span>39 libros</span></h3><div class="books">{books(old)}</div><details class="new-testament"><summary>Nuevo Testamento <span>27 libros</span></summary><div class="books">{books(new)}</div></details></section><section class="section tinted"><p class="eyebrow">MÁS ALLÁ DEL VERSÍCULO</p><h2>Cada palabra abre un mundo.</h2><p>Consulta los nombres, los lugares y los elementos del relato en nuestros cinco apéndices.</p><div class="appendix-grid">{cards('')}</div></section>''')
page('genesis/index.html','Génesis','''<section class="book-hero"><div><p class="eyebrow">ANTIGUO TESTAMENTO / LIBRO 01</p><h1>Génesis</h1><p class="intro">Los comienzos: el mundo, la vida y los primeros pasos de la humanidad.</p><a class="button" href="1/index.html">Leer el primer capítulo ↗</a><p>3 de 50 capítulos disponibles</p></div><img src="../assets/eden.jpg" alt="El jardín de Edén"></section><section class="section"><h2>Índice de capítulos</h2><div class="chapter-grid">'''+''.join(f'<a href="{i}/index.html"><b>{i:02}</b><span>{["La creación","El huerto de Edén","Fuera del paraíso"][i-1]}</span>↗</a>' if i<=3 else f'<div class="pending"><b>{i:02}</b><span>Próximamente</span></div>' for i in range(1,51))+'''</div></section>''')
art={1:('creacion.jpg','La creación'),2:('eden.jpg','El huerto de Edén'),3:('tentacion.webp','La serpiente y el fruto')};titles={1:'La creación',2:'El huerto de Edén',3:'Fuera del paraíso'}
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
headings=['Relaciones familiares','Hechos bíblicos','Identificación','Etimología','Descripción','Simbolismo cultural','Simbolismo','Apariciones','Especie','Estado actual','Estado de conservación','Cultura','Controversia','Ubicación']
def entrybody(e,pre):
 raw=e['body'];pats='|'.join(map(re.escape,headings));pieces=re.split(r'(?<!\w)('+pats+r')[.:]\s*',raw)
 out='<p>'+H(pieces[0])+'</p>'
 for i in range(1,len(pieces),2):out+=f'<h2>{H(pieces[i])}</h2><p>{H(pieces[i+1])}</p>'
 # Referencias a pasajes disponibles, sin alterar el texto visible.
 def ref(m):
  c=int(m[1]);v=int(m[2]);return f'<a href="{pre}genesis/{c}/index.html#v{v}">{m[0]}</a>' if any(x['chapter']==c and x['verse']==v for x in V) else m[0]
 out=re.sub(r'\b(?:Gn|Gen|Génesis)\s+(\d+):(\d+)(?:-\d+)?',ref,out)
 def cite(m):
  s=html.unescape(m[1]);first=s.split(',')[0].strip().lower();year=re.search(r'\d{4}',s);candidates=[i for i,b in enumerate(B) if first in b.lower() and (not year or year[0] in b)]
  target=f'#ref-{candidates[0]+1}' if len(candidates)==1 else ''
  return f'<a href="{pre}bibliografia/index.html{target}">{m[0]}</a>'
 out=re.sub(r'\[([^\]]+)\]',cite,out)
 if raw.startswith('Ver '):
  target=raw[4:].rstrip('.');dest=next((x for x in E if x['category']==e['category'] and x['name']==target),None)
  if dest:out=f'<p>Ver <a href="{pre}apendices/{dest["id"]}/index.html">{H(target)}</a>.</p>'
 return out
page('apendices/index.html','Apéndices','<section class="section"><p class="eyebrow">GUÍAS DE LECTURA</p><h1>El mundo de la Biblia.</h1><p class="intro">Cinco caminos para explorar lo que aparece en el relato.</p><div class="appendix-grid">'+cards('../')+'</div></section>')
for cat,(name,desc) in C.items():
 entries=[e for e in E if e['category']==cat]
 listing=''.join(f'<a class="entry-row {cat}" data-search="{H(e["title"].lower())}" href="{e["id"].split("/")[1]}/index.html"><strong>{H(e["title"])}</strong><span>↗</span></a>' for e in entries)
 page(f'apendices/{cat}/index.html',name,f'<section class="section directory"><p class="crumb"><a href="../index.html">Apéndices</a> / {name}</p><p class="eyebrow">{len(entries)} ENTRADAS</p><h1 class="{cat}">{name}</h1><p class="intro">{desc}</p><label class="search-label" for="entry-search">Buscar en este apéndice</label><input id="entry-search" type="search" placeholder="Escribe un nombre o término…"><p id="result-count" role="status">{len(entries)} entradas</p><div class="entry-list">{listing}</div></section>')
for e in E:
 cat=e['category'];chron='<p class="source-note">Las fechas expresan años desde la Creación según la cronología del Génesis.</p>' if cat=='onomastico' and re.search(r'\(\d',e['title']) else ''
 mentions=[]
 for v in V:
  rendered=verse(v,'../../../')
  if f'data-entry="{e["id"]}"' in rendered:mentions.append(f'<a href="../../../genesis/{v["chapter"]}/index.html#v{v["verse"]}">Gn {v["chapter"]}:{v["verse"]}</a>')
 backlinks='<div class="backlinks"><h2>En la lectura disponible</h2>'+ ' · '.join(mentions)+'</div>' if mentions else ''
 page(f'apendices/{e["id"]}/index.html',e['title'],f'<article class="section entry"><p class="crumb"><a href="../../index.html">Apéndices</a> / <a href="../index.html">{C[cat][0]}</a></p><p class="eyebrow {cat}">{C[cat][0]}</p><h1>{H(e["title"])}</h1>{chron}<div class="entry-body">{entrybody(e,"../../../")}</div>{backlinks}</article>')
page('bibliografia/index.html','Bibliografía','<section class="section bibliography"><p class="eyebrow">LAS FUENTES</p><h1>Bibliografía</h1><p class="intro">Obras y recursos que acompañan los apéndices de BIBLILU.</p><ol>'+''.join(f'<li id="ref-{i+1}">{H(b)}</li>' for i,b in enumerate(B))+'</ol></section>')
page('sobre/index.html','Sobre BIBLILU','''<section class="section entry"><p class="eyebrow">EL PROYECTO</p><h1>Leer. Mirar. Descubrir.</h1><p class="intro">BIBLILU es una edición ilustrada de la Biblia que conecta cada relato con sus personajes, lugares y referencias.</p><h2>Una publicación en marcha</h2><p>Esta primera entrega contiene Génesis 1–3. Los demás capítulos y libros se incorporarán progresivamente.</p><h2>Texto e ilustraciones</h2><p>Texto base: Reina-Valera 1960, según los documentos aportados por el editor. Se conserva su redacción. Las ilustraciones fueron creadas con ChatGPT para el proyecto BIBLILU.</p><p>Reina-Valera 1960 ® © Sociedades Bíblicas en América Latina, 1960. Renovado © Sociedades Bíblicas Unidas, 1988.</p><h2>Cómo leer los colores</h2><p>Los enlaces coloreados abren los apéndices. Dios, Jehová y las palabras atribuidas a Dios aparecen en rojo, sin hipervínculos. Las criaturas celestiales se incluyen en Animales.</p><h2>La cronología de Génesis</h2><p>Las fechas de las fichas del Génesis se expresan en años desde la Creación según el propio relato; no son fechas antes de Cristo.</p></section>''')
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'assets/entries.json').write_text(json.dumps({e['id']:{'title':e['title'],'category':C[e['category']][0],'body':e['body']} for e in E},ensure_ascii=False))
(OUT/'.nojekyll').touch()
print('Generadas',len(list(OUT.rglob('*.html'))),'páginas estáticas.')
