# BIBLILU · Protocolo editorial para libros completos (P0–P9)

**Estado: APROBADO por el editor el 20 de noviembre de 2026.**
**Alcance:** todos los libros bíblicos que incorpore BIBLILU, comenzando por la continuación de Génesis.
**Naturaleza:** documento rector permanente de trabajo, ubicado en el repositorio. No es una página pública.
**Principio:** cada dato se investiga una vez, se registra en su fuente editorial y se reutiliza mediante identificadores y relaciones estables. Las fichas, escenas y recursos ya aprobados no se reabren ni se sobrescriben por defecto.

> **Instrucción para nuevas conversaciones:** antes de proponer, editar, implementar o publicar un libro completo de BIBLILU, leer este protocolo y el informe del libro (`editorial/fase0-<libro>.md` o su equivalente). Consultar las fuentes vigentes del repositorio, no reconstruir decisiones por suposiciones. Si hay contradicción entre un borrador y una decisión editorial posterior aprobada, prevalece la más reciente; distinguir siempre propuesta, aprobación, implementación y publicación.

## Reglas transversales

1. **Preservación editorial.** Respetar la estructura, los títulos, las notas y los textos aprobados. No alterar el texto bíblico por una corrección estilística o una inferencia: la base es Reina-Valera 1960 según los documentos aportados por el editor. Las citas, diálogos, pensamientos, guiones y palabras atribuidas a Dios conservarán el formato editorial vigente; las palabras divinas se marcan en rojo. Las excepciones de enlaces dentro de intervenciones divinas deberán ser explícitas y preservar el color y el texto.
2. **Escenas ≠ capítulos.** Las escenas son unidades narrativas y pueden atravesar capítulos; conservar además un índice tradicional por capítulos y enlaces a versículos concretos. Identificadores canónicos estables.
3. **Registro maestro interno.** Usar `data/registro_maestro.json` como índice técnico **generado**, nunca como segunda versión manual de las fichas. Fuente y generador iniciales: `scripts/build_registry.mjs`. No crea una página de lectura; el repositorio es público, de modo que los archivos son accesibles en GitHub. Mantener IDs y URLs históricas, remisiones y variantes aprobadas. No fusionar homónimos, nombres personales, tribus o lugares solo por coincidencia ortográfica; registrar incertidumbres. El caso de Génesis está documentado en `editorial/criterios-identidades-genesis.md`.
4. **Extracción única.** Una pasada sistemática por el texto, con ocho categorías: personas; lugares; seres vivos naturales y seres celestiales; materiales; tribus y pueblos; objetos y símbolos; instrumentos musicales; pesos, medidas y monedas. Distinguir *entidad nueva* de *nueva mención de entidad existente*. Cada resultado incluye categoría, variantes, referencias a versículos y posible correspondencia a ficha existente. Los nombres ambiguos requieren revisión humana.
5. **Bibliografía continua.** Recoger y normalizar cada fuente en el momento de investigación y redacción, con identificadores estables y verificación de datos bibliográficos; al cierre, deduplicar y revisar citas y enlaces. No inventar referencias.
6. **Estados de seguimiento.** Para cada elemento conservar al menos: **Detectado → Propuesto → Aprobado → Implementado → Publicado**; además permitir *Descartado*, *En revisión* o *Pendiente de verificación*. No confundir contenido elaborado con contenido publicado. Mantener una matriz por libro y las tareas pendientes.
7. **Aprobación por lotes.** Solicitar aprobación editorial en los puntos de decisión previstos, sin volver a preguntar por decisiones ya tomadas. Redactar propuestas por categoría o bloques narrativos para ahorrar revisiones; una aprobación no significa publicación automática de materiales no aprobados.
8. **Implementación gradual y publicación controlada.** Pueden integrarse bloques aprobados durante el proyecto en una versión de trabajo. Antes de publicarlos, ejecutar comprobaciones. Distinguir envío del código, compilación correcta y despliegue accesible. No afirmar que se publicó sin comprobarlo.
9. **Fuentes protegidas.** Algunas escenas se conservan en `editorial/approved-pages/`; el generador añade después enlaces a apéndices y normalización bibliográfica. No sustituir automáticamente las fuentes editoriales por HTML generado ni asumir que deben ser idénticos byte a byte.
10. **Dispositivos y recursos.** Comprobar diseño en escritorio y móvil; las imágenes, mapas y árboles pueden tener colocaciones distintas según el dispositivo. Mantener referencias, visores y enlaces bidireccionales. Para seres sobrenaturales, no añadir ilustraciones a las fichas sin nueva autorización editorial.
11. **Compatibilidad de pasos antiguos.** Los P1–P30 del borrador original se conservan conceptualmente, pero se ejecutan dentro de las diez fases siguientes, evitando extracciones y revisiones redundantes.

