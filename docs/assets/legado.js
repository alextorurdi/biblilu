/* Legado · alternancia accesible de los tres paneles laterales según el pasaje leído. */
(()=>{
  if(!document.body.classList.contains('legado-scene'))return;
  const side=document.querySelector('[data-legado-side]');
  const first=document.getElementById('gn-16-7');
  const second=document.getElementById('gn-17-15');
  if(!side||!first||!second)return;
  const panels=[...side.querySelectorAll('[data-legado-panel]')];
  if(panels.length!==3)return;
  let last=-1,scheduled=false;
  function update(){
    scheduled=false;
    const line=Math.max(96,Math.min(window.innerHeight*.42,360));
    const stage=second.getBoundingClientRect().top<=line?2:first.getBoundingClientRect().top<=line?1:0;
    if(stage===last)return;
    last=stage;
    panels.forEach((panel,i)=>{
      const hide=i!==stage;
      panel.hidden=hide;
      panel.setAttribute('aria-hidden',String(hide));
    });
  }
  function schedule(){if(scheduled)return;scheduled=true;requestAnimationFrame(update)}
  document.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',schedule,{passive:true});
  window.addEventListener('load',schedule);
  update();
})();
