"""Publica Bibliografía APA 7 y reconstruye enlaces a partir de fuentes estables.

Se ejecuta al FINAL de scripts/build.py, después de restaurar las escenas
editoriales y crear el Atlas. Nunca reordena ni reescribe su texto.
"""
from pathlib import Path
from collections import defaultdict
from urllib.parse import quote
import html
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CATALOG = json.loads((ROOT / "data/bibliography_apa7.json").read_text(encoding="utf-8"))
BOOKS = CATALOG["entries"]
assert len(BOOKS) == 69, "Se esperan 69 referencias APA 7 (67 + 2 de Askenaz)"
assert len({b["id"] for b in BOOKS}) == 69
assert len({b["legacy"] for b in BOOKS}) == 69
BY_LEGACY = {b["legacy"]: b for b in BOOKS}
BY_ID = {b["id"]: b for b in BOOKS}

def norm(value):
    value = html.unescape(str(value)).casefold()
    value = unicodedata.normalize("NFD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", value).strip()

# Emparejamiento explícito: evita atribuir textos no bibliográficos a una obra.
CITATIONS = {
    "brown et al., 1906": 19,
    "brown, 1906": 19,
    "hess, 2007": 8,
    "hess, 1992": 48,
    "ivantchik, 2018": 72,
    "zadok, 2018": 73,
    "jones, 1856": 11,
    "the new open bible, 1990": 14,
    "kitchen, 2003": 34,
    "demsky, 2023": 16,
    "glueck, 1951": 36,
    "hamilton, 1990": 7,
    "sayce, 1899": 20,
    "olbrycht, 2000": 21,
    "redford, 2001": 35,
    "antiguedades, 1.6": 29,
    "antiguedades, 1,6": 29,
    "antiguedades, 1,6,4": 29,
    "hidalgo de la vega et al., 2008": 28,
    "kopanias, 2015": 32,
    "gowan, 1988": 23,
    "tiras, 1988": 33,
    "block,1998": 24,
    "burney,2004": 25,
    "gurney, 1952": 26,
    "barjamovic, 2011": 27,
    "weeden, 2017": 31,
    "hirsch & hyvernat, 1904": 9,
    "garcia-moreno, 1987": 5,
    "taylor, 2024": 12,
    "friedmann, 2013": 4,
    "gordon, 1997": 6,
    "day, 2013": 69,
    "rey, 2017": 70,
    "john day, 2012": 49,
    "day, 2012": 49,  # El texto aprobado de Génesis 6 utiliza el apellido solo.
    "jacobsen, 1939": 37,
    "algaze, 2013": 38,
    "ryken, wilhoit y longman, 1998": 71,
    # Adiciones/variaciones editoriales que ya aparecen en notas.
    "embry, 2011": 53,
    "bergsma y hahn, 2005": 54,
    "alexander, 2026": 55,
}
CITATIONS = {norm(label): number for label, number in CITATIONS.items()}

RETIREMENTS = {
    2: "Registro híbrido sin identificación bibliográfica, retirado tras la revisión editorial.",
    22: "Referencia retirada tras la revisión de la ficha de Askenaz.",
    30: "Referencia retirada tras la revisión de la ficha de Javán.",
}
# El asiento 3 duplicaba la edición 1906, cuyo número de origen es 19.
LEGACY_ALIAS = {3: 19}
CITATION_LINK = re.compile(r'<a href="([^"]*bibliografia/index\.html(?:#[^"]*)?)">(\[[^<\]]+\])</a>')
BIB_LINK = re.compile(r'href="[^"]*bibliografia/index\.html#(bib-[a-z0-9-]+|ref-\d+)"')

def target_id(fragment):
    if fragment in BY_ID:
        return fragment
    if fragment.startswith("ref-"):
        old = int(fragment[4:])
        old = LEGACY_ALIAS.get(old, old)
        return BY_LEGACY[old]["id"] if old in BY_LEGACY else None
    return None

def update_citations(page):
    raw = page.read_text(encoding="utf-8")
    bad = set()
    def rewrite(m):
        label = m.group(2)[1:-1]
        key = norm(label)
        number = CITATIONS.get(key)
        if number is None:
            # Evitar convertir [el dios], [su], [Ez 27:14], etc. en citas.
            if re.search(r"(?<!\d)(?:18|19|20)\d\d(?!\d)", label):
                bad.add(label)
            return m.group(2)
        entry = BY_LEGACY.get(number)
        if not entry:
            raise RuntimeError("Cita a asiento eliminado: " + label)
        link = m.group(1).split("#", 1)[0] + "#" + entry["id"]
        return '<a href="' + link + '">' + m.group(2) + "</a>"

    edited = CITATION_LINK.sub(rewrite, raw)
    if bad:
        raise RuntimeError("Citas sin resolver en " + str(page.relative_to(DOCS)) + ": " + ", ".join(sorted(bad)))
    if edited != raw:
        page.write_text(edited, encoding="utf-8")
    return edited