## P0 · Preparación e inventario

- Inspeccionar el repositorio real, despliegue y estado de las fuentes editoriales.
- Identificar qué capítulos, escenas, fichas, notas, imágenes, artículos, mapas y árboles ya existen, cuáles están aprobados, implementados o publicados y qué permanece pendiente.
- Crear o actualizar el registro maestro de entidades a partir de las fuentes existentes, sin duplicar descripciones. Anotar remisiones, homónimos, variantes y relaciones con escenas, mapas y genealogías.
- Preparar un informe de Fase 0 y una matriz de seguimiento por libro (estado por fase y por escena).
- Registrar explícitamente los problemas del generador, pruebas y despliegue; no reinterpretar decisiones antiguas.
- **Salida:** inventario verificado, lista de pendientes, diagnóstico inicial y base técnica para las siguientes fases.

**Génesis (primer caso):** `editorial/fase0-genesis.md`, `editorial/inventario-genesis.json` y `scripts/audit_genesis_p0.mjs`. El tramo Génesis 1–24 tiene 15 escenas aprobadas; se continúa desde Gn 25. El resto no debe sobrescribir el trabajo anterior.

## P1 · Estructura y escenificación

1. Leer el libro completo y analizar sus bloques temáticos y narrativos.
2. Proponer la división en escenas y su titulación. No imponer los límites de los capítulos tradicionales.
3. Precisar inicio y final de cada escena mediante referencias de versículos, evitando solapamientos y vacíos.
4. Identificar preliminarmente mapas, genealogías, ilustraciones y posibles artículos de fondo.
5. **Punto de aprobación editorial:** estructura y títulos de **todo el libro** (o solamente de la parte todavía no aprobada, como Génesis 25–50).

## P2 · Texto bíblico y formato

1. Incorporar el texto RVR1960 desde las fuentes editoriales autorizadas y distribuirlo según las escenas aprobadas.
2. Aplicar diálogos, guiones, cursivas, pensamientos, intervenciones divinas en rojo y convenciones establecidas.
3. Conectar los índices de escenas y capítulos tradicionales, navegación anterior/siguiente y anclas de versículos.
4. Preparar referencias a los apéndices mediante identificadores estables, conservando la redacción original.
5. **Control:** cobertura de capítulos y versículos, orden, ausencia de omisiones y duplicaciones, marcado y anclas.

## P3 · Extracción y clasificación única

Recorrer el libro una sola vez para detectar todas las categorías, con referencias exactas: personas; lugares; seres vivos y celestiales; materiales; tribus; objetos y símbolos; instrumentos musicales; pesos, medidas y monedas. Distinguir entidades ya conocidas, nuevas entidades, remisiones, variantes, homónimos e identidades inciertas. No crear fichas ni identidades por automatismo sin contraste editorial. **Salida:** catálogo de extracciones por categoría y lista de actualizaciones a fichas existentes.

## P4 · Fichas de apéndices

Trabajar por lotes de cada uno de los ocho apéndices existentes. Crear fichas nuevas, actualizar las existentes con nuevas menciones y resolver remisiones según los criterios ya aprobados. Emplear los esquemas propios de cada categoría; incluir referencias bíblicas, relaciones internas, bibliografía y distinción entre hecho textual, interpretación e hipótesis. **Punto de aprobación editorial:** nuevas fichas y modificaciones de fichas antiguas, categoría por categoría.

