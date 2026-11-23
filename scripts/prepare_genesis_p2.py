#!/usr/bin/env python3
"""P2 BIBLILU: valida Génesis 25–50 y prepara vistas NO PUBLICADAS.

  python scripts/prepare_genesis_p2.py --structure
  python scripts/prepare_genesis_p2.py --check-source
  python scripts/prepare_genesis_p2.py --check-format
  python scripts/prepare_genesis_p2.py --build-draft

No descarga la fuente BES 2026 (lo hace import_bes_genesis.py). Exige
el fichero data/genesis_25_50_bes.json producido desde su USFM oficial.
Protege íntegramente las 15 escenas RVR1960 de Génesis 1–24.
Nunca escribe en docs/, en data/genesis.json ni en approved-pages/.
"""
from pathlib import Path
import html
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "editorial/catalogo-escenas-genesis-25-50.json"
SOURCE = ROOT / "data/genesis_25_50_bes.json"
FORMATTED_SOURCE = ROOT / "data/genesis_25_50_bes_formato.json"
OLD_INDEX = ROOT / "editorial/approved-pages/genesis/index.html"
PREVIEW = ROOT / "build/p2"
PARAGRAPH_PLAN = ROOT / "editorial/p2-parrafos-genesis-25-50.json"
LENGTHS = {
    25:34,26:35,27:46,28:22,29:35,30:43,31:55,32:32,33:20,
    34:31,35:29,36:43,37:36,38:30,39:23,40:23,41:57,42:38,
    43:34,44:34,45:28,46:34,47:31,48:22,49:33,50:26
}
KINDS = {"plain", "speech", "divine", "thought"}


PROSE_CSS = """
/* Únicamente en borradores P2; el sitio publicado conserva su CSS original. */
.reader .verses .prose-paragraph {
  display: block;
  margin: 0 0 1.38em;
  line-height: 1.86;
  text-wrap: pretty;
}
.reader .verses .prose-paragraph.poetic-paragraph { margin-bottom: 1.28em; }
.reader .verses .verse-inline {
  display: inline;
  scroll-margin-top: 4rem;
  border-radius: .13em;
}
.reader .verses .verse-inline:target {
  background: #e9eedf;
  box-shadow: 0 0 0 3px #e9eedf;
}
.reader .verses .verse-inline .verse-num {
  white-space: nowrap;
  vertical-align: super;
  font-size: 10px;
  line-height: 0;
  margin-left: .12em;
  margin-right: .2em;
  text-decoration: none;
}
.reader .verses .prose-paragraph .speech,
.reader .verses .prose-paragraph .thought { font-style: italic; }
/* Cada intervención con raya comienza en una línea propia, como en prosa moderna.
   Se usa un salto HTML real para mantener la raya y todo el discurso
   siguiente en la MISMA línea. */
.reader .verses .p2-dialogue-break,
.reader .verses .p2-narrative-break { line-height: inherit; }
/* Inciso del narrador cuando el MISMO interlocutor reanuda su parlamento. */
.reader .verses .p2-inline-narrator-mark::before {
  content: "— ";
  font-style: normal;
}
/* Raya editorial de diálogo; aparece SOLO al comenzar un parlamento, no por versículo. */
.reader .verses .p2-spoken-dash {
  font-style: normal;
  white-space: nowrap;
  letter-spacing: 0;
}
.reader .verses .p2-quote-omitted { display: none; }
.reader .verses .prose-paragraph em.speech { color: inherit; }
/* El color de .divine y el control de ocultar colores los aporta style.css. */
.reader .verses .prose-paragraph em.thought { color: inherit; }
@media(max-width:700px) {
  .reader .verses .prose-paragraph { margin-bottom: 1.25em; }
  .reader .verses .verse-inline { scroll-margin-top: 5rem; }
}
@media print {
  .reader .verses .prose-paragraph { orphans: 2; widows: 2; }
}
"""

def error(message):
    raise SystemExit("P2: " + message)


def ref(chapter, verse):
    return (chapter, verse)


def fmt(point):
    return str(point["capitulo"]) + ":" + str(point["versiculo"])


def all_refs():
    return [(chapter, verse)
            for chapter, length in LENGTHS.items()
            for verse in range(1, length + 1)]


