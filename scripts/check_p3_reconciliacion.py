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
    assert len([x for x in corrections if x["codigo"]=="CT-17"]) == 39
    # Auditoría de cobertura: presencia y offsets independientes de los candidatos brutos.
    ct17 = [x for x in records if "CT-17" in x["fuentes"]]
    assert len(ct17) == 39
    def covered(ref, literal, required=1):
        return len([x for x in ct17 if x["ref"]==ref and x["literal"].casefold()==literal.casefold()]) == required
    assert covered("Gn 38:18","cordón") and covered("Gn 38:18","bastón")
    assert covered("Gn 40:17","canasta",2)
    assert covered("Gn 47:31","cama") and covered("Gn 32:32","israelitas")
    assert covered("Gn 27:28","rocío") and covered("Gn 37:31","sangre")
    # CT-18: jefaturas edomitas sin nuevas identidades personales ni enlaces inventados.
    ct18 = [x for x in corrections if x["codigo"] == "CT-18"]
    assert len(ct18) == 10
    for x in ct18:
        assert x["ref"] in ("Gn 36:40", "Gn 36:41", "Gn 36:42", "Gn 36:43")
        assert x["accion"] in ("clasificar_sin_id", "asociacion_contextual")
        assert any(y["ref"] == x["ref"] and y["start"] == x["start"] and y["end"] == x["end"]
                   and "CT-18" in y["fuentes"] and y["id"] == x["id"] for y in records)
    assert sum(x["accion"] == "clasificar_sin_id" for x in ct18) == 7
    assert sum(x["accion"] == "asociacion_contextual" for x in ct18) == 3
    # CT-19: 15 hijos horeos sin cobertura y una jefatura homónima.
    ct19 = [x for x in corrections if x["codigo"] == "CT-19"]
    assert len(ct19) == 16
    assert sum(x["accion"] == "clasificar_sin_id" for x in ct19) == 15
    assert sum(x["accion"] == "asociacion_contextual" for x in ct19) == 1
    assert any(x["ref"]=="Gn 36:16" and x["literal"]=="Coré" and x["id"]=="onomastico/core-hijo-de-esau" for x in ct19)
    for x in ct19:
        assert any(y["ref"]==x["ref"] and y["start"]==x["start"] and y["end"]==x["end"]
                   and y["literal"]==x["literal"] and y["id"]==x["id"] and "CT-19" in y["fuentes"]
                   for y in records)
    # CT-20: tres usos del gentilicio «hebreo» sin adscripción editorial prematura.
    ct20 = [x for x in corrections if x["codigo"] == "CT-20"]
    assert len(ct20) == 3
    assert {x["ref"] for x in ct20} == {"Gn 39:14", "Gn 39:17", "Gn 41:12"}
    assert all(x["literal"] == "hebreo" and x["categoria"] == "tribus"
               and x["id"] == "tribus/israelitas" and x["accion"] == "asignar" for x in ct20)
    # D-01 y CT-21: variantes históricas y validación contextual por nombre propio.
    assert rules["d01"]["estado"] == "aprobada" and rules["d01"]["opcion"] == "A"
    hebreos = [x for x in records if x["literal"].lower() in ("hebreo", "hebreos")]
    assert len(hebreos) == 5 and all(x["id"] == "tribus/israelitas" for x in hebreos)
    ct21 = [x for x in corrections if x["codigo"] == "CT-21"]
    assert len(ct21) == 393
    for x in ct21:
        y = indexed[(x["ref"], x["start"], x["end"])]
        assert y["categoria"] == "onomastico" and y["id"] == x["id"]
        assert "CT-21" in y["fuentes"]
    # CT-22: «Faraón» usa ficha histórica ya existente, sin identificar monarca.
    ct22 = [x for x in corrections if x["codigo"] == "CT-22"]
    assert len(ct22) == 74
    assert rules["d02"]["ficha"] == "onomastico/faraon"
    assert "onomastico/faraon" in historical_ids
    assert all(x["id"] == "onomastico/faraon" and x["categoria"] == "onomastico" for x in ct22)
    assert sum("CT-22" in x["fuentes"] for x in records) == 74
    # CT-23: siete identidades personales ya existentes en Onomástico.
    ct23 = [x for x in corrections if x["codigo"] == "CT-23"]
    assert len(ct23) == 330
    assert {x["id"] for x in ct23} == {"onomastico/esau", "onomastico/isaac",
        "onomastico/laban", "onomastico/raquel", "onomastico/lea",
        "onomastico/abraham", "onomastico/rebeca"}
    assert all(x["accion"] == "validar_identidad" and x["id"] in historical_ids for x in ct23)
    # D-03: Ismaelitas y Madianitas, dos pueblos distintos.
    assert rules["d03"]["opcion"] == "A"
    assert rules["d03"]["fichas_principales"] == ["tribus/ismaelitas","tribus/madianitas"]
    d03_mentions = [x for x in records if "D-03" in x["fuentes"]]
    assert len(d03_mentions) == 7
    assert sum(x["id"] == "tribus/ismaelitas" for x in d03_mentions) == 4
    assert sum(x["id"] == "tribus/madianitas" for x in d03_mentions) == 3
    assert all(x["id_futuro"] and x["categoria"] == "tribus" for x in d03_mentions)
    # CT-24: nombres personales del relato/genealogías y Egipto como lugar.
    ct24 = [x for x in corrections if x["codigo"] == "CT-24"]
    assert len(ct24) == 368
    assert sum(x["id"] == "lugares/egipto" for x in ct24) == 66
    assert all(x["id"] in historical_ids and x["accion"] == "validar_identidad" for x in ct24)
    assert all(indexed[(x["ref"], x["start"], x["end"])]["id"] == x["id"] for x in ct24)
    # CT-25: menciones directas contextuales en seis categorías.
    ct25 = [x for x in corrections if x["codigo"] == "CT-25"]
    assert len(ct25) == 155
    assert all(x["id"] in historical_ids and x["accion"] == "validar_identidad" for x in ct25)
    assert all(indexed[(x["ref"], x["start"], x["end"])]["id"] == x["id"] for x in ct25)
    # CT-26: 44 últimos candidatos, preservando homónimos y simbolismo.
    ct26 = [x for x in corrections if x["codigo"] == "CT-26"]
    assert len(ct26) == 44
    assert sum(x["accion"] == "asociacion_contextual" for x in ct26) >= 7
    assert not any(x["estado"] == "candidato_unico_no_validado" for x in records)
    assert all("CT-26" in indexed[(x["ref"], x["start"], x["end"])]["fuentes"] for x in ct26)
    # CT-27: cobertura de Israel personal, Er, familiares edomitas y topónimos del pacto.
    ct27 = [x for x in corrections if x["codigo"] == "CT-27"]
    assert len(ct27) == 47
    assert sum(x["literal"] == "Israel" for x in ct27) == 31
    assert sum(x["literal"] == "Er" for x in ct27) == 5
    assert any(x["literal"] == "Jegar-sahaduta" and x["id"] == "lugares/pacto-jacob-laban" for x in ct27)
    assert any(x["literal"] == "Mizpa" and x["id"] == "lugares/pacto-jacob-laban" for x in ct27)
    # CT-28: cobertura de seres vivos, objetos, materiales y genéricos.
    ct28 = [x for x in corrections if x["codigo"] == "CT-28"]
    assert len(ct28) == 84
    assert not any(x["ref"] in ("Gn 27:35", "Gn 31:24") and x["id"] == "materiales/vino" for x in ct28)
    assert any(x["ref"] == "Gn 30:14" and x["id"] == "animales/mandragora" for x in ct28)
    assert any(x["ref"] == "Gn 31:19" and x["id"] == "objetos/terafin" for x in ct28)
    assert any(x["ref"] == "Gn 49:27" and x["id"] == "animales/lobo" for x in ct28)
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
