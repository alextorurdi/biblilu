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
 if(!chapter3||!expulsion)return;
 const figures=Array.from(gallery.querySelectorAll('figure[data-illustration]'));
 let current=null,scheduled=false;
 function update(){
  scheduled=false;
  /* El cambio ocurre cuando empieza a leerse el nuevo capítulo. */
  const readingLine=Math.max(90,Math.min(window.innerHeight*0.42,350));
  let scene='eden';
  if(chapter3.getBoundingClientRect().top<=readingLine)scene='fall';
  if(expulsion.getBoundingClientRect().top<=readingLine)scene='sword';
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
