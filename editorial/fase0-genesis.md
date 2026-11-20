# Fase 0 — Génesis: inventario inicial

**Protocolo rector:** [Fases P0–P9](protocolo-libros.md). Este informe es el estado del primer libro y no sustituye el procedimiento general.

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

## Inventario de escenas (auditoría del 20/11/2026)

Fuente verificable: [inventario-genesis.json](inventario-genesis.json). Reconstrucción/validación reproducible: `node scripts/audit_genesis_p0.mjs --write` y `node scripts/audit_genesis_p0.mjs --check`. La matriz distingue las fuentes editoriales protegidas de las salidas HTML, que el generador puede completar con enlaces aprobados.

| Nº | Escena | Pasaje | Versículos | Notas | Recursos principales |
|---:|---|---|---:|---|---|
| 01 | Creación | 1:1–2:3 | 34 | 1–8 | Ilustración |
| 02 | Paraíso | 2:4–3:24 | 46 | 9–22 | 3 ilustraciones |
| 03 | Crueldad | 4:1–24 | 24 | 23–39 | Ilustración, instrumento y lámina 01 |
| 04 | De Adán a Noé | 4:25–5:32 | 34 | 40–53 | Ilustración y lámina 02 |
| 05 | Diluvio | 6:1–9:29 | 97 | 54–67 | 5 recursos visuales |
| 06 | Dispersión | 10:1–32 | 32 | 68–76 | 3 mapas y láminas 03–05 |
| 07 | Vanidad | 11:1–9 | 9 | 77–78 | Ilustración |
| 08 | De Noé a Abram | 11:10–32 | 23 | 79–81 | Mapa y lámina 06 |
| 09 | Viaje | 12:1–13:18 | 38 | 82–93 | Ilustración y 3 mapas |
| 10 | Guerra | 14:1–24 | 24 | 94–103 | Ilustración y 3 mapas |
| 11 | Promesas | 15:1–21 | 21 | 104–110 | Ilustración y mapa |
| 12 | Legado | 16:1–17:27 | 43 | 111–121 | 2 ilustraciones y mapa |
| 13 | Perdición | 18:1–19:38 | 71 | 122–130 | 2 ilustraciones y mapa |
| 14 | Cumplimiento | 20:1–23:20 | 96 | 131–144 | 4 ilustraciones, mapa y lámina 07 |
| 15 | Familia | 24:1–67 | 67 | 145–153 | 4 ilustraciones, mapa y lámina 19 |
| **Total** | **15 escenas** | **Génesis 1–24** | **659** | **153** | **15 mapas catalogados, 8 láminas SVG propias** |

### Resultado de las comprobaciones

- La secuencia de versículos publicados es completa para Génesis 1:1–24:67 y sus quince escenas (659 anclas canónicas); no se han detectado omisiones ni duplicaciones en el inventario efectuado.
- Las notas forman una secuencia continua de 1 a 153 y sus marcadores coinciden con las notas de las escenas.
- Todas las **450 rutas** del registro maestro tienen página en el repositorio: 432 fichas principales y 18 remisiones; se contabilizan 303 entidades con menciones explícitas, 245 relacionadas con genealogías y 56 con localización en los mapas catalogados. Estas relaciones no equivalen a una extracción exhaustiva de futuros capítulos.
- Los recursos referenciados por las escenas y las rutas de archivo revisadas están presentes en el árbol del repositorio.
- Los **15 mapas** del catálogo corresponden a las escenas, y las **8 láminas SVG** propias (01–07, 19) se utilizan en el texto. El visor incluye además otras láminas incrustadas: no confundir ambos recuentos.
- Están publicados los artículos «Día en Génesis» y «Cosmología hebrea». La bibliografía normalizada incluye **69 referencias**.
- Las escenas **03, 04, 05, 13, 14 y 15** producen una salida diferente de su fuente protegida: es **intencionado**, porque `scripts/build.py` añade después enlaces aprobados (objetos, instrumentos, medidas) y `scripts/build_bibliography.py` normaliza citas. **No copiar las salidas sobre los originales**.
- Se han ajustado `scripts/check.py` y `scripts/check_maps.py` para aceptar los enlaces editoriales aprobados sin desactivar sus controles. Esta revisión fue estática sobre el repositorio: **no equivale todavía a una ejecución completa del pipeline**.

### Límites y tareas futuras

1. **Génesis 25–50:** no existen aún versículos incorporados al JSON ni escenas publicadas. La escenificación se aprobará en P1, antes de añadir texto en P2.
2. **Identidades ambiguas:** aplicar `editorial/criterios-identidades-genesis.md` a los futuros personajes; no fusionar automáticamente homónimos ni las esposas de Esaú, Timna, Coré o los jefes edomitas.
3. **Pruebas escalables:** al empezar P2, adaptar las verificaciones que todavía presuponen 659 versículos, 153 notas y 69 referencias, además de actualizar el mapeo versículo → escena. Conservar las pruebas históricas para Gn 1–24.
4. **Revisión visual:** queda pendiente una comprobación en navegador de los diseños de escritorio y móvil. El inventario comprueba la presencia de los recursos, no su tamaño o posición en pantalla.
5. **Textos heredados:** la página «Sobre BIBLILU» y algunos párrafos antiguos del README contienen cifras de entregas anteriores; actualizar sus textos descriptivos cuando se intervenga de nuevo en la publicación general.
6. **Integración automatizada:** antes de publicar nuevos capítulos, ejecutar `node scripts/build_registry.mjs --check`, `node scripts/audit_genesis_p0.mjs --check`, `python scripts/check.py`, `python scripts/check_maps.py` y las comprobaciones de apéndices/bibliografía. Incorporar estas tareas al flujo de publicación después de probarlas en el entorno de integración.

**Estado de P0:** inventario técnico y registro maestro preparados; se puede pasar a P1. La revisión visual y la modernización del pipeline se mantienen como controles de publicación, sin reabrir las escenas ya aprobadas.
