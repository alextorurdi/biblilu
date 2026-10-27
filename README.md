# BIBLILU

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

La lectura principal sigue los capítulos temáticos originales: «Creación» (Gn 1:1–2:3) y «Paraíso» (Gn 2:4–3:24). El índice alternativo conserva la capitulación bíblica tradicional y enlaza a anclas canónicas únicas como `#gn-2-1`. Las notas numeradas se abren como ventanas accesibles; sin JavaScript se pueden consultar al final de la página. Las plantillas editoriales preservan estas decisiones al reconstruir el sitio.

## Verificación

`check.py` comprueba los enlaces locales, los 80 versículos, las 22 notas, las anclas canónicas, los índices y que las palabras de Dios no contengan hiperenlaces. La inspección visual del navegador debe cubrir ordenador y móvil antes de publicar cambios de diseño.
