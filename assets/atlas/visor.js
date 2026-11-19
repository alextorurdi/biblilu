(()=>{
'use strict';
const host=document.getElementById('atlas-pueblos');if(!host)return;
const base=document.body.dataset.base||'../../';
const list=host.querySelector('#atlas-list'),search=host.querySelector('#atlas-search'),status=host.querySelector('#atlas-status'),details=host.querySelector('#atlas-details'),svg=host.querySelector('#atlas-svg'),count=host.querySelector('#atlas-count');
const NS='http://www.w3.org/2000/svg';
const FULL=[0,0,1280,920];let box=FULL.slice(),features=[],selected='',drag=null,moved=false;
const LAND=[
[[24,21],[24,32.01],[28.91,30.87],[30.98,31.55],[31.69,31.43],[31.96,30.93],[32.19,31.26],[33.77,30.97],[34.56,31.55],[36,34.64],[36.15,35.82],[35.78,36.27],[36.16,36.65],[34.71,36.8],[34.03,36.22],[32.51,36.11],[31.7,36.64],[30.62,36.68],[29.7,36.14],[28.73,36.68],[27.64,36.66],[26.32,38.21],[26.8,38.98],[26.17,39.46],[27.28,40.42],[28.82,40.46],[29.24,41.22],[31.15,41.09],[33.51,42.02],[35.17,42.04],[38.35,40.95],[40.37,41.01],[41.55,41.54],[41.45,42.65],[39.1,44],[47.27,44],[47.59,43.66],[47.49,42.99],[49.62,40.57],[50.39,40.26],[49.22,39.05],[48.86,38.82],[49.2,37.58],[50.84,36.87],[52.26,36.7],[53.92,37.2],[53.88,38.95],[54.74,40.95],[53.72,42.12],[52.81,41.14],[52.5,42.79],[50.91,44],[56,44],[56,27.03],[54.72,26.48],[53.49,26.81],[51.52,27.87],[50.12,30.15],[49.58,29.99],[48.94,30.32],[48.57,29.93],[47.97,29.98],[48.81,27.69],[50.15,26.69],[50.11,25.94],[50.81,24.75],[51.01,26.01],[51.59,25.8],[51.39,24.63],[51.79,24.02],[54.01,24.12],[56,25.99],[56,21],[39.34,21],[39.07,22.58],[38.49,23.69],[37.48,24.29],[36.93,25.6],[35.13,28.06],[34.63,28.06],[34.96,29.36],[34.82,29.76],[33.92,27.65],[33.14,28.42],[32.42,29.85],[34.1,26.14],[35.69,23.93],[35.53,23.1],[36.87,22],[37.19,21],[24,21]],
[[32.98,34.57],[32.26,35.1],[34.58,35.67],[33.9,35.25],[34,34.98],[32.98,34.57]],
[[24,35.52],[25.74,35.18],[26.29,35.3],[26.16,35.0],[24.73,34.92],[24,35.2],[24,35.52]]
];
const project=c=>[(c[0]-24)*40,(44-c[1])*40];
const path=coords=>'M'+coords.map(c=>project(c).map(v=>v.toFixed(1)).join(',')).join('L')+'Z';
const line=coords=>'M'+coords.map(c=>project(c).map(v=>v.toFixed(1)).join(',')).join('L');
const elt=(tag,attrs,where)=>{const e=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs||{}))e.setAttribute(k,v);if(where)where.append(e);return e};
const norm=s=>(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const view=()=>{
 svg.setAttribute('viewBox',box.join(' '));
 // Keep labels and point symbols a readable size at any zoom level.
 const ratio=box[2]/FULL[2];
 svg.querySelectorAll('.atlas-point-ring').forEach(e=>e.setAttribute('r',(11*ratio).toFixed(2)));
 svg.querySelectorAll('.atlas-point').forEach(e=>e.setAttribute('r',(5*ratio).toFixed(2)));
 svg.querySelectorAll('.atlas-place-dot').forEach(e=>e.setAttribute('r',(2.6*ratio).toFixed(2)));
 svg.querySelectorAll('.atlas-place-name').forEach(e=>e.setAttribute('font-size',(11*ratio).toFixed(2)));
 svg.classList.toggle('atlas-show-details',box[2]<=530);
};
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function setZoom(f,cx,cy){const w=clamp(box[2]*f,95,FULL[2]*1.15),h=w*FULL[3]/FULL[2];box=[cx-w/2,cy-h/2,w,h];view()}
function reset(){box=FULL.slice();view()}
const allCoords=g=>{
 if(!g)return [];
 if(g.type==='Point')return [g.coordinates];
 if(g.type==='MultiPoint')return g.coordinates;
 if(g.type==='Polygon')return g.coordinates.flat();
 if(g.type==='MultiPolygon')return g.coordinates.flat(2);
 return [];
};
function focus(f){
 const c=allCoords(f.geometry);if(!c.length)return;
 const p=c.map(project),xmin=Math.min(...p.map(x=>x[0])),xmax=Math.max(...p.map(x=>x[0])),ymin=Math.min(...p.map(x=>x[1])),ymax=Math.max(...p.map(x=>x[1]));
 const w=clamp(Math.max(220,(xmax-xmin)*1.9),220,1100),h=w*FULL[3]/FULL[2];
 box=[(xmin+xmax)/2-w/2,(ymin+ymax)/2-h/2,w,h];view();
}
function caption(svgParent,at,text,size,cls){const t=elt('text',{x:project(at)[0],y:project(at)[1],class:cls||'atlas-label','font-size':size||16},svgParent);t.textContent=text;return t}
function background(){
 svg.replaceChildren();
 elt('rect',{x:0,y:0,width:1280,height:920,class:'atlas-sea'},svg);
 const land=elt('g',{class:'atlas-land'},svg);LAND.forEach(p=>elt('path',{d:path(p)},land));
 // Georeferenced public-site asset cropped to 24°–56° E / 21°–44° N.
 // The old schematic land polygon remains only as an offline/image-error fallback.
 const raster=elt('image',{
   href:base+'assets/atlas/relieve.webp',x:0,y:0,width:1280,height:920,
   preserveAspectRatio:'none',class:'atlas-relief','aria-hidden':'true'
 },svg);
 raster.addEventListener('error',()=>raster.remove());
 const grid=elt('g',{class:'atlas-grid'},svg);
 for(let lon=28;lon<=52;lon+=4){const x=project([lon,44])[0];elt('path',{d:'M'+x+' 0V920'},grid)}
 for(let lat=24;lat<=40;lat+=4){const y=project([24,lat])[1];elt('path',{d:'M0 '+y+'H1280'},grid)}

 const waters=elt('g',{class:'atlas-waterways'},svg);
 for(const a of [
 [[31.3,31.3],[31.25,30.4],[31.3,29.4],[31.5,27.5],[32.5,24.5]],
 [[35.58,33.2],[35.56,32.75],[35.55,32.3],[35.53,31.75],[35.55,31.15]],
 [[38.4,38.3],[38.75,37.2],[39.3,36.4],[40.2,35.8],[41.0,34.5],[42.3,33.6],[43.5,32.65],[44.4,31.6],[47.4,30.5]],
 [[40.3,39.5],[41.7,38.0],[42.1,36.6],[43.1,35.1],[44.0,33.6],[46.0,31.7],[47.8,30.5]]
 ])elt('path',{d:line(a)},waters);
 const lab=elt('g',{class:'atlas-geolabels','aria-hidden':'true'},svg);
 caption(lab,[28.0,33.8],'MAR MEDITERRÁNEO',18,'atlas-sea-label');
 caption(lab,[31.4,27],'EGIPTO',22,'atlas-label');
 caption(lab,[35.5,32.5],'CANAÁN',16,'atlas-label');
 caption(lab,[42.3,34.3],'MESOPOTAMIA',22,'atlas-label');
 caption(lab,[49.6,33.9],'ELAM',18,'atlas-label');
 caption(lab,[36.5,30.1],'TRANSJORDANIA',12,'atlas-label');
 caption(lab,[34.3,26.1],'MAR ROJO',14,'atlas-sea-label');
 caption(lab,[43.2,26.7],'PENÍNSULA ARÁBIGA',19,'atlas-label');
 caption(lab,[43.0,40.2],'ANATOLIA',16,'atlas-label');
 caption(lab,[38.8,32.1],'DESIERTO DE SIRIA',13,'atlas-label');
 // Detailed city labels become visible only at a close scale.
 const points=elt('g',{class:'atlas-places','aria-hidden':'true'},svg);
 const cities=[
  [[35.37,33.56],'Sidón'],[[35.19,33.27],'Tiro'],[[35.86,34.85],'Arvad'],
  [[36.75,35.13],'Hamat'],[[36.29,33.51],'Damasco'],
  [[35.24,31.78],'Jerusalén'],[[35.10,31.53],'Hebrón'],
  [[35.28,32.21],'Siquem'],[[35.18,31.85],'Gabaón'],
  [[34.46,31.50],'Gaza'],[[35.44,31.86],'Jericó'],
  [[44.42,32.54],'Babilonia'],[[46.10,30.96],'Ur'],
  [[48.27,32.19],'Susa'],[[43.15,36.35],'Nínive'],
  [[31.23,30.05],'Menfis / delta']
 ];
 for(const [at,name] of cities){
  const [x,y]=project(at);
  elt('circle',{cx:x,cy:y,r:2.6,class:'atlas-place-dot'},points);
  const t=elt('text',{x:x+7,y:y-6,'font-size':11,class:'atlas-place-name'},points);
  t.textContent=name;
 }
}
function drawFeature(f,layer){
 const p=f.properties,g=f.geometry;if(!g)return;
 const group=elt('g',{'data-pueblo':p.id,class:'atlas-feature atlas-'+p.kind,tabindex:0,role:'button','aria-label':p.name+', '+p.kind},layer);
 const title=elt('title',{},group);title.textContent=p.name+'. '+p.note;
 const addPoly=c=>elt('path',{d:path(c[0]),class:'atlas-territory'},group);
 const addPoint=c=>{const [x,y]=project(c);elt('circle',{cx:x,cy:y,r:13,class:'atlas-point-ring'},group);elt('circle',{cx:x,cy:y,r:5.4,class:'atlas-point'},group)};
 if(g.type==='Polygon')addPoly(g.coordinates);
 if(g.type==='MultiPolygon')g.coordinates.forEach(addPoly);
 if(g.type==='Point')addPoint(g.coordinates);
 if(g.type==='MultiPoint')g.coordinates.forEach(addPoint);
 group.addEventListener('click',e=>{e.stopPropagation();if(!moved)location.hash='pueblo='+encodeURIComponent(p.id)});
 group.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();location.hash='pueblo='+encodeURIComponent(p.id)}});
}
function renderMap(){background();const layer=elt('g',{id:'atlas-territories'},svg);features.forEach(f=>drawFeature(f,layer));const legend=elt('g',{'aria-hidden':'true'},svg);caption(legend,[24.65,21.5],'BIBLILU · ATLAS ORIENTATIVO',15,'atlas-watermark');view();styleSelection()}
function styleSelection(){
 svg.querySelectorAll('.atlas-feature').forEach(g=>g.classList.toggle('active',g.dataset.pueblo===selected));
 svg.classList.toggle('atlas-has-selection',!!selected);
 list.querySelectorAll('[data-pueblo]').forEach(e=>{e.classList.toggle('active',e.dataset.pueblo===selected);e.setAttribute('aria-current',e.dataset.pueblo===selected?'true':'false')});
}
function detail(f){
 const p=f.properties;details.replaceChildren();
 const badge=document.createElement('span');badge.className='atlas-kind';badge.textContent=({
 'aproximada':'Área aproximada','difusa':'Área difusa','nucleo':'Núcleo relacionado','nucleos':'Varios núcleos','desconocida':'Localización desconocida'
 })[p.kind]||p.kind;
 const h=document.createElement('h2');h.textContent=p.name;
 const d=document.createElement('p');d.textContent=p.note;
 const era=document.createElement('p');era.className='atlas-small';era.textContent='Contexto: '+p.era+'. Referencias: '+p.refs+'.';
 details.append(badge,h,d,era);
 if(p.kind==='desconocida'){const no=document.createElement('p');no.className='atlas-no-geometry';no.textContent='No se dibuja una ubicación porque la identificación es insuficiente.';details.append(no)}
 const link=document.createElement('a');link.className='button atlas-detail-link';link.href=base+'apendices/'+p.id+'/index.html';link.textContent='Ver ficha del pueblo ↗';
 // Las entradas nuevas pueden incorporarse después; no crear enlaces a fichas inexistentes.
 if(['sidonios','elamitas','caldeos'].includes(p.id.split('/')[1])){link.dataset.newTribe='true'}
 details.append(link);
}
function setSelected(id,shouldFocus){
 const f=features.find(x=>x.properties.id===id);selected=f?f.properties.id:'';
 styleSelection();
 if(f){detail(f);if(shouldFocus&&f.geometry)focus(f);if(!f.geometry){reset()}status.textContent=f.properties.name+(f.geometry?' · zona resaltada en el mapa':' · ubicación no determinada')}
 else{reset();details.innerHTML='<h2>Explora los pueblos</h2><p>Selecciona un nombre para resaltar su ubicación o conocer por qué no puede localizarse con seguridad.</p>';status.textContent=features.length+' pueblos registrados; los contornos son orientativos.'}
}
function updateList(){
 const q=norm(search.value.trim());list.replaceChildren();let c=0;
 features.forEach(f=>{
  const p=f.properties;
  if(!norm(p.name+' '+p.aliases+' '+p.era+' '+p.refs).includes(q))return;
  c++;
  const a=document.createElement('a');a.href='#pueblo='+encodeURIComponent(p.id);a.dataset.pueblo=p.id;a.className='atlas-entry';
  const name=document.createElement('strong');name.textContent=p.name;
  const tag=document.createElement('small');tag.textContent=p.kind==='desconocida'?'Sin ubicación':'Localización '+(p.kind==='nucleo'||p.kind==='nucleos'?'puntual':p.kind);
  a.append(name,tag);list.append(a);
 });
 count.textContent=c+' de '+features.length+' pueblos';styleSelection();
 if(!c){const no=document.createElement('p');no.textContent='Ninguna coincidencia. Prueba otra denominación.';list.append(no)}
}
function fromHash(){const p=new URLSearchParams(location.hash.slice(1));setSelected(p.get('pueblo')||'',true)}
host.querySelector('#atlas-reset').addEventListener('click',()=>{location.hash='';reset();setSelected('',false)});
host.querySelector('#atlas-in').addEventListener('click',()=>setZoom(.75,box[0]+box[2]/2,box[1]+box[3]/2));
host.querySelector('#atlas-out').addEventListener('click',()=>setZoom(1/.75,box[0]+box[2]/2,box[1]+box[3]/2));
host.querySelector('#atlas-full').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await host.querySelector('.atlas-map-panel').requestFullscreen()}catch{status.textContent='Pantalla completa no disponible en este navegador.'}});
search.addEventListener('input',updateList);
svg.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY,box:box.slice()};moved=false;svg.setPointerCapture(e.pointerId)});
svg.addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;moved ||= Math.abs(dx)+Math.abs(dy)>6;const r=svg.getBoundingClientRect();box=[drag.box[0]-dx*drag.box[2]/r.width,drag.box[1]-dy*drag.box[3]/r.height,drag.box[2],drag.box[3]];view()});
svg.addEventListener('pointerup',()=>drag=null);svg.addEventListener('pointercancel',()=>drag=null);
svg.addEventListener('wheel',e=>{e.preventDefault();const r=svg.getBoundingClientRect(),cx=box[0]+(e.clientX-r.left)/r.width*box[2],cy=box[1]+(e.clientY-r.top)/r.height*box[3];setZoom(e.deltaY>0?1.14:.88,cx,cy)},{passive:false});
svg.addEventListener('keydown',e=>{const d={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]}[e.key];if(d){e.preventDefault();box[0]+=d[0]*box[2]*.08;box[1]+=d[1]*box[3]*.08;view()}else if(e.key==='+'||e.key==='='){e.preventDefault();setZoom(.75,box[0]+box[2]/2,box[1]+box[3]/2)}else if(e.key==='-'){e.preventDefault();setZoom(1.33,box[0]+box[2]/2,box[1]+box[3]/2)}});
(async()=>{try{const r=await fetch(base+'assets/atlas/pentateuco.geojson');if(!r.ok)throw Error('HTTP '+r.status);const obj=await r.json();if(obj.type!=='FeatureCollection'||obj.features.length!==27)throw Error('Catálogo incompleto');features=obj.features.sort((a,b)=>a.properties.name.localeCompare(b.properties.name,'es'));renderMap();updateList();fromHash();window.addEventListener('hashchange',fromHash)}catch(e){status.textContent='No ha sido posible cargar el atlas. Recarga la página.';details.textContent='Error de carga del catálogo geográfico.';console.error('BIBLILU atlas',e)}})();
})();
