# Fase 2 · Génesis 25–50 — BES 2026, marcado e índices

**Fecha de inicio:** 23/11/2026. **Actualización editorial:** 23/11/2026.  
**Estado:** **EN CURSO — INFRAESTRUCTURA PREPARADA; IMPORTACIÓN BES Y REVISIÓN DEL TEXTO PENDIENTES.**  
**Alcance invariable de Etapa I:** 19 escenas, Gn 25:1–50:26, traducción **La Biblia en Español Sencillo 2026 (BES)**. Las 15 escenas de Gn 1–24 **conservan RVR1960** hasta la segunda etapa, sin cambios de texto ni notas.

**Documentos rectores:** [Protocolo P0–P9](protocolo-libros.md) · [BES en dos etapas](plan-dos-etapas-bes-genesis.md) · [P1 aprobada](fase1-genesis.md) · [Distribución de recursos](plan-ubicacion-escenas-genesis-25-50.md).

## Derechos y fuente oficial comprobados

- **Edición:** *La Biblia en Español Sencillo 2026*, publicada en eBible, traducción y edición de **Irma Flores**, AudioBiblia.org, fecha de la fuente **30/10/2026**.
- **Licencia declarada:** **dominio público**, según [página de derechos oficial de eBible](https://ebible.org/spabes/copyright.htm).
- **Génesis por capítulos:** [https://ebible.org/spabes/GEN.htm](https://ebible.org/spabes/GEN.htm).
- **Paquete USFM oficial:** [https://ebible.org/Scriptures/spabes_usfm.zip](https://ebible.org/Scriptures/spabes_usfm.zip); enlazado desde la [ficha de descargas](https://www.ebible.org/find/details.php?id=spabes).
- La declaración de dominio público permite trabajar sobre esta versión según la información del distribuidor; conservar atribución y procedencia documental aun cuando no se imponga una licencia de atribución.
- La traducción **no será homogeneizada con la RVR1960**: respetar literalmente los cambios de vocabulario y los nombres propios de la BES, anotando variantes y diferencias donde tengan repercusión editorial.

## Trabajo efectivamente registrado

1. **Catálogo P1:** [19 escenas aprobadas](catalogo-escenas-genesis-25-50.json), 874 versículos distribuidos sin solapamientos. Texto anterior de Gn 1–24: 659 versículos.
2. **Rutas y anclas:** [p2-rutas-genesis-25-50.json](p2-rutas-genesis-25-50.json) describe las 19 rutas y el índice tradicional de los 26 capítulos, con enlaces `gn-<capítulo>-<versículo>`.
3. **Validador y previsualizador:** [prepare_genesis_p2.py](../scripts/prepare_genesis_p2.py) exige datos con textos completos y admite marcar discursos/pensamientos/palabras divinas de modo reversible. Genera previsualizaciones en **`build/p2/`**, nunca en `docs/`.
4. **Importador para BES 2026:** [import_bes_genesis.py](../scripts/import_bes_genesis.py) descarga o acepta el ZIP USFM de eBible; selecciona Génesis, extrae sus versos, comprueba la cobertura exacta de 874 y verifica un versículo testigo (25:1). Escribe **`data/genesis_25_50_bes.json`** y **`editorial/procedencia-bes-genesis-25-50.json`** con hash de la fuente. **El script está incorporado, todavía no consta una importación ejecutada del ZIP oficial.**
5. **Prueba sintética:** [test_genesis_p2.py](../scripts/test_genesis_p2.py) prepara textos de prueba y comprueba las 874 anclas y que el marcado no cambie el texto; está incorporada pero su ejecución en el repositorio todavía no ha sido verificada.
6. **Esquema de datos:** [esquema-fuente-genesis-25-50.json](esquema-fuente-genesis-25-50.json). El fichero BES debe mantenerse separado del `data/genesis.json` histórico de RVR60.
7. **Cabeceras por traducción:** las 19 futuras escenas estarán identificadas **BES 2026**. Durante Etapa I, los índices tendrán una nota inequívoca del régimen mixto **1–15 RVR1960 / 16–34 BES 2026**, evitando anunciar todo Génesis como una única traducción.

## Instrucciones de la importación

```bash
# Paso I: importar desde el paquete USFM oficial BES 2026
python scripts/import_bes_genesis.py --download

# Alternativa: descargar primero el ZIP desde eBible
python scripts/import_bes_genesis.py --zip /ruta/spabes_usfm.zip

# Paso II: validar los datos y la estructura P1
python scripts/prepare_genesis_p2.py --structure
python scripts/prepare_genesis_p2.py --check-source
python scripts/test_genesis_p2.py

# Paso III: generar páginas e índices de borrador, NO publicables
python scripts/prepare_genesis_p2.py --build-draft
```

Los archivos resultantes de `build/p2/` son solo borradores de estructura y texto. La edición narrativa y tipográfica final —diálogos, cursivas, pensamientos, guiones y las palabras de Dios en rojo— requiere revisión textual según las decisiones de BIBLILU. Las herramientas automáticas **no deben adjudicar todas las palabras de «Dios» o «Señor» a un discurso divino**.

## Condiciones para cerrar P2

- [x] Pasaje, 19 escenas, títulos y distribución aprobados.
- [x] Rutas y diseño de los dos índices definidos.
- [x] BES 2026 localizada y licencia declarada como dominio público por el distribuidor.
- [x] Importador, comprobador y generador de borradores preparados en el repositorio.
- [ ] Importación real de los 874 versículos de BES 2026 y registro SHA-256 del ZIP.
- [ ] Comprobación de integridad textual y de los 26 capítulos frente a la fuente oficial, más allá del primer versículo testigo.
- [ ] Marcado y control de todas las intervenciones humanas y divinas, diálogo y pensamiento, con revisión editorial de la redacción BES.
- [ ] Borradores de 19 escenas generados, revisados, índices y navegación probados.
- [ ] Protección verificada de 15 escenas RVR1960 y correcta identificación de la edición mixta.

**No iniciar como si P2 hubiera finalizado**, ni publicar automáticamente. P3–P9 se desarrollarán secuencialmente sobre las escenas BES, siguiendo los puntos de aprobación del protocolo.
