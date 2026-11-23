# Fase 3 · Onomástico, lote 1: Génesis 25:1–18 (BES 2026)

**Estado:** **PROPUESTA PARA REVISIÓN**, sin modificación de fichas.  
**Fuente:** [BES 2026, datos base](../data/genesis_25_50_bes.json), Gn 25:1–18.  
**Registro:** [IDs aprobados hasta Génesis 24](../data/registro_maestro.json), con 450 identificadores.  
**Criterios:** [homónimos, variantes y equivalencias](criterios-identidades-genesis.md).

Esta es la primera **revisión contextual** de las coincidencias del barrido general P3. Se separan las coincidencias automáticas de las identidades que el propio texto permite resolver. Los hipervínculos a las fichas no se incorporan aún.

## 1. Descendencia de Abraham y Cetura (25:1–4)

| Grafía BES | Gn | Identificador que debe mantenerse | Observación |
|---|---|---|---|
| Abraham | 25:1 | `onomastico/abraham` | Persona ya registrada |
| Cetura | 25:1,4 | `onomastico/cetura` | Persona ya registrada |
| **Zimrán** | 25:2 | `onomastico/zimram` **(variante pendiente)** | La ficha histórica usa «Zimram». Conservar su ID y proponer «Zimrán» como variante de búsqueda BES, sin renombrar la ficha |
| Jocsán | 25:2–3 | `onomastico/jocsan` | Registrado |
| Medán | 25:2 | `onomastico/medan` | Registrado |
| Madián | 25:2,4 | `onomastico/madian` | Registrado |
| Isbac | 25:2 | `onomastico/isbac` | Registrado |
| **Súa** | 25:2 | `onomastico/sua` | Hijo de Cetura, **no** `onomastico/sua-suegro-de-juda`; la ficha existente ya distingue ambos |
| **Seba** | 25:3 | `onomastico/seba-hijo-de-jocsan` | No confundir con los Seba de Gn 10 |
| **Dedán** | 25:3 | `onomastico/dedan-hijo-de-jocsan` | No identificar con `onomastico/dedan` (descendiente de Raama) |
| Asurim, Letusim, Leumim | 25:3 | `onomastico/asurim`; `onomastico/letusim`; `onomastico/leumim` | Conservar las **tres fichas individuales** ya decididas editorialmente. BES usa «descendientes», no prueba por sí sola su individualidad histórica |
| Efa | 25:4 | `onomastico/efa` | Es un **nombre de hijo de Madián**, no una medida de capacidad |
| Efer | 25:4 | `onomastico/efer` | Registrado |
| **Hanoc** | 25:4 | `onomastico/hanoc-hijo-de-madian` | Diferente del Hanoc hijo de Rubén (Gn 46:9) |
| Abida | 25:4 | `onomastico/abida` | Registrado |
| Elda | 25:4 | `onomastico/elda` | Registrado |

## 2. Muerte de Abraham, sepultura y familia de Ismael (25:5–18)

| Nombre | Gn | Ficha correspondiente / decisión |
|---|---|---|
| Isaac | 25:5,9,11 | `onomastico/isaac` |
| Ismael | 25:9,12–17 | `onomastico/ismael` |
| Efrón | 25:9 | `onomastico/efron`, hijo del Zohar hitita de este pasaje |
| **Zohar** | **25:9** | **NO vincular a `onomastico/zohar`**: esa ficha documenta al **hijo de Simeón (Gn 46:10)**, mientras aquí se nombra al padre de Efrón. **Proponer ficha independiente** en P4: `onomastico/zohar-padre-de-efron` (ID provisional) |
| Sara | 25:10,12 | `onomastico/sara` |
| Agar | 25:12 | `onomastico/agar` |
| Nebaiot, Cedar, Adbeel, Mibsam | 25:13 | `onomastico/nebaiot`, `onomastico/cedar`, `onomastico/adbeel`, `onomastico/mibsam` |
| Misma, Duma, Massa | 25:14 | `onomastico/misma`, `onomastico/duma`, `onomastico/massa` |
| **Hadad** | **25:15** | **NO vincular a `onomastico/hadad-rey-de-edom`**: esa ficha es el hijo de Bedad de Gn 36:35; aquí es **un hijo de Ismael**. Proponer ficha independiente en P4: `onomastico/hadad-hijo-de-ismael` (ID provisional) |
| Tema, Jetur, Nafis, Cedema | 25:15 | `onomastico/tema`, `onomastico/jetur`, `onomastico/nafis`, `onomastico/cedema` |

**Nota sobre nombres homónimos:** la clasificación automática ha reconocido «Hadad» y «Zohar» como nombres que ya existen en fichas, pero **el contexto familiar de BES demuestra que esos identificadores existentes no son adecuados** para los individuos de 25:9 y 25:15. Estos casos deben impedirse específicamente al generar enlaces en P4/P6, sin reescribir ni fusionar las fichas antiguas.

## 3. Lugares y pueblos detectados en el mismo tramo (para sus lotes P3)

- **Macpela** (25:9–10): ficha existente de lugar/cueva, ligada a la sepultura.
- **Mamre** (25:9): mención **geográfica**, no remisión al patriarca amorreo homónimo.
- **Beer-lahai-roi** (25:11): topónimo BES que requiere contrastar con el lugar ya registrado «Pozo del Viviente-que-me-ve». **No unificar automáticamente**.
- **Havila y Sur** (25:18): lugares que delimitan la distribución de los descendientes de Ismael; «Sur» no aparece como encabezado de ficha histórica y debe estudiarse en el lote de Lugares.
- **Egipto** (25:18): ficha de lugar existente. La expresión «Agar la egipcia» (25:12) es un gentilicio, no un nuevo personaje.
- **Hitita / hijos de Het** (25:9–10): expresiones de pueblo o grupo, relacionadas con el tratamiento de los Heteos; registrar como **variantes léxicas por contrastar** en el lote Tribus.

## 4. Propuestas para resolución editorial

1. **Mantener** la ficha `onomastico/zimram` y **añadir «Zimrán» como variante BES** de búsqueda (solo tras aprobar la propuesta).
2. **Crear posteriormente dos fichas separadas** para **Zohar (padre de Efrón)** y **Hadad (hijo de Ismael)**, sin alterar las fichas preexistentes de los homónimos. Identificadores provisionales indicados arriba.
3. Resolver por contexto los homónimos ya registrados: Súa de Cetura; Seba y Dedán de Jocsán; Hanoc hijo de Madián; Efa como persona; Mamre como lugar.
4. Conservar Asurim, Letusim y Leumim **como fichas personales independientes**, conforme a la decisión editorial previa.
5. Pasar topónimos y gentilicios a los lotes propios de **Lugares** y **Tribus**, sin fusionar identidades por semejanza de nombres.

**No se ha creado ninguna ficha ni se ha modificado ningún enlace.** Los resultados del análisis automático de los 874 versículos siguen siendo candidatos; esta tabla es una primera propuesta contextualizada del Onomástico para revisión y aprobación.
