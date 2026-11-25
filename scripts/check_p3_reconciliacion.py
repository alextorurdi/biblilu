#!/usr/bin/env python3
"""Valida la capa editorial de reconciliación P3 sin modificar el barrido bruto ni las fichas."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def main():
    verses = read("data/genesis_25_50_bes.json")
    raw = read("data/p3-extracciones-genesis-25-50.json")
    rules = read("data/p3-reconciliacion-genesis-25-50.json")
    registry = read("data/registro_maestro.json")
    assert len(verses) == 874
    text = {f"Gn {v['chapter']}:{v['verse']}": v["text"] for v in verses}
    assert len(text) == 874
    historical_ids = {x["id"] for x in registry["entidades"]}
    raw_keys = {
        (x["ref"], x["start"], x["end"])
        for category in ("onomastico", "lugares")
        for x in raw["categorias"][category]
    }
    crosses = rules["cruces_onomastico_lugares"]
    assert len(crosses) == 55
    assert len({(x["ref"],x["start"],x["end"]) for x in crosses}) == 55
    expected = {"lugares": 45, "onomastico": 8, "tribus": 2}
    assert dict(Counter(x["categoria"] for x in crosses)) == expected
    for x in crosses:
        assert (x["ref"],x["start"],x["end"]) in raw_keys, x
        assert text[x["ref"]][x["start"]:x["end"]] == x["literal"], x
        assert x["id"].startswith(x["categoria"]+"/"), x
    corrections = rules["correcciones_contextuales"]
    assert len(corrections) >= 50
    for x in corrections:
        assert text[x["ref"]][x["start"]:x["end"]] == x["literal"], x
        if x["id"] is not None:
            assert x["id"].startswith(x["categoria"]+"/"), x
        if x["accion"] == "excluir":
            assert x["id"] is None
        if x["accion"] == "nota_contextual":
            assert x["ref"] == "Gn 31:27" and x.get("destinos") == ["instrumentos/tof","instrumentos/kinnor"]
    ids = {(x["ref"],x["literal"],x["codigo"],x["id"]) for x in corrections}
    for expected_item in [
        ("Gn 26:33","Seba","CT-01","lugares/seba-pozo"),
        ("Gn 33:19","monedas","CT-06","medidas/qesita"),
        ("Gn 35:16","cierta distancia","CT-07","medidas/kibra"),
        ("Gn 48:7","cierta distancia","CT-07","medidas/kibra"),
        ("Gn 37:24","pozo","CT-08","objetos/cisterna"),
        ("Gn 36:32","Edom","CT-05","lugares/edom"),
        ("Gn 42:5","Israel","CT-04","onomastico/jacob"),
    ]:
        assert expected_item in ids, expected_item
    assert any(x["ref"]=="Gn 29:15" and x["literal"]=="seas" and x["accion"]=="excluir" for x in corrections)
    assert all(x["accion"]=="excluir" for x in corrections if x["codigo"]=="CT-09")
    # El resultado derivado debe integrar cada regla una sola vez.
    catalog = read("data/p3-catalogo-reconciliado-genesis-25-50.json")
    records = catalog["menciones"]
    assert len(records) >= 1656, "Se perdieron menciones del inventario bruto"
    assert len({(x["ref"],x["start"],x["end"]) for x in records}) == len(records)
    for x in records:
        assert text[x["ref"]][x["start"]:x["end"]] == x["literal"], x
    indexed = {(x["ref"],x["start"],x["end"]): x for x in records}
    rule_keys = [(x["ref"],x["start"],x["end"]) for x in corrections]
    assert len(rule_keys) == len(set(rule_keys)), "Reglas duplicadas sobre la misma mención"
    for x in corrections:
        record = indexed[(x["ref"],x["start"],x["end"])]
        assert record["categoria"] == x["categoria"], x
        assert record["id"] == x["id"], x
        assert x["codigo"] in record["fuentes"], x
        if x["accion"] in ("clasificar_sin_id","homonimo_no_identificado"):
            assert record["id"] is None, x
    assert not any(x["estado"] == "candidato_no_reconciliado" for x in records)
    assert len([x for x in corrections if x["codigo"]=="CT-14"]) == 29
    def resolved(ref, literal, id):
        return any(x["ref"]==ref and x["literal"]==literal and x["id"]==id
                   and "CT-14" in x["fuentes"] for x in records)
    assert resolved("Gn 34:2","Siquem",None)
    assert resolved("Gn 36:2","Aná","onomastico/ana-hijo-de-zibeon")
    assert resolved("Gn 36:20","Aná","onomastico/ana-hijo-de-seir")
    assert resolved("Gn 38:30","Zera","onomastico/zara")
    assert resolved("Gn 36:33","Zera",None)
    assert rules["r01"]["ficha_principal"] == "tribus/israelitas"
    assert rules["r01"]["remision_futura"] == "tribus/israel"
    assert rules["r01"]["persona_distinta"] == "onomastico/jacob"
    # Los IDs de fichas futuras no se confunden con entradas ya materializadas.
    assert "tribus/israelitas" not in historical_ids
    assert "tribus/israel" not in historical_ids
    print("P3 reconciliación OK: 874 versículos, 55 cruces,",
          len(corrections), "acciones contextuales; R-01 aprobada.")

if __name__ == "__main__":
    main()
