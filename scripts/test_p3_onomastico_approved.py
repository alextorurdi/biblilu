#!/usr/bin/env python3
"""Control de identidad onomástica aprobada por el editor, lote P3 Gn 25:1–18."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
entries=json.loads((ROOT/"data/entries.json").read_text(encoding="utf-8"))
registry=json.loads((ROOT/"data/registro_maestro.json").read_text(encoding="utf-8"))
bes=json.loads((ROOT/"data/genesis_25_50_bes.json").read_text(encoding="utf-8"))
old_text=json.loads((ROOT/"data/genesis.json").read_text(encoding="utf-8"))
by={x["id"]:x for x in entries}
master={x["id"]:x for x in registry["entidades"]}
assert len(by)==len(entries) and len(master)==len(registry["entidades"])
assert len(master)==451, (len(master),len(entries))

def entry(id,title):
    x=by[id];m=master[id]
    assert x["title"]==x["name"]==title,(id,x["title"],x["name"])
    assert m["nombre"]==m["titulo"]==title,(id,m["nombre"],m["titulo"])
    assert m["ficha_principal"]==id and m["es_remision"] is False
    assert m["ruta"]=="docs/apendices/"+id+"/index.html"
    return x

zim=entry("onomastico/zimram","Zimram")
assert "Zimrán" in zim["body"]
assert master["onomastico/zimram"]["variantes_aprobadas"]==["Zimrán"]
z_het=entry("onomastico/zohar-heteo","Zohar (heteo)")
z_son=entry("onomastico/zohar","Zohar (hijo de Simeón)")
assert ("Gn 23:8" in z_het["mentions"] and "Gn 25:9" in z_het["mentions"])
assert z_son["mentions"]==["Gn 46:10"]
assert "Zera" in z_son["body"] and "Zera" in z_son["body"]
h_ish=entry("onomastico/hadar","Hadad (hijo de Ismael)")
h_ed=entry("onomastico/hadad-rey-de-edom","Hadad (rey de Edom)")
assert "Hadar" in h_ish["body"]
assert "Hadar" in master["onomastico/hadar"]["variantes_aprobadas"]
assert "onomastico/hadar-rey-de-edom" in master, "El otro rey Hadar debe permanecer separado."
assert len({v["id"] for v in (z_het,z_son,h_ish,h_ed)})==4
lookup={(r["chapter"],r["verse"]):r["text"] for r in bes}
assert "Zimrán" in lookup[(25,2)]
assert "Zohar el hitita" in lookup[(25,9)]
assert "Hadad" in lookup[(25,15)]
assert "Hadad, hijo de Bedad" in lookup[(36,35)]
assert "Zera" in lookup[(46,10)]
legacy={(r["chapter"],r["verse"]):r["text"] for r in old_text}
assert "Efrón hijo de Zohar" in legacy[(23,8)]
assert "Zohar" not in lookup[(46,10)]
assert "onomastico/zera" in master and "Zera" in by["onomastico/zera"]["name"]
assert "onomastico/hadar" in master and master["onomastico/hadar"]["genealogias"]
assert "onomastico/zohar" in master and master["onomastico/zohar"]["genealogias"]
print("P3 · Onomástico: dos Zohar, dos Hadad, Zimrán BES, Hadar RVR60; genealogías e IDs históricos conservados.")
