(async()=>{
 const host=document.querySelector('#map-viewer');if(!host)return;
 const base=document.body.dataset.base||'../../';
 const select=host.querySelector('select'),search=host.querySelector('input'),results=host.querySelector('#map-results'),status=host.querySelector('#map-status'),canvas=host.querySelector('#map-canvas'),caption=host.querySelector('#map-caption');
 const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 let maps,active,svg,original,view,request=0;
 const setView=()=>svg?.setAttribute('viewBox',view.join(' '));
 const zoom=f=>{if(!svg)return;const w=Math.min(original[2]*2,Math.max(original[2]/8,view[2]*f)),h=w*original[3]/original[2];view=[view[0]+(view[2]-w)/2,view[1]+(view[3]-h)/2,w,h];setView()};
 function renderResults(){
  const q=norm(search.value.trim());results.replaceChildren();if(!q){results.hidden=true;return}results.hidden=false;
  let count=0;
  for(const m of maps){
   const labels=m.labels.filter(l=>norm(l.label+' '+l.entries.join(' ').replaceAll('-',' ')).includes(q));
   if(!labels.length&&norm(m.title).includes(q)){const a=document.createElement('a');a.href='#mapa='+m.id;a.textContent='Mapa: '+m.title;results.append(a);count++}
   for(const l of labels){
   const a=document.createElement('a');a.href='#mapa='+m.id+'&rotulo='+l.index;a.textContent=l.label+' · '+m.title;results.append(a);count++;
  }
  }
  if(!count)results.textContent='No hay coincidencias en los mapas disponibles.';
 }
 async function open(){
  const token=++request,p=new URLSearchParams(location.hash.slice(1)),m=maps.find(m=>m.id===p.get('mapa'))||maps[0];active=m;select.value=m.id;status.textContent='Cargando mapa…';
  try{
   const response=await fetch(base+'assets/'+m.asset);if(!response.ok)throw Error();const xml=await response.text();if(token!==request)return;
   const parsed=new DOMParser().parseFromString(xml,'image/svg+xml');if(parsed.querySelector('parsererror'))throw Error();
   const shadow=canvas.shadowRoot||canvas.attachShadow({mode:'open'});shadow.replaceChildren();svg=document.importNode(parsed.documentElement,true);svg.style.cssText='width:100%;height:100%;display:block;touch-action:none;user-select:none';shadow.append(svg);
   original=svg.getAttribute('viewBox').split(/\s+/).map(Number);view=[...original];
   let label=m.labels.find(l=>l.entries.includes(p.get('lugar')))||m.labels.find(l=>String(l.index)===p.get('rotulo'));
   caption.replaceChildren();const scene=document.createElement('a');scene.href=base+'genesis/'+m.scene+'/index.html';scene.textContent='Volver a la escena →';caption.append(scene);
   if(label){
    const t=svg.querySelectorAll('text')[label.index],b=t.getBBox(),matrix=t.getCTM();
    const points=[[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(([x,y])=>new DOMPoint(x,y).matrixTransform(matrix));
    // Convert screen viewport coordinates back to the root SVG coordinate system.
    const inverse=svg.getCTM().inverse(),coords=points.map(p=>p.matrixTransform(inverse));
    const x=Math.min(...coords.map(p=>p.x))-10,y=Math.min(...coords.map(p=>p.y))-10,w=Math.max(...coords.map(p=>p.x))-x+10,h=Math.max(...coords.map(p=>p.y))-y+10;
    const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');for(const [k,v] of Object.entries({x,y,width:w,height:h,fill:'#ffc857','fill-opacity':'.22',stroke:'#9a4800','stroke-width':3,rx:5,'pointer-events':'none'}))rect.setAttribute(k,v);svg.append(rect);
    status.textContent='Rótulo resaltado: '+label.label+'. Se mantienen las incertidumbres del mapa.';
    for(const eid of label.entries){const a=document.createElement('a');a.href=base+'apendices/'+eid+'/index.html';a.textContent='Ficha: '+eid.split('/')[1].replaceAll('-',' ')+' ↗';caption.append(a)}
   }else status.textContent=m.title+'. Arrastra para desplazar el mapa y utiliza los controles para ampliar.';
   let drag,moved=false;
   svg.addEventListener('pointerdown',e=>{if(e.button!==0)return;svg.setPointerCapture(e.pointerId);moved=false;drag={x:e.clientX,y:e.clientY,view:[...view]}});
   svg.addEventListener('pointermove',e=>{if(!drag)return;moved ||= Math.abs(e.clientX-drag.x)+Math.abs(e.clientY-drag.y)>5;const r=svg.getBoundingClientRect(),scale=Math.max(view[2]/r.width,view[3]/r.height);view=[drag.view[0]-(e.clientX-drag.x)*scale,drag.view[1]-(e.clientY-drag.y)*scale,view[2],view[3]];setView()});
   svg.addEventListener('pointerup',()=>drag=null);svg.addEventListener('pointercancel',()=>drag=null);
   svg.addEventListener('click',e=>{if(moved)return;const text=e.target.closest('text');if(!text||!m.labels.some(l=>l.index===[...svg.querySelectorAll('text')].indexOf(text)))return;location.hash='mapa='+m.id+'&rotulo='+[...svg.querySelectorAll('text')].indexOf(text)});
  }catch{status.textContent='No se ha podido cargar el mapa. Puedes abrir el archivo original.';caption.replaceChildren();const a=document.createElement('a');a.href=base+'assets/'+m.asset;a.textContent='Abrir mapa original ↗';caption.append(a)}
 }
 select.addEventListener('change',()=>location.hash='mapa='+select.value);
 search.addEventListener('input',renderResults);
 host.querySelector('#map-in').onclick=()=>zoom(.75);host.querySelector('#map-out').onclick=()=>zoom(1/.75);host.querySelector('#map-reset').onclick=()=>{if(!svg)return;view=[...original];setView()};
 host.querySelector('#map-full').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await host.requestFullscreen()}catch{status.textContent='La pantalla completa no está disponible en este navegador.'}};
 canvas.addEventListener('keydown',e=>{if(!svg)return;const d={ArrowLeft:[-.1,0],ArrowRight:[.1,0],ArrowUp:[0,-.1],ArrowDown:[0,.1]}[e.key];if(d){e.preventDefault();view[0]+=view[2]*d[0];view[1]+=view[3]*d[1];setView()}else if(e.key==='+'||e.key==='=')zoom(.75);else if(e.key==='-')zoom(1/.75)});
 try{const r=await fetch(base+'assets/mapas/catalogo.json');if(!r.ok)throw Error();maps=await r.json();for(const m of maps){const o=document.createElement('option');o.value=m.id;o.textContent=m.title;select.append(o)}await open();addEventListener('hashchange',open)}catch{status.textContent='No se ha podido cargar el catálogo. Recarga la página para intentarlo de nuevo.'}
})();
