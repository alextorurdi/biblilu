# Fase 3 · Extracción y clasificación de Génesis 25–50

**Inicio:** 23/11/2026. **Texto base:** BES 2026. **Estado actual:** **P3 CERRADA el 25/11/2026**, tras aprobación editorial de las ocho categorías y GitHub Actions #37 en verde (commit `5ef657a`). Véase [acta definitiva](p3-cierre-definitivo-genesis-25-50-2026-11-25.md). Fichas, notas, enlaces, mapas y publicación corresponden a P4–P9. Las menciones históricas de «pendiente» que aparecen más abajo describen estados anteriores y quedan superadas por el acta final.

**Alcance:** Gn 25:1–50:26, 874 versículos, 19 escenas BES aprobadas en P1 y maquetadas en P2. Se preservan íntegramente las 15 escenas anteriores RVR1960.

**Protocolo:** [P3 — extracción y clasificación única](protocolo-libros.md). **Base:** [Fuente BES](../data/genesis_25_50_bes.json); [registro maestro](../data/registro_maestro.json); [criterios de identidad ya acordados](criterios-identidades-genesis.md).

## Método adoptado

1. **Una sola lectura de los 874 versículos** para elaborar un inventario provisional en las ocho categorías de BIBLILU: Onomástico, Lugares, Seres Vivos (clave `animales`), Materiales, Tribus, Objetos, Instrumentos Musicales y Medidas.
2. Recuperar las **fichas existentes por ID estable** desde el registro maestro (450 registros). Registrar por mención **referencia Gn capítulo:versículo**, coincidencia textual BES, contexto y uno o varios identificadores **solo propuestos**.
3. Clasificar como **ficha existente por verificar**, **homónimo/identificación ambigua**, **flexión o variante sin aprobar** o **término sin ficha por evaluar**, sin identificar por automatismo personas, clanes o lugares.
4. Recoger también nombres propios que la BES incorpora y que pueden no coincidir literalmente con los encabezados de las fichas RVR1960. La lista de nombres no reconocidos por el diccionario es **una cola de revisión**, no un índice de identidades ni un catálogo aprobado.
5. **Revisión editorial por categorías**, empezando por Onomástico. Resolver variantes, remisiones, homónimos y nuevas identidades usando el texto y los [criterios aprobados](criterios-identidades-genesis.md), sin reescribir Gn 1–24.
6. **No crear ni reescribir fichas** en esta fase: las nuevas entradas y correcciones de fichas antiguas corresponden a **P4**. Tampoco se insertarán hipervínculos en las escenas ni se modificarán genealogías o mapas hasta su fase.

## Archivos de trabajo

