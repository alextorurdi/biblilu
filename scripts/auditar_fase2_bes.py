#!/usr/bin/env python3
"""Auditoría integral y reproducible del borrador BES de Génesis 25–50.

Ejecutar DESPUÉS de scripts/prepare_genesis_p2.py --build-draft.
  python3 scripts/auditar_fase2_bes.py
  python3 scripts/auditar_fase2_bes.py --online

--online descarga solo en memoria la fuente USFM oficial, exige el SHA256
registrado y compara el texto íntegro de los 874 versículos con el importado.
No cambia textos bíblicos, fichas, escenas ni páginas públicas.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from urllib.request import urlopen, Request
import hashlib
import importlib.util
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build/p2"
REPORT = OUT / "auditoria-p2.json"
DOC = ROOT / "editorial"
SOURCE = ROOT / "data/genesis_25_50_bes.json"
FORMATTED = ROOT / "data/genesis_25_50_bes_formato.json"


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT/"scripts"/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p2 = load("p2_audit", "prepare_genesis_p2.py")
marker = load("marker_audit", "marcar_dialogos_bes_p2.py")
importer = load("importer_audit", "import_bes_genesis.py")


class Page(HTMLParser):
    """Recuperar texto BES exactamente desde HTML (sin su número de versículo)."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.current = None
        self.current_depth = None
        self.text = []
        self.ids = []
        self.verses = []
        self.paragraphs = 0
        self.links = []
        self.dashes = 0
        self.skip_separator = False

    def handle_starttag(self, tag, rawattrs):
        attrs = dict(rawattrs)
        css = set((attrs.get("class") or "").split())
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "p" and "prose-paragraph" in css:
            self.paragraphs += 1
        if "p2-spoken-dash" in css:
            self.dashes += 1
        for prop in ("href", "src"):
            if attrs.get(prop) is not None and tag in ("a", "link", "script", "img", "source"):
                self.links.append((tag, prop, attrs[prop]))
        if tag == "span" and "verse-inline" in css:
            if self.current is not None:
                raise AssertionError("ancla anidada")
            self.current = attrs["id"]
            self.current_depth = len(self.stack)
            self.text = []
            self.skip_separator = False
        ignore_parent = self.stack[-1][1] if self.stack else False
        ignore = (ignore_parent or "verse-num" in css or "data-source-char" in attrs)
        if self.current is not None and "data-source-char" in attrs and not ignore_parent:
            self.text.append(attrs["data-source-char"])
        if tag not in self.VOID:
            self.stack.append((tag, ignore, "verse-num" in css))

    def handle_endtag(self, tag):
        if not self.stack:
            return
        last_tag, ignore, verse_num = self.stack.pop()
        if last_tag != tag:
            raise AssertionError("HTML sin cierre estructural: " + str((tag,last_tag)))
        if verse_num:
            self.skip_separator = True
        if self.current is not None and len(self.stack) == self.current_depth:
            self.verses.append((self.current, "".join(self.text)))
            self.current = None
            self.current_depth = None

    def handle_data(self, data):
        if self.current is None or self.stack[-1][1]:
            return
        if self.skip_separator:
            if data.startswith(" "):
                data = data[1:]
            self.skip_separator = False
        self.text.append(data)


def parse_file(path):
    parser = Page()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    if parser.stack or parser.current:
        raise AssertionError("HTML malformado o versículo sin cierre: " + str(path))
    return parser


def ensure(condition, message):
    if not condition:
        raise AssertionError(message)


def audit_online(source, provenance):
    url = provenance["fuente_oficial"]
    with urlopen(Request(url, headers={"User-Agent":"BIBLILU P2/1.0 audit"}), timeout=50) as response:
        archive = response.read()
    actual_sha = hashlib.sha256(archive).hexdigest()
    ensure(actual_sha == provenance["sha256_zip"],
           "archivo BES oficial distinto del SHA256 fijado; revisión obligatoria")
    usfm_name, usfm = importer.find_book(archive)
    ensure(usfm_name == provenance["archivo_usfm_genesis"], "archivo GEN inesperado")
    parsed = importer.parse(usfm)
    for verse in source:
        c,v=verse["chapter"],verse["verse"]
        ensure(parsed[(c,v)] == verse["text"],
               "diferencia USFM/JSON en Gn " + str(c) + ":" + str(v))
    return {"fuente":url,"sha256":actual_sha,"archivo_genesis":usfm_name,
            "versiculos_comparados":len(source),"resultado":"identicos"}


