# Fase 3 · Extracción y clasificación de Génesis 25–50

**Inicio:** 23/11/2026. **Texto base:** BES 2026. **Estado:** **EN CURSO — barrido inicial de 874 versículos y revisión contextual del Onomástico por lotes. Lote 1 aprobado parcialmente; lotes 2 y 3 preparados para revisión editorial.**

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

**Estado del lote:** propuestas de asignación y nuevas fichas **pendientes de aprobación**. No se han modificado ni vinculado fichas históricas.

### Resolución editorial aplicada · Primer lote del Onomástico

El editor aprobó «Zimrán» como variante de `onomastico/zimram`, las **dos entradas separadas Zohar (heteo) / Zohar (hijo de Simeón)** y las **dos entradas diferenciadas Hadad (hijo de Ismael) / Hadad (rey de Edom)**.

Se han actualizado [las entradas fuente](../data/entries.json) y el [registro maestro](../data/registro_maestro.json), que cuenta ahora **451 rutas/identificadores**, incluidas 291 entradas onomásticas. Para el hijo de Ismael se conserva el ID `onomastico/hadar` por compatibilidad histórica: ese mismo individuo aparece como **Hadar en RVR1960** y **Hadad en BES 2026**. Se ha añadido la única ficha que faltaba: `onomastico/zohar-heteo`.

El [extractor P3](../scripts/extract_genesis_p3.py) asigna los casos aprobados en Gn 25:2, 25:9, 25:15 y 36:35–36, impidiendo cruces con sus homónimos. La BES usa **«Zera» en Gn 46:10** para el hijo de Simeón que se llama **Zohar** en RVR1960: se registra aparte como **diferencia textual que debe contrastarse** con la ficha histórica, sin dirigirla a `onomastico/zera` (hijo de Reuel).

[Detalle del primer lote aprobado parcialmente](p3-onomastico-lote1-genesis-25-1-18.md). **P3 sigue abierta:** no se interpretan como aprobadas las demás identificaciones ni se publican las escenas nuevas.

### Seguimiento de lotes onomásticos

| Lote | Tramo | Estado | Documento |
|---|---|---|---|
| 1 | Gn 25:1–18 | Aprobación parcial; Zimram, Zohar y Hadad incorporados | [Lote 1](p3-onomastico-lote1-genesis-25-1-18.md) |
| 2 | Gn 25:19–34 | Propuesta pendiente de aprobación; siete personas y Edom como sobrenombre de Esaú | [Lote 2](p3-onomastico-lote2-genesis-25-19-34.md) |
| 3 | Gn 26:1–35 | Propuesta pendiente de aprobación; Ahuzat y Beeri requieren nuevas fichas en P4 | [Lote 3](p3-onomastico-lote3-genesis-26.md) |

**Incidencia nueva del lote 3:** en Gn 26:33 «Seba» nombra un **pozo**, no una persona; la salida automática P3 lo considera erróneamente un candidato onomástico. La reclasificación está propuesta, pero el extractor aún no se ha corregido. No se han cambiado fichas ni contenido publicado por este lote.

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

## Precauciones específicas

- **Abimelec / Ficol:** mantener las fichas y sus menciones, sin resolver por automatismo la identidad personal entre generaciones.
- **Esposas de Esaú y Timna:** preservar designaciones y homónimos. No fusionar Ada, Basemat, Judit, Mahalat, Aholibama ni las Timna.
- **Hanoc, Seba, Heber, Saúl, etc.:** cuando hay varias fichas que comparten nombre, conservar los identificadores candidatos y exigir el contexto genealógico para elegir.
- **Israel, Edom y otras denominaciones:** comprobar si cada pasaje designa a una persona, pueblo o territorio, en vez de asignar por una coincidencia literal.
- **Variante textual BES respecto de RVR1960:** registrar la forma encontrada como *variante por estudiar*, no alterar títulos, URLs o textos de fichas aprobadas.

## Criterio de cierre de P3

**No está cerrada aún.** Requiere extraer todas las categorías, revisar el catálogo contextualizado, separar fichas existentes de fichas futuras y aprobar el conjunto de incidencias editoriales. Las fichas no se redactan hasta P4.

El informe automático valida **cobertura y literalidad de los candidatos** pero no reemplaza la revisión de nombres o identidades por una persona.
