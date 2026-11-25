# P3 Tribus · TR-29 aprobado y revisión de Génesis 48

**Fecha:** 24/11/2026. **Fuente primaria:** `data/genesis_25_50_bes.json` (BES 2026); contraste contextual con Josué 14:4 (RVR1960). **Estado:** criterio **TR-29 aprobado** por el editor; la lista definitiva de **13 fichas tribales**, incluyendo Efraín, Manasés y Levitas, ha sido aprobada posteriormente. Las referencias concretas de Gn 48 se regirán por el criterio mixto ya acordado. Las restantes acciones de la hoja «Incidencias» del Excel `BIBLILU_Genesis_P3_Tribus_25-50_Revision(2).xlsx` no se alteran en este documento.

## TR-29 · Resolución definitiva aprobada

**Opción 3: criterio mixto contextual.** Los nombres de los hijos de Jacob en Génesis 49 remiten a **Onomástico** cuando recuerdan biografías y acciones personales; a **Tribus** cuando expresan el futuro colectivo, territorial o político de sus descendientes; y llevan una nota cruzada cuando ambos sentidos confluyen.

**Cautelas:** Génesis 49:28 designa colectivamente «las doce tribus de Israel», pero la cifra no determina cuántas fichas distintas debe haber en un catálogo histórico a través de épocas distintas. No fusionar al individuo con la tribu ni crear una sola identidad que absorba ambos sentidos.

## Génesis 48 · propuesta de enlaces contextualizados

| Referencias | Evidencia en BES 2026 | Destino principal |
|---|---|---|
| Gn 48:1 | José trae «sus dos hijos, Manasés y Efraín» | `onomastico/manases`, `onomastico/efrain` |
| Gn 48:5 | «Efraín y Manasés ... serán míos ... como Rubén y Simeón» | Personas nombradas; añadir nota sobre su reconocimiento y futura base tribal |
| Gn 48:6 | Herencia «dentro de las tribus de sus hermanos» | Referencia contextual a descendencias tribales; no enlazar un nombre propio inexistente |
| Gn 48:8–14 | Los hijos se acercan, reciben el abrazo y la imposición de manos | Personas, Onomástico |
| Gn 48:16 | Bendición sobre «estos muchachos» y su multiplicación | Nota mixta: personas presentes y descendencias futuras |
| Gn 48:17–18 | José intenta cambiar la colocación de las manos | Personas, Onomástico |
| Gn 48:19 | Manasés «llegará a ser un pueblo»; la descendencia de Efraín será «un grupo de naciones» | **Tribus** mediante nota: el versículo NO nombra literalmente a ninguno de los dos; no hipervincular «él», «su hermano» ni pronombres arbitrariamente |
| Gn 48:20 | «Que Dios te haga como Efraín y Manasés»; Efraín precede a Manasés | Enlaces personales con referencia cruzada tribal; distinguir bendición presente y alcance futuro |

## Decisión posterior · Catálogo definitivo de trece fichas tribales

El editor **aprueba 13 fichas tribales** para los grupos descendientes de Jacob, en sustitución de las propuestas previas de «12 fichas» o «12 + 2», según el siguiente listado y orden editorial:

| N.º | Título aprobado | ID propuesto | Correspondencia personal |
|---:|---|---|---|
| 1 | Rubén | `tribus/ruben` | `onomastico/ruben` |
| 2 | Simeón | `tribus/simeon` | ficha personal de Simeón, sin fusionar |
| 3 | Judá | `tribus/juda` | ficha personal de Judá, sin fusionar |
| 4 | Gad | `tribus/gad` | ficha personal de Gad, sin fusionar |
| 5 | Aser | `tribus/aser` | ficha personal de Aser, sin fusionar |
| 6 | Dan | `tribus/dan` | `onomastico/dan` |
| 7 | Neftalí | `tribus/neftali` | ficha personal de Neftalí, sin fusionar |
| 8 | Isacar | `tribus/isacar` | ficha personal de Isacar, sin fusionar |
| 9 | Zabulón | `tribus/zabulon` | `onomastico/zabulon` |
| 10 | Benjamín | `tribus/benjamin` | ficha personal de Benjamín, sin fusionar |
| 11 | Efraín | `tribus/efrain` | `onomastico/efrain` |
| 12 | Manasés | `tribus/manases` | `onomastico/manases` |
| 13 | Levitas | `tribus/levitas` | no confundir con la persona Leví |

**Precisiones aprobadas o derivadas del acuerdo:**

- **No crear una ficha tribal independiente de José.** La persona `onomastico/jose` se mantiene; su descendencia tribal se representa mediante las fichas de Efraín y Manasés.
- La ficha **Levitas** es una entidad tribal colectiva, distinta de Leví como individuo.
- La cifra de **13** corresponde a las fichas documentales que se elaborarán, **no** a un enunciado de trece tribus territoriales simultáneas. En el reparto de la tierra, Efraín y Manasés son dos unidades, mientras que Leví tiene una situación territorial especial (Jos 14:4). El recuento tradicional de doce no debe reinterpretarse automáticamente como trece territorios.
- El catálogo general puede mantener **Israelitas** (`tribus/israelitas`) como ficha de pueblo paraguas y otras fichas de tribus externas (Edomitas, Ismaelitas, etc.); **no se incluyen** en estas trece fichas.
- Los identificadores son propuestas de alta **para P4**; no se han creado las 13 entradas en `data/entries.json`.

## Resolución de Gn 48 en relación con las dos nuevas fichas

| Versículos | Clasificación aprobada por criterio mixto |
|---|---|
| Gn 48:1,5,8–14,17–18 | Identidad personal de Efraín y Manasés → Onomástico; Gn 48:5 admite nota sobre efectos tribales de su adopción |
| Gn 48:6,16 | Anuncios y derechos de descendencia → nota contextual a Tribus cuando corresponda |
| Gn 48:19 | Promesa del futuro colectivo de ambos → referencia **en nota** a `tribus/efrain` y `tribus/manases`, ya que el versículo **no menciona literalmente sus nombres** |
| Gn 48:20 | Nombres personales en la fórmula de bendición; enlaces Onomástico y nota cruzada a las tribus por la precedencia de Efraín |
| Gn 49:22–26 | José como persona y figura paterna → Onomástico; nota contextual a Efraín y Manasés cuando se trate de la descendencia |

## Próximo trabajo

1. Incorporar a la matriz de P3 Tribus las trece altas y las referencias de Gn 48–49, preservando las distinciones Israel persona/pueblo.
2. En P4, redactar las fichas necesarias y establecer vínculos recíprocos entre individuos y colectivos.
3. No alterar las escenas BES ni generar enlaces rotos antes de que existan las fichas.


## R-01 · Decisión editorial definitiva (25/11/2026)

**Aprobado:** la ficha tribal principal será **Israelitas** (`tribus/israelitas`). «Israel» será variante de búsqueda y remisión colectiva mediante `tribus/israel` (no segunda ficha principal); no afecta al Israel personal `onomastico/jacob`. **Solo registro de P3:** las rutas/fichas no se crean en esta fase.
