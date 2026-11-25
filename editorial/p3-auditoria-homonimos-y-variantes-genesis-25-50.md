# P3 · Auditoría de homónimos y variantes en candidatos únicos (Gn 25–50)

**Fecha:** 25/11/2026. **Alcance:** revisión contextual focalizada sobre candidatos que el barrido automático había considerado unívocos, sin interpretar esa unicidad como validación editorial.

## Correcciones CT-13 (35 registros residuales)

- **Benoni (Gn 35:18)** → `onomastico/benjamin` (ficha existente).
- **Pérez (Gn 38:29; 46:12, dos menciones)** → `onomastico/fares` (ficha existente; forma BES).
- **Zafnat-panea (Gn 41:45)** → `onomastico/jose` (ficha existente).
- **Otros 29 registros** se identifican contextualmente por categoría, pero **sin ID** asignado todavía porque no hay ficha histórica inequívoca confirmada: Hamor, Hira, Potifar, Potifera, Ismaelitas, Madianitas. No equiparar `clasificado_sin_id` con ficha ya aprobada o enlace público.
- **Timna, jefatura Gn 36:40:** `homonimo_no_identificado`, sin afirmar que la jefatura es la concubina de Elifaz o la hermana de Lotán. Respeta el acuerdo de no crear fichas individuales de jefaturas.

## CT-14 · Corrección de homónimos que aparentaban identificador único

| Nombre | Referencias | Destino/contexto | Precaución |
|---|---|---|---|
| **Siquem**, hijo de Hamor | Gn 33:19; 34:2–26, 15 menciones del catálogo | **Onomástico, sin ID de ficha registrado** | La asignación automática `lugares/siquem` era errónea en estos casos |
| **Siquem**, ciudad | Gn 33:18; 35:4; 37:12–14 | `lugares/siquem` (mantener candidato) | No mezclar con el personaje |
| **Aná, hijo de Zibeón** | Gn 36:2,14,18,24,25 (7 apariciones) | `onomastico/ana-hijo-de-zibeon` — **ID futuro**, no página existente | Distinto del hijo de Seir; registrado en acuerdos editoriales |
| **Aná, hijo de Seir** | Gn 36:20,29 (2 apariciones) | `onomastico/ana-hijo-de-seir` (ficha existente) | Distinguir las dos genealogías |
| **Zera, hijo de Reuel** | Gn 36:13,17 | `onomastico/zera` (ficha existente) | No confundir con homónimos |
| **Zera, hijo de Judá y Tamar** | Gn 38:30; 46:12 | `onomastico/zara` (ficha histórica «Zara») | BES utiliza «Zera» |
| **Zera, padre de Jobab** | Gn 36:33 | **Onomástico, sin ID adjudicado** | No fusionar con Zera hijo de Reuel; requiere cotejo del Excel consolidado de Onomástico antes de proponer alta |
| **Zera, hijo de Simeón** | Gn 46:10 | `onomastico/zohar` (variante textual BES/RVR1960 ya documentada en lote inicial) | Mantener la cautela textual aprobada |

**Balance CT-14:** 29 apariciones reclasificadas. Los 15 «Siquem» personales, 9 «Aná» y 5 «Zera» se han conservado como menciones del texto BES, sin alterar los versículos.

## Estado de la reconciliación estructurada

- **874** versículos y **1.682** registros únicos en catálogo.
- **380** registros con regla contextual aplicada, incluidos **292** clasificados por contexto, **45** clasificados sin ID, **38** exclusiones, **2** asociaciones contextuales, **1** nota, **1** exclusión personal y **1** jefatura homónima no identificada.
- **1.302 candidatos de identificador único** restantes no se han certificado aún individualmente.
- **0 registros en estado `candidato_no_reconciliado`**: esto significa que la cola residual está **clasificada por contexto** o expresamente pendiente de ID, no que todas las fichas estén creadas ni que el control semántico esté completo.
- Los offsets y literales de los 1.682 registros se contrastaron directamente contra el texto BES sin diferencias; en el repositorio se reforzó el script de comprobación con regresiones concretas para Siquem/Aná/Zera.
- El resultado real del workflow GitHub Actions **no se ha podido confirmar**, por lo que no se certifica CI superado.

## Pendientes y límites

1. Auditar las restantes menciones `candidato_unico_no_validado` atendiendo a contexto, posibles usos figurados, jefaturas y diferencias de traducción.
2. Cotejar el registro de altas de Onomástico para **Siquem (hijo de Hamor), Hamor, Hira, Potifar, Potifera y Zera (padre de Jobab)**, sin fabricar nuevos identificadores.
3. Confirmar el tratamiento de gentilicios **Ismaelitas** y **Madianitas** respecto a fichas tribales y futuras altas.
4. Ejecutar el control Python y comprobar CI; no inferir que la falta de estados reportados equivale a una prueba satisfactoria.
5. Preparar fichas y enlaces en P4; no publicar rutas de fichas futuras durante P3.

**Resultado:** los homónimos detectados se han separado sin fusionar entidades, pero la **P3 continúa abierta técnicamente**.
