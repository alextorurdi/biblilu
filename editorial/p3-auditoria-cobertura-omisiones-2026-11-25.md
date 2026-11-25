# P3 · Auditoría adicional de cobertura por términos aprobados (25/11/2026)

**Alcance:** cotejo de las 874 unidades `data/genesis_25_50_bes.json` con los intervalos `start/end` de las 1.697 menciones de `data/p3-catalogo-reconciliado-genesis-25-50.json` (commit de referencia `796994cc3adfc364daf77c104a1db9bd614b4afd`). Se comprueba si existe un registro que **cubra la palabra exacta**, no simplemente si aparece su concepto en otra parte del versículo. Las ausencias son **hallazgos de cobertura**, no altas ni enlaces automáticamente aprobados.

## Omisiones comprobadas del catálogo

| Denominación en BES | Referencias sin cobertura | Nº de apariciones sin cobertura | Orientación editorial |
|---|---|---:|---|
| Flechas | Gn 27:3 | 1 | Objetos, ficha aprobada «Arco y flechas»; cotejar si «arco» de ese versículo está ya clasificado |
| Bastón | Gn 32:10; 38:18; 38:25; 49:10 | 4 | Objetos, ficha Bastón aprobada; distinguir bastón de mando en 49:10 del Cetro que también figura en el versículo |
| Cordón | Gn 38:18; 38:25 | 2 | Objetos, ficha conjunta aprobada «Sello y Cordón»; cotejar con las menciones «sello» ya inventariadas |
| Canasta | Gn 40:17 (dos veces) | 2 | Objetos, ficha Canasta aprobada |
| Cama | Gn 47:31; 48:2; 49:4; 49:33 | 4 | Objetos, ficha Cama aprobada; respetar el análisis léxico pendiente sobre los términos hebreos |
| Mesa | Gn 43:34 | 1 | Objetos, ficha Mesa aprobada; no extender a Mesa topónimo de Gn 10:30 |
| Cadena | Gn 41:42 | 1 | Elemento contextual sin ficha nueva propia por decisión de Objetos; comprobar si merece asociación con nota o registro descriptivo, sin enlazarla automáticamente |
| Aretes | Gn 35:4 | 1 | Objetos, ficha Aretes aprobada |
| Israelitas | Gn 32:32; 36:31 | 2 | Tribus, aplicar R-01: ficha principal futura Israelitas, variante/remisión Israel; no confundir con Jacob |
| Hebreos | Gn 40:15; 43:32 | 2 | Tribus: cotejar decisión editorial para el gentilicio antes de fijar ID o sinónimo |
| Sangre | Gn 37:22,26,31; 42:22; 49:11 | 5 | Materiales, ficha Sangre aprobada; distinguir usos literales y figurados |
| Agua | Gn 26:19,20,32; 29:3,7,8,10; 30:38,41; 37:24; 43:24; 49:4 | 12 | Materiales, ficha Agua aprobada; revisar expresiones negativas («no había agua»), usos y figura de Gn 49:4 |
| Rocío | Gn 27:28,39 | 2 | Materiales, ficha Rocío aprobada |

**Balance del muestreo dirigido:** 39 apariciones textuales no representadas en el catálogo, entre las 13 denominaciones de la tabla. **No son 39 nuevas entidades** y no se suman aún a las 1.697 menciones: queda pendiente establecer acciones y offsets únicos para no colisionar con registros existentes. La prueba de cobertura es independiente del control de integridad que solo asegura que no se pierdan registros previamente inventariados.

## Casos que no deben añadirse automáticamente

- **«sal» en Gn 31:13**: imperativo verbal; exclusión aprobada en Materiales.
- **«quinto» en Gn 30:17**: ordinal referido al quinto hijo de Lea, no medida tributaria; no conectar a la ficha Quinto.
- **«faraón»**: título ampliamente repetido en Gn 37–50. El muestreo localiza 74 apariciones textuales no representadas por el catálogo. Revisar por separado si el criterio de extracción de Onomástico requiere registrarlas como título/función, sin crear persona identificable por automatismo. No se incorporan al balance de las 39 apariciones anteriores.

## Requisitos técnicos de continuación

1. Añadir reglas de cobertura con referencias y **offsets exactos** obtenidos del BES, preservando texto y catálogo bruto.
2. Reutilizar las **aprobaciones editoriales existentes**, pero mantener separado el estado de aprobación de la ficha futura y el de cada mención.
3. Antes de regenerar el catálogo, resolver solapamientos y las dos «canasta» dentro del mismo versículo mediante `start/end`.
4. Extender el control P3 con regresiones de **presencia** (no solo correspondencia de offsets): Gn 38:18 cordón/bastón, Gn 40:17 canasta × 2, Gn 47:31 cama, Gn 32:32 israelitas, Gn 27:28 rocío y Gn 37:31 sangre.
5. Repetir la auditoría completa sobre las ocho categorías. Esta lista es dirigida y **no certifica exhaustividad**.
6. Mantener cerradas las decisiones de los ocho apéndices; nuevas ambigüedades, si surgen, se proponen al editor y no se resuelven silenciosamente.

**Estado:** P3 abierta; auditoría de cobertura ampliada con omisiones concretas reproducibles. Sin cambios de fichas, escenas BES, enlaces públicos ni publicación.
