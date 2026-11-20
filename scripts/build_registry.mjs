/** Genera y comprueba el registro maestro interno de BIBLILU.
 * Uso: node scripts/build_registry.mjs [--check]
 * No modifica fichas ni páginas publicadas; reconstituye el registro desde las fuentes.
 */
import {readFileSync,writeFileSync} from "node:fs";
import {fileURLToPath} from "node:url";
import {dirname,resolve} from "node:path";
const ROOT=resolve(dirname(fileURLToPath(import.meta.url)),"..");
const FILES=[
  "data/entries.json",
  "data/materiales_revision.json",
  "data/objetos_revision.json",
  "data/instrumentos_revision.json",
  "data/medidas_revision.json",
  "data/tribus_nuevas.json",
  "assets/genealogias/enlaces.json",
  "assets/mapas/catalogo.json",
  "assets/atlas/pentateuco.geojson",
  "data/genesis.json"
];
function buildRegistry(s) {
  const clone=x=>JSON.parse(JSON.stringify(x));
  const norm=x=>String(x||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase().trim().replace(/\s+/g," ");
  const base=clone(s["data/entries.json"]);
  const revPaths=["data/materiales_revision.json","data/objetos_revision.json","data/instrumentos_revision.json","data/medidas_revision.json"];
  const sourcesById=Object.fromEntries(base.map(e=>[e.id,["data/entries.json"]]));
  const byid=new Map();
  const errors=[];
  for(const e of base){
    if(byid.has(e.id))errors.push("Identificador duplicado: "+e.id);
    byid.set(e.id,e);
  }
  for(const path of revPaths){
    const rev=s[path];
    for(const e of rev.new_entries||[]){
      if(byid.has(e.id)){errors.push("Alta duplicada: "+e.id);continue}
      const obj=clone(e);base.push(obj);byid.set(obj.id,obj);sourcesById[obj.id]=[path];
    }
    for(const [id,title] of Object.entries(rev.titles||{})){
      if(!byid.has(id)){errors.push("Título de revisión sin ficha: "+id);continue}
      byid.get(id).title=title;
      sourcesById[id].push(path);
    }
    for(const [id,delta] of Object.entries(rev.revised||{})){
      if(!byid.has(id)){errors.push("Revisión sin ficha: "+id);continue}
      Object.assign(byid.get(id),delta);
      if(!sourcesById[id].includes(path))sourcesById[id].push(path);
    }
  }
  for(const e of s["data/tribus_nuevas.json"].new_entries||[]){
    if(byid.has(e.id)){errors.push("Tribu duplicada: "+e.id);continue}
    const obj=clone(e);base.push(obj);byid.set(obj.id,obj);sourcesById[obj.id]=["data/tribus_nuevas.json"];
  }
  // La antigua ficha amorreo es una ruta histórica, no una entidad adicional.
  const legacyAlias={"tribus/amorreo":"tribus/amorreos"};
  const gene=s["assets/genealogias/enlaces.json"];
  const maps=s["assets/mapas/catalogo.json"];
  const atlas=s["assets/atlas/pentateuco.geojson"].features;
  const atlasById=new Map(atlas.map(f=>[f.properties.id,f]));
  const lookup=new Map();
  for(const e of base){
    const key=e.category+"|"+norm(e.name);
    if(!lookup.has(key))lookup.set(key,e.id);
  }
  const remissions={...legacyAlias};
  for(const e of base){
    const clean=String(e.body||"").trim();
    const match=/^Ver\s+(?:\[\[([^\]|]+)\|[^\]]+\]\]|(.+?))\.?$/i.exec(clean);
    if(!match)continue;
    let target=match[1]||null;
    if(!target){
      let name=match[2].replace(/\.$/,"").trim();
      target=lookup.get(e.category+"|"+norm(name));
    }
    if(target&&byid.has(target)&&target!==e.id)remissions[e.id]=target;
    else errors.push("Remisión sin resolver: "+e.id+" => "+clean);
  }
  // Evita ciclos, sin fusionar identidades históricamente discutidas.
  function canonical(id){
    const seen=new Set();
    while(remissions[id]){
      if(seen.has(id)){errors.push("Remisión circular: "+id);break}
      seen.add(id);id=remissions[id];
    }
    return id;
  }
  const aliasesByCanonical={};
  for(const [id] of Object.entries(remissions)){
    const target=canonical(id);
    (aliasesByCanonical[target]??=[]).push(id);
  }
  const manualVariants={
    "onomastico/jacob":["Israel"],"onomastico/esau":["Edom"],
    "onomastico/jose":["Zafnat-panea"],"onomastico/benjamin":["Benoni"],
    "onomastico/kesed":["Kesed","Quesed"]
  };
  const related={};
  for(const path of revPaths){
    for(const [id,ids] of Object.entries(s[path].related||{})){
      (related[id]??=[]).push(...ids);
    }
  }
  const mapsById={};
  for(const m of maps){
    for(const label of m.labels||[]){
      for(const id of label.entries||[]){
        if(!byid.has(id))errors.push("Referencia de mapa sin ficha: "+m.id+" => "+id);
        (mapsById[id]??=[]).push({mapa:m.id,escena:m.scene,rotulo:label.label});
      }
    }
  }
  const ents=base.map(e=>{
    const person=e.category==="onomastico"?gene.entry_to_person[e.id.split("/")[1]]:null;
    const branches=person?(gene.person_to_sheets[person]||[]):[];
    const feature=e.category==="tribus"?atlasById.get(e.id):null;
    const relatedIds=[...new Set(related[e.id]||[])];
    for(const id of relatedIds)if(!byid.has(id))errors.push("Ficha relacionada ausente: "+e.id+" => "+id);
    return {
      id:e.id,
      categoria:e.category,
      nombre:e.name,
      titulo:e.title,
      ficha_principal:canonical(e.id),
      es_remision:canonical(e.id)!==e.id,
      remisiones_entrantes:(aliasesByCanonical[e.id]||[]).sort(),
      variantes_aprobadas:manualVariants[e.id]||[],
      ruta:"docs/apendices/"+e.id+"/index.html",
      fuentes:[...new Set(sourcesById[e.id]||[])].sort(),
      menciones_registradas:e.mentions||[],
      relaciones_fichas:relatedIds,
      genealogias:person?{persona_visor:person,laminas:branches}:null,
      mapas:mapsById[e.id]||[],
      atlas_pueblos:feature?{
        id:feature.properties.id,
        delimitacion:feature.properties.kind,
        representacion_geografica:!!feature.geometry,
        fuente:"assets/atlas/pentateuco.geojson"
      }:null
    };
  }).sort((a,b)=>a.id.localeCompare(b.id,"es"));
  const ids=new Set(ents.map(e=>e.id));
  for(const [slug,p] of Object.entries(gene.entry_to_person)){
    if(!ids.has("onomastico/"+slug))errors.push("Árbol sin ficha: "+slug+" => "+p);
  }
  for(const f of atlas)if(!ids.has(f.properties.id))errors.push("Pueblo del atlas sin ficha: "+f.properties.id);
  const totals={};
  for(const e of ents)totals[e.categoria]=(totals[e.categoria]||0)+1;
  const v=s["data/genesis.json"], chapterNos=[...new Set(v.map(x=>x.chapter))].sort((a,b)=>a-b);
  return {
    version_esquema:1,
    proposito:"Índice técnico interno generado de las fuentes editoriales; no sustituye ni reproduce el contenido de las fichas.",
    libro:"Génesis",
    cobertura_texto:{capitulos_disponibles:chapterNos,versiculos: v.length, capitulos_pendientes:Array.from({length:50},(_,i)=>i+1).filter(n=>!chapterNos.includes(n))},
    fuentes:files,
    totales:{rutas_registradas:ents.length,fichas_principales:ents.filter(e=>!e.es_remision).length,remisiones:ents.filter(e=>e.es_remision).length,por_categoria:totals,mapas:maps.length,arboles_svg:8,entradas_con_menciones:ents.filter(e=>e.menciones_registradas.length>0).length},
    diagnostico:{incidencias:[...new Set(errors)].sort(),identidades_no_fusionadas:"Se respetan las decisiones de editorial/criterios-identidades-genesis.md; no se infieren equivalencias por homonimia."},
    entidades:ents
  };
}
const source=Object.fromEntries(FILES.map(f=>[f,JSON.parse(readFileSync(resolve(ROOT,f),"utf8"))]));
const result=buildRegistry(source);
if(result.diagnostico.incidencias.length)throw new Error("Registro incoherente:\n"+result.diagnostico.incidencias.join("\n"));
const target=resolve(ROOT,"data/registro_maestro.json");
const content=JSON.stringify(result,null,2)+"\n";
if(process.argv.includes("--check")){
 if(readFileSync(target,"utf8")!==content)throw new Error("El registro maestro está desactualizado. Ejecuta node scripts/build_registry.mjs");
 console.log("OK registro maestro:",result.totales.rutas_registradas,"rutas,",result.totales.fichas_principales,"fichas principales.");
}else{
 writeFileSync(target,content,"utf8");
 console.log("Registro maestro generado:",result.totales.rutas_registradas,"rutas.");
}
