#!/usr/bin/env python3
"""Prueba sin Biblia: 874 textos sintéticos para verificar P2 sin copyright."""
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prepare_genesis_p2",
                                              ROOT / "scripts/prepare_genesis_p2.py")
p2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p2)

catalog, scenes, expected, _ = p2.structure()
assert len(expected) == 874
assert len(scenes) == 19
assert expected[0] == (25, 1)
assert expected[-1] == (50, 26)
assert scenes[0]["ruta_p2"] == "25"
assert scenes[-1]["ruta_p2"] == "50"
assert scenes[14]["titulo"] == "Hambre"
assert scenes[14]["versiculos"] == 121

with TemporaryDirectory(prefix="biblilu-p2-test-") as directory:
    base = Path(directory)
    source = base / "genesis_25_50.json"
    p2.SOURCE = source
    p2.PREVIEW = base / "preview"
    verses = []
    for c, v in expected:
        t = "CONTENIDO SINTÉTICO DE PRUEBA " + str(c) + ":" + str(v)
        verses.append({"chapter": c, "verse": v, "text": t, "revisado": False})
    verses[0]["parts"] = [
        {"kind": "plain", "text": "CONTENIDO SINTÉTICO DE PRUEBA "},
        {"kind": "divine", "text": "25:1"}
    ]
    source.write_text(json.dumps(verses, ensure_ascii=False), encoding="utf-8")
    assert len(p2.check_source(expected)) == 874
    p2.build_draft(catalog, scenes, expected, verses)
    scene_paths = [p2.PREVIEW / "genesis" / s["ruta_p2"] / "index.html"
                   for s in scenes]
    assert all(path.is_file() for path in scene_paths)
    assert sum(path.read_text(encoding="utf-8").count('<span class="verse-inline" id="gn-')
               for path in scene_paths) == 874
    assert sum(path.read_text(encoding="utf-8").count('<p class="prose-paragraph')
               for path in scene_paths) == 387
    first = scene_paths[0].read_text(encoding="utf-8")
    assert 'id="gn-25-1"' in first
    assert 'data-start="25:1"' in first
    assert 'data-start="25:5"' in first
    assert 'id="gn-25-4"' in first
    assert 'class="verse-inline"' in first
    assert '<p class="verse"' not in first
    assert (p2.PREVIEW / "assets/p2-prose.css").is_file()
    assert 'Biblia en Español Sencillo 2026 (BES)' in first
    assert '<span class="divine">25:1</span>' in first
    last = scene_paths[-1].read_text(encoding="utf-8")
    assert 'id="gn-50-26"' in last
    assert '<p class="prose-paragraph' in last
    book_index = (p2.PREVIEW / "genesis/index.html").read_text(encoding="utf-8")
    assert 'href="25/index.html#gn-25-1"' in book_index
    assert 'href="50/index.html#gn-50-1"' in book_index
    assert book_index.count("Continúa en escena") >= 1
    assert 'noindex,nofollow' in book_index
    assert 'escenas 1–15 RVR1960; escenas 16–34 BES 2026' in book_index
    assert json.loads((p2.PREVIEW / "validacion.json").read_text(encoding="utf-8"))["versiculos"] == 874
    verses[0]["parts"][1]["text"] = "VERSÍCULO MODIFICADO"
    source.write_text(json.dumps(verses, ensure_ascii=False), encoding="utf-8")
    try:
        p2.check_source(expected)
    except SystemExit:
        pass
    else:
        raise AssertionError("El validador aceptó un marcado que cambia el texto")
print("OK: estructura, borradores, 874 anclas, dos índices y preservación del texto.")
