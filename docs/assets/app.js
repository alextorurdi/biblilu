(() => {
  const base=document.body.dataset.base||'';
  const dialog=document.querySelector('#entry-dialog');
  let entriesPromise;
  document.addEventListener('click',async event=>{
    const link=event.target.closest('a[data-entry]');
    if(!link||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||event.button!==0)return;
    event.preventDefault();
    try{
      entriesPromise ||= fetch(base+'assets/entries.json').then(r=>{if(!r.ok)throw Error('fichas');return r.json()});
      const entry=(await entriesPromise)[link.dataset.entry];if(!entry)throw Error('entrada');
      const content=document.querySelector('#dialog-content');content.replaceChildren();
      const cat=document.createElement('p');cat.className='eyebrow';cat.textContent=entry.category;
      const title=document.createElement('h2');title.id='dialog-title';title.textContent=entry.title;
      const text=document.createElement('p');text.className='dialog-text';text.textContent=entry.body;
      const full=document.createElement('a');full.href=link.href;full.className='button';full.textContent='Abrir la ficha completa ↗';
      content.append(cat,title,text,full);dialog.showModal();dialog.scrollTop=0;
      if(link.dataset.entry.startsWith('onomastico/')){
        const slug=link.dataset.entry.split('/')[1];
        fetch(base+'assets/genealogias/enlaces.json').then(r=>{if(!r.ok)throw Error('enlaces');return r.json()}).then(map=>{
          const person=map.entry_to_person&&map.entry_to_person[slug];
          if(!person||!title.isConnected||!dialog.open)return;
          const treeLink=document.createElement('a');
          treeLink.className='genealogy-person-link';
          treeLink.href=base+'apendices/genealogias/index.html#persona='+encodeURIComponent(person);
          treeLink.textContent='Ver en el árbol genealógico ↗';
          content.appendChild(treeLink);
        }).catch(()=>{});
      }
    }catch{location.href=link.href}
  });
  dialog?.querySelector('.close').addEventListener('click',()=>dialog.close());
  dialog?.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
  let size=21;try{size=Number(localStorage.getItem('biblilu-font'))||21}catch{}size=Math.min(29,Math.max(17,size));
  const font=delta=>{size=Math.min(29,Math.max(17,size+delta));document.documentElement.style.setProperty('--reader',size+'px');try{localStorage.setItem('biblilu-font',size)}catch{}};font(0);
  document.querySelector('#font-minus')?.addEventListener('click',()=>font(-2));document.querySelector('#font-plus')?.addEventListener('click',()=>font(2));
  for(const [id,cls,noun] of [['toggle-images','hide-images','imágenes'],['toggle-colors','hide-colors','colores']])document.getElementById(id)?.addEventListener('click',e=>{const off=document.body.classList.toggle(cls);e.currentTarget.setAttribute('aria-pressed',String(off));e.currentTarget.textContent=(off?'Mostrar ':'Ocultar ')+noun});
  document.querySelector('#chapter-select')?.addEventListener('change',e=>location.href=e.target.value);
  const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  document.querySelector('#entry-search')?.addEventListener('input',e=>{const query=normalize(e.target.value);let count=0;document.querySelectorAll('[data-search]').forEach(row=>{row.hidden=!normalize(row.dataset.search).includes(query);if(!row.hidden)count++});document.querySelector('#result-count').textContent=count?`${count} ${count===1?'entrada':'entradas'}`:'No hay entradas que coincidan con tu búsqueda.'});
})();

