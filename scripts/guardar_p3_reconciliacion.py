#!/usr/bin/env python3
"""Regenera, valida y registra reglas + catálogo P3 en un único commit local.

Uso: editar data/p3-reconciliacion-genesis-25-50.json y ejecutar
     python3 scripts/guardar_p3_reconciliacion.py
No publica escenas ni empuja a GitHub; el commit se puede enviar con git push.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "data/p3-reconciliacion-genesis-25-50.json",
    "data/p3-catalogo-reconciliado-genesis-25-50.json",
)

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def main():
    if git("rev-parse", "--abbrev-ref", "HEAD") != "main":
        raise SystemExit("ERROR: ejecuta el procedimiento en la rama main.")
    # No mezclar otros cambios preparados con las dos fuentes de reconciliación.
    staged = set(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    if staged - set(FILES):
        raise SystemExit("ERROR: hay otros archivos preparados; revísalos antes de continuar.")
    subprocess.run([sys.executable, "scripts/build_p3_catalogo_reconciliado.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/check_p3_reconciliacion.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/build_p3_catalogo_reconciliado.py", "--check"], cwd=ROOT, check=True)
    subprocess.run(["git", "add", "--", *FILES], cwd=ROOT, check=True)
    changed = git("diff", "--cached", "--name-only")
    if not changed:
        print("Sin cambios P3; no se crea un commit.")
        return
    subprocess.run(["git", "commit", "-m", "P3: actualizar reglas y catálogo de reconciliación en un solo commit"], cwd=ROOT, check=True)
    print("Commit P3 preparado. Revisa antes de ejecutar git push.")

if __name__ == "__main__":
    main()
