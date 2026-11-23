#!/usr/bin/env python3
"""Fase P3 BES 2026: primer barrido en un paso de las ocho categorías.

La salida es un INVENTARIO DE CANDIDATOS, nunca enlaces ni fichas aprobadas.
- Fuente inmutable: data/genesis_25_50_bes.json, capítulos 25–50 (874 versículos).
- Registro antiguo inmutable: data/registro_maestro.json (450 identificadores).
- Salidas: data/p3-extracciones-genesis-25-50.json,
           editorial/p3-resumen-genesis-25-50.json.
- No fusionar personas homónimas ni identificar clanes como individuos.
- Las formas BES que difieran de RVR1960 son candidatas a variantes, NO sinónimos aprobados.
"""
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
BES = ROOT/"data/genesis_25_50_bes.json"
REGISTRY = ROOT/"data/registro_maestro.json"
EXTRACTIONS = ROOT/"data/p3-extracciones-genesis-25-50.json"
SUMMARY = ROOT/"editorial/p3-resumen-genesis-25-50.json"
CATEGORIES = ["onomastico","lugares","animales","materiales","tribus","objetos","instrumentos","medidas"]

# Conflictos comprobados en el primer lote onomástico (Gn 25:1–18):
# hay una ficha con el mismo nombre, pero su identidad es OTRA.
# La fuente BES distingue el parentesco; nunca sugerir ese ID como enlace.
IDENTITY_CONFLICTS = {
    (25,9,"zohar"): {
        "excluir":"onomastico/zohar",
        "motivo":"Zohar padre de Efrón, no Zohar hijo de Simeón (Gn 46:10)"
    },
    (25,15,"hadad"): {
        "excluir":"onomastico/hadad-rey-de-edom",
        "motivo":"Hadad hijo de Ismael, no el rey edomita hijo de Bedad (Gn 36:35)"
    }
}
# Grafías alternativas de BES por estudiar: no están aprobadas como
# equivalencias de búsqueda ni como cambios de ID histórico.
TEXT_VARIANTS_PENDING = {
    (25,2,"zimran"): {
        "proponer":"onomastico/zimram",
        "motivo":"Zimrán en BES; ficha previa Zimram, hijo de Abraham y Cetura"
    }
}