def structure():
    raw = json.loads(CATALOG.read_text(encoding="utf-8"))
    scenes = raw["escenas"]
    expected = all_refs()
    assert len(expected) == 874, "Recuento canónico inesperado"
    assert len(scenes) == 19, "P1 debe contener 19 escenas"
    assert [s["numero"] for s in scenes] == list(range(16, 35)), "Numeración no continua"
    coverage = []
    routes = set()
    first_chapters = set()
    chapters = {}
    for s in scenes:
        start = ref(s["inicio"]["capitulo"], s["inicio"]["versiculo"])
        end = ref(s["fin"]["capitulo"], s["fin"]["versiculo"])
        segment = [v for v in expected if start <= v <= end]
        assert len(segment) == s["versiculos"], ("Conteo incompatible", s["titulo"])
        assert segment, ("Escena vacía", s["titulo"])
        first = start[0] not in first_chapters
        route = str(start[0]) if first and start[1] == 1 else str(start[0]) + "-" + str(start[1])
        assert route not in routes, ("Ruta duplicada", route)
        first_chapters.add(start[0])
        routes.add(route)
        s["ruta_p2"] = route
        coverage.extend(segment)
        for point in segment:
            chapters.setdefault(point[0], {}).setdefault("start", s)
        if not str(s["titulo"]).strip():
            error("Título sin asignar")
    assert coverage == expected, "Hueco, solapamiento o cambio de orden en P1"
    assert sum(s["versiculos"] for s in scenes) == 874
    assert raw["versiculos_totales"] == 1533
    validate_paragraph_plan(scenes, expected)
    return raw, scenes, expected, chapters


def validate_paragraph_plan(scenes, expected):
    """Validar cortes editoriales sin reconstruir ni reescribir el texto bíblico."""
    if not PARAGRAPH_PLAN.is_file():
        error("falta el plan editorial P2 de párrafos")
    plan = json.loads(PARAGRAPH_PLAN.read_text(encoding="utf-8"))
    if plan.get("edicion") != "BES 2026" or len(plan.get("escenas", [])) != 19:
        error("plan de párrafos BES inválido")
    by_number = {row["numero"]: row for row in plan["escenas"]}
    if len(by_number) != 19:
        error("escenas duplicadas en el plan de párrafos")
    indices = {c + ":" + v: i for i, (c, v) in enumerate(
        (str(c), str(v)) for c,v in expected
    )}
    total = 0
    for scene in scenes:
        number = scene["numero"]
        if number not in by_number:
            error("falta plan de párrafos para escena " + str(number))
        row = by_number[number]
        begin = fmt(scene["inicio"])
        end = fmt(scene["fin"])
        starts = row["limites_parrafo"]
        required = row["limites_obligatorios_recursos"]
        if not starts or starts[0] != begin or len(starts) != len(set(starts)):
            error("inicios de párrafo duplicados o incorrectos en escena " + str(number))
        if not set(required).issubset(set(starts)):
            error("falta límite obligatorio de mapa, árbol o imagen: escena " + str(number))
        keys = []
        for start in starts:
            if start not in indices:
                error("inicio de párrafo no canónico: " + start)
            keys.append(indices[start])
        first, last = indices[begin], indices[end]
        if keys != sorted(keys) or keys[0] != first or keys[-1] > last:
            error("párrafos fuera del pasaje o desordenados: escena " + str(number))
        lengths = [b-a for a,b in zip(keys, keys[1:] + [last + 1])]
        if any(length < 1 or length > 12 for length in lengths):
            error("párrafo vacío o excesivamente largo: escena " + str(number))
        total += len(starts)
    return by_number, total


