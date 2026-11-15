/* Cumplimiento: alternancia de recursos en el lateral según los cortes de lectura. */
(()=>{
 if(!document.body.classList.contains('cumplimiento-scene'))return;
 const side=document.querySelector('[data-cumplimiento-side]');
 if(!side)return;
 const panels=[...side.querySelectorAll('[data-cumplimiento-panel]')];
 const anchorIDs=['gn-21-8','gn-21-22','gn-22-1','gn-22-20','gn-23-1'];
 const anchors=anchorIDs.map(id=>document.getElementById(id));
 if(panels.length!==6||anchors.some(x=>!x))return;
 let last=-1,scheduled=false;
 function update(){
   scheduled=false;
   const line=Math.max(100,Math.min(window.innerHeight*.42,360));
   let stage=0;
   for(const el of anchors){if(el.getBoundingClientRect().top<=line)stage++;}
   if(stage===last)return;
   last=stage;
   panels.forEach((panel,i)=>{
     const hide=i!==stage;
     panel.hidden=hide;
     panel.setAttribute('aria-hidden',String(hide));
   });
 }
 function schedule(){if(scheduled)return;scheduled=true;requestAnimationFrame(update);}
 document.addEventListener('scroll',schedule,{passive:true});
 window.addEventListener('resize',schedule,{passive:true});
 window.addEventListener('load',schedule);
 update();
})();