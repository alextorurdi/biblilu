"""Genera el Atlas de Pueblos y sus vínculos sin modificar mapas ni escenas originales.

Se ejecuta después de scripts/build.py. Mantiene las fuentes de datos en
assets/atlas/pentateuco.geojson y data/tribus_nuevas.json.
"""
from pathlib import Path
from urllib.parse import quote
import json, html, re, shutil, unicodedata

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
AP=DOCS/'apendices'
ATLAS=json.loads((ROOT/'assets/atlas/pentateuco.geojson').read_text(encoding='utf-8'))
FEATURES=ATLAS['features']
BY_ID={f['properties']['id']:f for f in FEATURES}
OLD=[e for e in json.loads((ROOT/'data/entries.json').read_text(encoding='utf-8')) if e['category']=='tribus' and e['id']!='tribus/amorreo']
NEW=json.loads((ROOT/'data/tribus_nuevas.json').read_text(encoding='utf-8'))['new_entries']
ENTRIES=OLD+NEW
assert len(ENTRIES)==len(BY_ID)==27 and {e['id'] for e in ENTRIES}==set(BY_ID)

# Nombre español, seguida de la transliteración hebrea aprobada.
TITLES={
 'amalecitas':('Amalecitas','ʿămālēqîm'), 'amonitas':('Amonitas','ʿammônîm'),
 'amorreos':('Amorreos','ʾĕmōrî'), 'araceo':('Araceos','ʿarqî'),
 'arvadeo':('Arvadeos','ʾarwādî'), 'cadmoneos':('Cadmoneos','qadmōnî'),
 'cananeo':('Cananeos','kənaʿănîm'), 'ceneos':('Ceneos','qênîm'),
 'cenezeos':('Cenezeos','qənizzî'), 'egipcios':('Egipcios','miṣrîm'),
 'emitas':('Emitas','ʾêmîm'), 'ferezeo':('Ferezeos','pərizzî'),
 'filisteos':('Filisteos','pəlištîm'), 'gergeseo':('Gergeseos','girgāšî'),
 'hamateo':('Hamateos','ḥămātî'), 'heteo':('Heteos','ḥittîm'),
 'heveo':('Heveos','ḥiwwî'), 'horeos':('Horeos','ḥōrîm'),
 'jebuseo':('Jebuseos','yəbûsî'), 'moabitas':('Moabitas','môʾābîm'),
 'refaitas':('Refaítas','rəfāʾîm'), 'sineo':('Sineos','sînî'),
 'zemareo':('Zemareos','ṣəmārî'), 'zuzitas':('Zuzitas','zûzîm'),
 'sidonios':('Sidonios','ṣīdōnîm'), 'elamitas':('Elamitas','ʿêlām'),
 'caldeos':('Caldeos','kaśdîm')
}
assert len(TITLES)==len(ENTRIES)
def esc(s):return html.escape(str(s),quote=True)
def inline(text):
 text=esc(text.strip().replace('\n',' '))
 text=re.sub(r'\*([^*\n]+)\*',r'<em>\1</em>',text)
 return text
def render_markdown(text):
 parts=[]
 for para in re.split(r'\n\s*\n',text.strip()):
  if para.startswith('### '):
   heading,_,tail=para.partition('\n')
   parts.append('<h2>'+esc(heading[4:].strip())+'</h2>')
   if tail.strip():parts.append('<p>'+inline(tail)+'</p>')
  else:
   parts.append('<p>'+inline(para)+'</p>')
 return ''.join(parts)

def atlas_panel(entryid):
 feature=BY_ID[entryid]
 text='Ver territorio o núcleo de referencia' if feature['geometry'] else 'Consultar ubicación desconocida'
 return '<div class="map-links"><strong>En el Atlas de Pueblos</strong><a href="../../../apendices/atlas-pueblos/index.html#pueblo='+quote(entryid,safe='')+'">'+text+' ↗</a></div>'