def prose_paragraphs(scene, verses, paragraph_plan):
    """Un <p> real por unidad narrativa; ancla inline por cada versículo."""
    start_refs = set(paragraph_plan[scene["numero"]]["limites_parrafo"])
    chunks = []
    group = []
    for verse in verses:
        r = str(verse["chapter"]) + ":" + str(verse["verse"])
        if r in start_refs:
            if group:
                chunks.append(group)
            group = []
        if not group and r not in start_refs:
            error("párrafo no delimitado en Gn " + r)
        group.append(verse)
    if group:
        chunks.append(group)
    if sum(len(g) for g in chunks) != len(verses):
        error("el renderizado por párrafos ha omitido algún versículo")
    def render(group):
        first = group[0]
        reference = str(first["chapter"]) + ":" + str(first["verse"])
        poetic = scene["numero"] == 33 and first["chapter"] == 49 and 3 <= first["verse"] <= 27
        css = "prose-paragraph poetic-paragraph" if poetic else "prose-paragraph"
        return ('<p class="' + css + '" data-start="' + reference + '">' +
                " ".join(verse_html(verse, first_in_paragraph=(idx == 0),
                                    prior_spoken_ended=(idx > 0 and
                                        ends_with_oral_closure(group[idx - 1])))
                         for idx, verse in enumerate(group)) + '</p>')
    return "".join(render(group) for group in chunks)


def check_source(expected):
    if not SOURCE.is_file():
        error("no existe data/genesis_25_50_bes.json. "
              "Se necesita importar el paquete oficial BES 2026 "
              "desde eBible; no se sustituirá ni inventará el texto.")
    verses = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(verses, list) or len(verses) != len(expected):
        error("la fuente debe contener exactamente 874 versículos ordenados")
    for n, ((c, v), item) in enumerate(zip(expected, verses)):
        if not isinstance(item, dict):
            error("versículo no es un objeto JSON: posición " + str(n))
        if (item.get("chapter"), item.get("verse")) != (c, v):
            error("ausencia, duplicación o desorden en " + str(c) + ":" + str(v))
        if "source_label" in item and item["source_label"] != str(c) + "-" + str(v):
            error("source_label contradictorio en " + str(c) + ":" + str(v))
        text = item.get("text")
        if not isinstance(text, str) or not text.strip() or "<" in text or ">" in text:
            error("texto vacío o con HTML incorporado en " + str(c) + ":" + str(v))
        if re.search(r'\|[a-zA-Z][a-zA-Z0-9-]*="', text) or re.search(r'\\[a-zA-Z]+', text):
            error("marcador USFM o atributo léxico sin limpiar en " + str(c) + ":" + str(v))
        if "parts" in item:
            pieces = item["parts"]
            if not isinstance(pieces, list) or not pieces:
                error("lista parts inválida en " + str(c) + ":" + str(v))
            if any(not isinstance(p, dict)
                   or p.get("kind") not in KINDS
                   or not isinstance(p.get("text"), str)
                   for p in pieces):
                error("partes de texto inválidas en " + str(c) + ":" + str(v))
            if "".join(p["text"] for p in pieces) != text:
                error("el marcado modifica el texto en " + str(c) + ":" + str(v))
        if "revisado" in item and type(item["revisado"]) is not bool:
            error("revisado debe ser booleano en " + str(c) + ":" + str(v))
    return verses


def check_format(expected, original):
    if not FORMATTED_SOURCE.is_file():
        error("falta el marcado BES: ejecutar scripts/marcar_dialogos_bes_p2.py")
    marked = json.loads(FORMATTED_SOURCE.read_text(encoding="utf-8"))
    if len(marked) != len(original):
        error("el marcado debe contener exactamente 874 versículos")
    for i, (m, o) in enumerate(zip(marked, original)):
        if (m.get("chapter"), m.get("verse")) != (o["chapter"], o["verse"]):
            error("marcado fuera de orden en la posición " + str(i))
        if m.get("text") != o["text"]:
            error("marcado altera texto BES en Génesis " + str(o["chapter"]) +
                  ":" + str(o["verse"]))
        parts = m.get("parts")
        if not isinstance(parts, list) or not parts:
            error("versículo sin partes formateadas: " + str((m["chapter"], m["verse"])))
        if any(p.get("kind") not in KINDS for p in parts):
            error("tipo de marcado no reconocido en " + str((m["chapter"], m["verse"])))
        if "".join(p["text"] for p in parts) != o["text"]:
            error("marcado no reversible en " + str((m["chapter"], m["verse"])))
        if m.get("revisado") is not False:
            error("el marcado automático no puede declararse revisado")
    return marked


def esc(value):
    return html.escape(str(value), quote=True)