## P5 · Recursos documentales y gráficos

1. **Árboles genealógicos:** crear o ampliar láminas necesarias y vincular personas que aparecen en varios árboles.
2. **Mapas geográficos:** documentar rutas, lugares y grados de certeza o hipótesis.
3. **Mapas tribales:** representar pueblos, asentamientos y relaciones territoriales sin convertir conjeturas en hechos.
4. **Imágenes de fichas:** obtener o elaborar imágenes de seres naturales, materiales, objetos e instrumentos (según criterios de licencias y revisión editorial). No ilustrar de momento fichas de seres sobrenaturales.
5. Integrar los recursos en los visores comunes de mapas y genealogías, enlazarlos con las fichas y mantener los originales.

## P6 · Revisión editorial de las escenas

Revisar las escenas en **lotes narrativos**, después de disponer de fichas y recursos comunes:

- P6.1 Revisión narrativa y textual.
- P6.2 Elaboración y validación de notas explicativas.
- P6.3 Selección y elaboración de imágenes para la escena.
- P6.4 Incorporación de mapas y árboles.
- P6.5 Distribución de recursos en escritorio y móvil.
- P6.6 Revisión de enlaces entre escena, apéndices, bibliografía, mapas, árboles y otras escenas.
- P6.7 Confirmación de los temas que merecen artículos de fondo.

**Punto de aprobación editorial:** escena o lote de escenas con notas, formato, imágenes, distribución y enlaces.

## P7 · Artículos de fondo y documentación

Consolidar los posibles artículos identificados en P1 y P6; eliminar duplicidades, redactar los aprobados, incorporar fuentes y recursos y enlazarlos desde escenas y apéndices. Completar la revisión general de la bibliografía reunida durante todas las fases; resolver duplicaciones y metadatos pendientes sin inventar fuentes.

## P8 · Integración y control general

Comprobar de manera automática y manual según proceda:

- Integridad de texto, capítulos, anclas y formato.
- Vínculos a fichas y referencias bidireccionales.
- Identidades únicas, remisiones, homónimos y relaciones entre árboles.
- Mapas, rutas, láminas, visor, búsqueda, índices y catálogo de recursos.
- Referencias cruzadas entre libros y enlaces históricos.
- Bibliografía normalizada y citas.
- Ausencia de archivos y recursos ausentes, páginas rotas o versiones antiguas.
- Visualización en móvil y escritorio, incluidas imágenes laterales.
- Reproducibilidad del generador sin pérdida de fuentes aprobadas.

Actualizar pruebas anteriores que contengan conteos fijos cuando se incorpore un nuevo libro o capítulo, conservando el control de los contenidos históricos.

## P9 · Implementación, publicación y cierre

1. Integrar únicamente los contenidos aprobados.
2. Regenerar la web con las fuentes oficiales y ejecutar las comprobaciones; corregir fallos.
3. Publicar en GitHub y confirmar el resultado real del despliegue.
4. Verificar las páginas publicadas (enlaces y presentación).
5. Actualizar inventario, registro maestro, matriz de estados, bibliografía y pendientes.
6. Documentar la versión y el punto exacto para iniciar el siguiente libro o reanudar el actual.

## Estado inicial al aprobar este protocolo

- **P0 Génesis:** inventario técnico ejecutado y registrado el 20/11/2026; quedaron expresamente señalados controles de ejecución integral del pipeline y revisión visual de dispositivos antes de una publicación futura.
- **P1 Génesis:** preparar propuesta de escenas y títulos para **Gn 25–50**, sin alterar las 15 escenas existentes de Gn 1–24.
- Ninguna fase pendiente se considera aprobada por el mero hecho de figurar en este documento.

## Para reanudar el trabajo en otro chat

Petición breve sugerida: **«Continúa BIBLILU siguiendo `editorial/protocolo-libros.md` del repositorio alextorurdi/biblilu. Revisa el último estado del libro antes de actuar.»** El documento y los registros del repositorio tienen precedencia sobre recuerdos incompletos; cualquier nueva decisión del editor se incorpora de forma explícita.