# Son CANDIDATOS de lectura, no nuevas fichas ni identidades aprobadas.
# La atribución de clase procede del contexto del pasaje y queda pendiente de P3.
PROPOSED_TERMS = {
 "onomastico": (
   "Zimrán", "Hamor", "Hira", "Potifar", "Potifera", "Ahuzat", "Beeri",
   "Pérez", "Zafnat-panea", "Benoni", "Benjamín", "Jetro", "Elda",
   "Asenat", "Zifión", "Paltiel", "Efa", "Timna", "Zohar"
 ),
 "lugares": (
   "Padán-aram", "Gosén", "Betel", "Galaad", "Efrata", "Timnat",
   "Rehobot", "Peniel", "Sucot", "Belén", "Dotán", "Adulam",
   "Enaim", "Nilo", "Beer-lahai-roi", "Sur", "Esec", "Sitna",
   "On", "Luz", "Mahanaim", "Siquem", "Seir", "Egipto"
 ),
 "tribus": (
   "hititas", "hitita", "heveos", "filisteos", "egipcios", "cananeos",
   "hijos de Het", "edomitas", "horeos", "ismaelitas", "madianitas"
 ),
 "animales": (
   "camellos", "ovejas", "vacas", "becerros", "corderos", "cabras",
   "asnos", "burros", "carneros", "ganado", "trigo", "lentejas",
   "espigas", "vid", "serpiente", "palomas", "aves", "asno"
 ),
 "materiales": (
   "oro", "plata", "bronce", "hierro", "piedra", "piedras",
   "ladrillos", "arena", "madera", "resina"
 ),
 "objetos": (
   "altar", "altares", "tienda", "tiendas", "puerta", "puertas",
   "carro", "carros", "anillo", "sello", "copa", "saco",
   "báculo", "cetro", "vestiduras", "tumba", "pozo", "pozos",
   "arco", "manto", "túnica"
 ),
 "instrumentos": (
   "arpa", "flauta", "tambor", "trompeta", "lira", "kinnor", "ugab"
 ),
 "medidas": (
   "codo", "codos", "siclo", "siclos", "seá", "seas", "efa",
   "efas", "quinta parte", "monedas", "pesos"
 )
}
# Flexiones y sustituciones léxicas de alta confianza: solo sugerencias de ficha.
# No añadir equivalencias de nombres propios dudosos ni de identidades.
INFLECTIONS = {
 "animales/camello":["camellos"],
 "animales/oveja":["ovejas"],
 "animales/vaca":["vacas"],
 "animales/becerro":["becerros"],
 "animales/cabra":["cabras"],
 "animales/cordero":["corderos"],
 "animales/asno":["asnos"],
 "animales/burro":["burros"],
 "animales/carnero":["carneros"],
 "animales/lentejas":["lenteja"],
 "materiales/piedra":["piedras"],
 "materiales/ladrillo":["ladrillos"],
 "objetos/altar":["altares"],
 "objetos/puerta":["puertas"],
 "objetos/tienda":["tiendas"],
 "medidas/codo":["codos"],
 "medidas/siclo":["siclos"]
}
# Excluir palabras capitalizadas por la sintaxis, no por ser nombres propios.
STOPWORDS = set("""
A Acaso Acércate Acabo Acuéstate Ahora Al Algo Algunas Algunos Allí Así Aunque
Además Antes Apenas Aquellos Aquí Aquel Aquella Aquelos Ay
Bien Bendíceme Cada Casi Cerca Ciertamente Como Con Conocen Cuando Cuanto Cualquiera Cuál
Dame Dan De Del Den Dentro Desde Después Durante Dije Dijo Dime Dio Digan Dos
El Él Ella Ellas Ellos En Entonces Entre Entró Era Eran Es Esa Ese Esas Esos
Escuchen Estoy Este Esta Esto Estos Estas
Finalmente Fue Fueron
Ha Había Habían Han Haré Has Hasta Haz He Hemos Hoy Hubo Huyó Hijo Hijos Hijas
Iré
La Las Le Les Levantémonos Lo Los Luego Llegó
Maldito Me Mi Mira Miren Mis Más Mientras Murió
Nada Nadie Ni No Nos Nosotros Nuestra Nuestro Nunca
O Otra Otras Otro Otros
Padre Para Pero Pensaba Porque Por Pon Ponlo Primero Pronto Preguntó Puso Puedes Pues
Qué Que Quién Quiénes Quédate
Respondieron Reúnanse
Se Según Sería Si Sí Siendo Siéntate Sin Solo Son Somos Soy Su Sus
Te Ten Tenía Tengo Termina Tienen Toda Todas Todavía Todo Todos Toma Tomó Tuvo
Traigan Traiganme Tráeme Tráiganlo Tomen Tu Tus Tuve Únete
Un Una Uno Unas Unos Ustedes
Vayan Ve Veo Verdad Verdaderamente Vi Vida Vio Vive Vivirás Vivan Volveré
Volvió Vamos Vete Vuelve Vuelvan
Ya Y Yo
""".split())
GENEALOGY_HINT = re.compile(
    r"(?:hij[oa]s?\s+de|padre\s+de|madre\s+de|llamad[oa]|nombre\s+de|"
    r"rey\s+de|ciudad\s+de|región\s+de|pueblo\s+de|esposa\s+de)\s*$",
    re.I
)
CAPITAL_TOKEN = re.compile(r"(?<!\w)[A-ZÁÉÍÓÚÑÜ][\wÁÉÍÓÚÑÜáéíóúñü]*(?:-[\wÁÉÍÓÚÑÜáéíóúñü]+)*(?!\w)")


def normalized_with_positions(text):
    chars,indices=[],[]
    for i,ch in enumerate(text):
        folded=unicodedata.normalize("NFD",ch)
        folded="".join(c for c in folded if not unicodedata.combining(c)).casefold()
        chars.append(folded)
        indices.extend([i]*len(folded))
    return "".join(chars),indices


