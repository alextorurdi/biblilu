# Materiales P3 · Acuerdos editoriales definitivos (Génesis 25–50)

**Fecha de aprobación:** 24/11/2026. **Estado:** revisión editorial P3 de Materiales **APROBADA y cerrada**. **Decisiones editoriales pendientes: 0.** La redacción definitiva, creación de fichas, enlaces y publicación siguen reservadas para P4 y fases posteriores.

**Fuentes de la decisión:** Excel del editor `BIBLILU_Genesis_P3_Materiales_25-50_Revision(3).xlsx`, columna «Acción editorial» (MAT-01–MAT-30), y **aprobación final posterior expresa** que confirmó «todas las decisiones» e incluyó **Madera (incluyendo leña)** y **Sangre**. La aprobación final prevalece sobre las propuestas originales de la columna «Propuesta editorial» y sobre el estado sin actualizar del propio Excel.

## Inventario aprobado antes de las altas Agua y Rocío

**12 fichas existentes:** Arena, Asfalto, Bedelio, Brea, Bronce, Gofer, Hierro, Ladrillo, Ónice, Oro, Piedra y Plata.

**13 fichas nuevas aprobadas para P4:**

1. Piel animal — `materiales/piel-animal`
2. Aceite — `materiales/aceite`
3. Lino — `materiales/lino`
4. Bálsamo — `materiales/balsamo`
5. Perfume — `materiales/perfume`
6. Polvo — `materiales/polvo`
7. Vino — `materiales/vino`
8. Leche — `materiales/leche`
9. Miel — `materiales/miel`
10. Sal — `materiales/sal`
11. Mirra — `materiales/mirra`
12. **Madera (incluyendo leña)** — `materiales/madera`
13. **Sangre** — `materiales/sangre`

**Balance del acuerdo inicial:** 12 existentes + 13 nuevas = **25 fichas previstas**. `materiales/madera` y `materiales/sangre` son **altas aprobadas aunque todavía no existan en `data/entries.json`**. La ausencia de un ID implementado NO anula una aprobación editorial.

## Decisiones posteriores de revisión exhaustiva

- **Agua** — `materiales/agua` — aprobada como **ficha independiente**; borrador [Agua](borradores/materiales-agua.md).
- **Rocío** — `materiales/rocio` — aprobada como **ficha independiente**; borrador [Rocío](borradores/materiales-rocio.md).
- **Corteza** de Gn 30:37 — descartada como nueva ficha de Materiales.
- **Ofrenda líquida** de Gn 35:14 — descartada como nueva ficha porque la composición no es identificable; la mención independiente del aceite del versículo permanece registrada.

**Balance vigente después de estos acuerdos:** **12 fichas existentes + 15 nuevas aprobadas = 27 fichas previstas** en Materiales. Son 27 fichas **planificadas**, no 27 fichas implementadas en la web.

## Traslados y exclusiones

- **Cilicio** (vinculado al «vestirse de tela áspera» de Gn 37:34) — **trasladado a Objetos**. La explicación y el enlace a su futura ficha se reservarán para una nota editorial; **no** se suma a Materiales.
- **Hilo**, **Especias aromáticas** y **Tierra (suelo)** — descartados como fichas nuevas de Materiales.
- **Corteza** y **Ofrenda líquida** — descartadas en la revisión posterior, como se indica arriba.
- Los productos y figuras poéticas admitidos como fichas (p. ej. Vino, Leche, Sangre) deben distinguir los usos literales de los figurados. La inclusión de Sangre en el apéndice fue **aprobada posteriormente**, y por ello **revoca la exclusión inicial propuesta en MAT-24**.
- **Madera:** incluye el término **leña** como materia leñosa; en Gn 30:37–42 la BES menciona ramas, no «madera», por lo que no debe inventarse una aparición literal del término.

## Reglas expresas de enlazado y regresión

| Pasaje | Regla aprobada |
|---|---|
| **Gn 14:3** | «Mar Salado» → **solo** `lugares/mar-salado` |
| **Gn 19:26** | «sal» → `materiales/sal` |
| **Gn 31:13** | «sal» es imperativo del verbo salir → **no enlazar** |
| **Gn 27:35; 31:24** | «vino» es forma verbal de *venir* → **no enlazar a Materiales** |

Se conserva la **revisión retrospectiva de Génesis 1–24** para incorporar enlaces a las fichas nuevas de Materiales, siempre respetando el texto RVR1960.

[**Revisión retrospectiva de Agua y Rocío (Génesis 1–24)**](p3-materiales-agua-rocio-enlaces-genesis-1-24.md): 52 apariciones literales de «agua/aguas» en 42 versículos, 0 de «rocío». Enlaces candidatos inventariados para P4; no aplicados todavía.

## Estado de implementación

El Excel original conserva columnas `Estado` que dicen «Pendiente de aprobación» aunque sus acciones editoriales y aprobación final ya las superaron. **No reabrir esas decisiones.** La aprobación es documental; **las fichas nuevas todavía no están implementadas en `data/entries.json` ni publicadas**, salvo las 12 entradas antiguas ya existentes.

La versión inicial de este registro contenía una afirmación errónea sobre Madera y Sangre y describía la fase como «parcial». **Queda sustituida explícitamente por esta versión** tras recuperar el acuerdo editorial completo. Los borradores de Agua y Rocío se conservan para su integración en P4.
