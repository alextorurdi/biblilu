"""Pruebas de publicación y de compatibilidad de la Bibliografía APA 7."""
from pathlib import Path
import json
import re
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
catalog = json.loads((ROOT / "data/bibliography_apa7.json").read_text(encoding="utf-8"))
items = catalog["entries"]
assert len(items) == 69, "Deben existir 69 fuentes normalizadas"
assert len({x["id"] for x in items}) == len(items), "Identificadores bibliográficos repetidos"
assert len({x["legacy"] for x in items}) == len(items), "Números de compatibilidad repetidos"
assert all(x["id"].startswith("bib-") and x["categories"] for x in items)
assert len(json.loads((ROOT / "data/bibliography.json").read_text(encoding="utf-8"))) == 69
assert all("Barton, SO" not in x["apa"] and "Yamauchi" not in x["apa"] for x in items)
page = (DOCS / "bibliografia/index.html").read_text(encoding="utf-8")
assert page.count('class="bib-item"') == 69
assert "bibliography.js" in page and "bibliography-search" in page and "bibliography-filter" in page
assert all('id="' + x["id"] + '"' in page for x in items)
assert all('id="ref-' + str(x["legacy"]) + '"' in page for x in items)
assert all('id="ref-' + str(n) + '"' in page for n in [2, 3, 22, 30, 48, 49, 53, 54, 55, 61, 62, 63])
assert "Utilizado en BIBLILU" in page
assert "https://doi.org/" in page and 'class="bib-external"' in page
assert (DOCS / "assets/bibliography.js").exists()

for slug in ["onomastico/abel","onomastico/askenaz","onomastico/javan","onomastico/tubal","lugares/erec","materiales/gofer"]:
    assert (DOCS / "apendices" / slug / "index.html").exists(), slug

abel = (DOCS / "apendices/onomastico/abel/index.html").read_text(encoding="utf-8")
ask = (DOCS / "apendices/onomastico/askenaz/index.html").read_text(encoding="utf-8")
javan = (DOCS / "apendices/onomastico/javan/index.html").read_text(encoding="utf-8")
tubal = (DOCS / "apendices/onomastico/tubal/index.html").read_text(encoding="utf-8")
erec = (DOCS / "apendices/lugares/erec/index.html").read_text(encoding="utf-8")
gofer = (DOCS / "apendices/materiales/gofer/index.html").read_text(encoding="utf-8")
assert "bib-brown-driver-briggs-1906-lexicon" in abel
assert "bib-ivantchik-2018-scythians" in ask and "bib-zadok-2018-iskuza" in ask
assert "bib-brown-driver-briggs-1906-lexicon" in javan
assert "aunque no demuestra la existencia histórica de un antepasado común llamado Javán" not in javan
assert "bib-weeden-2017-tabal" in tubal
assert "bib-jacobsen-1939-sumerian" in erec
assert "bib-hirsch-hyvernat-1904-gopher-wood" in gofer

# En las escenas aprobadas los vínculos se pueden normalizar sin cambiar notas.
note = (DOCS / "genesis/6/index.html").read_text(encoding="utf-8")
assert "bib-embry-2011-noah" in note
assert "bib-bergsma-hahn-2005-noah" in note
assert "bib-alexander-2026-ham" in note
assert "genesis/6/index.html#fn-67" in page
old = re.findall(r'bibliografia/index\.html#(ref-\d+)', ''.join(
    p.read_text(encoding="utf-8")
    for p in (DOCS / "genesis").glob("*/index.html")
))
assert all('id="' + x + '"' in page for x in old), "Hay enlaces históricos sin destino"

print("Bibliografía: 69 referencias, seis fichas, notas y enlaces comprobados.")
