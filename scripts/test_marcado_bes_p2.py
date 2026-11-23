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
# Aprobación editorial: Gn 31:11-13 y 32:26-29 en cursiva, SIN voz divina.
assert all(kind!="divine" for verse in range(11,14) for kind,part in kinds(31,verse))
assert all(kind!="divine" for verse in range(26,30) for kind,part in kinds(32,verse))
# Los nombres propios de Dios tienen color propio, pero "Señor" (43:20)
# es una fórmula de respeto a un funcionario egipcio.
assert '<span class="divine">Dios</span>' in p2.rendered_text(by_ref[(32,28)])
assert '<span class="divine">Señor</span>' in p2.rendered_text(by_ref[(25,21)])
assert '<span class="divine">Señor</span>' not in p2.rendered_text(by_ref[(43,20)])
assert '<span class="divine">señor</span>' not in p2.rendered_text(by_ref[(44,18)])
assert '<span class="divine">dioses</span>' not in p2.rendered_text(by_ref[(35,2)])
assert sum(1 for v in src for m in re.finditer(r"\b(?:Dios|Señor)\b",v["text"])
           if (v["chapter"],v["verse"],m.group(0)) not in p2.NON_DIVINE_NAME_REFS) == 137


# Restituye los signos originales BES a partir de las marcas reversibles
# del HTML visual, independientemente del estilo o de las rayas de diálogo.
from html.parser import HTMLParser

