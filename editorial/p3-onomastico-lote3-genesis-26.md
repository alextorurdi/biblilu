# Fase 3 · Onomástico, lote 3: Génesis 26 (BES 2026)

**Estado editorial: PROPUESTA DE CLASIFICACIÓN, NO APROBADA.** El texto base es `data/genesis_25_50_bes.json` (Gn 26:1–35). Se contrasta con `data/entries.json`, `data/registro_maestro.json` y los acuerdos de `editorial/criterios-identidades-genesis.md`.

## Inventario de personas (once nombres, dos pendientes de ficha)

| Denominación en el capítulo | Menciones BES | Identificador o alta propuesta | Resolución contextual |
|---|---|---|---|
| Abraham | 26:1,3,5,15,18,24 | `onomastico/abraham` | Padre de Isaac, ficha ya existente |
| Isaac | 26:1–33 (menciones repetidas) | `onomastico/isaac` | Protagonista, ficha ya existente |
| Rebeca | 26:7–8,35 | `onomastico/rebeca` | Esposa de Isaac, ficha ya existente |
| Abimelec | 26:1,8–11,16,26 | `onomastico/abimelec` | Rey de Gerar; conservar la ficha compartida con Gn 20–21 **sin afirmar identidad individual entre episodios** |
| Ficol | 26:26 | `onomastico/ficol` | Jefe del ejército; conservar la ficha compartida con Gn 21 **sin afirmar identidad individual entre episodios** |
| **Ahuzat** | **26:26** | **Nueva ficha propuesta `onomastico/ahuzat`** | Consejero de Abimelec en la BES; acompaña al rey y a Ficol en la visita a Isaac |
| Esaú | 26:34 | `onomastico/esau` | Hijo de Isaac y Rebeca, esposo de Judit y Basemat en el relato |
| Judit | 26:34 | `onomastico/judit-hija-de-beeri` | Hija de Beeri, distinta de Aholibama salvo prueba textual posterior |
| **Beeri** | **26:34** | **Nueva ficha propuesta `onomastico/beeri-heteo`** | Heteo, padre de Judit; preferir ID desambiguado para no identificarlo con otros homónimos de libros posteriores |
| Basemat | 26:34 | `onomastico/basemat-hija-de-elon` | Hija de Elón, no la `onomastico/basemat-hija-de-ismael`; no fusionar con Ada |
| Elón | 26:34 | `onomastico/elon-padre-de-basemat` | Heteo, padre de Basemat; distinto del `onomastico/elon` hijo de Zabulón (Gn 46:14) |

## Justificación de las dos altas propuestas

**Ahuzat (Gn 26:26).** La BES identifica a un acompañante de Abimelec como «Ahuzat, su consejero». Es un individuo con nombre propio que no tiene actualmente entrada `onomastico/ahuzat` en `data/entries.json` ni en el registro maestro. **P4:** preparar ficha con relaciones y hechos del pacto; no añadir genealogía ficticia.

**Beeri (Gn 26:34).** El pasaje identifica como «Beeri el hitita» al padre de Judit, una de las mujeres de Esaú. El nombre aparece en la ficha de Judit, pero no tiene ficha individual. **P4:** preparar `onomastico/beeri-heteo`, conservando la relación familiar; no identificarlo automáticamente con otro Beeri que aparezca en otros libros.

## Resoluciones establecidas anteriormente que se mantienen

1. **Abimelec:** el ID compartido agrupa referencias de Gn 20–21 y 26; no concluye que fueran un solo rey ni impone que fueran reyes diferentes. Véase `editorial/criterios-identidades-genesis.md`.
2. **Ficol:** se mantiene el mismo criterio: una ficha, identidad entre generaciones indeterminada.
3. **Judit y Basemat:** conservar cada una en su ficha. No equiparar a Judit con Aholibama ni a Basemat hija de Elón con Ada hija de Elón; tampoco confundir con Basemat hija de Ismael.
4. **Elón:** desambiguar al padre de Basemat frente a Elón hijo de Zabulón.
5. **Ahuzat y Beeri:** son **propuestas de nuevas fichas** (en P4), no altas aprobadas ni implementadas.

## Incidencia de extracción detectada

**Gn 26:33 «Seba»:** el extractor P3 registra el vocablo como si pudiera referirse a una de varias personas llamadas Seba. El texto BES lo determina explícitamente como **nombre del pozo**: «Isaac llamó al pozo Seba». Debe **excluirse del Onomástico en ese versículo** y remitirse a la revisión de **Lugares** como topónimo asociado a Beerseba. No crear persona ni ligar al hijo de Jocsán, ni a los Seba de Gn 10. La corrección del extractor/catálogo se hará tras la aprobación del lote, con prueba de regresión.

## Remisiones a otras categorías (sin decisión de ficha en P3 Onomástico)

- **Lugares:** Gerar (26:1,6,17,20,26), Egipto (26:2), Beerseba (26:23,33), y **Esec** (26:20), **Sitna** (26:21), **Rehobot** (26:22) y **Seba** (26:33), nombres de pozos. Esec, Sitna, Rehobot y Seba no figuran como fichas independientes en `data/entries.json`; estudiar en el lote de Lugares si corresponde ficha de lugar, remisión, tratamiento colectivo o nota.
- **Tribus:** filisteos (26:1,8,14–15,18); «hitita» (26:34, aplicado a Beeri y Elón), cotejar con la ficha de Heteos.
- **Seres Vivos:** ovejas y ganado (26:14). Las ovejas corresponden a ficha existente; evaluar el uso genérico de «ganado».
- **Objetos:** pozos (26:15,18–22,25,32–33), altar y tienda (26:25); las dos últimas categorías cuentan con fichas, sin decidir si los pozos genéricos precisan nueva ficha.
- **Instrumentos y Medidas:** no hay menciones candidatas en el barrido de este capítulo.

## Estado y siguiente tramo

**Sin cambios en las fichas fuente, los árboles o el texto bíblico.** Pendientes de aprobación: dos altas onomásticas, asignaciones contextuales del lote y corrección de la falsa clasificación «Seba» (Gn 26:33).

**Siguiente lote:** Génesis 27, con especial atención a la identidad personal de Esaú/Jacob, los nombres familiares en la bendición, y la separación entre menciones personales y gentilicios.


## Cierre editorial aprobado · 25/11/2026

7. **Abimelec y Ficol (Gn 26) — APROBADO:** Mantener las fichas compartidas con Gn 20–21 sin afirmar ni negar identidad biográfica entre los episodios.
8. **Ahuzat (26:26) — APROBADO:** Aprobada nueva ficha `onomastico/ahuzat` para elaborar en P4.
9. **Beeri (26:34) — APROBADO:** Aprobada nueva ficha `onomastico/beeri-heteo` para elaborar en P4.
10. **Familia de Esaú y Seba (Gn 26) — APROBADO:** Distinguir Judit, Basemat hija de Elón y Elón padre de Basemat; Seba (26:33) es pozo, excluido del Onomástico y remitido a Lugares.

**Estado final del lote 3: aprobado editorialmente.** Ahuzat y Beeri son **altas de fichas autorizadas para P4**, no fichas creadas ni publicadas. El registro de Seba (Gn 26:33) en el extractor es un **falso positivo técnico conocido**, pendiente de corrección y prueba de regresión; no constituye una decisión editorial abierta. Permanecen como tareas de P4 y fases siguientes las fichas, los vínculos, la actualización técnica del extractor y la publicación. Las posibles identificaciones personales entre episodios de Abimelec y Ficol quedan expresamente indeterminadas por criterio aprobado, no pendientes de aprobación.
