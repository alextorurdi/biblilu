#!/usr/bin/env python3
"""Capa derivada P3: conserva candidatos brutos y aplica solo reglas editoriales explícitas."""
from pathlib import Path
from collections import Counter
import argparse
import json
import re

ROOT=Path(__file__).resolve().parents[1]
def load(p):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
def key(x):
    return f"{x['ref']}|{x['start']}|{x['end']}"
def generate():
    raw=load("data/p3-extracciones-genesis-25-50.json")
    rules=load("data/p3-reconciliacion-genesis-25-50.json")
    reg=load("data/registro_maestro.json")
    historical={x["id"] for x in reg["entidades"]}
    entries={}
    for cat,items in raw["categorias"].items():
        for x in items:
            k=key(x)
            if k not in entries:
                entries[k]={"ref":x["ref"],"chapter":x["chapter"],"verse":x["verse"],
                    "start":x["start"],"end":x["end"],"literal":x["literal"],
                    "categorias_brutas":[],"candidatos_brutos":[],
                    "estado_bruto":x["estado"],"estado":"candidato_no_reconciliado",
                    "categoria":None,"id":None,"accion":None,"fuentes":[]}
            y=entries[k]
            if cat not in y["categorias_brutas"]:
                y["categorias_brutas"].append(cat)
            for candidate in x["candidatos_ficha"]:
                if candidate not in y["candidatos_brutos"]:
                    y["candidatos_brutos"].append(candidate)
    for x in rules["cruces_onomastico_lugares"]:
        y=entries[key(x)]
        y.update(categoria=x["categoria"],id=x["id"],
                 accion="asignar",estado="clasificado_por_contexto")
        y["fuentes"].append("CT-10")
    for x in rules["correcciones_contextuales"]:
        k=key(x)
        if k not in entries:
            ch,ve=map(int,re.match(r"Gn (\d+):(\d+)",x["ref"]).groups())
            entries[k]={"ref":x["ref"],"chapter":ch,"verse":ve,
                "start":x["start"],"end":x["end"],"literal":x["literal"],
                "categorias_brutas":[],"candidatos_brutos":[],
                "estado_bruto":None,"estado":"candidato_no_reconciliado",
                "categoria":None,"id":None,"accion":None,"fuentes":[]}
        y=entries[k]
        if y["accion"] and y["accion"]!=x["accion"]:
            raise ValueError("Acciones incompatibles: "+k)
        states={"excluir":"excluido_aprobado","nota_contextual":"nota_contextual_aprobada",
            "asociacion_contextual":"asociacion_contextual_aprobada",
            "no_enlazar_como_persona":"exclusion_personal_aprobada"}
        y.update(categoria=x["categoria"],id=x["id"],accion=x["accion"],
                 estado=states.get(x["accion"],"clasificado_por_contexto"))
        y["fuentes"].append(x["codigo"])
        if "destinos" in x:y["destinos_contextuales"]=x["destinos"]
        if "motivo" in x:y["motivo"]=x["motivo"]
    for y in entries.values():
        if (y["estado"]=="candidato_no_reconciliado"
            and len(y["categorias_brutas"])==len(y["candidatos_brutos"])==1):
            y.update(categoria=y["categorias_brutas"][0],id=y["candidatos_brutos"][0],
                     estado="candidato_unico_no_validado")
        elif y["estado"]=="candidato_no_reconciliado" and y["estado_bruto"]=="variante_ortografica_aprobada":
            y.update(categoria=y["categorias_brutas"][0],id=y["candidatos_brutos"][0],
                     estado="clasificado_previamente_aprobado")
        if y["id"] and y["id"] not in historical:y["id_futuro"]=True
    rows=sorted(entries.values(),key=lambda x:(x["chapter"],x["verse"],x["start"],x["end"]))
    by_state=dict(Counter(x["estado"] for x in rows))
    ids_future=sorted(set(x["id"] for x in rows if x.get("id_futuro")))
    return {"fase":"P3","edicion":"BES 2026","estado":"catalogo_derivado_parcial_no_certificado",
        "generador":"scripts/build_p3_catalogo_reconciliado.py",
        "texto":"data/genesis_25_50_bes.json",
        "inventario_original":"data/p3-extracciones-genesis-25-50.json",
        "reglas":"data/p3-reconciliacion-genesis-25-50.json",
        "resumen":{"total":len(rows),
          "brutos":len(raw["categorias"]["onomastico"])+len(raw["categorias"]["lugares"]),
          "reconciliados":sum(bool(x["fuentes"]) for x in rows),
          "por_estado":by_state,"ids_futuros":ids_future},
        "menciones":rows}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    output=ROOT/"data/p3-catalogo-reconciliado-genesis-25-50.json"
    result=generate()
    verses=load("data/genesis_25_50_bes.json")
    text={f"Gn {v['chapter']}:{v['verse']}":v["text"] for v in verses}
    assert len(verses)==len(text)==874
    for x in result["menciones"]:
        assert text[x["ref"]][x["start"]:x["end"]]==x["literal"],x
    encoded=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.check:
        assert output.read_text(encoding="utf-8")==encoded,"Catalogo no reproducible"
        print("Catalogo P3 OK:",len(result["menciones"]),"registros")
    else:
        output.write_text(encoded,encoding="utf-8")
        print("Catalogo P3 generado:",len(result["menciones"]),"registros")

if __name__=="__main__":
    main()
