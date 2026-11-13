/* Perdición: 2.º y 4.º corte cambian la imagen del lateral en escritorio. */
(()=>{
 if(!document.body.classList.contains('perdicion-scene'))return;
 const side=document.querySelector('[data-perdicion-side]');
 const second=document.getElementById('gn-19-1');
 const fourth=document.getElementById('gn-19-30');
 if(!side||!second||!fourth)return;
 const panels=[...side.querySelectorAll('[data-perdicion-panel]')];
 if(panels.length!==3)return;
 let last=-1,scheduled=false;
 const update=()=>{
  scheduled=false;
  const line=Math.max(96,Math.min(window.innerHeight*.42,360));
  const stage=fourth.getBoundingClientRect().top<=line?2:second.getBoundingClientRect().top<=line?1:0;
  if(stage===last)return;
  last=stage;
  panels.forEach((panel,i)=>{
   const hide=i!==stage;
   panel.hidden=hide;
   panel.setAttribute('aria-hidden',String(hide));
  });
 };
 const schedule=()=>{if(scheduled)return;scheduled=true;requestAnimationFrame(update)};
 document.addEventListener('scroll',schedule,{passive:true});
 window.addEventListener('resize',schedule,{passive:true});
 window.addEventListener('load',schedule);
 update();
})();