def audit():
    online = "--online" in sys.argv[1:]
    ensure(all(arg=="--online" for arg in sys.argv[1:]),
           "opción admitida: --online")
    _, scenes, expected, _ = p2.structure()
    source = p2.check_source(expected)
    formatted = p2.check_format(expected, source)
    ensure(len(source)==len(formatted)==874,"cobertura BES incorrecta")
    on_disk = json.loads(FORMATTED.read_text(encoding="utf-8"))
    generated, opened, _, evidence = marker.annotate(source)
    ensure([v["parts"] for v in generated] == [v["parts"] for v in on_disk],
           "los roles de discurso no reproducen el marcado vigente")
    ensure(all(not v.get("revisado") for v in formatted),
           "no marcar revisado individualmente sin decisión editorial")
    ensure(opened["divine"]==14 and opened["thought"]==6,
           "conteo de atribuciones divinas/pensamientos distinto al aprobado")
    approved = {(r["ref"],r["apertura"]) for r in evidence if r["tipo"]=="divine"}
    ensure(len(approved)==14,"número de aperturas divinas inesperado")
    provenance=json.loads((DOC/"procedencia-bes-genesis-25-50.json").read_text(encoding="utf-8"))
    official = audit_online(source,provenance) if online else {
        "fuente":provenance["fuente_oficial"],
        "sha256_fijado":provenance["sha256_zip"],
        "estado":"sin descargar (usar --online para cotejar los 874 versículos)"}
    ensure(OUT.is_dir() and (OUT/"genesis/index.html").exists(),
           "crear borrador antes de auditarlo")

    all_pages = list(OUT.rglob("*.html"))
    parsed = {page:parse_file(page) for page in all_pages}
    index = OUT/"genesis/index.html"
    idx = parsed[index]
    index_text = index.read_text(encoding="utf-8")
    ensure('class="pending"' not in index_text,
           "índice contiene tarjetas Próximamente para capítulos 25–50")
    ensure("1–15 RVR1960" in index_text and "16–34 BES 2026" in index_text,
           "índice no distingue las dos traducciones")
    ensure("Español · RVR 1960" not in index_text,
           "pie de índice aún anuncia solo RVR1960")
    ensure(index_text.count('class="chapter-grid"') == 2, "faltan índices tradicionales")

    verse_map = {}
    unique = Counter()
    paragraphs = 0
    dashes = 0
    checked_scenes = []
    for scene in scenes:
        begin = (scene["inicio"]["capitulo"],scene["inicio"]["versiculo"])
        end=(scene["fin"]["capitulo"],scene["fin"]["versiculo"])
        v = [row for row in source if begin <= (row["chapter"],row["verse"]) <= end]
        page = OUT/"genesis"/scene["ruta_p2"]/"index.html"
        ensure(page in parsed,"falta página de escena "+str(scene["numero"]))
        observed = parsed[page]
        original = [(f'gn-{row["chapter"]}-{row["verse"]}',row["text"]) for row in v]
        ensure(observed.verses==original,
               "HTML no recupera literalmente el texto BES en escena "+str(scene["numero"]) +
               "; primer contraste="+str(next(((i,a,b) for i,(a,b) in
               enumerate(zip(observed.verses,original)) if a!=b),None)))
        for ref,text in observed.verses:
            unique[ref]+=1
            verse_map[ref]=scene["ruta_p2"]
        expected_paragraphs=len(next(x for x in json.loads(
            (DOC/"p2-parrafos-genesis-25-50.json").read_text(encoding="utf-8"))["escenas"]
            if x["numero"]==scene["numero"])["limites_parrafo"])
        ensure(observed.paragraphs==expected_paragraphs,
               "párrafos distintos en escena "+str(scene["numero"]))
        paragraphs+=observed.paragraphs
        dashes+=observed.dashes
        checked_scenes.append({"numero":scene["numero"],"ruta":scene["ruta_p2"],
                               "versiculos":len(v),"parrafos":observed.paragraphs})
    ensure(len(unique)==874 and set(unique.values())=={1},
           "anclas ausentes o duplicadas en las 19 escenas")
    ensure(paragraphs==387,"párrafos distintos de los 387 acordados")
    ensure(dashes==299,"aperturas de diálogo distintas de 299")
    ensure(len(list((OUT/"genesis").glob("*/index.html")))==34,
           "se esperan 19 escenas BES y 15 puentes RVR60")
    for ref in [f"gn-{c}-1" for c in range(25,51)]:
        ensure(ref in verse_map, "falta inicio de capítulo BES "+ref)

    # Todas las rutas y fragmentos del ZIP deben resolver a un archivo real.
    # Si una escena RVR60 no forma parte del ZIP, se utiliza una página
    # puente informativa, NO una reproducción o una nueva edición.
    bad_links=[]
    tested_links=0
    for page,document in parsed.items():
        ensure(len(document.ids)==len(set(document.ids)),
               "IDs repetidos en "+str(page.relative_to(OUT)))
        for _,_,href in document.links:
            split = urlsplit(href)
            if split.scheme or split.netloc or href.startswith("//") or href.startswith("mailto:"):
                continue
            local = unquote(split.path)
            target=(page.parent/local).resolve() if local else page.resolve()
            if target.is_dir():
                target=target/"index.html"
            if not target.exists() or not target.is_file():
                bad_links.append({"origen":str(page.relative_to(OUT)),
                                  "referencia":href,"problema":"archivo ausente"})
                continue
            if not target.is_relative_to(OUT.resolve()):
                bad_links.append({"origen":str(page.relative_to(OUT)),
                                  "referencia":href,"problema":"sale del ZIP"})
                continue
            tested_links+=1
            if split.fragment:
                dest = parsed[target].ids if target in parsed else []
                if unquote(split.fragment) not in dest:
                    bad_links.append({"origen":str(page.relative_to(OUT)),
                                      "referencia":href,"problema":"ancla ausente"})
    ensure(not bad_links,"enlaces internos rotos: "+json.dumps(bad_links[:18],ensure_ascii=False))

    # Las 450 rutas de las fichas antiguas constituyen el universo de
    # identificadores estables reutilizables. La correspondencia con nombres
    # BES debe determinarse por extracción en P3, sin fusiones automáticas.
    registry=json.loads((ROOT/"data/registro_maestro.json").read_text(encoding="utf-8"))
    entities=registry["entidades"]
    missing_registries=[{"id":x["id"],"ruta":x.get("ruta")} for x in entities
                        if not x.get("ruta") or not (ROOT/x["ruta"]).is_file()]
    ensure(not missing_registries,
           "registro de apéndices contiene rutas inexistentes: "+str(missing_registries[:12]))
    unique_ids=[e["id"] for e in entities]
    ensure(len(unique_ids)==len(set(unique_ids)), "registro contiene IDs duplicados")
    ensure(len(unique_ids)>=450,"faltan fichas históricas del registro")

    report={
      "fase":"P2","fecha":"2026-11-23",
      "modo":"integridad global y enlaces con cotejo USFM opcional",
      "estado":"controles_automaticos_superados",
      "edicion":"BES 2026",
      "cobertura":{"escenas_bes":len(scenes),"escenas_rvr_protegidas":15,
                   "versiculos_bes":len(source),"capitulos_bes":26,
                   "parrafos":paragraphs,"anclas_unicas":len(unique),
                   "rayas_de_dialogo":dashes,
                   "pensamientos_aper":opened["thought"],
                   "discursos_divinos_aper":opened["divine"]},
      "texto":{"formato_reversible":True,"fuente_completa":True,
               "marcas_coinciden_con_generador":True,"fuente_oficial":official,
               "marcado_individual_revisado":0,
               "observacion":"validación automática exhaustiva ≠ verificación humana de toda atribución"},
      "navegacion":{"paginas_html":len(all_pages),"enlaces_locales_verificados":tested_links,
                    "enlaces_rotos":bad_links,"indice_escenas":34,
                    "indice_tradicional":50,
                    "puentes_rvr60":"15 informativos; no duplican escenas ni reemplazan la web publicada"},
      "apendices":{"ids_existentes":len(entities),"ids_unicos":len(unique_ids),
                   "rutas_fichas_existentes":len(entities),
                   "menciones_bes":"por identificar en P3, sin inventar correspondencias"},
      "escenas":checked_scenes,
      "limites":["Pendiente P3: asignar entidades BES a IDs y enlazarlas.",
                 "Pendiente P6/P9: integración real de escenas con Gn 24 y apéndices.",
                 "Este informe no convierte 874 revisado=false en aprobación humana."],
      "publicacion":"no_publicado"
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("AUDITORÍA P2 BES COMPLETA:",
          len(source),"versículos exactos,",len(unique),"anclas,",
          paragraphs,"párrafos,",dashes,"rayas,",tested_links,
          "enlaces internos,",len(entities),"rutas de apéndices.")
    if online:
        print("USFM oficial cotejado íntegro: SHA256 y 874/874 versículos iguales.")
    return report


if __name__ == "__main__":
    audit()
