# BIBLILU
## Entrega v0.9 · Perdición (Gn 18–19)

Escena 13 «Perdición»: una lectura continua de los 71 versículos de Génesis 18:1–19:38, con nueve notas 122–130. Se conservan sin modificar las originales 92, 93, 94, 96, 97, 98 y 99; se sustituye únicamente la original 95 (Gn 19:5) por el texto aprobado y se añade una nueva nota etimológica para Moab y Ben-ammi en 19:38. Quedan descartadas las nuevas notas propuestas para 19:11 y 19:26. Las palabras de Dios aparecen en rojo, los diálogos y pensamientos diferenciados, y los vínculos a las fichas de los apéndices se integran directamente en las menciones.

Distribución final de ilustraciones (imágenes definitivas en WebP y mapa vectorial en SVG): los tres visitantes de Abraham (`assets/perdicion-visita.webp`), mapa interpretativo del entorno del mar Muerto (`assets/perdicion-mapa.svg`) y la mujer de Lot (`assets/perdicion-mujer-lot.webp`). Cuatro cortes: después de Gn 18:9, 18:33, 19:23 y 19:29. En móvil aparecen la visita en el primer corte, el mapa en el tercero y la mujer de Lot en el cuarto; en escritorio el lateral cambia de la visita al mapa en el segundo corte y de este a la mujer de Lot en el cuarto. Se mantiene la incertidumbre arqueológica en el mapa y se evita la ilustración separada de la destrucción, descartada por el editor.

Publicado como `docs/genesis/18/index.html`, con fuente en `editorial/approved-pages/genesis/18/index.html`. Génesis 19 redirige al versículo 19:1 dentro de la misma escena. Actualizados índices, portada, selectores, navegación, generador, verificaciones y tareas (`editorial/tareas-perdicion.md`).

## Entrega v0.8 · Legado (Gn 16–17)

Publicada la escena 12 «Legado», que unifica las antiguas escenas previstas «Agar» y «Pacto» en una única lectura de 43 versículos (Génesis 16:1–17:27). Incorpora las cinco notas originales 87–91, con las modificaciones aprobadas de 87 y 88, y seis notas nuevas; numeración consecutiva 111–121. Se descarta la propuesta de nota explicativa sobre la circuncisión. Se mantienen los diálogos y los pensamientos en cursiva, las palabras divinas en rojo y los enlaces a los apéndices directamente en el texto.

El diseño definitivo incluye un mapa geográfico original en `assets/legado-mapa.svg`, una ilustración de Agar y el ángel en `assets/legado-agar-angel.webp` y una recreación artística de una hoja de sílex en `assets/legado-instrumento.webp`. El mapa presenta la costa geográfica real de la región, dibuja un trayecto hipotético hacia Shur y deja expresamente sin localizar Bered y el Pozo del Viviente-que-me-ve. En móvil se insertan tras Génesis 16:6, después de 16:14 y antes de 17:23, respectivamente. En escritorio ocupan un único lateral alternante, con transiciones en 16:7 y 17:15. Se han actualizado el índice principal y el tradicional, los selectores de escenas, la navegación, los enlaces de las fichas y las páginas fuente protegidas por el generador. Génesis 17 dispone de redirección a su ancla canónica dentro de Legado. Criterios y tareas: `editorial/tareas-legado.md`.

## Entrega v0.7 · Promesas (Gn 15)

Publicada la escena 11 «Promesas» (21 versículos, Génesis 15), con siete notas editoriales numeradas 104–110, incluidas las versiones aprobadas de las notas originales 81 y 85, la corrección puntual de la nota 82, las notas originales 83–84 y dos notas nuevas (Gn 15:6 y 15:18). Se descarta la propuesta de nota para 15:13. Ilustración original de Abram contemplando las estrellas y mapa geográfico de Canaán, Éufrates y posibles localizaciones del río de Egipto; transición sincronizada en escritorio y distribución móvil específica. No se crea ilustración del pacto. Se completan los enlaces de apéndices, índices, navegación y compatibilidad del generador. Acuerdos editoriales: incidencia #12.