def add_panel(s,entryid):
 start=s.index('<div class="entry-body tribus">')
 first=s.find('</p>',start)
 if first<0:raise RuntimeError('Ficha de Tribus sin primer párrafo: '+entryid)
 return s[:first+4]+atlas_panel(entryid)+s[first+4:]
def rename_title(s,old,name,hebrew):
 s=s.replace('<title>'+esc(old)+' · BIBLILU</title>','<title>'+esc(name+' ('+hebrew+')')+' · BIBLILU</title>',1)
 s=s.replace('<h1>'+esc(old)+'</h1>','<h1>'+esc(name)+'<span class="tribe-title-secondary">'+esc(hebrew)+'</span></h1>',1)
 assert '<span class="tribe-title-secondary">' in s,(name,old)
 return s
def css_in_head(s,depth):
 tag='<link rel="stylesheet" href="'+depth+'assets/atlas/atlas.css?v=2">'
 return s.replace('</head>',tag+'</head>',1)
# Fichas existentes: mantener su texto intacto, y añadir navegación y títulos
# normalizados. Sus reformulaciones editoriales pendientes se publican aparte.
template=(AP/'tribus/amonitas/index.html').read_text(encoding='utf-8')
for e in OLD:
 slug=e['id'].split('/')[1]
 name,trans=TITLES[slug]
 file=AP/'tribus'/slug/'index.html'
 s=file.read_text(encoding='utf-8')
 s=rename_title(s,e['title'],name,trans)
 s=add_panel(s,e['id'])
 s=css_in_head(s,'../../../')
 file.write_text(s,encoding='utf-8')

# Crear las tres fichas nuevas, partiendo de la misma plantilla de Tribus.
for e in NEW:
 slug=e['id'].split('/')[1]
 name,trans=TITLES[slug]
 s=re.sub(r'<title>.*?</title>',lambda _: '<title>'+esc(name+' ('+trans+')')+' · BIBLILU</title>',template,count=1)
 s=re.sub(r'<h1>.*?</h1>',lambda _: '<h1>'+esc(name)+'<span class="tribe-title-secondary">'+esc(trans)+'</span></h1>',s,count=1)
 s=re.sub(r'<div class="entry-body tribus">.*?</div>',lambda _: '<div class="entry-body tribus">'+render_markdown(e['body'])+'</div>',s,count=1,flags=re.S)
 s=re.sub(r'<div class="backlinks">.*?</div>', '', s, flags=re.S)
 s=add_panel(s,e['id'])
 s=css_in_head(s,'../../../')
 (AP/'tribus'/slug).mkdir(parents=True,exist_ok=True)
 (AP/'tribus'/slug/'index.html').write_text(s,encoding='utf-8')

# La ruta vieja «amorreo» conserva un redireccionamiento, para no romper enlaces.
(AP/'tribus/amorreo/index.html').write_text(
 '<!doctype html><html lang="es-ES"><head><meta charset="utf-8">'
 '<meta http-equiv="refresh" content="0; url=../amorreos/index.html">'
 '<link rel="canonical" href="../amorreos/index.html"><title>Amorreos · BIBLILU</title>'
 '</head><body><p>Ficha trasladada: <a href="../amorreos/index.html">Amorreos</a>.</p></body></html>',
 encoding='utf-8')

