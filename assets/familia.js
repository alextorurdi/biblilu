/* Familia: el lateral cambia en los cortes primero, segundo, cuarto y último. */
(()=>{
 if(!document.body.classList.contains('familia-scene'))return;
 const side=document.querySelector('[data-familia-side]');
 if(!side)return;
 const panels=[...side.querySelectorAll('[data-familia-panel]')];
 const anchors=[1,2,4,6].map(n=>document.getElementById('familia-corte-'+n));
 if(panels.length!==5||anchors.some(a=>!a))return;
 let last=-1,scheduled=false;
 function update(){
   scheduled=false;
   const line=Math.max(104,Math.min(window.innerHeight*.42,360));
   let index=0;
   for(const anchor of anchors){if(anchor.getBoundingClientRect().top<=line)index++;}
   if(last===index)return;
   last=index;
   panels.forEach((p,i)=>{let hide=i!==index;p.hidden=hide;p.setAttribute('aria-hidden',String(hide));});
 }
 function schedule(){if(scheduled)return;scheduled=true;requestAnimationFrame(update);}
 document.addEventListener('scroll',schedule,{passive:true});
 window.addEventListener('resize',schedule,{passive:true});
 window.addEventListener('load',schedule);
 update();
})();
