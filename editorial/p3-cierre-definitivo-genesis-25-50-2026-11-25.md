# BIBLILU · Génesis 25–50 · Acta de cierre de la Fase 3

**Cierre:** 25/11/2026. **Estado:** P3 CERRADA (revisión editorial y controles técnicos superados). El cierre no implica publicación web ni aprobación literal de fichas futuras.

## 1. Fuente y alcance

- Fuente textual: BES 2026, Génesis 25:1–50:26, **874 versículos** y **19 escenas**. No se altera el texto ni las escenas anteriores de Génesis 1–24 (RVR1960).
- Ocho categorías revisadas editorialmente: **Onomástico, Lugares, Seres Vivos, Materiales, Tribus, Objetos y Símbolos, Instrumentos Musicales, Medidas y Unidades**.
- Inventario bruto: **1.711 registros de categoría**, **1.656 posiciones únicas** y **55 solapamientos Onomástico/Lugares**.
- Catálogo reconciliado derivado: **1.973 menciones**, **1.918 reglas contextuales** y **55 cruces desambiguados**. Conserva exclusiones, asociaciones contextuales y fichas futuras sin inventar enlaces.

## 2. Decisiones definitivas

- **R-01:** Israelitas es ficha tribal principal; Israel es variante/remisión. Jacob / Israel personal permanece en Onomástico.
- **D-01:** Hebreos como variante/remisión a Israelitas, sin ficha tribal separada.
- **D-02:** Faraón utiliza la ficha onomástica existente como título regio, sin determinar monarcas.
- **D-03:** Ismaelitas y Madianitas son dos fichas tribales futuras distintas de Ismael y Madián; **4 y 3 menciones** respectivamente.
- **D-04:** crear en P4 una ficha independiente de **Débora, nodriza de Rebeca** (onomastico/debora-nodriza-rebeca), por Gn 35:8, con remisiones a Rebeca y Alón-bacut. El identificador está reservado; no hay todavía ficha pública.

**Aprobaciones editoriales adicionales conocidas pendientes: ninguna.**

## 3. Controles y validación final

- **CT-31:** coherencia formal de referencias, posiciones, identidades, 1.918 reglas y 55 cruces; sin errores detectados.
- **CT-32:** 24 familias léxicas y 230 apariciones contrastadas sin omisiones dentro del conjunto; cribado de mayúsculas interiores sin nuevo antropónimo/topónimo claramente confirmado.
- **GitHub Actions:** flujo P3 · Control de reconciliación Génesis 25–50, ejecución **#37**, rama **main**, commit **5ef657ac9a9a841864feba19e4c1f28889f05e74**, **éxito (verde)**, duración **9 segundos**, según captura aportada por el editor el 25/11/2026.
- El workflow comprende los scripts check_p3_reconciliacion.py, check_p3_cobertura_lexica.py y build_p3_catalogo_reconciliado.py --check, además de proteger los archivos fuente. El error anterior de D-03 se corrigió para verificar las reglas CT-13 existentes.

**Límite expreso:** el control CT-32 es dirigido y ningún algoritmo garantiza exhaustividad semántica absoluta. P3 se considera operativamente cerrada por conformidad editorial, controles satisfactorios y ausencia de incidencia concreta pendiente. Los hallazgos nuevos durante P4 se documentarán como revisiones retrospectivas.

## 4. Transferencia a P4 y fases siguientes

- **P4:** redactar y actualizar fichas por apéndice, revisar la existencia real de cada identificador, elaborar remisiones y relaciones; no crear rutas falsas ni reescribir fichas sin revisión.
- **P5:** árboles, mapas e imágenes; **P6:** revisión de escenas y notas; **P7:** documentación y bibliografía; **P8:** control integral; **P9:** publicar y verificar la web accesible.
- Preservar la distinción entre persona, colectivo y territorio (Israel/Edom); los homónimos (Siquem, Aná, Zera, Basemat, Abimelec/Ficol); las exclusiones de ganado y falsos positivos verbales; las notas interversionales Tof/Kinnor sin alterar BES.

## 5. Trazabilidad

- Registro: editorial/fase3-genesis.md
- Reglas: data/p3-reconciliacion-genesis-25-50.json
- Catálogo: data/p3-catalogo-reconciliado-genesis-25-50.json
- Auditoría: editorial/p3-ct31-control-integridad-25-11-2026.md
- Cobertura: editorial/p3-ct32-cobertura-lexica-y-nombres-genesis-25-50.md
- Workflow: .github/workflows/control-p3-reconciliacion.yml

**Conclusión: P3 de Génesis 25–50 cerrada. Se inicia la preparación de P4, sin publicar cambios.**