# Renovar el índice de Tribus: 27 entradas alfabéticas y marca de localización.
index=AP/'tribus/index.html'
s=index.read_text(encoding='utf-8')
s=s.replace('25 ENTRADAS','27 ENTRADAS').replace('25 entradas','27 entradas')
intro='<p class="intro">Pueblos de la Antigüedad</p>'
s=s.replace(intro,intro+'<a class="button genealogy-directory-link" href="../atlas-pueblos/index.html">Explorar el Atlas de Pueblos ↗</a>',1)
mapglyph='<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/></svg>'
rows=[]
for e in sorted(ENTRIES,key=lambda x:unicodedata.normalize('NFD',TITLES[x['id'].split('/')[1]][0]).casefold()):
 slug=e['id'].split('/')[1]
 name,trans=TITLES[slug]
 label=esc(name)+' <small class="tribe-index-original"><em>'+esc(trans)+'</em></small>'
 query=esc(' '.join([name,trans,e['name'],BY_ID[e['id']]['properties'].get('aliases','')]).lower())
 if BY_ID[e['id']]['geometry']:
  tail='<span class="entry-row-tail"><span class="map-index-mark" role="img" aria-label="Representado en el Atlas de Pueblos" title="Representado en el Atlas de Pueblos">'+mapglyph+'</span><span>↗</span></span>'
 else:tail='<span>↗</span>'
 rows.append('<a class="entry-row tribus" data-search="'+query+'" href="'+esc(slug)+'/index.html"><strong>'+label+'</strong>'+tail+'</a>')
s=re.sub(r'<div class="entry-list">.*?</div>',lambda _: '<div class="entry-list">'+''.join(rows)+'</div>',s,count=1,flags=re.S)
s=css_in_head(s,'../../')
index.write_text(s,encoding='utf-8')

# El índice general incorpora el icono de personas y acceso al Atlas.
index=AP/'index.html';s=index.read_text(encoding='utf-8')
old='<a class="appendix-card tribus" href="../apendices/tribus/index.html"><span class="dot"></span><h3>Tribus</h3><p>Pueblos de la Antigüedad</p><span aria-hidden="true">↗</span></a>'
people='<svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="9" cy="8" r="3"/><path d="M2.5 20v-2a6.5 6.5 0 0 1 13 0v2M17 5a3 3 0 0 1 0 6M18 14a5 5 0 0 1 3.5 5v1"/></svg>'
new='<div class="appendix-card tribus appendix-card-family"><a class="appendix-card-main" href="../apendices/tribus/index.html"><span class="dot"></span><h3>'+people+' Tribus</h3><p>Pueblos de la Antigüedad</p><span aria-hidden="true">↗</span></a><a class="appendix-tree-link" href="../apendices/atlas-pueblos/index.html">Atlas de Pueblos <span aria-hidden="true">↗</span></a></div>'
if old not in s:raise RuntimeError('No se encontró tarjeta Tribus en el índice general')
index.write_text(s.replace(old,new,1),encoding='utf-8')

# Entradas de ventanas emergentes (app.js) incluidas las tres fichas nuevas.
entriesfile=DOCS/'assets/entries.json'
entries=json.loads(entriesfile.read_text(encoding='utf-8'))
entries.pop('tribus/amorreo',None)
for e in ENTRIES:
 slug=e['id'].split('/')[1]
 name,trans=TITLES[slug]
 if e['id'] not in entries:
  entries[e['id']]={'title':name+' ('+trans+')','category':'Tribus','body':e['body'].split('\n\n',1)[0],'mentions':[]}
 else: entries[e['id']]['title']=name+' ('+trans+')'
entriesfile.write_text(json.dumps(entries,ensure_ascii=False),encoding='utf-8')

# Cartografía de escenas: se conserva y solo se añade acceso al nuevo atlas.
oldmaps=AP/'mapas/index.html';m=oldmaps.read_text(encoding='utf-8')
needle='<p><a href="../lugares/index.html">Consultar el Apéndice de Lugares →</a></p>'
if needle not in m:raise RuntimeError('No se encontró el enlace al apéndice de Lugares')
m=m.replace(needle,needle+'<p><a href="../atlas-pueblos/index.html">Explorar el Atlas de Pueblos →</a></p>',1)
oldmaps.write_text(m,encoding='utf-8')

