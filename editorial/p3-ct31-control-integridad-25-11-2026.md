# P3 · CT-31 — Control de integridad tras D-04 (25/11/2026)

**Alcance:** Génesis 25–50, BES 2026. Se han revisado directamente los archivos `data/genesis_25_50_bes.json`, `data/p3-extracciones-genesis-25-50.json`, `data/p3-reconciliacion-genesis-25-50.json` y `data/registro_maestro.json`. El catálogo derivado se ha **regenerado desde esas fuentes** con la estructura de `scripts/build_p3_catalogo_reconciliado.py`.

## Resultados directos

| Comprobación | Resultado |
|---|---:|
| Versículos BES | 874 |
| Registros de extracción bruta | 1.711 |
| Posiciones brutas únicas | 1.656 |
| Desajustes texto/posición en inventario bruto | 0 |
| Cruces Onomástico/Lugares | 55 |
| Cruces sin soporte literal en inventario bruto | 0 |
| Reglas contextuales CT/R-01 | 1.918 |
| Errores de posición/literal en reglas | 0 |
| Reglas duplicadas sobre igual posición | 0 |
| IDs de categoría incompatible | 0 |
| Exclusiones con ID inapropiado | 0 |
| Asignaciones sin ID | 0 |
| Identificadores repetidos en registro maestro (451 entidades) | 0 |
| Registros resultantes del catálogo derivado | 1.973 |
| Registros del catálogo con regla contextual | 1.973 |
| Candidatos únicos sin validar en catálogo regenerado | 0 |

**Estados del catálogo derivado regenerado:** clasificado por contexto 1.803; asociación contextual aprobada 50; excluido aprobado 44; clasificado sin ID 73; nota contextual aprobada 1; exclusión personal 1; homónimo no identificado 1. El catálogo contiene referencias a **95 identificadores futuros distintos** en las reglas; no deben confundirse con fichas implementadas.

## D-04 y CT-30

La decisión editorial **D-04, opción A, está aprobada**: crear en P4 la ficha independiente `Débora (nodriza de Rebeca)` por Gn 35:8. El identificador **reservado, no enlazable hasta P4**, es `onomastico/debora-nodriza-rebeca`. La regla CT-30 conserva `clasificar_sin_id` e `id: null` en la extracción P3 para no fingir la existencia material de la ficha. El control automático comprueba tanto la aprobación como la ausencia provisional del enlace. Referencias cruzadas previstas: Rebeca (`onomastico/rebeca`, ficha existente) y Alón-bacut (`lugares/alon-bacut`, alta futura). Se distingue de Débora profetisa/jueza de Jueces 4–5.

## Límites de la certificación

Esta ejecución constituye una **verificación directa de coherencia formal y de reglas**, no una comprobación de que todas las palabras potencialmente pertinentes del texto han sido detectadas ni una ejecución demostrada de GitHub Actions. No se ha recibido confirmación de estado de CI asociada al último commit. La comparación byte por byte del archivo regenerado con la serialización producida por Python (`--check`) requiere la ejecución del workflow en GitHub o un entorno local con el repositorio completo. El conteo de cero candidatos no prueba por sí solo cobertura semántica perfecta.

**Pendientes antes del cierre P3:** confirmar el workflow `control-p3-reconciliacion.yml`, ejecutar `python3 scripts/check_p3_reconciliacion.py` y `python3 scripts/build_p3_catalogo_reconciliado.py --check` en CI, y documentar el alcance de la auditoría de omisiones y excepciones léxicas. No se crea ninguna ficha ni se publica la web durante esta fase.