def norm(s):
    return unicodedata.normalize("NFD",s).casefold().translate(
        dict.fromkeys(range(0x300,0x370)))


def short(verse, start, end):
    l=max(0,start-60)
    r=min(len(verse),end+90)
    return verse[l:r]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true",
                        help="comprobar resultados frente a una nueva extracción")
    args=parser.parse_args()
    verses=json.loads(BES.read_text(encoding="utf-8"))
    registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert len(verses)==874 and len({(x["chapter"],x["verse"]) for x in verses})==874
    registered=registry["entidades"]
    assert len(registered)>=450  # Identificadores crecen con fichas aprobadas
    byid={x["id"]:x for x in registered}
    assert len(byid)==len(registered)

    lexicon=defaultdict(list)
    stopwords_normalized={norm(word) for word in STOPWORDS}
    for e in registered:
        # Los calificadores de paréntesis son pistas desambiguadoras,
        # pero la forma literal antes del paréntesis sí se puede buscar.
        candidate=re.sub(r"\s+\([^)]*\)$","",e["nombre"]).strip()
        if len(candidate)<3:continue
        lexicon[norm(candidate)].append({
            "id":e["id"],"category":e["categoria"],"forma_diccionario":candidate,
            "ruta":e["ruta"],"tipo":"nombre_registrado",
            "remision":e["es_remision"],"principal":e["ficha_principal"]
        })
    for id,words in INFLECTIONS.items():
        if id not in byid:
            raise ValueError("ID de flexión inexistente: "+id)
        e=byid[id]
        for word in words:
            lexicon[norm(word)].append({
                "id":id,"category":e["categoria"],"ruta":e["ruta"],"forma_diccionario":word,
                "tipo":"flexion_sugerida","remision":e["es_remision"],
                "principal":e["ficha_principal"]
            })
    for category,terms in PROPOSED_TERMS.items():
        for term in terms:
            lexicon[norm(term)].append({
                "id":None,"category":category,"ruta":None,"forma_diccionario":term,
                "tipo":"clase_propuesta_por_contexto",
                "remision":False,"principal":None
            })
    # El mismo literal puede tener más de una categoría o ficha.
    # Mantener ambas hipótesis sin fusionarlas automáticamente.
    terms=sorted(lexicon,key=lambda x:(-len(x),x))
    pattern=re.compile(r"(?<!\w)(?:"+"|".join(re.escape(x) for x in terms)+r")(?!\w)")
    mentions=[]
    unmatched=[]
    by_category=Counter()
    statuses=Counter()
    visited=[]
    for verse in verses:
        c,v=verse["chapter"],verse["verse"]
        passage=verse["text"]
        txt,positions=normalized_with_positions(passage)
        matches=[]
        for m in pattern.finditer(txt):
            start=positions[m.start()]
            end=positions[m.end()-1]+1
            label=passage[start:end]
            candidates=lexicon[m.group(0)]
            # Los nombres de personas y lugares se reconocen en su grafía
            # propia; los sustantivos de materiales y animales sí minúsculos.
            valid=[
                e for e in candidates
                if (
                    (e["category"] not in ("onomastico","lugares")
                     or label[0].isupper())
                    # No confundir "oró" con "oro" ni "sea" con "seá".
                    and (e["category"] not in ("materiales","medidas")
                         or unicodedata.normalize("NFC", e["forma_diccionario"]).casefold()
                         == unicodedata.normalize("NFC", label).casefold())
                    # Efa en Gn 25:4 es nombre propio; no una medida.
                    and not (e["category"]=="medidas" and
                             norm(label)=="efa" and label[0].isupper())
                )
            ]
            if not valid:continue
            unique={}
            for x in valid:
                key=(x["id"],x["category"],x["tipo"])
                unique[key]=x
            choices=list(unique.values())
            ids=sorted(set(e["id"] for e in choices if e["id"]))
            cats=sorted(set(e["category"] for e in choices))
            conflict = IDENTITY_CONFLICTS.get((c,v,norm(label)))
            spelling = TEXT_VARIANTS_PENDING.get((c,v,norm(label)))
            if conflict:
                assert conflict["excluir"] in ids
                # No se puede vincular este nombre a la ficha preexistente.
                ids = [x for x in ids if x != conflict["excluir"]]
                state="colision_de_identidad_por_revisar"
            elif spelling:
                assert spelling["proponer"] in byid
                # Sugerencia SOLO editorial, nunca enlace automático.
                ids=[spelling["proponer"]]
                state="variante_ortografica_por_aprobar"
            elif len(ids)>1 or len(cats)>1:
                state="ambiguo_desambiguar"
            elif len(ids)==1:
                state=("flexion_por_comprobar" if
                       not any(e["tipo"]=="nombre_registrado" for e in choices)
                       else "ficha_existente_por_verificar")
            else:
                state="termino_sin_ficha_por_evaluar"
            matches.append({
                "ref":f"Gn {c}:{v}","chapter":c,"verse":v,
                "start":start,"end":end,"literal":label,"contexto":short(passage,start,end),
                "categorias":cats,"candidatos_ficha":ids,"estado":state,
                "incidencia":(conflict["motivo"] if conflict else
                             spelling["motivo"] if spelling else None),
                "origen":"coincidencia_lexica_fuente_BES",
            })
        # Solapamientos internos: preferir la expresión más larga; no borrar
        # ambigüedad entre categorías que usan exactamente las mismas letras.
        matches.sort(key=lambda m:(m["start"],-(m["end"]-m["start"])))
        kept=[]
        for match in matches:
            if any(x["start"]<=match["start"] and x["end"]>=match["end"]
                   for x in kept):
                continue
            kept.append(match)
        mentions.extend(kept)
        for item in kept:
            statuses[item["estado"]]+=1
            for cat in item["categorias"]:by_category[cat]+=1

        covered=[(x["start"],x["end"]) for x in kept]
        for m in CAPITAL_TOKEN.finditer(passage):
            term=m.group(0)
            if norm(term) in stopwords_normalized or norm(term) in {"dios","senor","jehova"}:continue
            if any(a<=m.start()<b for a,b in covered):continue
            # Nombres no catalogados y términos nuevos: señales, NO fichas.
            # Los tokens iniciales habituales se filtran después de contar,
            # salvo que los asista un contexto genealógico o toponímico.
            prefix=passage[max(0,m.start()-65):m.start()]
            hint=bool(GENEALOGY_HINT.search(prefix))
            sentence_start=(m.start()==0 or bool(re.search(r"[.!?»]\s+$",prefix)))
            unmatched.append({
                "ref":f"Gn {c}:{v}","chapter":c,"verse":v,
                "literal":term,"start":m.start(),"end":m.end(),
                "contexto":short(passage,m.start(),m.end()),
                "indice_contextual":hint,
                "inicio_oracion":sentence_start
            })
        visited.append(f"Gn {c}:{v}")

    counts_unknown=Counter(norm(x["literal"]) for x in unmatched)
    unmatched=[x for x in unmatched
               if counts_unknown[norm(x["literal"])]>=2 or x["indice_contextual"]
               or "-" in x["literal"]]
    for item in unmatched:
        item["repeticiones"]=counts_unknown[norm(item["literal"])]
        item["estado"]="nombre_no_correspondido_por_clasificar"

    # Convertir coincidencias en lista por categoría para P3 / P4.
    bycat={cat:[] for cat in CATEGORIES}
    for mention in mentions:
        for cat in mention["categorias"]:
            bycat[cat].append(mention)

    summary_by_category={}
    for cat in CATEGORIES:
        xs=bycat[cat]
        summary_by_category[cat]={
            "menciones_candidatas":len(xs),
            "versiculos_con_candidatos":len(set(x["ref"] for x in xs)),
            "fichas_existentes_sugeridas":len(set(i for x in xs for i in x["candidatos_ficha"])),
            "pendientes_ambiguos":sum(x["estado"]=="ambiguo_desambiguar" for x in xs),
            "sin_ficha_por_evaluar":sum(x["estado"]=="termino_sin_ficha_por_evaluar" for x in xs),
            "ejemplos":[{"literal":x["literal"],"ref":x["ref"],"ids":x["candidatos_ficha"],
                          "estado":x["estado"]} for x in xs[:8]]
        }
    queue=sorted([x for x in mentions if x["estado"] in (
        "ambiguo_desambiguar","termino_sin_ficha_por_evaluar",
        "colision_de_identidad_por_revisar","variante_ortografica_por_aprobar")],
        key=lambda x:(x["chapter"],x["verse"],x["start"]))
    unknownfreq=defaultdict(list)
    for item in unmatched:
        if len(unknownfreq[norm(item["literal"])])<15:
            unknownfreq[norm(item["literal"])].append(item)
    suggested_names=sorted([
        {"literal":v[0]["literal"],"menciones":counts_unknown[key],
         "referencias":list(dict.fromkeys(x["ref"] for x in v)),
         "contexto_inicial":v[0]["contexto"],
         "estado":"nombre_no_correspondido_por_clasificar"}
        for key,v in unknownfreq.items()
    ],key=lambda x:(-x["menciones"],x["literal"]))

    output={
      "fase":"P3","edicion":"BES 2026",
      "estado":"primer_barrido_automatico_pendiente_de_revisión_editorial",
      "fuente":"data/genesis_25_50_bes.json",
      "universo_fichas":"data/registro_maestro.json",
      "versiculos_recorridos":len(visited),
      "referencias_recorridas":visited,
      "categorias":bycat,
      "nombres_capitalizados_sin_match":unmatched,
      "criterio":"Son CANDIDATOS; las coincidencias de nombre no prueban identidad ni vínculo. Ninguna ficha, mapa, genealogía o enlace se modifica."
    }
    summary={
      "fase":"P3","edicion":"BES 2026","estado":output["estado"],
      "versiculos":874,"apendices":8,"identificadores_historicos":450,
      "menciones_candidatas":len(mentions),
      "por_estado":dict(statuses),"por_categoria":summary_by_category,
      "pendientes_ambiguedad_y_nueva_ficha":len(queue),
      "prioridad_desambiguacion":queue[:100],
      "nombres_sin_match_frecuentes":suggested_names[:100],
      "nota":"Primer barrido literal. La revisión contextual del Onomástico y demás categorías continúa. No publicar, no redactar fichas, no fusionar identidades."
    }

    # Control estructural de referencias y expresiones originales.
    originals={(x["chapter"],x["verse"]):x["text"] for x in verses}
    for x in mentions+unmatched:
        verse=originals[(x["chapter"],x["verse"])]
        assert verse[x["start"]:x["end"]]==x["literal"],x
        if x.get("candidatos_ficha"):
            assert all(k in byid for k in x["candidatos_ficha"])
    assert len(visited)==874 and len(set(visited))==874
    specific={(x["chapter"],x["verse"],norm(x["literal"])):x for x in mentions}
    assert specific[(25,9,"zohar")]["estado"]=="colision_de_identidad_por_revisar"
    assert "onomastico/zohar" not in specific[(25,9,"zohar")]["candidatos_ficha"]
    assert specific[(25,15,"hadad")]["estado"]=="colision_de_identidad_por_revisar"
    assert "onomastico/hadad-rey-de-edom" not in specific[(25,15,"hadad")]["candidatos_ficha"]
    assert specific[(25,2,"zimran")]["estado"]=="variante_ortografica_por_aprobar"
    assert specific[(25,2,"zimran")]["candidatos_ficha"]==["onomastico/zimram"]
    if args.check:
        assert EXTRACTIONS.exists() and SUMMARY.exists()
        prev=json.loads(EXTRACTIONS.read_text(encoding="utf-8"))
        oldsum=json.loads(SUMMARY.read_text(encoding="utf-8"))
        assert prev==output and oldsum==summary,"Los informes P3 no reproducen el barrido BES"
        print("P3 OK: primer barrido reproducible en las ocho categorías.")
        return
    EXTRACTIONS.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("P3: 874 versículos, 8 categorías, candidatos",len(mentions),
          "por tipo",dict(statuses),"ambigüedades/nuevos",len(queue),
          "nombres no catalogados",len(suggested_names))
    print("Por categoría:",dict(by_category))


if __name__=="__main__":
    main()
