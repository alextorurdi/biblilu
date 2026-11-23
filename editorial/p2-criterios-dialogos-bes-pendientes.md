# P2 · Criterios de marcado BES aprobados

**Edición:** BES 2026, Génesis 25–50.  
**Fecha:** 23/11/2026.  
**Estado:** **CRITERIOS APROBADOS por el editor el 23/11/2026**. Aprobación de reglas y de los seis casos identificados, **no** declaración de revisión individual de los 874 versículos ni publicación.  
**Fuente primaria:** [texto BES intacto](../data/genesis_25_50_bes.json).  
**Borrador de formato:** [BES con `parts`](../data/genesis_25_50_bes_formato.json).  
**Control automático:** [informe de la revisión](p2-revision-dialogos-genesis-25-50.json).

## Regla aprobada

Mantener literalmente la ortografía, los signos « » y “ ”, y los cortes de versículo de la BES **en el archivo de texto base y en la capa estructurada `parts`**. **Decisión de presentación posterior (23/11/2026): recuperar las rayas de diálogo del estilo original de BIBLILU**: en el HTML visible, cada apertura de parlamento oral « se muestra como **—**, su cierre » no se muestra; esto ocurre **solo una vez por intervención**, aunque abarque varios versículos. Los pensamientos y frases hipotéticas aparecen en cursiva **sin raya**. Las citas interiores “ ” y ‘ ’ se conservan como citas de segundo o tercer nivel. La transformación es reversible (las comillas originales se registran en atributos `data-source-char` y se recuperan en las pruebas). **Marcar en rojo solamente las intervenciones atribuidas a Dios o las citas textuales explícitas de esas intervenciones**, no todas las palabras de una persona que menciona a Dios.

En la versión web existente de Génesis 1–24 también se resaltan nombres divinos. Se aprueba conservar ese criterio de identificación visual en las nuevas escenas, pero comprobando las apariciones de «Señor» que puedan ser tratamientos humanos. No debe resaltarse automáticamente «Señor» en Gn 43:20 como si se refiriera a Dios, pues se habla a un funcionario de Egipto. El resaltado de nombres debe comprobar el referente y utilizar una capa visual distinta de la marca de discurso divino; las comprobaciones técnicas siguen vigentes.

## Seis casos resueltos en sus criterios de marcado

| Pasaje | Estado del borrador | Valoración y propuesta |
|---|---|---|
| **Gn 26:7** | «Es mi hermana» en diálogo; «Es mi mujer» como discurso hipotético y el pensamiento posterior como pensamiento. | **Mantener**: el texto contrapone lo que Isaac dice, lo que teme decir y lo que piensa. No tratar la frase hipotética como diálogo pronunciado. |
| **Gn 31:11–13** | Palabras del ángel en cursiva, sin rojo. | **Criterio aprobado: cursiva sin rojo**. El mensajero habla en primera persona y se identifica como «el Dios de Betel» (31:13). Marcar en rojo implicaría atribuir su discurso a Dios; mantenerlo en cursiva evita decidir editorialmente una identidad discutida. |
| **Gn 31:29** | Labán cita literalmente las palabras de Dios: la cita interna está en rojo. | **Mantener** el rojo limitado a la cita interna, no a todo el parlamento de Labán. |
| **Gn 32:9** | En su oración, Jacob reproduce palabras divinas en segundo nivel de comillas, marcadas en rojo. | **Mantener**, por coherencia con otros discursos directos de Dios citados por humanos. |
| **Gn 32:26–29** | La voz del luchador de Jaboc está en cursiva, sin rojo. | **Criterio aprobado: cursiva sin rojo**: Gn 32:24 lo presenta como «un hombre» y 32:30 incluye la interpretación de Jacob. El color rojo podría anticipar una conclusión exegética. |
| **Gn 48:4** | Jacob cita en un discurso humano palabras de Dios que aparecen en comillas internas y en rojo. | **Mantener** rojo solo en la cita atribuida a Dios, no en las palabras narrativas de Jacob. |

## Cuestiones de formato aprobadas (sin alterar el texto)

1. **Menciones de Dios y Señor:** en capítulos 1–24, los nombres divinos aparecen habitualmente en rojo aunque el narrador los mencione. Para la BES, comprobar el referente de cada «Señor» antes de resaltarlo, y evitar pintar de rojo tratamientos humanos o referencias a «dioses» ajenos. Criterio aprobado: registrar estos resaltados visuales separadamente de `parts.kind=divine`, que debe significar únicamente intervención de Dios.
2. **Cita anidada:** conservar las comillas BES intactas en los datos. En la web, transformar exclusivamente las comillas externas de intervenciones o pensamientos; mantener visibles las comillas **interiores** “ ” y ‘ ’ cuando reproducen un discurso dentro de otro. La raya sustituye solo la apertura del parlamento oral principal, no se añade una raya a cada versículo ni a una cita de segundo nivel.
3. **Cortes entre versículos:** las comillas que comienzan en un versículo y terminan en el siguiente deben permanecer en cursiva en todo el tramo y salir del estilo en el versículo de cierre.
4. **Disposición:** la previsualización actual no incluye ilustraciones, mapas o árboles; corresponden a P5 y deben respetar el plan de P1. Las notas nuevas, referencias y fichas se elaboran en las fases posteriores.
5. **Puntos de lectura:** cada página BES y ambos índices deben identificar la traducción en uso. El enlace de ida desde «Familia» se añadirá al preparar publicación, sin cambiar su texto ni sus notas RVR1960.

## Aplicación de las convenciones históricas de diálogo · 23/11/2026

Tras revisar [Legado](tareas-legado.md), [Cumplimiento](tareas-cumplimiento.md) y [Familia](tareas-familia.md), el editor ordenó restaurar estas convenciones en **las 19 escenas nuevas**: discurso humano en **cursiva y negro, con raya (—)**; pensamientos en **cursiva sin raya**; palabras de Dios en **rojo y cursiva**; palabras del ángel en **negro** salvo cita explícita de Dios; narrador en redonda; cambio de interlocutor identificado por una nueva raya.

**Regla de fidelidad:** la BES de `data/genesis_25_50_bes.json` y `data/genesis_25_50_bes_formato.json` debe conservar todas las comillas y versículos. Solo el **renderizado HTML no publicado** efectúa esta sustitución visual, comprobable por pruebas de recuperación del texto literal a partir de sus atributos de procedencia.

La disposición en **387 párrafos** y sus **874 anclas** se conserva. El cambio de voz se indica con una raya por apertura de intervención; las citas anidadas no cuentan como un cambio de hablante. Queda pendiente la revisión visual individual, sin autorizar publicación ni cambiar los anteriores Gn 1–24.

## Resolución editorial

El editor **aprobó íntegramente los criterios y las seis decisiones**. Se mantiene el texto BES literal, las comillas originales, la diferenciación entre discurso y nombres divinos, los criterios de casos particulares y la cautela en la identificación del ángel y del adversario del Jaboc. **No se cierra aún P2**, pues siguen pendientes el control editorial integral y la revisión visual de los borradores. `revisado=false` no deberá cambiar automáticamente por esta aprobación de criterios.