# El nombre divino es un criterio visual distinto de la voz divina.
# BES capitaliza "Dios" y "Señor" para referirse a Dios; el caso 43:20
# es una fórmula de tratamiento a un funcionario egipcio, no nombre divino.
# No resaltar "señor" humano ni "dioses" / "dios" de religiones ajenas.
DIVINE_NAMES_RE = re.compile(r"\b(?:Dios|Señor)\b")
NON_DIVINE_NAME_REFS = {(43, 20, "Señor")}


def name_highlights(text, chapter, verse, inside_divine=False):
    if inside_divine:
        return esc(text)
    result = []
    previous = 0
    for match in DIVINE_NAMES_RE.finditer(text):
        token = match.group(0)
        result.append(esc(text[previous:match.start()]))
        if (chapter, verse, token) in NON_DIVINE_NAME_REFS:
            result.append(esc(token))
        else:
            result.append('<span class="divine">' + esc(token) + '</span>')
        previous = match.end()
    result.append(esc(text[previous:]))
    return "".join(result)


# La BES original se mantiene INALTERADA en data/*.json.
# En la visualización se sustituyen solo las comillas EXTERNAS « »:
# - discurso oral humano / divino: apertura « -> raya — ; cierre » -> nada
# - pensamiento / frase hipotética: apertura y cierre quedan ocultos, SIN raya
# Las comillas interiores “ ” y ‘ ’ se conservan como citas dentro del parlamento.
# Cada sustitución expone data-source-char para hacer reversible el HTML.
# Continuaciones del MISMO personaje separadas por una acotación en BES.
# Ordinal = apertura de comillas « en el versículo (no citas “ ” internas).
# Se revisaron los 37 pares de intervenciones de un mismo versículo.
SAME_SPEAKER_CONTINUATIONS = {(27, 36, 2), (43, 29, 2), (45, 4, 2)}
ORAL_KINDS = {"speech", "divine"}
DIALOGUE_BREAK = '<br class="p2-dialogue-break" aria-hidden="true">'
NARRATIVE_BREAK = '<br class="p2-narrative-break" aria-hidden="true">'


def starts_with_spoken_quote(item):
    """El texto del versículo abre directamente un parlamento (sin narración previa)."""
    parts = item.get("parts") or [{"kind": "plain", "text": item["text"]}]
    return bool(parts and parts[0]["kind"] in ORAL_KINDS and
                parts[0]["text"].startswith("«"))


def same_speaker_positions(item):
    """Aperturas que RETOMAN la misma voz tras una acotación, sin línea nueva.

    Las tres BES están documentadas editorialmente. Una acotación clásica
    entre comas (», dijo Fabián, «) se reconoce también sin cambiar la fuente.
    """
    result = set()
    text = item["text"]
    for number, match in enumerate(re.finditer("«", text), 1):
        position = match.start()
        ref = (item["chapter"], item["verse"], number)
        # Buscar el cierre anterior ANTES de clasificar esta apertura.
        previous_close = text.rfind("»", 0, position)
        interlude = text[previous_close + 1:position] if previous_close >= 0 else ""
        if ref in SAME_SPEAKER_CONTINUATIONS or (
            previous_close >= 0 and re.fullmatch(
                r"\s*,\s*(?:dijo|preguntó|añadió|comentó|respondió)\b[^«»]{1,85},\s*",
                interlude, flags=re.I
            )
        ):
            result.add(position)
    return result


def ends_with_oral_closure(item):
    """El último acto del verso fue terminar un diálogo, no una acción narrada."""
    parts = item.get("parts") or [{"kind": "plain", "text": item["text"]}]
    for i in range(len(parts) - 1, -1, -1):
        last = parts[i]["text"].rfind("»")
        if last >= 0:
            tail = parts[i]["text"][last + 1:] + "".join(
                p["text"] for p in parts[i + 1:]
            )
            return parts[i]["kind"] in ORAL_KINDS and (
                not tail.strip(" \t\n.,;:!?…")
            )
    return False


