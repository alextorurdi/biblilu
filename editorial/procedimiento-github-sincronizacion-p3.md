# Procedimiento de publicación segura y reconciliación P3

**Fecha:** 25/11/2026. **Aprobación:** cuatro medidas para reducir errores recurrentes de GitHub.

## Causas comprobadas

1. El control de reconciliación fallaba entre commits consecutivos de las reglas y el catálogo con `AssertionError: Catalogo no reproducible`. Los últimos controles comprobados finalizaron correctamente.
2. GitHub Pages ejecuta su proceso administrado de publicación para los cambios en `main`; al recibir numerosos commits consecutivos, algunos despliegues aparecen cancelados aunque otro posterior finalice con éxito.
3. El workflow «Publicar apéndices de BIBLILU» sufrió una carrera de escritura el 23/11: `git push` fue rechazado con `main -> main (fetch first)`.

## Medidas implementadas

- `scripts/guardar_p3_reconciliacion.py` genera y valida el catálogo, prepara exclusivamente reglas + catálogo y los integra en **un solo commit local**; el `push` posterior es una decisión separada. Las actualizaciones vía GitHub API también deben hacerse en un solo commit de árbol, no con dos llamadas secuenciales a `update_file`.
- `control-p3-reconciliacion.yml` usa `actions/checkout@v7`, preserva validación de reglas y catálogo y cancela validaciones P3 obsoletas si otro commit nuevo llega a la misma rama.
- `publicar-seres-vivos.yml` ya no cancela una publicación anterior al entrar otro cambio; antes de cada intento de `push` recupera y rebasa `main`, con hasta cinco reintentos sin `--force`. Un conflicto real de rebase continúa deteniendo la ejecución para revisión manual.
- No se han cambiado reglas del texto BES, fichas ni el contenido publicado.

## Límite de GitHub Pages

El workflow «pages build and deployment» es un proceso administrado por GitHub, no una tarea declarada en `.github/workflows`. **No es posible filtrar por rutas sus ejecuciones con este cambio de código**. Para que cambios exclusivamente editoriales de `main` no lo inicien, hay que modificar la fuente de publicación de GitHub Pages a **GitHub Actions** (en *Settings → Pages*) y configurar entonces un workflow explícito que se active solo con cambios de `docs/**` o por orden manual. Ese cambio **no se ha realizado**: requiere verificar antes la configuración de Pages y evitar interrumpir la web activa. Hasta entonces, agrupar commits reducirá la frecuencia de cancelaciones, pero no la eliminará completamente.

## Validación

Confirmar las próximas ejecuciones del control P3 y la publicación de apéndices en GitHub Actions. No confundir los workflows correctos con despliegues dinámicos de Pages cancelados a causa de sucesivas publicaciones.
