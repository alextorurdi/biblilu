/** Inventario reproducible de la Fase 0 de Génesis (no cambia páginas públicas).
 * node scripts/audit_genesis_p0.mjs [--write|--check]
 */
import {readFileSync,writeFileSync,existsSync} from "node:fs";
import {resolve,dirname,join} from "node:path";
import {fileURLToPath} from "node:url";
const ROOT=resolve(dirname(fileURLToPath(import.meta.url)),"..");
const p=x=>resolve(ROOT,x);
const read=x=>readFileSync(p(x),"utf8");
const j=x=>JSON.parse(read(x));
const html=read("docs/genesis/index.html");
const scenePart=html.split("ÍNDICE TRADICIONAL")[0];
const sceneMatches=[...scenePart.matchAll(/<a href="([0-9]+(?:-[0-9]+)?)\/index\.html"><b>(\d+)<\/b><span>([^<]+)<\/span>/g)];
const sceneIds=sceneMatches.map(m=>m[1]);
const text=j("data/genesis.json"),maps=j("assets/mapas/catalogo.json");
const registry=j("data/registro_maestro.json"),bibliography=j("data/bibliography_apa7.json");
const errors=[];
const expected=new Set(text.map(v=>v.chapter+":"+v.verse));
if(expected.size!==text.length) errors.push("Versículos duplicados en data/genesis.json");
if(sceneIds.length!==new Set(sceneIds).size) errors.push("Escenas duplicadas en el índice");
const found=new Set(),footnotes=new Set(),sceneData=[];
for(const match of sceneMatches){
 const id=match[1],order=Number(match[2]),label=match[3];
 const pathname="docs/genesis/"+id+"/index.html";
 const source="editorial/approved-pages/genesis/"+id+"/index.html";
 if(!existsSync(p(pathname))){errors.push("Página de escena ausente: "+pathname);continue}
 const page=read(pathname);
 const verses=[...page.matchAll(/<p class="verse(?: poetry)?" id="gn-(\d+)-(\d+)"/g)].map(m=>m[1]+":"+m[2]);
 const markers=[...page.matchAll(/id="fnref-(\d+)"/g)].map(m=>Number(m[1]));
 const notes=[...page.matchAll(/<li id="fn-(\d+)"/g)].map(m=>Number(m[1]));
 for(const verse of verses){
   if(!expected.has(verse))errors.push("Versículo ajeno a data/genesis.json: "+id+" "+verse);
   if(found.has(verse))errors.push("Versículo repetido en las escenas: "+verse);
   found.add(verse);
 }
 if(JSON.stringify(markers)!==JSON.stringify(notes))errors.push("Marcadores y notas discrepantes: escena "+id);
 for(const n of notes){if(footnotes.has(n))errors.push("Nota duplicada: "+n);footnotes.add(n)}
 const assets=[...new Set([...page.matchAll(/src="\.\.\/\.\.\/assets\/([^"]+\.(?:svg|webp|png|jpg|jpeg))(?:\?[^"]*)?"/gi)]
    .map(m=>m[1]).filter(x=>x!=="favicon.svg"))];
 for(const a of assets)if(!existsSync(p("docs/assets/"+a)))errors.push("Recurso no publicado en escena "+id+": "+a);
 const treeAssets=assets.filter(x=>/^genealogias\/\d+\.svg$/.test(x));
 const mapsForScene=maps.filter(m=>String(m.scene)===id);
 for(const m of mapsForScene)if(!existsSync(p("docs/assets/"+m.asset)))errors.push("Mapa del catálogo ausente: "+m.id);
 const mapAssets=assets.filter(x=>mapsForScene.some(m=>m.asset===x));
 const illustrations=assets.filter(x=>!treeAssets.includes(x)&&!mapAssets.includes(x));
 for(const e of [...page.matchAll(/data-entry="([^"]+)"/g)]){
   const id=e[1];
   if(!existsSync(p("docs/apendices/"+id+"/index.html")))errors.push("Ficha enlazada ausente: "+id+" desde "+pathname);
 }
 sceneData.push({
   numero:order,escena:label,ruta:pathname,
   inicio:verses[0]||null,final:verses.at(-1)||null,versiculos:verses.length,
   notas:notes.length,primera_nota:notes[0]||null,ultima_nota:notes.at(-1)||null,
   ilustraciones:illustrations,arboles:treeAssets,mapas:mapsForScene.map(m=>m.id),
   fuente_editorial:source,
   fuente_igual_a_salida:existsSync(p(source))?read(source)===page:null
 });
 if(!existsSync(p(source)))errors.push("Falta fuente editorial protegida: "+source);
}
for(const verse of expected)if(!found.has(verse))errors.push("Versículo no encontrado en escenas: "+verse);
for(let n=1;n<=footnotes.size;n++)if(!footnotes.has(n))errors.push("Laguna en numeración de notas: "+n);
const chapters=[...new Set(text.map(v=>v.chapter))].sort((a,b)=>a-b);
const result={
 version_esquema:1,libro:"Génesis",
 texto:{capitulos:chapters,versiculos:text.length,
        capitulos_pendientes:Array.from({length:50},(_,i)=>i+1).filter(n=>!chapters.includes(n))},
 resumen:{escenas:sceneData.length,notas:footnotes.size,
          mapas_catalogados:maps.length,arboles_svg:[...new Set(sceneData.flatMap(s=>s.arboles))].length,
          registros_maestros:registry.totales.rutas_registradas,
          fichas_principales:registry.totales.fichas_principales,
          referencias_bibliograficas:bibliography.entries.length},
 escenas:sceneData,incidencias:errors
};
const dest="editorial/inventario-genesis.json";
const output=JSON.stringify(result,null,2)+"\n";
if(process.argv.includes("--check")){
 if(read(dest)!==output)throw new Error("Inventario desactualizado: node scripts/audit_genesis_p0.mjs --write");
}else if(process.argv.includes("--write"))writeFileSync(p(dest),output,"utf8");
if(errors.length){console.error(errors.join("\n"));process.exitCode=1}
console.log("Génesis:",sceneData.length,"escenas,",found.size,"versículos,",footnotes.size,"notas,",maps.length,"mapas. Errores:",errors.length);