def display_piece(text, chapter, verse, kind, source_offset=0,
                  inline_positions=frozenset()):
    chunks = []
    buffer = []

    def flush():
        if buffer:
            chunks.append(name_highlights(
                "".join(buffer), chapter, verse, inside_divine=kind == "divine"
            ).replace("\n", " "))
            buffer.clear()

    for pos, char in enumerate(text):
        if char in "«»" and kind in ("speech", "divine", "thought"):
            flush()
            if char == "«" and kind != "thought":
                offset = source_offset + pos
                if offset > 0 and offset not in inline_positions:
                    chunks.append(DIALOGUE_BREAK)
                chunks.append('<span class="p2-spoken-dash" data-source-char="«">— </span>')
            else:
                chunks.append('<span class="p2-quote-omitted" data-source-char="' +
                              char + '"></span>')
        else:
            buffer.append(char)
    flush()
    return "".join(chunks)


def rendered_text(item):
    """Restituir estilo novelístico y poder recuperar literalmente la BES."""
    parts = item.get("parts") or [{"kind": "plain", "text": item["text"]}]
    if "".join(p["text"] for p in parts) != item["text"]:
        error("el formato altera la fuente BES en " +
              str(item["chapter"]) + ":" + str(item["verse"]))
    inline_positions = same_speaker_positions(item)
    offsets = []
    offset = 0
    for part in parts:
        offsets.append(offset)
        offset += len(part["text"])
    out = []
    for i, p in enumerate(parts):
        kind = p["kind"]
        begins_after_speech = (
            kind == "plain" and i > 0 and parts[i - 1]["kind"] in ORAL_KINDS
            and parts[i - 1]["text"].endswith("»")
        )
        if begins_after_speech:
            # Conservar el punto/coma que la BES coloca FUERA de las comillas
            # en la misma línea que el parlamento. La narración comienza
            # inmediatamente en la línea siguiente, salvo inciso del mismo.
            m = re.match(r"^([.,;:!?…]*\s*)([^\s.,;:!?…][\s\S]*)$", p["text"])
            if m:
                prefix, narrative = m.group(1), m.group(2)
                next_idx = i + 1
                inline_incise = (
                    next_idx < len(parts)
                    and parts[next_idx]["kind"] in ORAL_KINDS
                    and parts[next_idx]["text"].startswith("«")
                    and offsets[next_idx] in inline_positions
                )
                marker = (
                    '<span class="p2-inline-narrator-mark" aria-hidden="true"></span>'
                    if inline_incise else NARRATIVE_BREAK
                )
                value = (name_highlights(prefix, item["chapter"], item["verse"]) +
                         marker +
                         name_highlights(narrative, item["chapter"], item["verse"]))
            else:
                value = display_piece(p["text"], item["chapter"], item["verse"],
                                      kind, offsets[i], inline_positions)
        else:
            value = display_piece(p["text"], item["chapter"], item["verse"],
                                  kind, offsets[i], inline_positions)
        if kind == "divine":
            out.append('<em class="speech"><span class="divine">' + value + "</span></em>")
        elif kind == "speech":
            out.append('<em class="speech">' + value + "</em>")
        elif kind == "thought":
            out.append('<em class="thought">' + value + "</em>")
        else:
            out.append(value)
    return "".join(out)


def verse_html(item, first_in_paragraph=True, prior_spoken_ended=False):
    c, v = item["chapter"], item["verse"]
    anchor = "gn-" + str(c) + "-" + str(v)
    label = str(c) + ":" + str(v) if v == 1 else str(v)
    # Poner el número del verso y las palabras en la MISMA línea nueva.
    # No duplicar el salto al empezar un párrafo.
    prefix = (DIALOGUE_BREAK if not first_in_paragraph and
              (starts_with_spoken_quote(item) or prior_spoken_ended) else "")
    return (prefix + '<span class="verse-inline" id="' + anchor +
            '"><a class="verse-num" href="#' + anchor +
            '" aria-label="Génesis ' + str(c) + ":" + str(v) + '">' +
            label + "</a> " + rendered_text(item) + "</span>")


