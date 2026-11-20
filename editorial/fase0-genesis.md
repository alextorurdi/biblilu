# Fase 0 — Génesis: inventario inicial

Estado: registro maestro interno generado desde los datos actuales. Este informe no aprueba por sí mismo nuevas fichas ni cambia interpretaciones.

## Alcance verificado

- Texto cargado: capítulos **1–24**, **659 versículos** en `data/genesis.json`. Pendientes de incorporación: **25–50**.
- Datos base: **445** entradas en `data/entries.json`. Se aplican las revisiones de Materiales, Objetos, Instrumentos y Medidas, se agregan dos medidas y tres fichas tribales; se conserva la ruta heredada de **Amorreo** como remisión a Amorreos.
- Registro maestro: **450** identificadores históricos, **432** fichas principales y **18** remisiones.
- Categorías: `animales` 35; `instrumentos` 2; `lugares` 73; `materiales` 12; `medidas` 3; `objetos` 7; `onomastico` 290; `tribus` 28.
- Genealogías: **8 SVG individuales** en `assets/genealogias`; relaciones de personas y láminas procedentes de `enlaces.json`, sin cambiar sus identificadores. El visor también contiene láminas incrustadas que no deben contarse como archivos SVG independientes.
- Cartografía: **15** mapas en `assets/mapas/catalogo.json` y **27** pueblos del Atlas de Pueblos procedentes de `assets/atlas/pentateuco.geojson`.
- Artículos publicados: **2** (`concepto-dia-genesis` y `cosmologia-hebrea`).

## Reglas de identidad

1. La clave primaria es la ruta existente, por ejemplo `onomastico/abraham`: no se sustituyen enlaces públicos.
2. Una remisión, como `onomastico/abram`, mantiene su ruta y apunta a su ficha principal. Los homónimos permanecen diferenciados.
3. Las variantes aprobadas (Jacob/Israel, Esaú/Edom, José/Zafnat-panea y Benjamín/Benoni) son denominaciones de **un solo registro existente**, no nuevas fichas.
4. Los nombres de personas, tribus y lugares no se fusionan por coincidencia ortográfica. Aplicar `editorial/criterios-identidades-genesis.md` antes de alterar cualquier relación.
5. El registro enlaza identificadores y fuentes, pero no copia el texto descriptivo de las fichas.
6. Las menciones bíblicas se toman de los metadatos explícitos. La lista vacía significa **no indexado**, no que el nombre no figure en el texto.
7. `ficha_principal` es una remisión editorial, **no** una prueba historiográfica sobre identidad.

## Cómo actualizar

```bash
node scripts/build_registry.mjs
node scripts/build_registry.mjs --check
```

Editar las fuentes originales, **nunca** mantener este JSON a mano. El registro es interno en la arquitectura de la web: no genera páginas visibles. Dado que el repositorio de GitHub es público, sus archivos técnicos pueden consultarse en GitHub.

## Pendientes de la Fase 0

- Inventariar escena por escena lo aprobado, lo implementado y los recursos disponibles antes de abordar Gn 25–50.
- Auditar exhaustivamente los enlaces internos de los capítulos pendientes de publicar.
- Revisar al avanzar las menciones no indexadas y la pertinencia de ampliar las fichas existentes; no crear identidades por extracción automática sin revisión.
- Incorporar comprobación del registro a la secuencia de integración y publicación cuando se actualice el generador general.
