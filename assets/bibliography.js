(() => {
  'use strict';
  const root=document.querySelector('.bib-apa7');
  if(!root)return;
  const search=root.querySelector('#bibliography-search');
  const filter=root.querySelector('#bibliography-filter');
  const counter=root.querySelector('#bibliography-results');
  const empty=root.querySelector('#bibliography-empty');
  const items=[...root.querySelectorAll('.bib-item')];
  const normalize=s=>(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
  function apply(){
    const q=normalize(search.value),tag=filter.value;
    let shown=0;
    for(const item of items){
      const matchesText=!q||normalize(item.dataset.search).includes(q);
      const matchesTag=tag==='Todas las materias'||item.dataset.categories.split('|').includes(tag);
      const visible=matchesText&&matchesTag;
      item.hidden=!visible;
      if(visible)shown++;
    }
    counter.textContent=shown+' referencia'+(shown===1?'':'s')+' de '+items.length;
    empty.hidden=shown!==0;
  }
  search.addEventListener('input',apply);
  filter.addEventListener('change',apply);
  apply();
})();