- [Extractor P3 reproducible](../scripts/extract_genesis_p3.py), sin dependencias ni acceso de escritura a las fichas.
- [Catálogo de menciones por categoría](../data/p3-extracciones-genesis-25-50.json): referencias exactas, texto encontrado y posibles fichas.
- [Resumen y cola priorizada](p3-resumen-genesis-25-50.json): estadísticas, casos ambiguos y nombres nuevos por cotejar.
- [Ejecuciones del extractor](https://github.com/alextorurdi/biblilu/actions/workflows/extraccion-p3-bes.yml): generación automática y comprobación reproducible.

## Resultados efectivos del primer barrido · 23/11/2026

**Ejecución verificada:** [GitHub Actions · P3 BES](https://github.com/alextorurdi/biblilu/actions/runs/45274695280), **success**. Se recorrieron exactamente los **874 versículos BES**, con la fuente y el registro histórico protegidos.

**Inventario provisional:** **1.656 menciones candidatas únicas**, que incluyen **1.259** coincidencias con fichas previas por verificar, **68** flexiones, **93** ambigüedades, **233** términos sin ficha por evaluar, **2** colisiones de identidad y **1** variante de grafía BES pendiente de aprobación.

| Apéndice | Coincidencias candidatas |
|---|---:|
| Onomástico | 1.210 |
| Lugares | 228 |
| Seres Vivos (clave `animales`) | 115 |
| Materiales | 23 |
| Tribus | 43 |
| Objetos | 87 |
| Instrumentos Musicales | 0 |
| Medidas | 5 |

**Importante:** un término ambiguo puede aparecer en más de una categoría, por lo que la suma de estas filas supera las 1.656 menciones únicas. Cero coincidencias instrumentales **no equivale a certificar ausencia**, hasta completar revisión contextual. Ninguna coincidencia automática se da por validada y no hay nuevas fichas ni enlaces publicados.

**Depuración verificada:** se rechazaron homografías erróneas como «oró» → «oro» y «sea» → «seá», y se separó «Efa» como nombre personal de Gn 25:4, no como medida. La revisión mantiene en cola expresiones ambivalentes como «Israel», «Edom», pueblos, topónimos y personas homónimas.

### Primer lote de revisión: Onomástico, Génesis 25:1–18

[**Abrir propuesta editorial completa**](p3-onomastico-lote1-genesis-25-1-18.md).

- **«Zimrán» (Gn 25:2):** propuesta de variante BES para la ficha anterior `onomastico/zimram`, sin cambiar su URL ni su identidad.
- **«Zohar» (Gn 25:9):** padre de Efrón, diferente del Zohar hijo de Simeón de Gn 46:10. Se ha impedido proponer el ID histórico erróneo; posible ficha independiente en P4.
- **«Hadad» (Gn 25:15):** hijo de Ismael, diferente del rey edomita hijo de Bedad (Gn 36:35). Se ha impedido proponer el ID del rey; posible ficha independiente en P4.
- **Súa, Seba, Dedán, Hanoc y Efa:** la propuesta resuelve estos casos por su parentesco explícito, respetando los IDs diferenciados existentes.
- **Asurim, Letusim, Leumim:** se conservan fichas personales independientes, de acuerdo con la decisión editorial previa.

**Estado del lote:** asignaciones y nuevas fichas **aprobadas editorialmente** (25/11/2026); las implementaciones aprobadas anteriormente se conservan. No se han modificado ni vinculado fichas históricas.

### Resolución editorial aplicada · Primer lote del Onomástico

El editor aprobó «Zimrán» como variante de `onomastico/zimram`, las **dos entradas separadas Zohar (heteo) / Zohar (hijo de Simeón)** y las **dos entradas diferenciadas Hadad (hijo de Ismael) / Hadad (rey de Edom)**.

Se han actualizado [las entradas fuente](../data/entries.json) y el [registro maestro](../data/registro_maestro.json), que cuenta ahora **451 rutas/identificadores**, incluidas 291 entradas onomásticas. Para el hijo de Ismael se conserva el ID `onomastico/hadar` por compatibilidad histórica: ese mismo individuo aparece como **Hadar en RVR1960** y **Hadad en BES 2026**. Se ha añadido la única ficha que faltaba: `onomastico/zohar-heteo`.

El [extractor P3](../scripts/extract_genesis_p3.py) asigna los casos aprobados en Gn 25:2, 25:9, 25:15 y 36:35–36, impidiendo cruces con sus homónimos. La BES usa **«Zera» en Gn 46:10** para el hijo de Simeón que se llama **Zohar** en RVR1960: se registra aparte como **diferencia textual que debe contrastarse** con la ficha histórica, sin dirigirla a `onomastico/zera` (hijo de Reuel).

[Detalle del primer lote aprobado parcialmente](p3-onomastico-lote1-genesis-25-1-18.md). **P3 pendiente del control transversal:** las demás identificaciones onomásticas de este lote se aprobaron el 25/11/2026; las escenas nuevas siguen sin publicarse.

### Cierre editorial Onomástico · 25/11/2026

**Las diez decisiones finales del editor sobre Gn 25–26 están aprobadas** y documentadas en los tres registros de lotes. Lote 1: Súa, Seba y Dedán, Hanoc, Efa, Mamre, menciones restantes, Asurim/Letusim/Leumim y remisiones; lote 2: Edom como sobrenombre de Esaú (25:30); lote 3: Abimelec y Ficol con identidad intergeneracional no determinada, dos fichas nuevas **Ahuzat** y **Beeri** aprobadas para P4, desambiguación de la familia de Esaú y falsa clasificación de Seba (26:33) como persona.

**Sin decisiones onomásticas por aprobar** en Gn 25–50. No confundir las tareas de implementación pendientes con decisiones editoriales abiertas. El control transversal final de P3 debe comprobar coherencia entre categorías y registrar cualquier incidencia nueva si apareciera.

### Seguimiento de lotes onomásticos

| Lote | Tramo | Estado | Documento |
|---|---|---|---|
| 1 | Gn 25:1–18 | Aprobado completo (25/11); Zimram, Zohar y Hadad incorporados anteriormente | [Lote 1](p3-onomastico-lote1-genesis-25-1-18.md) |
| 2 | Gn 25:19–34 | Aprobado (25/11); siete personas y Edom como sobrenombre de Esaú | [Lote 2](p3-onomastico-lote2-genesis-25-19-34.md) |
| 3 | Gn 26:1–35 | Aprobado (25/11); Ahuzat y Beeri aprobados para P4 | [Lote 3](p3-onomastico-lote3-genesis-26.md) |

**Incidencia técnica conocida del lote 3:** en Gn 26:33 «Seba» nombra un **pozo**, no una persona; la salida automática P3 lo considera erróneamente un candidato onomástico. La reclasificación está aprobada (25/11/2026), pero el extractor aún no se ha corregido. No se han cambiado fichas ni contenido publicado por este lote.

### Lote único Gn 27–50 · decisiones editoriales aprobadas (24/11/2026)

[Registro de acuerdos](p3-onomastico-decisiones-genesis-27-50.md): están cerradas las incidencias de identidad del lote, incluidas las asignaciones de Israel y Edom, la prohibición de crear fichas separadas de jefaturas y las correcciones de Basemat, familiares horeos, Aná y Potifar/Potifera. El Excel consolidado mantiene la columna «Acción» del editor y un cruce por apéndices.

**Alcance del acuerdo:** clasificaciones editoriales aprobadas, **no** fichas nuevas implementadas ni cambios publicados. P3 continúa para las demás categorías y P4 debe elaborar las fichas y relaciones correspondientes.

### Lugares · Génesis 25–50 — revisión aprobada (24/11/2026)

[**Acuerdos editoriales completos**](p3-lugares-decisiones-genesis-25-50.md): las **34 incidencias** de la revisión de Lugares quedan aprobadas, incluidas las reglas contextuales para falsos positivos y **27 pruebas de regresión especificadas** (aún pendientes de automatización). Las **31 propuestas de fichas** son altas aprobadas para preparar en P4, no entradas creadas o publicadas.

**Excepción expresa respecto de la columna «Acción editorial» inicial:** la mención de **Edom en Gn 36:32 se clasifica en Lugares** (`lugares/edom`), junto a Gn 32:3; 36:16–17,21,31. Solo «jefes de Edom» en Gn 36:43 se remite a Tribus (`tribus/edomitas`), mientras que «Esaú» en el mismo versículo es personal (`onomastico/esau`).

Se conserva el barrido automático como inventario bruto para auditoría. No se han modificado las escenas BES, fichas fuente ni el sitio publicado. **La Fase 3 global continúa** para las otras categorías.

### Seres Vivos · Génesis 25–50 — revisión aprobada (24/11/2026)

[**Acuerdos editoriales completos**](p3-seres-vivos-decisiones-genesis-25-50.md): las **30 incidencias** SV-01–SV-30 quedan aprobadas, con **10 nuevas fichas** para redactar en P4. El Excel consolidado registra **158** menciones de término-versículo, incluidas pruebas contextuales sin enlace.

**Decisiones que prevalecen:** no marcar «ganado» en ningún versículo; Gn 40:17,19 «aves» → `animales/aves-de-rapina`; Gn 31:11 y 48:16 → `animales/angel-de-jehova` por decisión editorial (sin atribuir al texto el título); descartar Nueces por ahora; remisión «Almendra» → Almendro y corrección de la ficha Vaca → Ganado Bovino durante P4. Las diez altas y el resto de clasificaciones están aprobados cuando no contradicen la columna «Acción editorial» aportada por el editor.

**Alcance:** aprobación documental P3; fichas, remisiones, enlaces y publicación todavía pendientes. Los falsos positivos y omisiones del extractor siguen como controles para una implementación técnica futura. La Fase 3 del Génesis continúa con los apéndices restantes.

### Materiales · Génesis 25–50 — revisión editorial aprobada (24/11/2026)

[**Acuerdos editoriales definitivos**](p3-materiales-acuerdos-parciales-genesis-25-50.md): tras recuperar la aprobación completa del editor, las **30 incidencias originales y sus resoluciones finales** están cerradas, sin decisiones pendientes. **Madera (incluyendo leña)** y **Sangre** figuran expresamente **aprobadas**, pese a que sus fichas todavía no se han implementado. De las propuestas originales se trasladó **Cilicio a Objetos**, y se descartaron Hilo, Especias aromáticas y Tierra (suelo).

**Balance del acuerdo inicial:** 12 fichas existentes + 13 nuevas aprobadas = **25**. **Revisión posterior:** aprobación de dos fichas independientes más, [Agua](borradores/materiales-agua.md) y [Rocío](borradores/materiales-rocio.md); descarte de Corteza y Ofrenda líquida. **Balance vigente: 12 existentes + 15 nuevas aprobadas = 27 fichas previstas en Materiales**, no publicadas todas.

**Reglas explícitas:** Gn 14:3 «Mar Salado» solo Lugares; Gn 19:26 «sal» a Materiales/Sal; Gn 31:13 «sal» imperativo, no enlazar; «vino» verbal no enlazar. Revisar retrospectivamente Génesis 1–24 para los enlaces de las nuevas fichas durante la fase adecuada. El Excel original mantiene algunos estados de «pendiente» obsoletos frente a las decisiones finales, que prevalecen.

**Alcance:** cierre **editorial** de P3 Materiales; la redacción e implementación de las nuevas fichas y enlaces corresponde a P4 y fases siguientes. La **Fase 3 global de Génesis** continúa abierta para las demás categorías.

### Tribus · Génesis 48–49 — TR-29 y lista definitiva de fichas (24/11/2026)

[**TR-29 y acuerdo de 13 fichas tribales**](p3-tribus-tr29-genesis-48-49.md): aprobado el **criterio mixto contextual** para Gn 48–49 y una lista definitiva de **13** fichas de los grupos descendientes de Jacob: Rubén, Simeón, Judá, Gad, Aser, Dan, Neftalí, Isacar, Zabulón, Benjamín, Efraín, Manasés y Levitas. La ficha colectiva de José **no se creará**; permanece José como persona en Onomástico y sus descendencias se documentan mediante Efraín y Manasés. La ficha Levitas representa al colectivo y no sustituye a Leví como individuo.

**Alcance:** 13 fichas nuevas **aprobadas para preparación en P4**, no implementadas ni publicadas. La cifra no equivale a trece asignaciones territoriales: Leví posee un régimen distinto (Jos 14:4). El resto de grupos/pueblos (como Israelitas) son entidades separadas y no se cuentan entre estas 13.

### Instrumentos Musicales · Génesis 25–50 — revisión aprobada (24/11/2026)

[**Acuerdos editoriales de Instrumentos Musicales**](p3-instrumentos-musicales-decisiones-genesis-25-50.md): revisión del tramo BES de 874 versículos completada y **11 incidencias resueltas**. Gn 31:27 es la única referencia relevante; la BES emplea «cantos y música», mientras que el hebreo y RVR1960 mencionan **Tof** (tamborín) y **Kinnor** (lira/«arpa»). Se **aprueba la nueva ficha `instrumentos/tof`** y una **nota editorial** en ese versículo con enlaces a Tof y Kinnor; no convertir «música» en un enlace directo ni reescribir la BES. Labán formula una despedida hipotética, no una actuación celebrada.

**Balance:** 2 fichas existentes (Kinnor y Ugab) + 1 alta aprobada (Tof) = **3 fichas previstas**; Ugab sin menciones en Gn 25–50. Redacción de la ficha, nota funcional y publicación reservadas para P4/P9; P3 global continúa abierta para las categorías restantes.

### Medidas y Unidades · Génesis 25–50 — revisión editorial cerrada (25/11/2026)

[**Registro definitivo de acuerdos**](p3-medidas-y-unidades-decisiones-genesis-25-50.md): **30/30 incidencias cerradas**. Hay **21 respuestas explícitas** del editor y **9 celdas sin rellenar (valor «355»)** que, por autorización posterior del editor, se han resuelto **por inferencia documentada** a partir de los otros acuerdos. No se confunden con aprobaciones escritas en el Excel. **0 incidencias pendientes**.

**Cuatro nuevas fichas aprobadas para P4:** **Qesitá** (Gn 33:19), **Kibrá** (Gn 35:16; 48:7), **Diezmo** (Gn 28:22) y **Quinto** (Gn 41:34; 47:24,26). **Semana** descartada, al igual que fichas para tiempo cotidiano o días de camino; las cuatro quintas partes de Gn 47:24 se explicarán dentro de Quinto. **Notas editoriales aprobadas:** Kibrá; Gn 37:28 («veinte de plata») y Gn 45:22 («trescientos de plata»), con enlaces a Plata y Siclo desde sus notas. Gn 33:19 no genera un enlace a Plata o Siclo: es Qesitá de equivalencia desconocida. Preservar Codo y Seá, aprobados anteriormente, y Siclo, ya existente.

**Precaución MU-28:** la coincidencia «monedas» de Gn 33:19 ya está en el barrido P3; falta clasificarla como Qesitá. La actualización técnica del extractor se reserva para la fase pertinente.

**Estado:** P3 de Medidas y Unidades **cerrada editorialmente**; fichas, notas, enlaces, correcciones técnicas y publicación **todavía pendientes**. La Fase 3 global sigue su curso para las demás categorías.

### Objetos · Génesis 25–50 — revisión editorial cerrada (25/11/2026)

[**Registro de las 40 decisiones de Objetos**](p3-objetos-decisiones-genesis-25-50.md): **39 respuestas expresas del editor** y la celda OB-05 con el valor «38» (sin decisión nueva; **Cilicio ya estaba aprobado** por Materiales). **40/40 incidencias resueltas, sin decisiones pendientes de P3 Objetos**. La [propuesta de revisión original](p3-objetos-propuesta-genesis-25-50.md) sigue disponible como auditoría, pero las decisiones posteriores prevalecen.

**Altas aprobadas:** **26 nuevas** (Pozo, Cisterna, Túnica, Terafín, Ídolo, Estela, Majano, Escalera de Jacob, Arco y flechas, Espada, Yugo, Bastón, Cetro, Sello y Cordón, Velo, Copa, Saco, Canasta, Carro, Anillo, Aretes, Manto, Tumba, Cabaña, Cama, Mesa) **+ Cilicio previamente aprobada** = **27 altas a implementar en P4**. Permanecen las **7 fichas existentes**; total proyectado: **34 fichas de Objetos**. El editor solicita expresamente **Sello y Cordón como ficha única**, separa **Terafín/Ídolo** y **Estela/Majano**, y descarta Bolsa (remisión a Saco), Silla de camello y Vestimenta genérica. No se crean fichas independientes de Cadena, Piedra, Oro, Plata, Lino o Adivinación por esta revisión.

**Nota conceptual aprobada:** Gn 37:24 sobre «pozo» BES / *bôr* (Cisterna) frente a *bəʾēr* (Pozo de agua). La redacción exacta del borrador asistido **no está aprobada literalmente**: reservar para P4. La BES permanece inalterada.

**Retrospectiva aprobada y auditada inicialmente:** Gn 1–24, con candidatos para Túnica, Pozo, Arco y flechas, Velo, Tumba y una posible variante de Aretes; excluir falsos positivos como Gn 10:30 «Mesa» (lugar), Gn 3:24 (Espada encendida), Gn 9:13–16 (Arco iris) y Gn 14:10 (pozos de asfalto). Los enlaces aún no se han aplicado.

**Estado:** P3 Objetos **cerrada editorialmente**, pero **sin** fichas nuevas, notas ni enlaces publicados. El extractor requiere correcciones técnicas y el sitio no cambia hasta la implementación y publicación en fases posteriores.

## Precauciones específicas

- **Abimelec / Ficol:** mantener las fichas y sus menciones, sin resolver por automatismo la identidad personal entre generaciones.
- **Esposas de Esaú y Timna:** preservar designaciones y homónimos. No fusionar Ada, Basemat, Judit, Mahalat, Aholibama ni las Timna.
- **Hanoc, Seba, Heber, Saúl, etc.:** cuando hay varias fichas que comparten nombre, conservar los identificadores candidatos y exigir el contexto genealógico para elegir.
- **Israel, Edom y otras denominaciones:** comprobar si cada pasaje designa a una persona, pueblo o territorio, en vez de asignar por una coincidencia literal.
- **Variante textual BES respecto de RVR1960:** registrar la forma encontrada como *variante por estudiar*, no alterar títulos, URLs o textos de fichas aprobadas.

## Criterio de cierre de P3

**Las revisiones editoriales por categoría están aprobadas.** Falta ejecutar y registrar el **control transversal de cierre P3** de extracción, duplicidades y clasificaciones cruzadas. Las fichas y vínculos nuevos corresponden a P4 y fases posteriores. Las fichas no se redactan hasta P4.

El informe automático valida **cobertura y literalidad de los candidatos** pero no reemplaza la revisión de nombres o identidades por una persona.


## Casos separados para control posterior · 25/11/2026

- **Sin aprobaciones editoriales pendientes conocidas** de los lotes Onomástico 1–3: las diez decisiones expresas están registradas.
- **Control transversal P3, no nueva aprobación:** verificar que Edom/Israel y homónimos se clasifiquen según contexto y que el inventario de las ocho categorías no deje omisiones o duplicidades.
- **Corrección técnica posterior:** eliminar falso positivo onomástico «Seba» de Gn 26:33 y asegurar su tratamiento como pozo/topónimo; revisar pruebas de regresión y correcciones automáticas del extractor.
- **P4:** crear fichas Ahuzat y Beeri, preparar enlaces y relaciones aprobados; no afirmar identidad de Abimelec o Ficol entre generaciones.
- **P4–P9:** completar las restantes fichas aprobadas, notas, enlaces, pruebas y publicación. Ninguna de estas tareas representa una aprobación editorial aún no concedida.


### Control transversal de P3 · 25/11/2026

[**Auditoría transversal documentada**](p3-control-transversal-genesis-25-50.md): integridad estructural verificada para 874 versículos y 1.711 registros de categoría (1.656 menciones únicas). **0 referencias, posiciones textuales, identificadores o registros internos duplicados erróneos** detectados en los controles formales. Se identifican **55 coincidencias Onomástico/Lugares** todavía candidatas en el inventario bruto y **10 grupos de actuaciones de reconciliación técnica (CT-01–CT-10)**: Seba (pozo), «seas» verbal, instrumentos de Gn 31:27, Israel/Edom, Qesitá, Kibrá, Cisterna y exclusión de «ganado», entre otros. **Las ocho categorías están aprobadas editorialmente; no se certifica aún cierre técnico total P3.** Ninguna ficha ni escena web se publica por esta auditoría.


### Reconciliación técnica y R-01 · 25/11/2026

**R-01 aprobado y registrado:** `tribus/israelitas` será ficha principal **Israelitas**; `tribus/israel` queda como remisión/variante futura, sin duplicar la ficha; `onomastico/jacob` conserva el uso personal. Se ha incorporado la [capa estructurada de reglas contextuales](../data/p3-reconciliacion-genesis-25-50.json) con los **55 cruces Onomástico/Lugares** asignados (45 Lugares, 8 Onomástico, 2 Tribus) y **57 acciones puntuales de corrección/nota/exclusión**, incluyendo CT-01–CT-09 y R-01. Se añade [comprobador reproducible](../scripts/check_p3_reconciliacion.py). La comprobación directa de integridad de estas reglas contra los versículos e inventario actuales ha pasado (posiciones y categorías coherentes). **Pendiente ejecutar el comprobador Python en CI y materializar la clasificación derivada completa**; el barrido bruto se mantiene intacto como auditoría. Tampoco se han creado fichas ni enlaces, y P3 no se declara técnicamente cerrada todavía.


### Catálogo reconciliado derivado y CI · 25/11/2026

Se ha generado el [catálogo técnico derivado](../data/p3-catalogo-reconciliado-genesis-25-50.json), basado en el inventario original sin sobrescribirlo. **1.682 registros únicos**: 1.656 posiciones textuales originales + 26 añadidas a partir de reglas de contexto (asociaciones/no enlaces incluidos). **112 registros** incorporan reglas aprobadas; se mantienen como **1331 candidatos únicos no validados** y **239 candidatos no reconciliados**. Otras categorías de estado: 81 clasificados por contexto, 27 exclusiones aprobadas, 2 asociaciones contextuales, 1 nota instrumental y 1 exclusión personal. Estas magnitudes expresan el estado técnico del catálogo, **no** 1.570 nuevas decisiones editoriales pendientes ni un recuento de fichas.

El [generador reproducible](../scripts/build_p3_catalogo_reconciliado.py) permite `--check`, y el [comprobador contextual](../scripts/check_p3_reconciliacion.py) valida los acuerdos expresos. Se añadió [workflow de GitHub Actions](../.github/workflows/control-p3-reconciliacion.yml) en modo lectura, activado por modificaciones pertinentes. Las verificaciones de posiciones efectuadas al preparar el catálogo no revelaron errores, pero **el resultado de la ejecución de GitHub Actions aún no ha sido confirmado**. El cierre completo de P3 necesita verificar CI y ampliar las clasificaciones contextuales fuera de las reglas actualmente codificadas. No se crean nuevas fichas ni se modifica el texto bíblico.


### Segunda pasada de reconciliación · 25/11/2026

[**Informe de la segunda pasada**](p3-reconciliacion-segunda-pasada.md): el catálogo derivado contiene ahora **316 registros con reglas aprobadas**, frente a 112 antes de la ampliación, y una cola reducida de **35 registros sin reconciliar**; otros **1.331** siguen como candidatos únicos **no validados**. Se añaden **196 correcciones CT-11** y **8 CT-12**, incluida la separación Galaad región/majano y la exclusión de «sacó» verbal. Las posiciones se contrastaron sin errores en el procesamiento. GitHub Actions **todavía sin resultado confirmado**. La Fase 3 **no está técnicamente cerrada**; siguen pendientes verificación de candidatos únicos, cobertura y comprobación del workflow. No se publican fichas ni cambios en escenas.


### Tercera pasada · homónimos y variantes (25/11/2026)

[**Auditoría Siquem / Aná / Zera y cola residual**](p3-auditoria-homonimos-y-variantes-genesis-25-50.md): reconciliados **35 registros antes residuales** mediante CT-13, sin inventar URLs para 30 casos sin ficha inequívoca; aplicadas **29 correcciones CT-14** a candidatos engañosamente unívocos: Siquem persona (15), Aná (9), Zera (5). El catálogo derivado mantiene **1.682 registros**, de los cuales **380** tienen regla contextual y **1.302** siguen como candidatos únicos no validados; **0** continúan en estado `candidato_no_reconciliado`, pero ello **no constituye cierre semántico**. Siquem personal y Zera padre de Jobab no reciben ID ficticio. Se reforzaron regresiones del script de validación. La ejecución real de CI sigue sin confirmarse; sin fichas o enlaces publicados.


### Control CT-31 y CT-32 · 25/11/2026

- [CT-31: auditoría de integridad tras D-04](p3-ct31-control-integridad-25-11-2026.md): 874 versículos, 1.711 registros brutos (1.656 posiciones únicas), 55 cruces y 1.918 reglas contextuales examinadas sin errores de posición ni duplicaciones de regla. Catálogo derivado regenerado con **1.973 menciones**. **D-04 opción A aprobada:** ficha futura independiente Débora, nodriza de Rebeca (`onomastico/debora-nodriza-rebeca`), sin enlace material hasta P4.
- [CT-32: regresión léxica y cribado de nombres](p3-ct32-cobertura-lexica-y-nombres-genesis-25-50.md): 24 familias y **230 apariciones** contrastadas, sin omisiones en ese conjunto; prueba automatizada incorporada a `control-p3-reconciliacion.yml`. El cribado de mayúsculas no confirmó antropónimos o topónimos nuevos. Títulos teológicos de Gn 49:24 reservados para tratamiento editorial de escena (P6).
- **Estado prudente:** reglas y coberturas dirigidas verificadas en lectura directa, pero GitHub Actions no ha aportado aún una ejecución confirmada y quedan por verificar en CI `check_p3_reconciliacion.py`, `check_p3_cobertura_lexica.py` y `build_p3_catalogo_reconciliado.py --check`. Por tanto, **P3 sigue sin certificarse cerrada**, aunque no hay una nueva decisión editorial pendiente conocida. No se ha publicado contenido nuevo.


## Cierre definitivo y traspaso a P4 · 25/11/2026

**[Acta definitiva de cierre P3](p3-cierre-definitivo-genesis-25-50-2026-11-25.md).** GitHub Actions, ejecución **#37**, confirmada verde mediante captura aportada por el editor: commit `5ef657a` en `main`, duración 9 s. Validación de reconciliación contextual, cobertura léxica CT-32, reproducibilidad del catálogo y protección de fuentes. **Fase P3 cerrada**, sin reclamar exhaustividad semántica absoluta ni adelantar fichas o publicación. La redacción de fichas y relaciones pendientes pasa a **P4** conforme al protocolo. Esta entrada final prevalece sobre los párrafos históricos que describen la fase como abierta.