class SourceRecovery(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text=[]
        self.skip=0
    def handle_starttag(self,tag,attrs):
        if self.skip:
            self.skip+=1
        elif tag=="span" and (original:=dict(attrs).get("data-source-char")):
            self.text.append(original)
            self.skip=1
    def handle_endtag(self,tag):
        if self.skip:
            self.skip-=1
    def handle_data(self,data):
        if not self.skip:
            self.text.append(data)

def recover_source(rendered):
    reader=SourceRecovery()
    reader.feed(rendered)
    assert reader.skip==0
    return "".join(reader.text)

speaker_count=0
thought_count=0
for a,b in zip(src,marked):
    assert a["text"]==b["text"]
    assert "".join(part["text"] for part in b["parts"])==a["text"]
    assert b["revisado"] is False
    rendered=p2.rendered_text(b)
    assert recover_source(rendered)==a["text"],(a["chapter"],a["verse"])
    speaker_count += rendered.count('class="p2-spoken-dash"')
    thought_count += sum(1 for p in b["parts"] if p["kind"]=="thought" and "«" in p["text"])
    assert f'id="gn-{a["chapter"]}-{a["verse"]}"' in p2.verse_html(b)

expected_speaker_dashes = sum(
    p["text"].count("«") for verse in marked for p in verse["parts"]
    if p["kind"] in ("speech","divine")
)
assert speaker_count == expected_speaker_dashes, (speaker_count,expected_speaker_dashes)
assert speaker_count > 250
# Regla novelística adicional: cada apertura de diálogo con raya comienza
# en otra línea, sin repetirla en las continuaciones de versículos.
# Solo dos versículos empiezan directamente con comillas de diálogo, y
# ambos abren un párrafo (34:21 y 42:30): no se introduce línea vacía.
break_count = sum(p2.rendered_text(v).count('class="p2-dialogue-break"')
                  for v in marked)
leading_speech = [v for v in marked if p2.starts_with_spoken_quote(v)]
assert {(v["chapter"],v["verse"]) for v in leading_speech} == {(34,21),(42,30)}
inline_count = sum(len(p2.same_speaker_positions(v)) for v in marked)
assert inline_count == 3, inline_count
assert break_count == speaker_count-len(leading_speech)-inline_count, (
    break_count,speaker_count,inline_count
)
# Caso mostrado por el editor: narrador Gn 26:2 y parlamento divino 26:2–5.
g26 = p2.rendered_text(by_ref[(26,2)])
assert 'le dijo: ' in g26
assert 'le dijo: <em class="speech"><span class="divine"><br class="p2-dialogue-break" aria-hidden="true"><span class="p2-spoken-dash"' in g26
assert all('class="p2-dialogue-break"' not in p2.rendered_text(by_ref[(26,n)])
           for n in (3,4,5))
# Conversación con dos voces dentro del mismo versículo: cada raya en su línea.
g269 = p2.rendered_text(by_ref[(26,9)])
assert g269.count('class="p2-dialogue-break"') == 2
assert g269.count('class="p2-spoken-dash"') == 2
assert g269.count('class="p2-narrative-break"') == 1
assert 'Isaac respondió:' in g269
assert 'Isaac respondió:' in recover_source(g269)
# Caso expuesto en la captura: narración del otro interlocutor baja
# inmediatamente después de que termine la primera intervención.
g268 = p2.rendered_text(by_ref[(26,8)])
g2610 = p2.rendered_text(by_ref[(26,10)])
g2611 = p2.rendered_text(by_ref[(26,11)])
assert 'class="p2-narrative-break"' not in g268
assert 'class="p2-narrative-break"' not in g2610
assert 'class="p2-narrative-break"' not in g2611
assert p2.ends_with_oral_closure(by_ref[(26,9)])
assert p2.verse_html(by_ref[(26,10)], first_in_paragraph=False,
                     prior_spoken_ended=True).startswith(
                     '<br class="p2-dialogue-break" aria-hidden="true"><span class="verse-inline" id="gn-26-10"')
assert not p2.ends_with_oral_closure(by_ref[(27,25)])
assert p2.verse_html(by_ref[(27,26)], first_in_paragraph=False,
                     prior_spoken_ended=False).startswith('<span class="verse-inline"')
# Mismo hablante después de un inciso del narrador: no crear nueva línea,
# pero mostrar el inciso delimitado por una raya editorial.
for c,v in ((27,36),(43,29),(45,4)):
    verse = by_ref[(c,v)]
    quote_pos = [m.start() for m in re.finditer("«",verse["text"])]
    assert len(quote_pos) == 2
    assert quote_pos[1] in p2.same_speaker_positions(verse)
    rendered = p2.rendered_text(verse)
    assert rendered.count('class="p2-spoken-dash"') == 2
    assert rendered.count('class="p2-dialogue-break"') == 1
    assert rendered.count('class="p2-inline-narrator-mark"') == 1
    assert 'class="p2-narrative-break"' not in rendered
    assert recover_source(rendered) == verse["text"]
# También admitir la acotación clásica de un escritor entre comas.
synthetic = {"chapter":27, "verse":36,
             "text": "«José no lo vio», dijo Fabián, «Tuve que recordárselo».",
             "parts": [
                 {"kind":"speech","text":"«José no lo vio»"},
                 {"kind":"plain","text":", dijo Fabián, "},
                 {"kind":"speech","text":"«Tuve que recordárselo»"},
                 {"kind":"plain","text":"."}
             ]}
syn = p2.rendered_text(synthetic)
assert len(p2.same_speaker_positions(synthetic)) == 1
assert syn.count('class="p2-inline-narrator-mark"') == 1
assert syn.count('class="p2-dialogue-break"') == 0
assert recover_source(syn) == synthetic["text"]
# Pensamientos: cursiva, sin guiones ni líneas forzadas.
g267 = p2.rendered_text(by_ref[(26,7)])
assert g267.count('class="p2-dialogue-break"') == 1
assert g267.count('class="p2-spoken-dash"') == 1
# Una intervención que comienza en el primer carácter del versículo:
# si continúa un párrafo previo, su ancla y raya cambian juntas de línea.
start_quote = by_ref[(34,21)]
assert not p2.verse_html(start_quote,first_in_paragraph=True).startswith("<br")
assert p2.verse_html(start_quote,first_in_paragraph=False).startswith(
    '<br class="p2-dialogue-break" aria-hidden="true"><span class="verse-inline" id="gn-34-21"'
)
assert p2.verse_html(start_quote,first_in_paragraph=False).count(
    'class="p2-dialogue-break"') == 1

assert thought_count == opens["thought"]
assert p2.rendered_text(by_ref[(26,9)]).count('class="p2-spoken-dash"') == 2
assert p2.rendered_text(by_ref[(46,2)]).count('class="p2-spoken-dash"') == 2
assert p2.rendered_text(by_ref[(31,13)]).count('class="p2-spoken-dash"') == 0
assert p2.rendered_text(by_ref[(32,9)]).count('class="p2-spoken-dash"') == 1
assert "“Vuelve" in p2.rendered_text(by_ref[(32,9)])
assert "<em class=\"thought\">" in p2.rendered_text(by_ref[(26,7)])
assert p2.rendered_text(by_ref[(26,7)]).count('class="p2-spoken-dash"') == 1
assert 'class="p2-quote-omitted" data-source-char="«"' in p2.rendered_text(by_ref[(26,7)])
assert 'class="p2-spoken-dash"' not in p2.rendered_text(by_ref[(32,8)])

if marks.OUTPUT.is_file():
    on_disk=json.loads(marks.OUTPUT.read_text(encoding="utf-8"))
    assert [(x["chapter"],x["verse"],x["text"],x["parts"]) for x in on_disk] == [
        (x["chapter"],x["verse"],x["text"],x["parts"]) for x in marked]
catalog,scenes,expected,_=p2.structure()
plan, nparagraphs = p2.validate_paragraph_plan(scenes,expected)
assert nparagraphs == 387
assert len(plan) == 19
assert plan[16]["limites_parrafo"][:5] == ["25:1","25:5","25:7","25:9","25:11"]
assert "25:18" in plan[16]["limites_obligatorios_recursos"]
assert "41:53" in plan[30]["limites_obligatorios_recursos"]
assert "46:30" in plan[31]["limites_parrafo"]
assert all(set(row["limites_obligatorios_recursos"]).issubset(set(row["limites_parrafo"]))
           for row in plan.values())
assert len(scenes)==19 and expected[-1]==(50,26)
assert p2.check_source(expected)[0]["text"]==src[0]["text"]
assert p2.check_format(expected,src)[-1]["text"]==src[-1]["text"]
index=p2.index_html(scenes,expected)
assert index.count('href="')>40
assert '25/index.html#gn-25-1' in index
assert '50/index.html#gn-50-1' in index
assert 'BES 2026' in index and 'RVR1960' in index
first_scene = p2.make_scene_html(scenes[0],
    [v for v in marked if v["chapter"]==25 and v["verse"]<=18],scenes)
assert first_scene.count('<p class="prose-paragraph') == 8
assert first_scene.count('<span class="verse-inline" id="gn-') == 18
assert '<span class="verse-inline" id="gn-25-4"' in first_scene
assert '<span class="verse-inline" id="gn-25-5"' in first_scene
assert '<p class="verse"' not in first_scene
assert 'p2-prose.css' in first_scene
print("P2 real BES: 874 versículos y 387 párrafos, comillas recuperables, rayas por intervención, pensamientos sin raya, voces divinas y dos índices.")
