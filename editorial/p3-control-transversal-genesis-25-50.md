# P3 · Control transversal de Génesis 25–50 (BES 2026)

**Fecha de ejecución:** 25/11/2026. **Estado:** **CONTROL ESTRUCTURAL EJECUTADO; CONTROL CONTEXTUAL TÉCNICO PENDIENTE**. Las ocho revisiones editoriales están aprobadas, pero **no se certifica todavía el cierre técnico de P3 ni la publicación**. Esta auditoría utiliza los archivos actuales de GitHub (rama `main`) y los registros editoriales aprobados; el extractor automático sigue siendo una capa de candidatos, no el catálogo clasificado definitivo.

## A. Integridad del texto y de los candidatos

- Fuente `data/genesis_25_50_bes.json`: **874 versículos**, **874 referencias distintas**, tramo Gn 25:1–50:26 (26 capítulos).
- Inventario `data/p3-extracciones-genesis-25-50.json`: **1711 registros de categoría**, con **1.656 menciones únicas** según el resumen de extracción: la diferencia incluye **55 coincidencias entre Onomástico y Lugares** sobre la misma posición textual. Las coincidencias cruzadas **no son duplicidades indebidas por sí mismas**; son candidatos sin desambiguación definitiva en el archivo bruto.
- Reparto bruto de registros: `onomastico` 1210; `lugares` 228; `animales` 115; `materiales` 23; `tribus` 43; `objetos` 87; `instrumentos` 0; `medidas` 5.
- Errores estructurales encontrados: referencias sin versículo **0**; posiciones/literales incompatibles con el versículo **0**; IDs candidatos inexistentes en el registro histórico **0**; registros idénticos dentro de una categoría **0**.
- **Limitación:** las pruebas anteriores verifican integridad formal, pero no detectan omisiones léxicas ni certifican automáticamente asignaciones individuales.

## B. Desajustes comprobados entre inventario automático y acuerdos aprobados

| Código | Evidencia actual | Decisión editorial vigente | Acción necesaria |
|---|---|---|---|
| CT-01 | Gn 26:33: `Seba` se propone aún como cuatro personas en Onomástico | Es un **pozo**; ficha futura `lugares/seba-pozo` aprobada en Lugares | Suprimir falso candidato personal y registrar candidato geográfico, con prueba de regresión |
| CT-02 | Gn 29:15: `seas` figura como posible medida | Es forma verbal («aunque seas»), no `Seá` | Excluir de Medidas; prueba de falsos positivos |
| CT-03 | Gn 31:27: **0 registros instrumentales**, aunque el versículo dice «cantos y música» | Nota editorial con Tof/Kinnor aprobada; la BES no menciona literalmente los nombres | Mantener **mención contextual interversional**, sin inventar aparición literal en BES; implementar nota y ficha en P4 |
| CT-04 | Gn 42:5, 45:21, 46:8 y 50:25 contienen «hijos de Israel», sin captura de «Israel» | Onomástico aprobó remisión personal a Jacob en estos pasajes | Incluir expresiones compuestas según contexto, sin generalizar a todas las menciones |
| CT-05 | Gn 32:3 y 36:32 presentan Edom territorial; el barrido bruto no registra de manera íntegra sus menciones en Lugares | Clasificación territorial en `lugares/edom`, incluida **Gn 36:32** por corrección expresa | Completar inventario y respetar la excepción territorial aprobada |
| CT-06 | Gn 33:19: `monedas` queda sin ID en Medidas | Ficha futura Qesitá, equivalencia monetaria no determinada | Relacionar la mención BES con `medidas/qesita`, sin inferir siclos |
| CT-07 | Gn 35:16 y 48:7: ninguna mención registrada como Kibrá por el extractor literal | Ficha Kibrá y nota explicativa aprobadas | Registrar asociación contextual sin alterar «cierta distancia» en BES |
| CT-08 | Gn 37:24: dos apariciones de «pozo» se registran sin ficha | Distinción aprobada: cisterna seca (*bôr*) frente a pozo de agua | Asignar ambas apariciones a futura ficha Cisterna, preparar nota P4; no modificar la BES |
| CT-09 | El extractor mantiene candidatos `ganado` en Seres Vivos | Acuerdo expreso: **no enlazar «ganado»** en Génesis 25–50 | Preservar como exclusión/no enlace y añadir prueba de regresión |
| CT-10 | 55 coincidencias de Onomástico/Lugares sobre igual fragmento | Distinguir homónimos por contexto: Mamre, Havila, Harán, Dan, Canaán, Seir, Bela, etc. | Producir matriz exhaustiva de 55 cruces y resolver contra los acuerdos; no contarlos como 55 errores |

## C. Control de coherencia editorial

- **Onomástico:** los lotes Gn 25–26 están aprobados, junto con Gn 27–50. Conservar las identidades separadas de Súa, Seba, Dedán, Hanoc, Zohar, Hadad, Judit/Basemat, Potifar/Potifera y las reglas contextualizadas de Israel/Edom. Abimelec/Ficol mantienen **identidad biográfica indeterminada**, conforme al acuerdo, sin nueva aprobación necesaria.
- **Lugares:** 34 incidencias aprobadas; 31 altas previstas, incluido Seba (pozo), que no sustituye automáticamente a Beerseba.
- **Seres Vivos:** 30 incidencias y 10 altas aprobadas; respetar la exclusión de «ganado» y las asociaciones aprobadas al Ángel de Jehová.
- **Materiales:** 30 incidencias cerradas; 15 altas aprobadas sobre 12 existentes; Cilicio se ubica en Objetos, no Materiales. «Mar Salado» (Gn 14:3) no se enlaza a Sal; Gn 19:26 sí corresponde a Sal.
- **Tribus:** 13 fichas del conjunto de Jacob aprobadas; aplicar criterio mixto persona/colectivo en Gn 48–49 y no crear José (tribu).
- **Objetos:** 40 incidencias resueltas; 27 altas (26 aprobadas en la revisión + Cilicio ya aprobado), 7 fichas preexistentes; nota sobre Cisterna pendiente de redacción final P4.
- **Instrumentos:** 11 incidencias aprobadas; Tof es alta y Kinnor existente; Gn 31:27 requiere nota, no vinculación léxica directa de «música».
- **Medidas:** 30 incidencias cerradas (21 respuestas expresas + 9 inferidas con autorización); Qesitá, Kibrá, Diezmo y Quinto son altas aprobadas.

## D. Estado y separación de trabajo

1. **Decisiones editoriales pendientes de aprobación:** ninguna detectada en los registros de cierre consultados. No reabrir las decisiones ya tomadas por la mera presencia de candidatos antiguos.
2. **Incidencias técnicas verificadas:** CT-01 a CT-09, más la matriz contextual exhaustiva CT-10. Estas son tareas para actualizar/certificar el catálogo y añadir pruebas, no nuevas preguntas al editor.
3. **Pruebas no ejecutadas:** no consta en este control una ejecución regenerada del extractor con todas las reglas editoriales, ni una comparación automatizada completa de los 55 cruces, ni un control de cobertura semántica de todas las expresiones BES. Por tanto, **P3 no se certifica como cerrada técnicamente**.
4. **P4 y posteriores:** redacción de fichas, notas definitivas y enlaces; recursos, revisión visual y publicación conforme al protocolo. No modificar el texto BES como atajo del extractor.

**Conclusión:** superada la comprobación de integridad formal del inventario, **queda abierto el control de clasificación contextual**. Las ocho categorías sí están aprobadas editorialmente, pero no procede declarar cierre integral hasta reconciliar los candidatos brutos con las decisiones y correr controles de regresión.