def make_scene_html(s, verses, scenes):
    n = s["numero"]
    i = n - 16
    prev = ("../24/index.html" if i == 0 else
            "../" + scenes[i-1]["ruta_p2"] + "/index.html")
    nxt = ("../" + scenes[i+1]["ruta_p2"] + "/index.html"
           if i+1 < len(scenes) else "../index.html")
    previous_title = "Familia" if i == 0 else scenes[i-1]["titulo"]
    next_title = scenes[i+1]["titulo"] if i+1 < len(scenes) else "Índice de escenas"
    controls = "".join('<option value="../' + s2["ruta_p2"] + '/index.html"' +
                       (' selected' if s2["numero"] == n else "") + '>' +
                       str(s2["numero"]) + " · " + esc(s2["titulo"]) +
                       "</option>" for s2 in scenes)
    plan, _ = validate_paragraph_plan(scenes, all_refs())
    body = prose_paragraphs(s, verses, plan)
    return ('''<!doctype html><html lang="es-ES"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>''' + esc(s["titulo"]) + ''' · Génesis · BIBLILU [BORRADOR P2]</title>
<link rel="stylesheet" href="../../assets/style.css">
<link rel="stylesheet" href="../../assets/p2-prose.css">
<script src="../../assets/app.js" defer></script>
</head><body data-base="../../" class="reader v05-scene">
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="header"><a class="brand" href="../../index.html">BIBLILU<span>LA BIBLIA ILUSTRADA</span></a>
<nav><a href="../index.html">Génesis</a><a href="../../apendices/index.html">Apéndices</a></nav></header>
<main id="contenido"><div class="reader-heading">
<p class="crumb"><a href="../index.html">Génesis</a> / Escena ''' + str(n) + '''</p>
<p class="eyebrow">GÉNESIS · ESCENA ''' + str(n) + ''' · BORRADOR P2 NO PUBLICADO</p>
<h1>''' + esc(s["titulo"]) + '''</h1>
<p class="subtitle">La Biblia en Español Sencillo 2026 (BES) · Génesis ''' + fmt(s["inicio"]) + "–" + fmt(s["fin"]) + '''</p>
<div class="reader-tools"><label>Escena <select id="chapter-select">''' +
            controls + '''</select></label></div></div>
<div class="reading-layout"><article class="verses">''' + body + '''</article>
<aside class="reading-art"><p class="source-note">Maqueta P2: recursos gráficos, notas y vínculos a fichas pendientes de las fases posteriores.</p></aside></div>
</main><nav class="chapter-nav"><a href="''' + prev + '">← ' + esc(previous_title) +
            '</a><a href="' + nxt + '">' + esc(next_title) +
            ''' →</a></nav><footer><a class="brand" href="../../index.html">BIBLILU</a>
<p>Borrador editorial. No publicado.</p></footer></body></html>''')


def append_cards(index, marker, cards):
    pos = index.find(marker)
    if pos < 0:
        error("marcador de índice no localizado: " + marker)
    begin = index.find('<div class="chapter-grid">', pos)
    if begin < 0:
        error("rejilla del índice no localizada: " + marker)
    # La rejilla tradicional contiene 26 <div class="pending"> anidados.
    # Buscar su cierre REAL, no el primer </div> de una tarjeta pendiente.
    depth = 0
    end = None
    for match in re.finditer(r"</?div\b[^>]*>", index[begin:], flags=re.I):
        if match.group(0).lower().startswith("</div"):
            depth -= 1
            if depth == 0:
                end = begin + match.start()
                break
        else:
            depth += 1
    if end is None:
        error("cierre del índice equilibrado no localizado")
    return index[:end] + cards + index[end:]