# Enlaces inversos de las fichas y las notas restauradas desde las escenas
# editoriales. Las escenas mantienen texto y numeración originales.
BACKLINKS = defaultdict(dict)
for page in DOCS.rglob("index.html"):
    if page == DOCS / "bibliografia/index.html":
        continue
    raw = update_citations(page)
    anchors = list(BIB_LINK.finditer(raw))
    if not anchors:
        continue
    title_match = re.search(r'<title>(.*?)</title>', raw, flags=re.S)
    title = html.unescape(re.sub(r'<[^>]+>', "", title_match.group(1))) if title_match else page.parent.name
    title = title.removesuffix(" · BIBLILU")
    relative = page.relative_to(DOCS).as_posix()
    for m in anchors:
        entry_id = target_id(m.group(1))
        if not entry_id:
            continue
        # Si la cita está dentro de <li id="fn-N">, enlazar directamente
        # a la nota. En las fichas enlazar a la ficha completa.
        point = ""
        if relative.startswith("genesis/"):
            before = raw[:m.start()]
            opened = re.search(r'<li id="fn-(\d+)"[^>]*>(?:(?!</li>).)*$', before, flags=re.S)
            if opened:
                point = "#fn-" + opened.group(1)
        href = "../" + relative + point
        label = title + (" · nota " + point[4:] if point.startswith("#fn-") else "")
        BACKLINKS[entry_id][href] = label

def apa_html(apa):
    # La fuente del catálogo utiliza *cursivas*, no HTML, para que sea editable.
    content = html.escape(apa)
    content = re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", content)
    content = re.sub(
        r"https?://[^\s<]+",
        lambda m: '<a class="bib-external" href="' + m.group(0) + '" rel="noopener noreferrer" target="_blank">' + m.group(0) + "</a>",
        content,
    )
    return content

def sort_key(book):
    text = book["apa"].lstrip("*")
    # Primera palabra, apellido compuesto e iniciales; respetar autor corporativo
    # y ordenar títulos anónimos por su denominación.
    return norm(text.replace("*", ""))

display = sorted(BOOKS, key=sort_key)
rows = []
for item in display:
    aliases = ''.join(
        '<span class="bib-legacy-anchor" id="ref-' + str(n) + '" aria-hidden="true"></span>'
        for n in ([item["legacy"]] + ([3] if item["legacy"] == 19 else []))
    )
    backlinks = sorted(BACKLINKS.get(item["id"], {}).items(), key=lambda x: (x[1], x[0]))
    if backlinks:
        links = "".join(
            '<li><a href="' + html.escape(href, quote=True) + '">' + html.escape(label) + '</a></li>'
            for href, label in backlinks
        )
        use = '<details class="bib-uses"><summary>Utilizado en BIBLILU · ' + str(len(backlinks)) + ' referencia' + ('s' if len(backlinks) != 1 else '') + '</summary><ul>' + links + "</ul></details>"
    else:
        use = ""
    plain = item["apa"].replace("*", "")
    cats = "|".join(item["categories"])
    rows.append(
        '<article class="bib-item" id="' + item["id"] + '" data-search="' +
        html.escape(norm(plain), quote=True) + '" data-categories="' +
        html.escape(cats, quote=True) + '">' + aliases +
        '<p class="bib-reference">' + apa_html(item["apa"]) + '</p>' + use +
        "</article>"
    )

retired = '<div class="bib-retired-links" aria-label="Referencias históricas retiradas">' + ''.join(
    '<p class="bib-retired" id="ref-' + str(n) + '"><strong>Referencia retirada (n.º ' + str(n) + ').</strong> ' +
    html.escape(reason) + "</p>"
    for n, reason in RETIREMENTS.items()
) + "</div>"

topics = [
    "Todas las materias", "Estudios bíblicos", "Lenguas y lexicografía",
    "Historia y arqueología", "Cultura y naturaleza", "Textos y fuentes antiguas",
]
choices = "".join('<option value="' + html.escape(c) + '">' + html.escape(c) + "</option>" for c in topics)
main = (
    '<main id="contenido"><section class="section bibliography bib-apa7">'
    '<p class="eyebrow">LAS FUENTES</p><h1>Bibliografía</h1>'
    '<p class="intro">Fuentes citadas y consultadas para las escenas y los apéndices de BIBLILU. '
    'Referencias normalizadas conforme a APA 7.ª edición.</p>'
    '<p class="bib-count"><strong>' + str(len(BOOKS)) + '</strong> referencias · Orden alfabético</p>'
    '<div class="bib-controls"><div><label for="bibliography-search">Buscar autor, título, año o palabra clave</label>'
    '<input id="bibliography-search" type="search" autocomplete="off" placeholder="Buscar en la Bibliografía…"></div>'
    '<div><label for="bibliography-filter">Materia</label><select id="bibliography-filter">' + choices + '</select></div></div>'
    '<p id="bibliography-results" class="bib-result-count" aria-live="polite">' +
    str(len(BOOKS)) + ' referencias</p>'
    '<div class="bib-list" id="bibliography-list">' + ''.join(rows) + '</div>'
    '<p id="bibliography-empty" class="bib-empty" hidden>No hay referencias que coincidan con la búsqueda.</p>'
    + retired +
    '<p class="bib-method">Los enlaces «Utilizado en BIBLILU» reúnen las citas explícitas detectadas '
    'en las escenas y fichas disponibles. La ausencia de enlaces no implica que una obra no haya sido consultada.</p>'
    '</section></main>'
)

page = DOCS / "bibliografia/index.html"
raw = page.read_text(encoding="utf-8")
assert len(re.findall(r'<main id="contenido">', raw)) == 1
raw = re.sub(r'<main id="contenido">.*?</main>', lambda _: main, raw, count=1, flags=re.S)
raw = raw.replace('href="../assets/style.css"', 'href="../assets/style.css?v=bibliografia-apa7-20261120"')
raw = raw.replace("</head>", '<script src="../assets/bibliography.js?v=20261120" defer></script></head>', 1)
page.write_text(raw, encoding="utf-8")
print("Bibliografía APA 7 publicada:", len(BOOKS), "referencias,", sum(map(len, BACKLINKS.values())), "apariciones con enlaces inversos.")
