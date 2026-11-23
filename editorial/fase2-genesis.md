# Fase 2 · Génesis 25–50 — BES 2026, marcado e índices

**Fecha de inicio:** 23/11/2026. **Actualización editorial:** 23/11/2026.  
**Estado:** **REVISIÓN VISUAL APROBADA — 19 BORRADORES BES EN 387 PÁRRAFOS; CONTROL TEXTUAL/EDITORIAL INTEGRAL Y VÍNCULOS DE FICHAS PENDIENTES.**  
**Alcance invariable de Etapa I:** 19 escenas, Gn 25:1–50:26, traducción **La Biblia en Español Sencillo 2026 (BES)**. Las 15 escenas de Gn 1–24 **conservan RVR1960** hasta la segunda etapa, sin cambios de texto ni notas.

**Documentos rectores:** [Protocolo P0–P9](protocolo-libros.md) · [BES en dos etapas](plan-dos-etapas-bes-genesis.md) · [P1 aprobada](fase1-genesis.md) · [Distribución de recursos](plan-ubicacion-escenas-genesis-25-50.md).

## Derechos y fuente oficial comprobados

- **Edición:** *La Biblia en Español Sencillo 2026*, publicada en eBible, traducción y edición de **Irma Flores**, AudioBiblia.org, fecha de la fuente **30/10/2026**.
- **Licencia declarada:** **dominio público**, según [página de derechos oficial de eBible](https://ebible.org/spabes/copyright.htm).
- **Génesis por capítulos:** [https://ebible.org/spabes/GEN.htm](https://ebible.org/spabes/GEN.htm).
- **Paquete USFM oficial:** [https://ebible.org/Scriptures/spabes_usfm.zip](https://ebible.org/Scriptures/spabes_usfm.zip); enlazado desde la [ficha de descargas](https://www.ebible.org/find/details.php?id=spabes).
- La declaración de dominio público permite trabajar sobre esta versión según la información del distribuidor; conservar atribución y procedencia documental aun cuando no se imponga una licencia de atribución.
- La traducción **no será homogeneizada con la RVR1960**: respetar literalmente los cambios de vocabulario y los nombres propios de la BES, anotando variantes y diferencias donde tengan repercusión editorial.

## Trabajo efectivamente registrado

1. **Catálogo P1:** [19 escenas aprobadas](catalogo-escenas-genesis-25-50.json), 874 versículos distribuidos sin solapamientos. Texto anterior de Gn 1–24: 659 versículos.
2. **Rutas y anclas:** [p2-rutas-genesis-25-50.json](p2-rutas-genesis-25-50.json) describe las 19 rutas y el índice tradicional de los 26 capítulos, con enlaces `gn-<capítulo>-<versículo>`.
3. **Validador y previsualizador:** [prepare_genesis_p2.py](../scripts/prepare_genesis_p2.py) exige datos con textos completos y admite marcar discursos/pensamientos/palabras divinas de modo reversible. Genera previsualizaciones en **`build/p2/`**, nunca en `docs/`.
4. **Importador para BES 2026:** [import_bes_genesis.py](../scripts/import_bes_genesis.py) descarga o acepta el ZIP USFM de eBible; selecciona Génesis, extrae sus versos, comprueba la cobertura exacta de 874 y verifica un versículo testigo (25:1). Escribe **`data/genesis_25_50_bes.json`** y **`editorial/procedencia-bes-genesis-25-50.json`** con hash de la fuente. **Importación ejecutada satisfactoriamente el 23/11/2026** mediante [GitHub Actions](https://github.com/alextorurdi/biblilu/actions/runs/45210964335), con corrección de etiquetas léxicas Strong y separadores USFM. La fuente está en [data/genesis_25_50_bes.json](../data/genesis_25_50_bes.json).
5. **Prueba sintética:** [test_genesis_p2.py](../scripts/test_genesis_p2.py) prepara textos de prueba y comprueba las 874 anclas y que el marcado no cambie el texto; se ha ejecutado correctamente en GitHub Actions el 23/11/2026.
6. **Esquema de datos:** [esquema-fuente-genesis-25-50.json](esquema-fuente-genesis-25-50.json). El fichero BES debe mantenerse separado del `data/genesis.json` histórico de RVR60.
7. **Cabeceras por traducción:** las 19 futuras escenas estarán identificadas **BES 2026**. Durante Etapa I, los índices tendrán una nota inequívoca del régimen mixto **1–15 RVR1960 / 16–34 BES 2026**, evitando anunciar todo Génesis como una única traducción.

## Instrucciones de la importación

```bash
# Paso I: importar desde el paquete USFM oficial BES 2026
python scripts/import_bes_genesis.py --download

# Alternativa: descargar primero el ZIP desde eBible
python scripts/import_bes_genesis.py --zip /ruta/spabes_usfm.zip

# Paso II: validar los datos y la estructura P1
python scripts/prepare_genesis_p2.py --structure
python scripts/prepare_genesis_p2.py --check-source
python scripts/test_genesis_p2.py

# Paso III: generar páginas e índices de borrador, NO publicables
python scripts/prepare_genesis_p2.py --build-draft
```

Los archivos resultantes de `build/p2/` son solo borradores de estructura y texto. La edición narrativa y tipográfica final —diálogos, cursivas, pensamientos, guiones y las palabras de Dios en rojo— requiere revisión textual según las decisiones de BIBLILU. Las herramientas automáticas **no deben adjudicar todas las palabras de «Dios» o «Señor» a un discurso divino**.


## Resultado de la importación · 23/11/2026

- **Archivo de versículos:** [`data/genesis_25_50_bes.json`](../data/genesis_25_50_bes.json), 874 registros de BES 2026, capítulos 25–50 (26 capítulos); `revisado=false` hasta la revisión editorial del marcado.
- **Origen:** archivo `02-GENspabes.usfm` extraído del [ZIP USFM oficial](https://ebible.org/Scriptures/spabes_usfm.zip).
- **SHA-256 del paquete fuente:** `45c412d35fd1cbcf51ad4405ed0c3dea840cb7db39b157c0bbebd244fe51c578`.
- **Metadatos trazables:** [`editorial/procedencia-bes-genesis-25-50.json`](procedencia-bes-genesis-25-50.json).
- **Verificaciones superadas:** cobertura exacta de 874 versículos, sin duplicaciones, huecos, textos vacíos ni residuos `|strong="..."`; también detecta separadores USFM falsos tras «, ¿ e ¡; prueba sintética del generador y controles de no modificación de los archivos RVR1960.
- **Ejecución final:** [GitHub Actions, importación BES](https://github.com/alextorurdi/biblilu/actions/runs/45210964335) — **success**. La acción confirma que no se han modificado `docs/`, `data/genesis.json` ni las fuentes protegidas de las quince escenas antiguas.
- **Límite:** esta importación no constituye el marcado narrativo final, ni crea o publica las escenas 16–34. Los textos continúan pendientes de revisión editorial en P2.

## Marcado narrativo y borradores P2 · 23/11/2026

**Ejecución:** [GitHub Actions · Preparar Fase 2 BES](https://github.com/alextorurdi/biblilu/actions/runs/45213289258), **completada correctamente**, sin escrituras en `docs/`, `data/genesis.json` ni `editorial/approved-pages/genesis/`.

- **874 versículos originales sin modificar.** El archivo de formato [`data/genesis_25_50_bes_formato.json`](../data/genesis_25_50_bes_formato.json) es una capa separada: cada fragmento `parts` (narración, diálogo humano, pensamiento, voz divina) se concatena hasta formar exactamente el texto del versículo BES. El registro `revisado=false` permanece en los 874 versículos.
- **Marcado provisional:** 325 aperturas de discurso humano, 14 de discurso divino o citas textuales atribuidas a Dios, 6 de pensamiento. En total, 491 segmentos de diálogo, 21 segmentos divinos (incluidas continuaciones entre versículos) y 6 segmentos de pensamiento.
- **Alcance de la atribución:** las palabras de Dios en Gn 25:23; 26:2–5, 26:24; 28:13–15; 31:3, 31:24; 35:1, 35:10–12; 46:2–4, y las citas directas atribuidas a Dios en 31:29, 32:9 y 48:4 están marcadas provisionalmente en rojo. Las intervenciones del adversario de Gn 32:26–29 y el ángel del sueño de Gn 31:11–13 se dejan en diálogo no divino mientras se revisa su identificación.
- **Control de ambigüedades:** [`editorial/p2-revision-dialogos-genesis-25-50.json`](p2-revision-dialogos-genesis-25-50.json) registra los casos pendientes. El informe no declara revisada la atribución teológica ni el estilo.
- **Criterios aprobados por el editor:** [p2-criterios-dialogos-bes-pendientes.md](p2-criterios-dialogos-bes-pendientes.md) recoge la aprobación expresa de los seis pasajes (26:7; 31:11–13 y 31:29; 32:9 y 32:26–29; 48:4) y la separación entre el rojo de nombres divinos y el rojo de intervenciones divinas. El adversario del Jaboc y el mensajero de Gn 31 permanecen en cursiva sin rojo.
- **Generación de las 19 escenas BES:** páginas HTML, encabezados con identificación **BES 2026**, navegación anterior/siguiente, anclas de los 874 versículos y **dos índices** creados exclusivamente en `build/p2/`. Los borradores se guardaron como **artefacto de GitHub Actions** llamado `biblilu-borradores-bes-p2` durante 14 días; [abrir ejecución para obtener el artefacto](https://github.com/alextorurdi/biblilu/actions/runs/45213289258).
- **Pruebas P2:** [`scripts/test_marcado_bes_p2.py`](../scripts/test_marcado_bes_p2.py) y pruebas de páginas/índices superadas. Las quince escenas anteriores quedaron protegidas por comparaciones SHA-256 y no se alteraron.
- **Nota de presentación:** la BES conserva en el borrador sus comillas « » y “ ” originales en cursiva. No se han añadido guiones nuevos que cambien la literalidad del texto. El tratamiento gráfico definitivo de los recursos corresponde a fases posteriores.

**Condiciones antes de declarar P2 completamente cerrada:** los **criterios** de pensamiento, discursos, citas divinas y nombres divinos **están aprobados**. Falta el control editorial y visual integral de los 874 versículos y las 19 páginas, la revisión de sus enlaces y navegación y la aprobación de cierre. Todos los versículos conservan `revisado=false` hasta ese control. **Nada de esto implica publicación.**

## Aprobación del formato y nueva prueba · 23/11/2026

- El editor aprobó **todos los criterios** propuestos para las seis situaciones de Gn 26, 31, 32 y 48, incluidos la cursiva **sin rojo** en las palabras del ángel en Gn 31:11–13 y del adversario en Gn 32:26–29, y el rojo en las citas internas de Dios (31:29, 32:9, 48:4).
- Se ha actualizado el registro [`p2-criterios-dialogos-bes-pendientes.md`](p2-criterios-dialogos-bes-pendientes.md) para reflejar aprobación, sin confundirla con revisión integral de los 874 versículos.
- Se aplicó una **capa visual independiente de nombres divinos**, conservando el significado de `parts.kind=divine` para la **voz de Dios**. La BES contiene **99 apariciones de «Dios» y 39 de «Señor»**, de las que se excluye **Gn 43:20 «Señor»**, tratamiento de un funcionario egipcio; los 27 «señor» minúsculos y los «dioses» no se clasifican como nombre divino. Se registran 137 apariciones candidatas en esta fase; su control editorial completo sigue pendiente.
- **Prueba automática superada:** [GitHub Actions · P2 BES aprobado por criterios](https://github.com/alextorurdi/biblilu/actions/runs/45216746610). Se verifica integridad de los 874 textos, las 19 páginas no públicas, los dos índices, las excepciones aprobadas y la protección SHA-256 de las quince escenas anteriores.
- La ejecución genera un nuevo paquete de borradores de trabajo. **No se han integrado páginas nuevas en el directorio público `docs/` ni alterado los 659 versículos RVR1960.**

## Párrafos narrativos BES · 23/11/2026

**Orden editorial:** dejar de presentar una línea independiente por versículo y volver a la lectura continua, prosaica y moderna, sin modificar una palabra de la BES. **Ejecución técnica completada**, sujeta a inspección visual de la distribución.

- [Plan editorial de 387 párrafos para las 19 escenas](p2-parrafos-genesis-25-50.json): los límites se fijaron atendiendo a unidades narrativas, cambios de interlocutor, genealogías, bendiciones y la estructura de la escena; **no** se dividió mecánicamente cada cierto número de versículos.
- En «De Abraham a Isaac» los grupos son **25:1–4, 25:5–6, 25:7–8, 25:9–10, 25:11, 25:12–16, 25:17, 25:18**. La división inicial de siete párrafos pasa a ocho porque el **Árbol 10 debe insertarse después de 25:17**; así no se rompe después el párrafo al incorporar el recurso.
- En las 19 escenas se preservan los cortes necesarios tras versículos aprobados de P1 para **mapas, árboles e imágenes en móvil o ambos formatos**. Los lugares definitivos de los recursos continúan siendo los acordados en P1.
- Cada versículo sigue teniendo su ancla `gn-capítulo-versículo`, un número enlazable en superíndice y el **texto BES íntegro**. La composición HTML cambia a **párrafos literarios** con fragmentos de versículo en línea; se conserva la cursiva y los resaltados divinos aprobados.
- El generador [`scripts/prepare_genesis_p2.py`](../scripts/prepare_genesis_p2.py) incorpora el renderizado de párrafos y una hoja CSS exclusivamente en **`build/p2/assets/p2-prose.css`**, sin alterar el CSS ni las escenas públicas.
- **Prueba correcta:** [GitHub Actions · Generación de borradores narrativos](https://github.com/alextorurdi/biblilu/actions/runs/45223416217); 19 escenas, **387 párrafos y 874 anclas** verificados. Artefacto `biblilu-borradores-bes-p2`, disponible hasta el **07/12/2026** en la sección Artifacts de dicha ejecución.
- El flujo comprobó por SHA-256 que **Gn 1–24 RVR1960 y sus páginas originales permanecen intactos**.
- **Aún pendiente:** inspeccionar visualmente cortes, diálogos largos, pasajes genealógicos y poemas en escritorio/móvil. La aprobación del método de agrupación no equivale a dar por revisado cada corte y los 874 registros siguen con `revisado=false`.

## Recuperación de las rayas de diálogo originales · 23/11/2026

**Instrucción editorial expresa y ejecutada:** seguir las convenciones históricas documentadas en [Legado](tareas-legado.md), [Cumplimiento](tareas-cumplimiento.md) y [Familia](tareas-familia.md).

- **Diálogo humano:** cursiva, color normal y **raya «—»** al comienzo de cada intervención; no usar una raya nueva al continuar un parlamento a través de un número de versículo.
- **Pensamiento o frase no pronunciada:** cursiva, **sin raya**; en el HTML visible se omiten las comillas externas de esta clase, mientras la fuente BES conserva todas sus comillas.
- **Voz divina:** cursiva y rojo, con raya al inicio del parlamento directo. Los nombres divinos siguen coloreándose según el referente, por separado de las intervenciones.
- **Ángel / adversario del Jaboc:** se mantienen las decisiones previas de cursiva y negro (Gn 31:11–13; 32:26–29), excepto las citas expresamente atribuidas a Dios, coloreadas en rojo.
- **Citas dentro de un parlamento:** las comillas internas “ ” y ‘ ’ continúan visibles; una cita secundaria no abre una nueva raya de diálogo. **El cambio de interlocutor** en un mismo versículo sí produce una raya independiente, sin duplicar el texto de la atribución narrativa.
- **Traducción BES intacta:** las comillas « » originales permanecen en los 874 objetos de origen y en la capa `parts`; el HTML de borrador sustituye solo la apertura externa por la raya y oculta el cierre. Se conserva la correspondencia en `data-source-char` y las pruebas recuperan **exactamente** el texto original desde el HTML, incluidas las comillas y puntuación.
- **Cobertura verificada automáticamente:** **299 aperturas de parlamento con raya** (288 humanas y 11 divinas) y **6 pensamientos** sin raya. Las **40 comillas anidadas** de cita o atribución no generan rayas nuevas. Siguen intactos los **387 párrafos**, los **874 enlaces de versículo** y los 19 borradores.
- **Solo borradores:** estas reglas se implementaron en [`scripts/prepare_genesis_p2.py`](../scripts/prepare_genesis_p2.py) con estilos únicamente de `build/p2/assets/p2-prose.css`. No se alteraron el texto RVR1960 de Génesis 1–24, sus fuentes aprobadas, `docs/` ni el CSS publicado.

**Estado:** implementación técnica verificada; el control visual individual del formato y la revisión editorial integral de los 874 versículos **siguen pendientes antes del cierre P2**. La acción de pruebas regenerará el ZIP disponible en GitHub Actions; su finalización se comprobará por separado.

## Regla adicional de salto de línea antes de rayas · 23/11/2026

**Instrucción editorial ejecutada:** cada intervención que comienza con raya (—) se coloca en **una línea propia**, como en una novela moderna, aunque la frase introductoria del narrador esté dentro del mismo versículo. Ejemplo: **Gn 26:2**, tras «El Señor se apareció a Isaac y le dijo:», el discurso divino comienza en la línea siguiente y continúa en **Gn 26:3–5** sin añadir nuevas rayas.

- **Mismo versículo, varios hablantes:** cada parlamento nuevo con raya pasa a su propia línea, sin romper artificialmente el párrafo literario.
- **Intervención al principio de un versículo:** número de versículo y raya van juntos en la misma línea; si abre también un párrafo, se omite un salto redundante.
- **Pensamientos y citas dentro de otro discurso:** no se fuerzan saltos de línea ni rayas.
- **Integridad:** se introducen saltos HTML exclusivamente en el borrador visual. Los 874 textos BES con sus comillas originales, los 387 párrafos y los enlaces no cambian.
- **Validación automática:** [scripts/test_marcado_bes_p2.py](../scripts/test_marcado_bes_p2.py) comprueba Gn 26:2–5, 26:9, las intervenciones al principio de un versículo y la recuperación literal de la BES. [GitHub Actions: borradores actualizados](https://github.com/alextorurdi/biblilu/actions/runs/45266022438) finalizó correctamente y verificó la protección de las 15 escenas anteriores.

La Fase 2 sigue abierta para revisión visual y editorial. **No se han publicado las escenas nuevas.**
## Refinamiento del fin de diálogo y de los incisos · 23/11/2026

**Aprobado e implementado.** El final de un parlamento seguido por narración independiente o por la introducción de otro hablante impone una nueva línea, además de la nueva línea inicial que ya se utiliza para cada raya. En cambio, si el narrador intercala una atribución o nota breve **y continúa hablando el mismo personaje**, el inciso se dispone entre rayas dentro de la misma línea.

- **Ejemplo comprobado:** Gn 26:8–11. Tras la pregunta de Abimelec, «Isaac respondió:» comienza en otra línea y su réplica se abre también en línea propia. La intervención de Abimelec en Gn 26:10 conserva su propio inicio. No se duplica el punto ni se modifica el texto de la BES.
- **Continuaciones expresamente identificadas:** Gn 27:36, 43:29 y 45:4; el generador también admite incisos entre comas cuando es explícito que sigue hablando la misma persona.
- **Números y enlaces:** cuando cambia la línea al comenzar otro versículo, el superíndice y sus palabras permanecen juntos; no hay interrupciones adicionales cuando una cita simplemente continúa en otro versículo.
- **Pruebas aprobadas:** [GitHub Actions](https://github.com/alextorurdi/biblilu/actions/runs/45268499246), con los 874 textos recuperables, 387 párrafos, 19 escenas, 299 aperturas orales y protección de los quince capítulos/escenas antiguos. [Criterio editorial documentado](p2-criterios-dialogos-bes-pendientes.md).

**No publicado.** P2 continúa pendiente de la revisión visual de las 19 escenas y el control integral de las 874 lecturas.

## Aprobación visual comunicada por el editor · 23/11/2026

El editor ha confirmado expresamente **«revisión visual completada»** para los borradores de las 19 escenas BES (Génesis 25–50), después de las correcciones de párrafos, guiones, cambios de interlocutor y continuidad narrativa. **La revisión visual se considera terminada y aprobada.**

Se mantienen por separado los controles de integridad automáticos que ya superó el flujo, y la **revisión editorial integral de las 874 lecturas/atribuciones** que el registro anterior todavía marca como pendiente. Esta confirmación visual no permite cambiar automáticamente los 874 indicadores `revisado=false` a `true`, ni presupone que los vínculos de apéndices estén listos. Las referencias a apéndices se podrán completar con los identificadores comprobados en P3.

**Siguiente actividad del protocolo:** iniciar **P3, extracción y clasificación única** de las ocho categorías en Gn 25–50, distinguiendo entidades nuevas y nuevas menciones de fichas existentes. No publicar las escenas ni migrar Gn 1–24 (Etapa II).

## Condiciones para cerrar P2

- [x] Pasaje, 19 escenas, títulos y distribución aprobados.
- [x] Rutas y diseño de los dos índices definidos.
- [x] BES 2026 localizada y licencia declarada como dominio público por el distribuidor.
- [x] Importador, comprobador y generador de borradores preparados en el repositorio.
- [x] **Importación real de los 874 versículos BES 2026** y registro SHA-256 del ZIP oficial (ver [procedencia](procedencia-bes-genesis-25-50.json)).
- [x] **Comprobación estructural:** 26 capítulos, 874 versículos únicos y ordenados, sin vacíos ni restos USFM; cotejos textuales de control con la edición HTML oficial de 25:1, 25:23, 45:3 y 50:26. **Pendiente:** revisión editorial completa del texto y de los discursos.
- [x] Marcado reversible de diálogo, pensamiento y voz divina en los 874 versículos; **seis casos específicos y reglas generales aprobados editorialmente el 23/11/2026**; pendiente el control integral versículo por versículo.
- [x] 19 páginas en **387 párrafos narrativos**, con 874 anclas de versículo, ambos índices y controles automáticos superados; disponibles como artefacto no público. **Revisión visual completada y aprobada por el editor; pendiente el control textual/editorial integral de las 874 lecturas y las referencias definitivas a fichas.**
- [x] La acción de importación verificó mediante sumas SHA-256 que el texto RVR1960 de Gn 1–24 y las quince páginas editoriales protegidas no sufrieron modificaciones. Se ha preparado la identificación de la edición mixta, aún no aplicada a páginas públicas.

**No iniciar como si P2 hubiera finalizado**, ni publicar automáticamente. P3–P9 se desarrollarán secuencialmente sobre las escenas BES, siguiendo los puntos de aprobación del protocolo.