def index_html(scenes, expected):
    base = OLD_INDEX.read_text(encoding="utf-8")
    cards = "".join(
        '<a href="' + s["ruta_p2"] + '/index.html"><b>' +
        str(s["numero"]).zfill(2) + "</b><span>" + esc(s["titulo"]) +
        "</span><small>Gn " + fmt(s["inicio"]) + "–" + fmt(s["fin"]) +
        "</small>↗</a>" for s in scenes)
    base = append_cards(base, "ÍNDICE PRINCIPAL", cards)
    byverse = {}
    for s in scenes:
        a = (s["inicio"]["capitulo"], s["inicio"]["versiculo"])
        b = (s["fin"]["capitulo"], s["fin"]["versiculo"])
        for point in expected:
            if a <= point <= b:
                byverse[point] = s
    chapter_cards = ""
    for c in LENGTHS:
        first = byverse[(c, 1)]
        subsequent = [s["numero"] for s in scenes
                      if s["inicio"]["capitulo"] == c and s["inicio"]["versiculo"] > 1]
        further = ("<small>Continúa en escena" + ("s " if len(subsequent)>1 else " ") +
                   ", ".join(str(n) for n in subsequent) + "</small>") if subsequent else ""
        chapter_cards += ('<a href="' + first["ruta_p2"] + '/index.html#gn-' +
                          str(c) + '-1"><b>' + str(c).zfill(2) +
                          '</b><span>Génesis ' + str(c) + '</span>' + further + '↗</a>')
    base = append_cards(base, "ÍNDICE TRADICIONAL", chapter_cards)
    # El índice histórico reserva 25–50 como "Próximamente"; al añadir
    # esos capítulos reales, quitar los 26 marcadores caducados.
    base = re.sub(r'<div class="pending">.*?</div>', "", base, flags=re.S)
    base = base.replace("<h2>Escenas del manuscrito</h2>", "<h2>Escenas del manuscrito</h2><p><strong>Traducciones:</strong> escenas 1–15 RVR1960; escenas 16–34 BES 2026. Migración de las primeras quince escenas reservada para la Etapa II.</p>")
    base = base.replace("Quince escenas disponibles · Génesis 1–24",
                        "34 escenas previstas · Génesis 1–24: RVR1960 · Génesis 25–50: BES 2026 · PREVISUALIZACIÓN P2")
    # Versión mixta inequívoca también en el pie de página.
    base = base.replace("Español · RVR 1960",
                        "Español · escenas 1–15 RVR1960 / 16–34 BES 2026")
    base = base.replace("</head>", '<meta name="robots" content="noindex,nofollow"></head>', 1)
    return base


def preview_stub(title, body, back, asset_prefix="", back_label="Volver al índice"):
    """Páginas informativas, SIN duplicar la RVR1960 ni inventar escenas."""
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex,nofollow">'
            '<link rel="stylesheet" href="' + asset_prefix +
            'assets/style.css"><title>' + esc(title) + ' · BIBLILU [BORRADOR]</title>'
            '</head><body><main class="section" style="max-width:800px;margin:5rem auto">'
            '<h1>' + esc(title) + '</h1><p>' + esc(body) + '</p>'
            '<p><a href="' + back + '">' + esc(back_label) + '</a></p>'
            '</main></body></html>')


def legacy_bridge_pages():
    """Enlaces válidos para la previsualización, sin copiar texto RVR1960.

    Se extrae el mapa de 15 escenas y las primeras anclas de capítulos
    de la fuente editorial previa; no se reescribe ninguno de sus archivos.
    """
    content = OLD_INDEX.read_text(encoding="utf-8")
    grids = re.findall(r'<div class="chapter-grid">(.*?)</div>', content, flags=re.S)
    if len(grids) != 2:
        error("no se encuentran los dos índices antiguos para los puentes")
    old_scenes = re.findall(
        r'<a href="([^"]+/index.html)"><b>\d+</b><span>(.*?)</span>',
        grids[0], flags=re.S
    )
    if len(old_scenes) != 15:
        error("el índice anterior no contiene exactamente 15 escenas")
    chapter_anchors = re.findall(
        r'href="([^"]+/index.html)#(gn-\d+-1)"', grids[1]
    )
    if len(chapter_anchors) != 24:
        error("se esperan 24 anclas iniciales del índice antiguo")
    by_route = {}
    for relative, anchor in chapter_anchors:
        by_route.setdefault(relative, []).append(anchor)
    for relative, title in old_scenes:
        route = relative.removesuffix("/index.html")
        page = PREVIEW/"genesis"/route/"index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        original_url = "https://github.com/alextorurdi/biblilu/blob/main/docs/genesis/" + relative
        labels = "".join('<span id="' + anchor + '"></span>' for anchor in
                         by_route.get(relative, []))
        body = ('La escena RVR1960 «' + html.unescape(title) + '» ya está '
                'publicada, pero no se reproduce en este ZIP de trabajo BES. '
                'Este enlace es un puente informativo, no la escena bíblica.')
        page.write_text(
            preview_stub(title, body, "../index.html", asset_prefix="../../").replace(
                "</main>", labels +
                '<p><a href="' + original_url +
                '">Consultar el archivo publicado en GitHub</a></p></main>'
            ), encoding="utf-8"
        )


