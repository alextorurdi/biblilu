#!/usr/bin/env python3
"""Marca provisionalmente diálogos/pensamientos y voces divinas de la BES 2026.

Entrada: data/genesis_25_50_bes.json (FUENTE INMUTABLE)
Salidas:
  data/genesis_25_50_bes_formato.json (marcado, texto original intacto)
  editorial/p2-revision-dialogos-genesis-25-50.json (control de calidad)
No crea ni edita páginas públicas ni reemplaza RVR1960.
El marcado automático es BORRADOR y tiene revisado=false.
"""
from collections import Counter
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/"data/genesis_25_50_bes.json"
OUTPUT = ROOT/"data/genesis_25_50_bes_formato.json"
REPORT = ROOT/"editorial/p2-revision-dialogos-genesis-25-50.json"
# Cada clave es (capítulo, versículo, número de apertura « de ese versículo).
# Solo instancias donde el discurso se atribuye explícitamente a Dios/Señor.
DIVINE_OPENINGS = {
 (25,23,1),  # El Señor a Rebeca
 (26,2,1), (26,24,1),  # El Señor a Isaac
 (28,13,1),  # El Señor en Betel
 (31,3,1), (31,24,1),  # El Señor a Jacob; Dios a Labán
 (35,1,1), (35,10,1), (35,11,1),  # Dios a Jacob/Israel
 (46,2,1), (46,3,1),  # Dios habla durante la visión de Israel
}
# Citas textuales de palabras atribuidas a Dios, dentro de un parlamento humano.
# Mantener fuente y guillemets. Revisión editorial especialmente en 32:9.
DIVINE_NESTED = {(31,29,1),(32,9,1),(48,4,1)}
# Criterios aprobados explícitamente por el editor el 23/11/2026.
# La aprobación de reglas NO marca revisados los 874 versículos por separado.
EDITORIAL_DECISIONS = [
 {"ref":"26:7","decision":"Mantener diálogo real; frase temida como discurso hipotético y pensamiento final como pensamiento."},
 {"ref":"31:11–13","decision":"Mensajero de Betel: intervención en cursiva SIN rojo; no imponer identificación teológica."},
 {"ref":"31:29","decision":"Labán cita las palabras de Dios: rojo únicamente en la cita interna."},
 {"ref":"32:9","decision":"Jacob recuerda palabras de Dios: rojo únicamente en la cita interna."},
 {"ref":"32:26–29","decision":"Adversario del Jaboc: intervención en cursiva SIN rojo; no anticipar identificación."},
 {"ref":"48:4","decision":"Jacob cita palabras de Dios: rojo únicamente en la cita interna."}
]


def role_at_open(c,v,n,opener,context,parent):
    if opener=="«" and (c,v,n) in DIVINE_OPENINGS:
        return "divine","atribucion_explicita"
    if opener=="“" and (c,v,n) in DIVINE_NESTED:
        return "divine","cita_interna_de_dios"
    if opener=="«":
        context=re.split(r"[.!?»]",context)[-1][-140:]
        if re.search(r"\b(?:pensaba|pensó|se dijo a sí mism[oa]|pensaba para sí)\s*:\s*$",
                     context,flags=re.I):
            return "thought","pensamiento_explicito"
        if re.search(r"\b(?:temía|miedo de decir)\s*:\s*$",context,flags=re.I):
            return "thought","discurso_hipotetico"
    if opener=="“":
        return "speech","cita_anidada"
    return "speech","discurso_directo"


def add(parts,kind,char):
    if parts and parts[-1]["kind"]==kind:
        parts[-1]["text"]+=char
    else:
        parts.append({"kind":kind,"text":char})