/* Notas accesibles y compatibilidad con enlaces de capítulos tradicionales */
(()=>{
 const dialog=document.querySelector('#note-dialog');let origin;
 document.addEventListener('click',e=>{
  const trigger=e.target.closest('a[data-note]');if(!trigger||!dialog||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
  const note=document.getElementById('fn-'+trigger.dataset.note);if(!note)return;e.preventDefault();origin=trigger;
  document.getElementById('note-dialog-title').textContent='Nota '+trigger.dataset.note;
  const area=document.getElementById('note-dialog-content');area.replaceChildren();area.append(note.querySelector('div').cloneNode(true));
  dialog.showModal();dialog.querySelector('.close').focus();
 });
 dialog?.querySelector('.close')?.addEventListener('click',()=>dialog.close());
 dialog?.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
 dialog?.addEventListener('close',()=>origin?.focus());
 document.addEventListener('click',e=>{
  const a=e.target.closest('a[href]');if(!a||a.dataset.note)return;
  const m=a.getAttribute('href')?.match(/^(.*?)genesis\/([123])\/index\.html#v(\d+)$/);
  if(!m)return;
  const c=Number(m[2]),v=Number(m[3]),unit=c===1||(c===2&&v<=3)?1:2;
  a.setAttribute('href',m[1]+'genesis/'+unit+'/index.html#gn-'+c+'-'+v);
 },true);
 if(location.pathname.match(/\/genesis\/2\/index\.html$/)&&/^#v[123]$/.test(location.hash))location.replace('../1/index.html#gn-2-'+location.hash.slice(2));
})();

/* Imagen lateral sincronizada con los capítulos bíblicos de la escena Paraíso */
(()=>{
 const gallery=document.querySelector('[data-scene-illustrations]');
 if(!gallery)return;
 const chapter3=document.getElementById('gn-3-1');
 const expulsion=document.getElementById('gn-3-24');
 const descent=document.getElementById('gn-4-17');
 const music=document.getElementById('gn-4-21');
 const cruelty=gallery.dataset.scene==='crueldad';
 if(cruelty?(!descent||!music):(!chapter3||!expulsion))return;
 const figures=Array.from(gallery.querySelectorAll('figure[data-illustration]'));
 let current=null,scheduled=false;
 function update(){
  scheduled=false;
  /* El cambio ocurre cuando empieza a leerse el nuevo capítulo. */
  const readingLine=Math.max(90,Math.min(window.innerHeight*0.42,350));
  let scene=cruelty?'envy':'eden';
  if(cruelty){
   if(descent.getBoundingClientRect().top<=readingLine)scene='lineage';
   if(music.getBoundingClientRect().top<=readingLine)scene='music';
  }else{
   if(chapter3.getBoundingClientRect().top<=readingLine)scene='fall';
   if(expulsion.getBoundingClientRect().top<=readingLine)scene='sword';
  }
  if(scene===current)return;
  current=scene;
  for(const figure of figures){
   const active=figure.dataset.illustration===scene;
   figure.classList.toggle('is-active',active);
   figure.setAttribute('aria-hidden',active?'false':'true');
  }
 }
 function schedule(){
  if(scheduled)return;
  scheduled=true;
  window.requestAnimationFrame(update);
 }
 window.addEventListener('scroll',schedule,{passive:true});
 window.addEventListener('resize',schedule);
 window.addEventListener('hashchange',schedule);
 window.addEventListener('pageshow',schedule);
 window.addEventListener('load',schedule);
 schedule();
})();


/* Navegación bidireccional entre el Onomástico y las láminas genealógicas. */
(()=>{
 const base=document.body.dataset.base||'';
 const frame=document.querySelector('.genealogy-frame');
 if(frame){
  const initial=frame.getAttribute('src').split('#')[0];
  const full=document.querySelector('.genealogy-actions .button');
  function route(){
   const params=new URLSearchParams(location.hash.slice(1));
   const person=params.get('persona'),section=params.get('lamina');
   let hash='';
   if(person&&/^[a-z0-9_-]+$/.test(person))hash='#persona='+encodeURIComponent(person);
   else if(section&&/^(general|0[1-9]|1[0-8])$/.test(section))hash='#lamina='+encodeURIComponent(section);
   const src=initial+hash;
   if(frame.getAttribute('src')!==src)frame.setAttribute('src',src);
   if(full)full.setAttribute('href',src);
  }
  route();
  window.addEventListener('hashchange',route);
 }
 const directory=document.querySelector('.directory .entry-list');
 const entry=document.querySelector('.entry .entry-body');
 if(!directory&&!entry)return;
 const match=location.pathname.match(/\/apendices\/onomastico\/([^/]+)\/(?:index\.html)?$/);
 fetch(base+'assets/genealogias/enlaces.json').then(r=>{
  if(!r.ok)throw Error('enlaces genealógicos');
  return r.json();
 }).then(map=>{
  const links=map.entry_to_person||{};
  if(directory){
   for(const row of directory.querySelectorAll('.entry-row')){
    const slug=(row.getAttribute('href')||'').split('/')[0];
    if(!links[slug]||row.querySelector('.genealogy-index-mark'))continue;
    const mark=document.createElement('span');
    mark.className='genealogy-index-mark';
    mark.title='Representado en los árboles genealógicos';
    mark.setAttribute('role','img');
    mark.setAttribute('aria-label','Incluido en los árboles genealógicos');
    mark.innerHTML='<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 6v5M5 17v-6h14v6"/><rect x="9" y="2" width="6" height="4" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/></svg>';
    const arrow=row.querySelector('span:last-child');
    if(arrow){
     const tail=document.createElement('span');
     tail.className='entry-row-tail';
     arrow.replaceWith(tail);
     tail.append(mark,arrow);
    }else row.append(mark);
   }
  }
  const id=match&&links[match[1]];
  if(entry&&id&&!entry.querySelector('.genealogy-person-link')){
   const link=document.createElement('a');
   link.className='genealogy-person-link';
   link.href=base+'apendices/genealogias/index.html#persona='+encodeURIComponent(id);
   const lead=document.createElement('span');
   lead.className='genealogy-person-lead';
   lead.textContent='Ver en el árbol genealógico ↗';
   const subtitle=document.createElement('small');
   subtitle.textContent='Abrir su lámina y destacar al personaje';
   link.append(lead,subtitle);
   const h=Array.from(entry.querySelectorAll('h2')).find(x=>x.textContent.trim()==='Relaciones familiares');
   const anchor=h&&h.nextElementSibling&&h.nextElementSibling.tagName==='P'?h.nextElementSibling:null;
   if(anchor)anchor.after(link);
   else entry.append(link);
  }
 }).catch(()=>{ /* Se conservan las fichas si no está disponible el índice de vínculos. */ });
})();


/* v0.3.1 · Panel lateral fijo: árbol hasta Gn 5:24; cronología desde Gn 5:25. */
(()=>{
 const aside=document.querySelector('[data-scene-four-side]');
 const threshold=document.getElementById('gn-5-25');
 if(!aside||!threshold)return;
 const panels=Array.from(aside.querySelectorAll('figure[data-panel]'));
 if(!panels.length)return;
 let current='',scheduled=false;
 const update=()=>{
  scheduled=false;
  const readingLine=Math.max(90,Math.min(window.innerHeight*.42,350));
  const next=threshold.getBoundingClientRect().top<=readingLine?'chronology':'tree';
  if(next===current)return;
  current=next;
  for(const panel of panels){
   const active=panel.dataset.panel===next;
   panel.classList.toggle('is-active',active);
   panel.hidden=!active;
   panel.setAttribute('aria-hidden',String(!active));
  }
 };
 const schedule=()=>{
  if(scheduled)return;
  scheduled=true;
  window.requestAnimationFrame(update);
 };
 /* Escucha el desplazamiento de la página, incluidos los saltos a versículos. */
 window.addEventListener('scroll',schedule,{passive:true});
 window.addEventListener('resize',schedule);
 window.addEventListener('hashchange',schedule);
 window.addEventListener('pageshow',schedule);
 window.addEventListener('load',schedule);
 update();
})();


/* Escena 5 · Diluvio: ilustraciones sincronizadas con la lectura. */
(()=>{
 const aside=document.querySelector('[data-scene-five-side]');
 if(!aside)return;
 const order=[['construccion','gn-6-1'],['medidas','gn-6-14'],['tormenta','gn-7-17'],['paloma','gn-8-6'],['arcoiris','gn-8-18']];
 const stops=order.map(([name,id])=>({name,node:document.getElementById(id)}));
 const panels=Array.from(aside.querySelectorAll('figure[data-flood-panel]'));
 if(stops.some(x=>!x.node)||!panels.length)return;
 let current='',scheduled=false;
 function update(){
  scheduled=false;
  const readingLine=Math.max(90,Math.min(window.innerHeight*.42,350));
  let active=stops[0].name;
  for(const stop of stops)if(stop.node.getBoundingClientRect().top<=readingLine)active=stop.name;
  if(active===current)return;
  current=active;
  for(const figure of panels){
   const visible=figure.dataset.floodPanel===active;
   figure.hidden=!visible;
   figure.classList.toggle('is-active',visible);
   figure.setAttribute('aria-hidden',String(!visible));
  }
 }
 const schedule=()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(update)};
 addEventListener('scroll',schedule,{passive:true});
 addEventListener('resize',schedule);
 addEventListener('pageshow',schedule);
 addEventListener('hashchange',schedule);
 addEventListener('load',schedule);
 update();
})();

/* Escena 6 · Dispersión: cambiar árbol lateral al entrar en Jafet, Cam o Sem. */
(()=>{
 const aside=document.querySelector('[data-scene-six-side]');
 if(!aside)return;
 const order=[['jafet','gn-10-1'],['cam','gn-10-6'],['sem','gn-10-21']];
 const stops=order.map(([key,id])=>({key,node:document.getElementById(id)}));
 const panels=[...aside.querySelectorAll('figure[data-dispersion-panel]')];
 if(stops.some(s=>!s.node)||panels.length!==3)return;
 let current='',waiting=false;
 const update=()=>{
  waiting=false;
  const readingLine=Math.max(90,Math.min(innerHeight*.42,350));
  let active=stops[0].key;
  for(const s of stops)if(s.node.getBoundingClientRect().top<=readingLine)active=s.key;
  if(active===current)return;
  current=active;
  for(const p of panels){
   const isActive=p.dataset.dispersionPanel===active;
   p.hidden=!isActive;
   p.classList.toggle('is-active',isActive);
   p.setAttribute('aria-hidden',String(!isActive));
  }
 };
 const schedule=()=>{if(!waiting){waiting=true;requestAnimationFrame(update)}};
 addEventListener('scroll',schedule,{passive:true});
 addEventListener('resize',schedule);
 addEventListener('pageshow',schedule);
 addEventListener('hashchange',schedule);
 addEventListener('load',schedule);
 update();

})();

/* Escena 8 · De Noé a Abram: árbol 06 hasta Gn 11:30, mapa desde Gn 11:31. */
(()=>{
  if (!document.body.classList.contains('scene-8')) return;
  const anchor=document.getElementById('gn-11-31');
  const genealogy=document.querySelector('.v05-genealogy');
  const map=document.querySelector('.v05-map');
  if (!anchor || !genealogy || !map) return;
  let scheduled=false;
  const update=()=>{
    scheduled=false;
    const readingLine=Math.max(90,Math.min(window.innerHeight*.42,350));
    const active=anchor.getBoundingClientRect().top<=readingLine;
    document.body.classList.toggle('v05-show-map',active);
    genealogy.setAttribute('aria-hidden',String(active));
    map.setAttribute('aria-hidden',String(!active));
  };
  const schedule=()=>{
    if(scheduled)return;
    scheduled=true;
    requestAnimationFrame(update);
  };
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',schedule);
  addEventListener('hashchange',schedule);
  addEventListener('pageshow',schedule);
  addEventListener('load',schedule);
  update();
})();



/* v0.6 · Mapas sincronizados en las escenas 9 (Viaje) y 10 (Guerra). */
(()=>{
  const isNine=document.body.classList.contains('scene-9');
  const isTen=document.body.classList.contains('scene-10');
  if(!isNine&&!isTen)return;
  const aside=document.querySelector('[data-v06-side]');
  if(!aside)return;
  const steps=isNine
    ? [['viaje-1','gn-12-1'],['viaje-2','gn-12-10'],['viaje-3','gn-13-5']]
    : [['guerra-1','gn-14-1'],['guerra-2','gn-14-5'],['guerra-3','gn-14-13'],[null,'gn-14-17']];
  const anchors=steps.map(([name,id])=>({name,node:document.getElementById(id)}));
  const panels=Array.from(aside.querySelectorAll('[data-v06-panel]'));
  if(anchors.some(a=>!a.node)||panels.length!==3)return;
  let selected,queued=false;
  const update=()=>{
    queued=false;
    const readingLine=Math.max(90,Math.min(window.innerHeight*.42,350));
    let active=steps[0][0];
    for(const step of anchors)if(step.node.getBoundingClientRect().top<=readingLine)active=step.name;
    if(active===selected)return;
    selected=active;
    for(const panel of panels){
      const on=panel.dataset.v06Panel===active;
      panel.hidden=!on;
      panel.setAttribute('aria-hidden',String(!on));
    }
  };
  const schedule=()=>{if(queued)return;queued=true;requestAnimationFrame(update);};
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',schedule);
  addEventListener('pageshow',schedule);
  addEventListener('hashchange',schedule);
  addEventListener('load',schedule);
  update();
})();


/* v0.7 · Sincronización de la ilustración y el mapa en «Promesas». */
(()=>{
  if(!document.body.classList.contains('scene-11'))return;
  const side=document.querySelector('[data-v07-side]');
  const transition=document.getElementById('gn-15-18');
  if(!side||!transition)return;
  const star=side.querySelector('[data-v07-panel="stars"]');
  const map=side.querySelector('[data-v07-panel="map"]');
  if(!star||!map)return;
  let last=null,scheduled=false;
  const update=()=>{
    scheduled=false;
    const line=Math.max(90,Math.min(window.innerHeight*.42,350));
    const showMap=transition.getBoundingClientRect().top<=line;
    if(last===showMap)return;
    last=showMap;
    star.hidden=showMap;
    map.hidden=!showMap;
    star.setAttribute('aria-hidden',String(showMap));
    map.setAttribute('aria-hidden',String(!showMap));
  };
  const schedule=()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(update);};
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',schedule);
  addEventListener('pageshow',schedule);
  addEventListener('hashchange',schedule);
  addEventListener('load',schedule);
  update();
})();