def preview_support_pages():
    pages = {
        "index.html": ("BIBLILU · vista previa BES",
                       "Previsualización local no publicada. Las escenas RVR1960 originales permanecen en el sitio publicado.",
                       "genesis/index.html"),
        "apendices/index.html": ("Apéndices de BIBLILU",
                       "Los apéndices pertenecen a la web publicada. Las referencias BES se incorporarán después de P3.",
                       "../genesis/index.html"),
        "bibliografia/index.html": ("Bibliografía de BIBLILU",
                       "La bibliografía del proyecto se mantiene en la web publicada.",
                       "../genesis/index.html"),
        "sobre/index.html": ("Créditos de BIBLILU",
                       "La información general del proyecto se mantiene en la web publicada.",
                       "../genesis/index.html"),
    }
    for relative, (title, body, back) in pages.items():
        page = PREVIEW/relative
        page.parent.mkdir(parents=True, exist_ok=True)
        asset_prefix = "../" * (len(page.relative_to(PREVIEW).parts) - 1)
        content = preview_stub(title, body, back, asset_prefix)
        if relative == "index.html":
            content = content.replace("</main>", '<span id="libros"></span></main>')
        page.write_text(content, encoding="utf-8")


def build_draft(raw, scenes, expected, verses):
    if PREVIEW.exists():
        shutil.rmtree(PREVIEW)
    (PREVIEW/"genesis").mkdir(parents=True)
    for s in scenes:
        start = ref(s["inicio"]["capitulo"], s["inicio"]["versiculo"])
        end = ref(s["fin"]["capitulo"], s["fin"]["versiculo"])
        sample = [item for item in verses if start <= ref(item["chapter"], item["verse"]) <= end]
        page = PREVIEW/"genesis"/s["ruta_p2"]/"index.html"
        page.parent.mkdir(parents=True,exist_ok=True)
        page.write_text(make_scene_html(s, sample, scenes), encoding="utf-8")
    (PREVIEW/"genesis"/"index.html").write_text(index_html(scenes, expected),encoding="utf-8")
    legacy_bridge_pages()
    preview_support_pages()
    assets = PREVIEW/"assets"
    assets.mkdir()
    (assets/"p2-prose.css").write_text(PROSE_CSS, encoding="utf-8")
    for name in ("style.css","app.js","favicon.svg","eden.jpg"):
        src = ROOT/"docs"/"assets"/name
        if src.exists():
            shutil.copyfile(src, assets/name)
    validation = {
        "fase": "P2", "estado": "borrador_no_publicado", "escenas": len(scenes),
        "versiculos": len(verses),
        "parrafos": sum(len(validate_paragraph_plan(scenes, expected)[0][s["numero"]]["limites_parrafo"]) for s in scenes),
        "traduccion": "BES 2026",
        "formato": "borrador_automatico_pendiente_revision",
        "con_formato_revisado": sum(1 for x in verses if x.get("revisado") is True),
        "sin_formato_revisado": sum(1 for x in verses if x.get("revisado") is not True),
        "advertencia": "No usar estas páginas como fuentes aprobadas ni publicar automáticamente."
    }
    (PREVIEW/"validacion.json").write_text(json.dumps(validation,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Previsualización generada en build/p2 (NO PUBLICADA):", len(scenes),
          "escenas,",len(verses),"versículos.")


def main():
    mode = sys.argv[1] if len(sys.argv) == 2 else "--help"
    if mode not in ("--structure","--check-source","--check-format","--build-draft"):
        error("uso: --structure | --check-source | --check-format | --build-draft")
    raw, scenes, expected, _ = structure()
    if mode == "--structure":
        print("P1 válido:",len(scenes),"escenas,",len(expected),
              "versículos, 26 capítulos; rutas sin solapamientos.")
        for s in scenes:
            print(str(s["numero"]), s["ruta_p2"], s["titulo"],
                  fmt(s["inicio"])+"–"+fmt(s["fin"]))
        return
    verses = check_source(expected)
    if mode == "--check-source":
        print("Fuente íntegra:",len(verses),"versículos; textos y marcas consistentes.")
        return
    marked = check_format(expected, verses)
    if mode == "--check-format":
        print("Formato reversible validado:",len(marked),
              "versículos; texto BES intacto; todo pendiente de aprobación editorial.")
        return
    build_draft(raw, scenes, expected, marked)


if __name__ == "__main__":
    main()
