# Decisión editorial · Adopción de la BES en dos etapas

**Fecha:** 23 de noviembre de 2026. **Estado:** APROBADA por el editor.  
**Nombre de edición:** *La Biblia en Español Sencillo 2026* (BES 2026, SPNBES / `spabes`).  
**Fuente primaria:** https://ebible.org/spabes/GEN.htm  
**Licencia declarada por el editor de la traducción en eBible:** **dominio público**: https://ebible.org/spabes/copyright.htm (ficha también: https://www.ebible.org/find/details.php?id=spabes; edición de 30 de octubre de 2026).  
**Procedencia indicada:** AudioBiblia.org; traducido y editado por Irma Flores. Conservar la atribución y enlace a edición en la página o créditos del proyecto, aunque la fuente esté declarada de dominio público.

## Etapa I — Aprobada y activa

**Génesis 25:1–50:26, escenas 16–34:** continuar las fases **P2, P3, P4, P5, P6, P7, P8 y P9** usando **exclusivamente BES 2026 como texto base**, según el protocolo P0–P9. Mantener la Fase 1 **cerrada**, con los 19 títulos, 874 versículos y distribuciones de recursos ya aprobados.

- **P2**: importar BES 2026 desde su distribución oficial, no RVR1960; conservar los versículos literalmente y marcar discursos humanos/pensamientos y las palabras divinas en rojo, sin reescribir la traducción; generar las nuevas escenas, el índice por escenas y el índice tradicional solo cuando estén validados.
- **P3–P4**: extraer entidades y preparar fichas/relaciones contra la redacción de BES. **Los identificadores ya existentes no cambian**. Referencias RVR60, etimologías, variantes de nombres y notas existentes pueden diferir en BES: tratarlo como una cuestión editorial y conservar las relaciones, registrando variantes, sin sustituir el lenguaje de la primera etapa.
- **P5–P7**: reutilizar mapa, árbol, ilustraciones y decisiones de P1, ajustando la denominación y los enlaces solo en las escenas nuevas. Preparar artículos/notas nuevos conforme a BES, sin copiar explicaciones que dependan de una expresión peculiar de RVR60.
- **P8**: comprobar cobertura exacta de Gn 25–50 (874 versículos), integridad textual, texto divino en rojo, navegación entre «Familia» y «De Abraham a Isaac», links de apéndices y etiquetas visibles de versión mixta.
- **P9**: publicar las nuevas escenas únicamente después de revisar y aprobar su contenido según el protocolo. **No publicar borradores/maquetas ni eliminar/reconstruir las quince escenas anteriores.**

## Etapa II — Explicitamente pospuesta

**Génesis 1:1–24:67, escenas 1–15:** cuando el editor la abra expresamente, se migrarán **de RVR1960 a BES 2026**.

Hasta entonces quedan protegidos:

1. Su **texto bíblico RVR1960**, guiones, cursivas, discurso divino, notas 1–153 y revisión editorial aprobada.
2. Sus imágenes, mapas, árboles, índices, identificadores, enlaces, archivos de origen protegidos y páginas públicas.
3. Las citas textuales de RVR1960 en sus notas y fichas, salvo cambios mínimos indispensables para permitir la navegación hacia las escenas nuevas y la aclaración de edición de cada escena. Un ajuste de navegación nunca autoriza cambiar el contenido.

La traducción **no se cambia globalmente** en `data/genesis.json`, en `editorial/approved-pages/genesis/` ni en rutas anteriores a Génesis 25 durante la Etapa I. La fuente BES de capítulos 25–50 debe almacenarse separada (propuesta: `data/genesis_25_50_bes.json`).

## Convivencia temporal de versiones

Durante la Etapa I la web tendrá una edición **mixta y explícitamente indicada**:

| Escenas | Pasaje | Texto base | Estado |
|---|---|---|---|
| 01–15 | Gn 1–24 | **Reina-Valera 1960 (RVR60)** | Edición existente, protegida |
| 16–34 | Gn 25–50 | **Biblia en Español Sencillo 2026 (BES)** | En preparación P2–P9 |

- Poner la traducción correcta en el subtítulo/encabezado y créditos de cada escena nueva. El índice del libro debe explicar la coexistencia temporal.
- No etiquetar todo el libro como BES mientras queden las quince escenas anteriores en RVR60.
- No reescribir las notas para suprimir la diferencia de traducción; en el límite entre Gn 24 y 25 se podrá advertir el cambio de versión.
- Proteger anclas de versículo `gn-<capítulo>-<versículo>`, IDs, URL históricas y fichas. Cualquier nueva referencia desde BES a una ficha antigua requiere verificar homónimos y variantes.
- Las imágenes y genealogías se mantienen alineadas con los pasajes aprobados, no con el léxico de una traducción.

## Estado de ejecución

La decisión en dos etapas **no equivale a haber importado o publicado el texto**. El cambio a BES y su licencia declarada ya se han verificado en la página de eBible; el archivo de datos BES, la maquetación y las pruebas de P2 deben registrarse separadamente como realizados o pendientes conforme se ejecuten. La Etapa II permanece fuera de alcance hasta nueva orden editorial.