## Entrega v0.6 · Viaje y Guerra (Gn 12–14)

Implementadas las escenas 9 «Viaje» (Génesis 12–13) y 10 «Guerra» (Génesis 14), con 62 versículos del manuscrito y las 22 notas editoriales definitivas (82–103). La nota original 68 se suprime; se conservan las demás, salvo las correcciones 66 y 74 y la sustitución íntegra de la 77 sobre Melquisedec. Se incorporan nuevas notas en Gn 12:1, 13:13, 14:10, 14:14 y 14:18 y bibliografía de Nissenbaum (2004). Mapas geográficos originales de las seis fases narrativas, ilustraciones del manuscrito optimizadas, sincronización en escritorio, mapas tras cada sección en móvil, formato de diálogo y enlaces a los apéndices. Se han actualizado índices, selectores y navegación. Fuentes: el manuscrito editorial y acuerdos recogidos en la incidencia #12. El generador mantiene las páginas aprobadas de las escenas 9 y 10.

## Entrega v0.5 · Vanidad y De Noé a Abram

Implementadas las escenas 7 y 8 (Génesis 11:1–32), con el texto del manuscrito original, notas 77–81, ilustración contemporánea de Babel, lámina genealógica 06, mapa esquemático Ur–Harán, correcciones cronológicas del Onomástico y tres erratas de fichas. Las páginas están en `docs/genesis/11/` y `docs/genesis/11-10/`; el generador conserva las plantillas aprobadas. Incorporación a `main` mediante PR #7.

## Entrega v0.4 · Dispersión\n\nPublicada la escena «Dispersión» (Génesis 10:1–32) con 32 versículos, notas 68–76, tres mapas geográficos y tres láminas genealógicas enlazadas al Apéndice. Escritorio: árbol lateral sincronizado; móvil: árbol desplegable y mapa al final de cada bloque. La fuente canónica continúa en `data/genesis.json`; la página aprobada se conserva en `editorial/approved-pages/genesis/10/index.html`.\n\n
Biblia ilustrada en español de España, preparada para GitHub Pages. Versión 0.1: «Creación» (Gn 1:1–2:3) y «Paraíso» (Gn 2:4–3:24), cinco apéndices y bibliografía. El texto se importa de los documentos editoriales del proyecto sin corregir su redacción.

## Estructura

- `docs/`: sitio estático completo, listo para publicar. Incluye las dos páginas temáticas revisadas y un redireccionamiento para la antigua ruta de Génesis 3.
- `data/genesis.json`: 80 versículos con numeración canónica interna y etiqueta original independiente.
- `data/entries.json`: 290 entradas de los apéndices.
- `data/bibliography.json`: bibliografía del editor.
- `assets/`: ilustraciones originales, CSS y JavaScript.
- `scripts/build.py`: generador estático sin dependencias externas.
- `scripts/import_docx.py`: importador OOXML sin dependencias externas.
- `scripts/check.py`: comprobación de enlaces, texto, numeración y marcado.
- `editorial/approved-pages/`: páginas temáticas aprobadas, restauradas al final de cada ejecución de `scripts/build.py` para no perder las notas y la edición.

## Convención editorial

En BIBLILU las divisiones temáticas originales del manuscrito se denominan **escenas**: «Creación», «Paraíso», etc. El término **capítulo** se reserva exclusivamente para la división bíblica tradicional (Génesis 1, Génesis 2, Génesis 3, etc.). Una escena puede abarcar varios capítulos o partes de ellos. Este criterio se aplica al código, la documentación y la interfaz; no modifica los títulos originales de las escenas ni los versículos.

## Generar y comprobar

Se necesita Python 3. Ejecutar desde la raíz del repositorio:

```sh
python scripts/build.py
python scripts/check.py
```

Para volver a importar los documentos originales, proporcionar la carpeta que los contiene:

```sh
python scripts/import_docx.py /ruta/a/documentos
python scripts/build.py
python scripts/check.py
```

Los documentos Word no se requieren para generar de nuevo el sitio desde los JSON.

## GitHub Pages

Publicar la carpeta `/docs` de la rama principal en Settings → Pages → Deploy from a branch. Las rutas son relativas y funcionan bajo `/biblilu/` y con un dominio propio. El sitio no necesita servidor, base de datos, servicios externos ni claves. El lector básico y las fichas completas funcionan sin JavaScript; la consulta lateral y los controles lo usan como mejora.

Para probar las consultas laterales localmente, servir `docs/` con un servidor HTTP; abrir directamente archivos permite navegar, pero algunos navegadores bloquean la carga JSON y la consulta abre la página completa como alternativa.

## Edición progresiva

El estado inicial publica únicamente tres capítulos. Los demás capítulos y libros se presentan como pendientes sin enlaces vacíos. Para incorporar capítulos, añadir sus datos y asociaciones de ilustraciones, ampliar la lista de capítulos publicados en el generador y revisar las referencias disponibles. Revisar manualmente los nombres ambiguos y las intervenciones de Dios. No aplicar un reemplazo global por nombres a todo el corpus.

Se preservan las entradas repetidas mediante identificadores independientes. Las referencias bíblicas enlazan solo a capítulos disponibles. Las citas bibliográficas enlazan a una fuente individual cuando la correspondencia es única; en caso contrario abren el índice bibliográfico para no inventar una identificación.

La lectura principal sigue las **escenas** del manuscrito: «Creación» (Gn 1:1–2:3) y «Paraíso» (Gn 2:4–3:24). El índice alternativo conserva los **capítulos** bíblicos tradicionales y enlaza a anclas canónicas únicas como `#gn-2-1`. Las notas numeradas se abren como ventanas accesibles; sin JavaScript se pueden consultar al final de la página. Las plantillas editoriales preservan estas decisiones al reconstruir el sitio.

## Verificación

`check.py` comprueba los enlaces locales, los 80 versículos, las 22 notas, las anclas canónicas, los índices y que las palabras de Dios no contengan hiperenlaces. La inspección visual del navegador debe cubrir ordenador y móvil antes de publicar cambios de diseño.

## Apéndice genealógico

`apendices/genealogias/` contiene el visor del Génesis, con árbol general, 18 láminas, buscador, referencias y notas. Se accede desde la misma tarjeta del Onomástico en la portada y en el índice de apéndices, y desde el directorio onomástico. La fuente autocontenida está en `assets/genealogias/visor.html`; el generador la copia a `docs/assets/genealogias/` y crea su página dentro de la navegación habitual.

## Escena 5 · Diluvio (Génesis 6:1–8:22)

Publicada en `docs/genesis/6/index.html`, con fuente editorial en `editorial/approved-pages/genesis/6/index.html`. Incluye 68 versículos, doce notas (54–65), cinco posiciones visuales en el lateral para escritorio y después de cada sección en móvil, cronología final y las citas bibliográficas aprobadas. Los cinco recursos visuales se encuentran en `assets/diluvio-*.svg` y en su copia publicada `docs/assets/`.

Los enlaces de las nuevas notas llevan a dos páginas de artículo en preparación, sin contenido especulativo. Los capítulos tradicionales Génesis 6, 7 y 8 enlazan a la misma escena mediante anclas canónicas. `scripts/build.py` conserva la página y las páginas de los artículos al reconstruir el sitio; `scripts/check.py` valida ahora 206 versículos y 65 notas. Para la revisión visual de las imágenes y de la activación lateral, probar el sitio desde navegador en escritorio y móvil.

<!-- Preparación de Dispersión (Gn 10). -->