# Crear la nueva página con la cabecera, navegación y pie de BIBLILU.
title='<title>Mapas · BIBLILU</title>'
m=m.replace(title,'<title>Atlas de Pueblos · BIBLILU</title>',1)
m=css_in_head(m,'../../')
body="""<section class="section atlas-page">
<p class="crumb"><a href="../index.html">Apéndices</a> / <a href="../tribus/index.html">Tribus</a> / Atlas de Pueblos</p>
<p class="eyebrow tribus">CARTOGRAFÍA · PENTATEUCO</p>
<h1>Atlas de Pueblos</h1>
<p class="intro">Encuentra los pueblos mencionados en el Pentateuco y explora sus regiones o núcleos de referencia. Los datos pertenecen a períodos diferentes, no representan una situación simultánea.</p>
<nav class="atlas-top-links"><a href="../tribus/index.html">Consultar las 27 fichas de Tribus ↗</a><a href="../mapas/index.html">Mapas de las escenas ↗</a></nav>
<div class="atlas-layout" id="atlas-pueblos">
<aside class="atlas-sidebar"><label for="atlas-search">Buscar un pueblo</label><input id="atlas-search" type="search" autocomplete="off" placeholder="Amorreos, sidonios, zamzumitas…" aria-controls="atlas-list"><p class="atlas-count" id="atlas-count">Cargando pueblos…</p><nav id="atlas-list" class="atlas-list" aria-label="Índice de pueblos"></nav></aside>
<div class="atlas-map-panel">
<div class="atlas-toolbar"><strong>Colección: Pueblos del Pentateuco</strong><div class="atlas-buttons"><button id="atlas-in" aria-label="Ampliar">+</button><button id="atlas-out" aria-label="Reducir">−</button><button id="atlas-reset">Mapa completo</button><button id="atlas-full">Pantalla completa</button></div></div>
<div class="atlas-canvas"><svg id="atlas-svg" role="img" aria-label="Mapa interactivo de pueblos de Oriente Próximo. Selecciona un territorio o utiliza el listado." viewBox="0 0 1280 920" tabindex="0"></svg></div>
<p class="atlas-status" id="atlas-status" role="status">Cargando catálogo geográfico…</p>
<section id="atlas-details" class="atlas-details" aria-live="polite"><h2>Explora los pueblos</h2><p>Selecciona una entrada en la lista o en el mapa.</p></section>
</div></div>
<div class="atlas-legend" aria-label="Leyenda"><span><i class="atlas-swatch"></i> Área aproximada</span><span><i class="atlas-swatch diffuse"></i> Zona difusa</span><span><i class="atlas-swatch point"></i> Núcleo de referencia</span><span><i class="atlas-swatch unknown"></i> Ubicación desconocida</span></div>
<p class="atlas-note">Los contornos son zonas interpretativas, nunca fronteras históricas. Los puntos señalan centros citados o propuestos, sin atribuirles todo el territorio de un pueblo. Se incluyen épocas distintas, desde tradiciones patriarcales hasta la Edad del Hierro. Los pueblos sin localización suficientemente fundamentada permanecen en el índice sin geometría inventada.</p>
<p class="atlas-note">Relieve topográfico: imagen mundial <em>shadedrelief</em> incluida en Basemap-data (LGPL-3.0 o posterior), recortada para este visor; <a href="https://github.com/matplotlib/basemap" target="_blank" rel="noopener noreferrer">fuente</a> y <a href="https://spdx.org/licenses/LGPL-3.0-or-later.html" target="_blank" rel="noopener noreferrer">licencia</a>. Geometrías de pueblos: reconstrucción editorial orientativa, revisable conforme avance la documentación. Los mapas originales de las escenas se conservan intactos.</p>
</section><script src="../../assets/atlas/visor.js?v=2" defer></script>"""
m=re.sub(r'<main id="contenido">.*?</main>',lambda _: '<main id="contenido">'+body+'</main>',m,count=1,flags=re.S)
target=AP/'atlas-pueblos/index.html'
target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(m,encoding='utf-8')

print('Atlas generado:',len(ENTRIES),'pueblos,',sum(bool(f['geometry']) for f in FEATURES),'con geometría.')
