# Fase 3 · Medidas y Unidades — respuestas editoriales recibidas (Génesis 25–50)

**Fecha de registro:** 25/11/2026. **Texto base:** BES 2026, `data/genesis_25_50_bes.json` (874 versículos). **Fuente de autoridad:** archivo del editor `BIBLILU_Genesis_P3_Medidas_y_Unidades_25-50_Revision(1).xlsx`, pestaña **Incidencias**, columna «Acción editorial». **Estado:** decisiones **parcialmente consolidadas**; **21 interpretables y 9 celdas con el valor no explicado «355»**. NO cerrar P3 Medidas y Unidades ni interpretar «355» como aprobación o rechazo.

## Altas decididas expresamente para P4

| Incidencia | Ficha | ID futuro | Pasaje | Acuerdo |
|---|---|---|---|---|
| MU-01 | Qesitá | `medidas/qesita` | Gn 33:19 | **Aprobar**. Valor antiguo desconocido; no inventar equivalente moderno ni identificar sin reservas con el siclo |
| MU-03 | Kibrá | `medidas/kibra` | Gn 35:16; 48:7 | **Crear ficha y nota editorial** con texto del editor, reproducido íntegro abajo |
| MU-08 | Diezmo | `medidas/diezmo` | Gn 28:22 | **Ficha Diezmo** (proporción 1/10; nueva alta por decisión expresa del editor) |
| MU-09 | Quinto | `medidas/quinto` | Gn 41:34; 47:24,26 | **Ficha Quinto** (fracción 1/5 = 20%; nueva alta por decisión expresa del editor) |

El editor descartó expresamente **Semana** (MU-05/06), «tres días de camino» como nueva ficha (MU-07) y las unidades de tiempo ordinarias (MU-24), aunque se conservan como información contextual cuando aparece en el texto. **Siclo** figura en el catálogo publicado; **Codo** y **Seá** están aprobados editorialmente desde una revisión anterior, pero aún pendientes de alta.

## Notas editoriales autorizadas

### MU-03 · Gn 35:16 y Gn 48:7, Kibrá

> El término hebreo kibrāh, traducido como «media legua» en la RVR1960, designa una extensión de terreno cuya longitud se desconoce. No está claro si constituía una unidad de medida convencional o si simplemente expresaba una distancia indeterminada como "a un tiro de piedra", "andando un trecho", etc.

**Enlace:** `medidas/kibra`, desde las notas del texto BES, preservando «cierta distancia» en los versículos. La atribución de una longitud concreta en kilómetros no está respaldada por el hebreo; véase [BDB/H3530](https://www.blueletterbible.org/lexicon/h3530/nasb20/wlc/).

### MU-11 · Gn 37:28, veinte piezas de plata

> El texto hebreo dice literalmente «veinte de plata», sobreentendiéndose el siclo como unidad de peso. No se trataba necesariamente de monedas, puesto que en aquella época la plata se utilizaba como medio de pago mediante su pesaje.

**Instrucción literal del editor:** «Enlazar Plata y Siclo». Destinos `materiales/plata` y `medidas/siclo` desde la nota, sin sustituir «piezas de plata» en BES.

### MU-12 · Gn 45:22, trescientas piezas de plata

> El texto hebreo dice literalmente «trescientos de plata», sobreentendiéndose el siclo como unidad de peso. No se trataba necesariamente de monedas, puesto que en aquella época la plata se utilizaba como medio de pago mediante su pesaje.

**Instrucción literal del editor:** «Enlazar Plata y siclo». Destinos `materiales/plata` y `medidas/siclo` desde la nota, sin alterar la BES.

El análisis del original hebreo confirma que «siclo» es una unidad contextual sobreentendida, no un sustantivo expresamente presente en esas dos cláusulas. Véanse los análisis interlineales de [Gn 37:28](https://biblehub.com/text/genesis/37-28.htm) y [Gn 45:22](https://biblehub.com/text/genesis/45-22.htm).

## Otras decisiones expresas

- **Descartar**: MU-05, MU-06, MU-07, MU-13, MU-14, MU-15, MU-24, MU-25, MU-26, MU-27.
- **No enlazar**: MU-16 (**Efa**, persona Gn 25:4), MU-17 (**Gera**, persona Gn 46:21), MU-18 (**seas**, verbo Gn 29:15), MU-19 (**sea**, verbo), MU-20 (**cabo** en «al cabo de»).
- Estos descartes no borran sus menciones de las hojas de auditoría, ni anulan las altas expresas de **Diezmo y Quinto**.

## Nueve celdas ambiguas: «355»

En el Excel recibido, las siguientes incidencias muestran **solo «355»** en «Acción editorial»: **MU-02, MU-04, MU-10, MU-21, MU-22, MU-23, MU-28, MU-29, MU-30**.

Su significado **no se puede inferir** y no equivale a aprobado, descartado o «sin cambios». En `Altas_propuestas` aparece también «355» en las tres filas originales; para Qesitá, Kibrá y Semana prevalecen las instrucciones expresas de MU-01, MU-03 y MU-05/06. Las nueve incidencias ambiguas **siguen pendientes de aclaración** aunque algunas sean coherentes con criterios aprobados.

## Estado y entrega

- 30 incidencias recibidas; **21 interpretables**, **9 por aclarar**.
- 4 altas nuevas autorizadas para preparar en P4: Qesitá, Kibrá, Diezmo, Quinto. Semana descartada.
- 3 notas editoriales autorizadas: Kibrá (Gn 35:16 y 48:7), Plata/Siclo (Gn 37:28), Plata/Siclo (Gn 45:22).
- Excel consolidado en la conversación: `BIBLILU_Genesis_P3_Medidas_y_Unidades_25-50_Respuestas_Consolidadas.xlsx`, con acciones originales preservadas, resultados de incidencia, fichas y notas.
- **Sin cambios en `data/entries.json`, escenas o web publicada.** No cerrar editorialmente esta categoría hasta resolver las nueve celdas.
