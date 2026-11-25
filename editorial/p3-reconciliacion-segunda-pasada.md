# P3 · Reconciliación ampliada y cola residual (25/11/2026)

**Estado:** control contextual parcialmente ejecutado; no declarar P3 cerrada. Se conserva sin cambios el texto BES, el registro histórico y el barrido bruto.

## Resultado reproducible en el catálogo derivado

- **874** versículos BES, **1.682** registros de mención en el catálogo derivado.
- **316 registros** con reglas explícitas de reconciliación: **274 asignaciones contextuales**, **38 exclusiones**, **2 asociaciones contextuales**, **1 nota contextual**, **1 exclusión personal**.
- **1.331 candidatos de identificador único** permanecen en estado `candidato_unico_no_validado`: no suponer que son enlaces aprobados solo por tener un ID sugerido.
- **35 registros** siguen `candidato_no_reconciliado` (agrupados abajo). Esta cola no equivale automáticamente a 35 fichas nuevas.
- Se añadieron **196 reglas CT-11** y **8 reglas CT-12**, derivadas de aprobaciones existentes y de la lectura contextual del texto. Incluyen Súa, Basemat, Dan/Seir/Bela (matriz previa), Betel, Efrata, Gosén, Pozo/Cisterna, Copa, Saco, Galaad, Mahanaim y falsos positivos «sacó»/«espigas».
- La comprobación estructural directa de offsets contra BES y de las asignaciones múltiples ha pasado durante la generación del catálogo, sin detectar errores. **El resultado efectivo de GitHub Actions no se ha podido verificar** mediante los controles de estado disponibles (sin estados ni ejecuciones devueltos para el commit consultado). No se debe afirmar CI superado.

## Cola residual: términos para cotejo de fichas e IDs

| Término | Menciones | Referencias | Criterio de continuación |
|---|---:|---|---|
| Hamor | 10 | Gn 33:19, Gn 34:2, Gn 34:4, Gn 34:6, Gn 34:8, Gn 34:13, Gn 34:18, Gn 34:20, Gn 34:24, Gn 34:26 | Comprobar alta/variante e ID aprobado en el Excel de Onomástico y fuentes de P4 antes de fijar destino |
| Benoni | 1 | Gn 35:18 | Comprobar alta/variante e ID aprobado en el Excel de Onomástico y fuentes de P4 antes de fijar destino |
| madianitas | 3 | Gn 36:35, Gn 37:28, Gn 37:36 | Confirmar ID de pueblo o gentilicio en decisiones de Tribus antes de incorporar una ficha |
| Timna | 1 | Gn 36:40 | Jefatura homónima: no equiparar automáticamente a las Timna personales |
| ismaelitas | 4 | Gn 37:25, Gn 37:27, Gn 37:28, Gn 39:1 | Confirmar ID de pueblo o gentilicio en decisiones de Tribus antes de incorporar una ficha |
| Potifar | 4 | Gn 37:36, Gn 39:1, Gn 39:4, Gn 39:6 | Comprobar alta/variante e ID aprobado en el Excel de Onomástico y fuentes de P4 antes de fijar destino |
| Hira | 5 | Gn 38:1, Gn 38:12, Gn 38:20, Gn 38:22 | Comprobar alta/variante e ID aprobado en el Excel de Onomástico y fuentes de P4 antes de fijar destino |
| Pérez | 3 | Gn 38:29, Gn 46:12 | Comprobar alta/variante e ID aprobado en el Excel de Onomástico y fuentes de P4 antes de fijar destino |
| Zafnat-panea | 1 | Gn 41:45 | Comprobar alta/variante e ID aprobado en el Excel de Onomástico y fuentes de P4 antes de fijar destino |
| Potifera | 3 | Gn 41:45, Gn 41:50, Gn 46:20 | Comprobar alta/variante e ID aprobado en el Excel de Onomástico y fuentes de P4 antes de fijar destino |

## Precauciones técnicas

1. Las nuevas rutas `id_futuro` son **previsiones editoriales**, no páginas existentes; no crear enlaces públicos hasta P4/P9.
2. La matriz de 55 cruces ya está trasladada a la capa de reglas; el inventario original conserva sus alternativas para auditoría.
3. La capa de reglas no constituye todavía un extractor semántico que detecte todos los nombres/objetos ausentes. Faltan la revisión de cobertura total y la validación efectiva del workflow.
4. No declarar `candidato_unico_no_validado` como aprobado sin examinar su contexto; entre ellos puede haber homónimos y figuras retóricas.

**Siguiente actuación:** cotejar el Excel consolidado de Onomástico y el de Tribus para la cola residual; revisar los 1.331 candidatos únicos con reglas de exclusión, y confirmar el resultado de CI. No hay nuevas decisiones propuestas al editor en este documento.
