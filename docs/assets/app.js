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