def annotate(verses):
    stack=[]
    annotated=[]
    opened=Counter()
    occupied=Counter()
    evidence=[]
    expect_chapter=25
    for v in verses:
        c,n=v["chapter"],v["verse"]
        if c!=expect_chapter:
            if stack: raise ValueError(f"Comillas abiertas al acabar el capítulo {expect_chapter}: {stack}")
            expect_chapter=c
        opening_counts={"«":0,"“":0}
        parts=[]
        s=v["text"]
        for i,ch in enumerate(s):
            if ch in "«“":
                opening_counts[ch]+=1
                qn=opening_counts[ch]
                role,reason=role_at_open(c,n,qn,ch,s[:i],stack[-1] if stack else None)
                stack.append({"open":ch,"kind":role,"at":f"{c}:{n}","why":reason})
                opened[role]+=1
                evidence.append({"ref":f"{c}:{n}","tipo":role,"apertura":ch,"ordinal":qn,"motivo":reason})
                add(parts,role,ch)
            elif ch in "»”":
                required={"»":"«","”":"“"}[ch]
                if not stack or stack[-1]["open"]!=required:
                    raise ValueError(f"Comillas desordenadas en {c}:{n}, posición {i}")
                add(parts,stack[-1]["kind"],ch)
                stack.pop()
            else:
                kind=stack[-1]["kind"] if stack else "plain"
                add(parts,kind,ch)
                occupied[kind]+=1
        if "".join(p["text"] for p in parts)!=s:
            raise AssertionError(f"El marcado altera el texto literal en {c}:{n}")
        if not parts:raise ValueError(f"Versículo vacío: {c}:{n}")
        annotated.append({**v,"parts":parts,"revisado":False})
    if stack:raise ValueError("Comillas sin cerrar al final de Génesis 50")
    return annotated,opened,occupied,evidence


def main():
    verses=json.loads(SOURCE.read_text(encoding="utf-8"))
    assert len(verses)==874
    marked,opened,occupied,evidence=annotate(verses)
    assert len(marked)==874
    marked_text=[(v["chapter"],v["verse"],v["text"]) for v in marked]
    base_text=[(v["chapter"],v["verse"],v["text"]) for v in verses]
    assert marked_text==base_text,"El archivo de formato NO puede modificar el texto base"
    # Control por capítulo y por escena; la configuración de la escenificación es externa.
    counts={}
    for v in marked:
        for p in v["parts"]:
            if p["kind"] not in ("plain","speech","thought","divine"):raise ValueError("Rol inválido")
        for p in v["parts"]:
            if p["kind"]!="plain":
                counts[p["kind"]]=counts.get(p["kind"],0)+1
    report={
        "edicion":"BES 2026","fase":"P2","estado":"criterios de marcado aprobados; aplicación automática pendiente de revisión integral",
        "versiculos":len(marked),"con_partes":len(marked),
        "texto_literal_igual_fuente":True,
        "aperturas_por_tipo":dict(opened),
        "segmentos_por_tipo":counts,
        "caracteres_por_tipo":dict(occupied),
        "aperturas_atribuidas_a_dios":[x for x in evidence if x["tipo"]=="divine"],
        "casos_resueltos_por_el_editor":EDITORIAL_DECISIONS,
        "nombres_divinos":{"referencias_Dios_y_Senor_en_mayuscula":138,
                           "exclusion_referente_humano":["43:20 Señor"],
                           "marcas_visualizadas_fuera_de_discurso_divino":"según renderer P2",
                           "pendiente":"control textual integral antes de aprobar todos los versículos"},
        "criterio":"APROBADO: distinguir nombres divinos de voz divina; conservar comillas y BES literales; cursiva en discursos humanos y casos ambiguos; rojo en discursos de Dios y en citas atribuidas a Dios.",
        "fuente":"data/genesis_25_50_bes.json",
        "borrador":"data/genesis_25_50_bes_formato.json",
        "cobertura":"Génesis 25:1–50:26"
    }
    OUTPUT.write_text(json.dumps(marked,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Marcado P2:",len(marked),"versículos,","aperturas",dict(opened),
          "segmentos",counts,"decisiones_aprobadas",len(EDITORIAL_DECISIONS))


if __name__=="__main__":
    main()
