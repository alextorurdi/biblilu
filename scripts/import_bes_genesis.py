#!/usr/bin/env python3
"""Importación reproducible de BES 2026 (dominio público) desde eBible.

Uso: python scripts/import_bes_genesis.py --download
     python scripts/import_bes_genesis.py --zip /ruta/spabes_usfm.zip

Escribe SOLO data/genesis_25_50_bes.json y editorial/procedencia-bes-genesis-25-50.json.
Nunca modifica data/genesis.json, escenas RVR1960, docs ni approved-pages.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/genesis_25_50_bes.json"
PROVENANCE = ROOT / "editorial/procedencia-bes-genesis-25-50.json"
URL = "https://ebible.org/Scriptures/spabes_usfm.zip"
LENGTHS = {
 25:34,26:35,27:46,28:22,29:35,30:43,31:55,32:32,33:20,
 34:31,35:29,36:43,37:36,38:30,39:23,40:23,41:57,42:38,
 43:34,44:34,45:28,46:34,47:31,48:22,49:33,50:26
}
NOTES = re.compile(r"\\(?:f|fe|x)\b.*?\\(?:f|fe|x)\*", re.S)
MARKERS = re.compile(r"\\\+?[a-zA-Z][a-zA-Z0-9-]*\*?")
VERSE = re.compile(r"^\\v\s+([0-9]+(?:-[0-9]+)?)\s*(.*)$")
CHAPTER = re.compile(r"^\\c\s+(\d+)\b")
OPEN = re.compile(r"^\\([a-zA-Z0-9-]+)\s*(.*)$")
SKIP = {"id","ide","rem","sts","h","h1","toc1","toc2","toc3",
 "mt","mt1","mt2","imt","imt1","s","s1","s2","s3",
 "ms","ms1","d","r","sr","cl","cp","qa","sp","usfm","b","ib"}

def fail(reason):
 raise ValueError("BES 2026: "+reason)

def clean(text):
 text=NOTES.sub("",text)
 text=re.sub(r"\\(?:fig|jmp)\b.*?\\(?:fig|jmp)\*","",text,flags=re.S)
 text=MARKERS.sub("",text).replace("~","\N{NO-BREAK SPACE}")
 return " ".join(text.split()).strip()

def parse(usfm):
 found={}
 chapter=None; number=None; parts=[]
 def flush():
  if number is None:return
  if chapter is None:fail("versículo sin capítulo")
  key=(chapter,number)
  if key in found:fail("versículo repetido "+str(key))
  value=clean(" ".join(parts))
  if not value:fail("versículo vacío "+str(key))
  found[key]=value
 for raw in usfm.replace("\ufeff","").splitlines():
  line=raw.strip()
  if not line:continue
  m=CHAPTER.match(line)
  if m:
   flush();chapter=int(m[1]);number=None;parts=[];continue
  m=VERSE.match(line)
  if m:
   flush()
   if "-" in m[1]:fail("rango de versículos combinado: "+m[1])
   number=int(m[1]);parts=[m[2]];continue
  m=OPEN.match(line)
  if m:
   marker,body=m[1].lower(),m[2]
   if marker in SKIP:continue
   if marker.startswith(("p","q","m","li","nb")):
    if number is not None and body:parts.append(body)
    continue
  if number is not None:parts.append(line)
 flush()
 return found

def find_book(blob):
 with ZipFile(BytesIO(blob)) as z:
  matches=[]
  for name in z.namelist():
   if not name.lower().endswith((".usfm",".sfm",".txt")):continue
   text=z.read(name).decode("utf-8-sig")
   if re.search(r"(?m)^\\id\s+GEN\b",text):matches.append((name,text))
  if len(matches)!=1:fail("se necesita un único libro GEN; encontrados "+str([n for n,_ in matches]))
  return matches[0]

def convert(blob,origin):
 name,usfm=find_book(blob)
 found=parse(usfm)
 expected=[(c,v) for c,m in LENGTHS.items() for v in range(1,m+1)]
 if len(expected)!=874:fail("las longitudes canónicas son incorrectas")
 actual=sorted(k for k in found if k[0] in LENGTHS)
 if actual!=expected:
  fail("faltan "+str(sorted(set(expected)-set(actual))[:15])+
       "; inesperados "+str(sorted(set(actual)-set(expected))[:15]))
 if found[(25,1)]!="Abraham tomó otra mujer llamada Cetura.":
  fail("Gn 25:1 no coincide con BES 2026 (comparación contra eBible.org)")
 verses=[{"chapter":c,"verse":v,"source_label":f"{c}-{v}",
          "text":found[(c,v)],"revisado":False} for c,v in expected]
 SOURCE.parent.mkdir(parents=True,exist_ok=True)
 PROVENANCE.parent.mkdir(parents=True,exist_ok=True)
 SOURCE.write_text(json.dumps(verses,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 provenance={"edicion":"La Biblia en Español Sencillo 2026 (BES)",
 "identificador":"spabes","fuente_oficial":URL,
 "licencia_declarada":"Public Domain",
 "licencia_url":"https://ebible.org/spabes/copyright.htm",
 "origen_importacion":origin,"archivo_usfm_genesis":name,
 "sha256_zip":sha256(blob).hexdigest(),
 "fecha_importacion_utc":datetime.now(timezone.utc).isoformat(),
 "capitulos":26,"versiculos":874,"datos":"data/genesis_25_50_bes.json",
 "estado":"importado, pendiente de revisión textual y marcado",
 "fuentes_protegidas":["data/genesis.json","editorial/approved-pages/genesis"]}
 PROVENANCE.write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("Importados 874 versículos de BES 2026 desde",name)
 return verses

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 g=parser.add_mutually_exclusive_group(required=True)
 g.add_argument("--download",action="store_true",help="descargar USFM oficial de eBible")
 g.add_argument("--zip",type=Path,help="paquete USFM oficial ya descargado")
 args=parser.parse_args()
 if args.zip:
  blob=args.zip.read_bytes();origin=str(args.zip)
 else:
  request=Request(URL,headers={"User-Agent":"BIBLILU/1.0 editorial source importer"})
  with urlopen(request,timeout=45) as response:blob=response.read()
  origin=URL
 convert(blob,origin)

if __name__=="__main__":main()
