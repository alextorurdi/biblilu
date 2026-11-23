#!/usr/bin/env python3
"""P2 BIBLILU: valida Génesis 25–50 y prepara vistas NO PUBLICADAS.

  python scripts/prepare_genesis_p2.py --structure
  python scripts/prepare_genesis_p2.py --check-source
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
OLD_INDEX = ROOT / "editorial/approved-pages/genesis/index.html"
PREVIEW = ROOT / "build/p2"
LENGTHS = {
    25:34,26:35,27:46,28:22,29:35,30:43,31:55,32:32,33:20,
    34:31,35:29,36:43,37:36,38:30,39:23,40:23,41:57,42:38,
    43:34,44:34,45:28,46:34,47:31,48:22,49:33,50:26
}
KINDS = {"plain", "speech", "divine", "thought"}


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
    return raw, scenes, expected, chapters


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


def esc(value):
    return html.escape(str(value), quote=True)


def rendered_text(item):
    parts = item.get("parts") or [{"kind": "plain", "text": item["text"]}]
    out = []
    for p in parts:
        value = esc(p["text"]).replace("\n", " ")
        kind = p["kind"]
        if kind == "divine":
            out.append('<em class="speech"><span class="divine">' + value + "</span></em>")
        elif kind == "speech":
            out.append('<em class="speech">' + value + "</em>")
        elif kind == "thought":
            out.append('<em class="thought">' + value + "</em>")
        else:
            out.append(value)
    return "".join(out)


def verse_html(item):
    c, v = item["chapter"], item["verse"]
    anchor = "gn-" + str(c) + "-" + str(v)
    return ('<p class="verse" id="' + anchor +
            '"><a class="verse-num" href="#' + anchor +
            '" aria-label="Génesis ' + str(c) + ":" + str(v) + '">' +
            str(c) + ":" + str(v) + "</a> " + rendered_text(item) + "</p>")


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
    body = "".join(verse_html(item) for item in verses)
    return ('''<!doctype html><html lang="es-ES"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>''' + esc(s["titulo"]) + ''' · Génesis · BIBLILU [BORRADOR P2]</title>
<link rel="stylesheet" href="../../assets/style.css">
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
    end = index.find("</div>", begin)
    if end < 0:
        error("cierre de índice no localizado")
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
    base = base.replace("<h2>Escenas del manuscrito</h2>", "<h2>Escenas del manuscrito</h2><p><strong>Traducciones:</strong> escenas 1–15 RVR1960; escenas 16–34 BES 2026. Migración de las primeras quince escenas reservada para la Etapa II.</p>")
    base = base.replace("Quince escenas disponibles · Génesis 1–24",
                        "34 escenas previstas · Génesis 1–24: RVR1960 · Génesis 25–50: BES 2026 · PREVISUALIZACIÓN P2")
    base = base.replace("</head>", '<meta name="robots" content="noindex,nofollow"></head>', 1)
    return base


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
    assets = PREVIEW/"assets"
    assets.mkdir()
    for name in ("style.css","app.js","favicon.svg"):
        src = ROOT/"docs"/"assets"/name
        if src.exists():
            shutil.copyfile(src, assets/name)
    validation = {
        "fase": "P2", "estado": "borrador_no_publicado", "escenas": len(scenes),
        "versiculos": len(verses),
        "con_formato_revisado": sum(1 for x in verses if x.get("revisado") is True),
        "sin_formato_revisado": sum(1 for x in verses if x.get("revisado") is not True),
        "advertencia": "No usar estas páginas como fuentes aprobadas ni publicar automáticamente."
    }
    (PREVIEW/"validacion.json").write_text(json.dumps(validation,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Previsualización generada en build/p2 (NO PUBLICADA):", len(scenes),
          "escenas,",len(verses),"versículos.")


def main():
    mode = sys.argv[1] if len(sys.argv) == 2 else "--help"
    if mode not in ("--structure","--check-source","--build-draft"):
        error("uso: --structure | --check-source | --build-draft")
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
    build_draft(raw, scenes, expected, verses)


if __name__ == "__main__":
    main()
