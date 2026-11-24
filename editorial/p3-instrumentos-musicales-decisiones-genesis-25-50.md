# Fase 3 · Instrumentos Musicales — decisiones editoriales aprobadas (Génesis 25–50)

**Fecha:** 24/11/2026. **Estado:** P3 de Instrumentos Musicales **aprobada editorialmente**. No implica que las nuevas fichas o notas se hayan implementado en las escenas publicadas.

**Base:** texto BES 2026, `data/genesis_25_50_bes.json` (874 versículos); texto RVR1960 y original hebreo para contraste interversional; ficha existente `instrumentos/kinnor` en `data/instrumentos_revision.json`; revisión en `BIBLILU_Genesis_P3_Instrumentos_Musicales_25-50_Revision.xlsx`, incidencias IM-01–IM-11.

## Decisiones aprobadas

1. **Alta nueva:** ficha **Tof (tōf)**, ID previsto `instrumentos/tof`, instrumento de percusión descrito prudentemente como tamborín o tambor de mano. Reservar descripción y recursos definitivos para P4. No atribuirle necesariamente sonajas metálicas.
2. **Reutilizar ficha existente:** `instrumentos/kinnor` (lira, traducida «arpa» en RVR1960), que ya incluye Gn 31:27.
3. **Nota editorial obligatoria en Gn 31:27:** explicar la especificación hebrea/RVR1960 que la BES 2026 recoge con «cantos y música» y enlazar **Tof** y **Kinnor** desde la nota.
4. **Preservar íntegramente la BES 2026**, sin reemplazar «música» por «tamborín y arpa» ni crear un enlace automático desde una sola palabra genérica hacia dos fichas.
5. **Precaución interpretativa:** Labán afirma que **habría podido** despedir a Jacob con música; el versículo **no relata que esa celebración se produjera**.
6. **Cantos** es expresión vocal, no instrumento físico; no origina una ficha en este apéndice.
7. `instrumentos/ugab` se conserva y no recibe una mención nueva en Génesis 25–50; Gn 4:21 continúa como mención de *ugab* y *kinnor* en el tramo RVR1960.
8. **Controles negativos:** Gn 27:21 «tocarte» (contacto físico); Gn 29:22 y 40:20 «fiesta» (sin instrumento nombrado); Gn 49:5 «instrumentos de violencia» (armas).
9. **Extractor P3:** registrar el contraste interversional Gn 31:27 como prueba técnica, pero no inventar menciones literales de `tōf` y `kinnôr` en la BES.
10. **Recursos visuales de Tof:** no seleccionar una representación organológica definitiva sin revisar las evidencias y cronología.

Las **11 incidencias** del Excel quedan resueltas conforme a estas instrucciones, sin alterar las menciones documentales.

## Texto propuesto de la nota editorial para Gn 31:27

> La expresión «cantos y música» de la BES 2026 resume dos instrumentos mencionados expresamente en el texto hebreo: el *tōf*, y el *kinnôr*, traducido como traducido «tamborín» y «arpa» respectivamente en la RVR1960.

**Anclaje editorial:** Gn 31:27, asociado a la cláusula «cantos y música». Al implementar la nota, enlazar los términos *tōf* y *kinnôr* a `instrumentos/tof` y `instrumentos/kinnor` respectivamente, **sin añadir ni cambiar palabras** del texto aprobado y sin enlazar la palabra genérica «música» de la BES. Los enlaces son metadatos/maquetación, no contenido adicional. El texto de la nota se conserva **literalmente**, incluso la reiteración «traducido como traducido».

## Inventario final de Instrumentos Musicales (Génesis)

| Ficha | Situación | Génesis |
|---|---|---|
| `instrumentos/kinnor` | Existente, conservar | Gn 4:21 (RVR1960); Gn 31:27 (nota interversional) |
| `instrumentos/ugab` | Existente, sin aparición nueva Gn 25–50 | Gn 4:21 (RVR1960) |
| `instrumentos/tof` | **Alta aprobada**, por crear en P4 | Gn 31:27 (hebreo/RVR1960; nota BES) |

**Balance:** 2 fichas existentes + 1 ficha aprobada para nueva creación = **3 fichas previstas** del Apéndice, sin perjuicio de otras que puedan incorporarse en libros posteriores. El desarrollo de la ficha Tof, la nota funcional, enlaces y publicación se reservan para P4 y fases posteriores.
