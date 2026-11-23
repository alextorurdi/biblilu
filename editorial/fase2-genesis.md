# Fase 2 · Génesis 25–50 — Texto, marcado e índices

**Fecha de inicio:** 23/11/2026.  
**Estado:** **EN CURSO — ESTRUCTURA PREPARADA, TRANSCRIPCIÓN PENDIENTE.**  
**No publicado:** todas las páginas y datos públicos siguen limitados a Génesis 1–24.

Documentos rectores: [Protocolo P0–P9](protocolo-libros.md) · [Escenificación aprobada P1](fase1-genesis.md) · [Plan de distribución de recursos](plan-ubicacion-escenas-genesis-25-50.md).

## Trabajo ejecutado en GitHub

1. **Escenificación y rutas.** Se han fijado técnicamente las 19 rutas de lectura y sus anclas de versículo, comprobando la secuencia completa de **874 versículos** en los **26 capítulos** de Gn 25–50, sin cortes dobles ni vacíos. El total previsto de Génesis es de 34 escenas y 1.533 versículos. Archivo: [p2-rutas-genesis-25-50.json](p2-rutas-genesis-25-50.json).
2. **Generador de trabajo.** [prepare_genesis_p2.py](../scripts/prepare_genesis_p2.py) valida el catálogo, controla las 874 referencias de la fuente y puede generar, **solo cuando el texto autorizado esté disponible**, 19 páginas de **previsualización no pública** con referencias canónicas y navegación.
3. **Dos índices.** El generador prepara las entradas para el índice por escenas y el tradicional por capítulos 25–50, tomando como base el índice editorial protegido de Génesis 1–24; **no reescribe el índice público ni los 15 relatos aprobados**. Los capítulos divididos entre varias escenas tendrán aviso de continuidad.
4. **Integridad de los versículos.** La fuente requiere un registro por versículo, con `chapter`, `verse`, `text` y opcionalmente `source_label`. Pueden añadirse `parts` para marcar discurso humano, pensamiento o palabras divinas; el validador comprueba que la concatenación de los segmentos sea **idéntica al texto literal**. No se añaden frases, se altera la ortografía ni se infieren intervenciones divinas automáticamente.
5. **Prueba reproducible sin texto bíblico.** [test_genesis_p2.py](../scripts/test_genesis_p2.py) comprueba la estructura, la creación de borradores, 874 anclas, índice por escenas y tradicional y rechazo de marcas que cambian el texto usando 874 **cadenas sintéticas**. El test se ha incorporado al repositorio para su ejecución; **no se afirma su ejecución satisfactoria en el entorno GitHub**.
6. **Esquema de importación:** [esquema-fuente-genesis-25-50.json](esquema-fuente-genesis-25-50.json), para no depender de una transcripción manual en la interfaz de GitHub.

## Fuente textual pendiente y derechos

- **Fuente actual real:** `data/genesis.json` contiene solamente los **659 versículos de Gn 1–24**. No hay en el repositorio una fuente íntegra aprobada para Gn 25–50; no introducir 874 versículos inventados ni copiar una edición diferente.
- **RVR1960 está sujeta a derechos.** La información de derechos de American Bible Society y de Sociedades Bíblicas Unidas indica condiciones para citas limitadas y necesidad de tramitar el uso excedente. Referencias: https://www.americanbible.org/rights-and-permissions/ y https://www.ubscopyrights.org/index.php/pages/view/rules. El texto completo propuesto para esta fase supera las condiciones generales de citas sin autorización. Registrar la fuente y verificar la autorización de reproducción antes de publicarlo.
- El archivo **`data/genesis_25_50.json` todavía NO existe**. Se creará únicamente con texto que proporcione el editor desde una fuente adecuada y con situación de derechos verificada.
- Una fuente aportada en DOCX, TXT o similar puede convertirse en el JSON requerido, preservando literalmente el texto y las 874 anclas, siempre que se establezca la procedencia y se revise cualquier diferencia con los capítulos publicados.

## Formato previsto

El generador de **borradores** admite registros como este ejemplo **ficticio, no bíblico**:

```json
{
  "chapter": 25,
  "verse": 1,
  "source_label": "25-1",
  "text": "TEXTO AUTORIZADO DE EJEMPLO",
  "parts": [
    {"kind": "plain", "text": "TEXTO AUTORIZADO DE EJEMPLO"}
  ],
  "revisado": false
}
```

Los segmentos `plain`, `speech`, `divine` y `thought` permiten preservar exactamente la cadena `text`. La marcación final requiere revisión editorial verso a verso; la propiedad `revisado` es solo un seguimiento editorial, **no** una autorización legal de reproducción.

### Instrucciones reproducibles

```bash
python scripts/prepare_genesis_p2.py --structure
python scripts/test_genesis_p2.py
# Cuando se haya incorporado data/genesis_25_50.json desde fuente autorizada:
python scripts/prepare_genesis_p2.py --check-source
python scripts/prepare_genesis_p2.py --build-draft
```

El resultado opcional se construye únicamente en **`build/p2/`**, fuera de la web pública. Las futuras páginas integradas en `docs/` y las fuentes protegidas en `editorial/approved-pages/` se establecerán después de validar fuente y marcado, y siguiendo las fases de aprobación, control y publicación.

## Pendientes reales para cerrar P2

- [x] 19 escenas aprobadas y anclas canónicas previstas.
- [x] Rutas P2 y plan de los dos índices.
- [x] Validador de cobertura y preservación literal preparado.
- [x] Generación de borradores no públicos preparada.
- [ ] Proporcionar / localizar la transcripción **RVR1960 autorizada** de Gn 25:1–50:26.
- [ ] Incorporar y comprobar los 874 textos literales, sin omisiones, duplicados ni modificaciones.
- [ ] Marcar intervenciones de Dios en rojo, intervenciones humanas y pensamientos conforme al estilo aprobado (revisión editorial).
- [ ] Generar borradores y revisar los 19 relatos, índices y navegación.
- [ ] Confirmar las condiciones de reproducción para la versión completa antes de hacerla pública.

**Estado de entrega:** estructura técnica P2 adelantada, NO P2 completada y NO publicación. No iniciar fases posteriores como si el nuevo texto ya estuviera integrado.
