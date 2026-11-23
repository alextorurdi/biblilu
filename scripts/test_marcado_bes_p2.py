#!/usr/bin/env python3
"""Controles P2 reales: marcado BES 2026, sin modificar el texto original."""
import html
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/"scripts"/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

marks=load("marcar_bes","marcar_dialogos_bes_p2.py")
p2=load("prepare_bes","prepare_genesis_p2.py")
src=json.loads(marks.SOURCE.read_text(encoding="utf-8"))
marked,opens,occupied,evidence=marks.annotate(src)
assert len(src)==len(marked)==874
assert sum(opens.values())>150, opens
assert opens["divine"]>=10, opens
assert opens["thought"]>=2, opens
assert marks.DIVINE_OPENINGS=={
 (25,23,1),(26,2,1),(26,24,1),(28,13,1),(31,3,1),(31,24,1),
 (35,1,1),(35,10,1),(35,11,1),(46,2,1),(46,3,1)
}
by_ref={(v["chapter"],v["verse"]):v for v in marked}

def kinds(c,v):
    return [(p["kind"],p["text"]) for p in by_ref[(c,v)]["parts"]]

assert any(k=="divine" and "Dos naciones" in s for k,s in kinds(25,23))
assert any(k=="divine" for k,s in kinds(26,3))
assert any(k=="divine" for k,s in kinds(31,24))
assert any(k=="divine" for k,s in kinds(35,11))
assert any(k=="divine" for k,s in kinds(46,4))
assert any(k=="divine" and "Jacob, Jacob" in s for k,s in kinds(46,2))
assert any(k=="speech" and "Aquí estoy" in s for k,s in kinds(46,2))
assert any(k=="divine" and "Te haré fecundo" in s for k,s in kinds(48,4))
assert any(k=="thought" and "Si Esaú ataca" in s for k,s in kinds(32,8))
assert all(k!="divine" for k,s in kinds(32,28))
assert all(k=="plain" for k,s in kinds(36,5))

def flatten_html(fragment):
    stripped=re.sub(r"<[^>]*>","",fragment)
    return html.unescape(stripped)

for a,b in zip(src,marked):
    assert a["text"]==b["text"]
    assert "".join(part["text"] for part in b["parts"])==a["text"]
    assert b["revisado"] is False
    rendered=p2.rendered_text(b)
    assert flatten_html(rendered)==a["text"],(a["chapter"],a["verse"])
    assert f'id="gn-{a["chapter"]}-{a["verse"]}"' in p2.verse_html(b)

if marks.OUTPUT.is_file():
    on_disk=json.loads(marks.OUTPUT.read_text(encoding="utf-8"))
    assert [(x["chapter"],x["verse"],x["text"],x["parts"]) for x in on_disk] == [
        (x["chapter"],x["verse"],x["text"],x["parts"]) for x in marked]
catalog,scenes,expected,_=p2.structure()
assert len(scenes)==19 and expected[-1]==(50,26)
assert p2.check_source(expected)[0]["text"]==src[0]["text"]
assert p2.check_format(expected,src)[-1]["text"]==src[-1]["text"]
index=p2.index_html(scenes,expected)
assert index.count('href="')>40
assert '25/index.html#gn-25-1' in index
assert '50/index.html#gn-50-1' in index
assert 'BES 2026' in index and 'RVR1960' in index
print("P2 real BES: 874 versículos intactos, segmentos reversibles, voces divinas y dos índices. APTO PARA REVISIÓN.")
