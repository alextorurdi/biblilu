#!/usr/bin/env python3
"""CT-32: comprueba 24 familias léxicas en BES 2026 contra extracción + reglas P3.

Control dirigido de regresión, NO certificación semántica exhaustiva.
Las exclusiones contextuales permanecen en la cobertura, pero no generan enlaces.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

FAMILIAS = {
    "sangre": r"\bsangre\b",
    "agua": r"\bagua\b",
    "caballo": r"\bcaballos?\b",
    "asno": r"\b(?:asnos?|asnas?|burros?)\b",
    "oveja": r"\bovejas?\b",
    "camello": r"\bcamellos?\b",
    "leche": r"\bleche\b",
    "vino": r"\bvino\b",
    "oro": r"\boro\b",
    "plata": r"\bplata\b",
    "sal": r"\bsal\b",
    "espada": r"\bespadas?\b",
    "cama": r"\bcamas?\b",
    "copa": r"\bcopas?\b",
    "saco": r"\bsacos?\b",
    "mesa": r"\bmesas?\b",
    "cadena": r"\bcadenas?\b",
    "cordon": r"\bcordones?\b|\bcordón\b",
    "anillo": r"\banillos?\b",
    "aretes": r"\baretes?\b",
    "canasta": r"\bcanastas?\b",
    "rocio": r"\brocío\b",
    "pozo": r"\bpozos?\b",
    "faraon": r"\bfaraón\b",
}

def main():
    verses = load("data/genesis_25_50_bes.json")
    raw = load("data/p3-extracciones-genesis-25-50.json")
    rules = load("data/p3-reconciliacion-genesis-25-50.json")
    assert len(verses) == 874
    occupied = {
        (x["ref"], x["start"], x["end"])
        for items in raw["categorias"].values()
        for x in items
    }
    occupied.update(
        (x["ref"], x["start"], x["end"])
        for x in rules["correcciones_contextuales"]
    )
    missing = []
    total = 0
    for family, pattern in FAMILIAS.items():
        expression = re.compile(pattern, re.IGNORECASE)
        for v in verses:
            ref = f"Gn {v['chapter']}:{v['verse']}"
            for match in expression.finditer(v["text"]):
                total += 1
                pos = (ref, match.start(), match.end())
                if pos not in occupied:
                    missing.append((family, ref, match.group(), match.start(), match.end()))
    assert not missing, f"Menciones sin inventariar ({len(missing)}): {missing[:35]}"
    print(f"CT-32 OK: {len(FAMILIAS)} familias, {total} apariciones cubiertas en 874 versículos")
    print("Alcance: solo control léxico dirigido; exclusiones no equivalen a enlaces.")

if __name__ == "__main__":
    main()
