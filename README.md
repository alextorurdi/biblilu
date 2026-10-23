# BIBLILU

Biblia ilustrada en español de España, preparada para GitHub Pages. Primera entrega: Génesis 1–3, cinco apéndices y bibliografía. El texto se importa de los documentos editoriales del proyecto sin corregir su redacción.

## Estructura

- `docs/`: sitio estático completo, listo para publicar. Contiene 303 páginas.
- `data/genesis.json`: 80 versículos con numeración canónica interna y etiqueta original independiente.
- `data/entries.json`: 290 entradas de los apéndices.
- `data/bibliography.json`: bibliografía del editor.
- `assets/`: ilustraciones originales, CSS y JavaScript.
- `scripts/build.py`: generador estático sin dependencias externas.
- `scripts/import_docx.py`: importador OOXML sin dependencias externas.
- `scripts/check.py`: comprobación de enlaces, texto, numeración y marcado.
- `editorial/revision-genesis-1-3.md`: diferencias observadas; ninguna aplicada.

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

Las diferencias de numeración del documento no se corrigen silenciosamente: Gn 2:2 mantiene «1» visible, con nota y ancla estable `#v2`.

## Verificación

`check.py` comprueba los enlaces locales, las anclas, los 80 versículos y su fidelidad al texto importado, la ausencia de enlaces en las palabras de Dios y casos de diálogo. La inspección visual del navegador debe cubrir ordenador y móvil antes de publicar cambios de diseño.
