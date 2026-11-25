# BIBLILU · P3 · CT-32: cobertura léxica dirigida y cribado de nombres
**Fecha:** 25/11/2026. **Libro:** Génesis 25–50 (BES 2026). **Carácter:** auditoría complementaria, sin publicar la web.

## A. Prueba reproducible

Se ha añadido `scripts/check_p3_cobertura_lexica.py` al workflow `.github/workflows/control-p3-reconciliacion.yml`, con **24 familias léxicas** controladas contra la unión del inventario bruto y las reglas contextuales aprobadas: sangre, agua, caballo, asno, oveja, camello, leche, vino, oro, plata, sal, espada, cama, copa, saco, mesa, cadena, cordón, anillo, aretes, canasta, rocío, pozo y faraón.

La revisión directa de los **874 versículos** halló **230 apariciones** para esas 24 familias, **todas** con posición de texto registrada en al menos una de las capas P3; **0 omisiones** en estas familias. Se conservan exclusiones contextuales (p. ej., `vino` verbal, `sal` imperativo), que **no** se confunden con enlaces de materiales.

## B. Cribado adicional de mayúsculas interiores

Se compararon tokens iniciados con mayúscula dentro de versículos contra las posiciones registradas de candidatos y reglas. Los residuos son mayoritariamente palabras normales al comienzo de otra frase o intervención: *Entonces, Pensaba, Hiciste, Vayan*, etc. No se confirmó un nuevo antropónimo o topónimo omitido en esa pasada heurística.

**Casos de lectura retórica**: Gn 49:24, «Poderoso», «Pastor», «Roca de Israel» son títulos/designaciones teológicas figuradas. No deben generar por sí solos personas distintas ni un enlace literal a `materiales/piedra`; reservar el tratamiento de la expresión para P6 (revisión de escena/notas), conservando el texto BES.

## C. Separación de P3/P4 y estado de cierre

D-04 permanece aprobada para la ficha futura **Débora (nodriza de Rebeca)** (`onomastico/debora-nodriza-rebeca`), mencionada en Gn 35:8. La regla CT-30 sigue con `id:null`, porque **P3 clasifica, P4 materializa fichas y enlaces**. Otras identidades correctamente identificadas sin ficha histórica (p. ej. Hamor, Siquem persona, Hira, Potifar, Potifera, descendientes horeos) se resolverán en P4 conforme a sus acuerdos, sin inventar URL funcional.

**Limitación explícita:** el control de 24 familias es dirigido, no exhaustivo de todo el vocabulario BES. La revisión de mayúsculas tampoco garantiza exhaustividad semántica. El nuevo workflow está preparado, pero la herramienta de consulta de ejecuciones solo devuelve las asociadas a PR y el estado combinado de los últimos commits no proporciona checks; **no se puede certificar desde aquí que GitHub Actions haya terminado en verde**. Falta confirmación externa o una ejecución completa verificable de los scripts `check_p3_reconciliacion.py`, `check_p3_cobertura_lexica.py` y `build_p3_catalogo_reconciliado.py --check`.

**Resultado:** CT-32 sin incidencias nuevas en el dominio examinado; P3 técnicamente aún abierta hasta validación de CI y certificación explícita de la cobertura final. No pedir al editor aprobación de lo ya resuelto.
