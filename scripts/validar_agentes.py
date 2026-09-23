#!/usr/bin/env python3
"""Validaciones de gobernanza del repositorio (guia-equipo-remoto-agentes-ia).

Solo usa la libreria estandar para que el entorno sea identico en cada maquina
y en CI (no hay dependencias que bloquear).

Uso:
  python scripts/validar_agentes.py estructura
  python scripts/validar_agentes.py rama <nombre-de-rama>
  python scripts/validar_agentes.py aislamiento <autor-github> <base-ref>

Codigo de salida 0 = OK, 1 = hay errores.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AGENTES = RAIZ / "agents"
OWNERS = AGENTES / "owners.json"

PATRON_CARPETA = re.compile(r"^agent-[a-z0-9]+(-[a-z0-9]+)*$")
PATRON_RAMA = re.compile(r"^(feature|fix|docs|chore|refactor|test)/[a-z0-9]+(-[a-z0-9]+)+$")
PATRON_SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

ARCHIVOS_OBLIGATORIOS = {"system_prompt.md", "memory_store.json", "config.yaml"}
ARCHIVOS_OPCIONALES = {"README.md"}

# Claves de config.yaml: nombre -> (tipo, validador, descripcion)
CONFIG_SCHEMA = {
    "model": (str, lambda v: bool(v.strip()), "texto no vacio"),
    "prompt_version": (str, lambda v: bool(PATRON_SEMVER.match(v)), "version semantica X.Y.Z"),
    "temperature": ((int, float), lambda v: 0 <= v <= 1, "numero entre 0 y 1"),
    "seed": (int, lambda v: v >= 0, "entero >= 0 (semilla fija)"),
    "max_tokens": (int, lambda v: v > 0, "entero > 0"),
}

# Manifiestos de dependencias y sus archivos de bloqueo aceptados.
LOCKFILES = {
    "package.json": ("package-lock.json", "pnpm-lock.yaml", "yarn.lock"),
    "pyproject.toml": ("poetry.lock", "uv.lock"),
    "Pipfile": ("Pipfile.lock",),
    "Gemfile": ("Gemfile.lock",),
}


def parse_yaml_plano(texto):
    """Parser minimo para YAML plano 'clave: valor' (sin anidacion ni listas)."""
    datos = {}
    for n, linea in enumerate(texto.splitlines(), 1):
        limpia = linea.split(" #", 1)[0].rstrip() if not linea.lstrip().startswith("#") else ""
        if not limpia.strip():
            continue
        if linea[:1] in (" ", "\t"):
            raise ValueError(f"linea {n}: solo se admite YAML plano (sin anidacion)")
        if ":" not in limpia:
            raise ValueError(f"linea {n}: se esperaba 'clave: valor'")
        clave, valor = (p.strip() for p in limpia.split(":", 1))
        if clave in datos:
            raise ValueError(f"linea {n}: clave duplicada '{clave}'")
        datos[clave] = convertir_escalar(valor)
    return datos


def convertir_escalar(v):
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def cargar_owners():
    if not OWNERS.exists():
        return None, [f"falta {OWNERS.relative_to(RAIZ)}"]
    try:
        owners = json.loads(OWNERS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return None, [f"agents/owners.json no es JSON valido: {e}"]
    errores = []
    if not isinstance(owners.get("admins"), list) or not owners["admins"]:
        errores.append("agents/owners.json: 'admins' debe ser una lista no vacia")
    if not isinstance(owners.get("agents"), dict):
        errores.append("agents/owners.json: 'agents' debe ser un objeto {carpeta: usuario-github}")
    return owners, errores


def validar_carpeta(carpeta):
    errores = []
    nombre = carpeta.name
    archivos = {p.name for p in carpeta.iterdir() if p.is_file()}
    subdirs = [p.name for p in carpeta.iterdir() if p.is_dir()]

    for falta in sorted(ARCHIVOS_OBLIGATORIOS - archivos):
        errores.append(f"{nombre}: falta {falta}")
    for extra in sorted(archivos - ARCHIVOS_OBLIGATORIOS - ARCHIVOS_OPCIONALES):
        errores.append(f"{nombre}: archivo no permitido '{extra}'")
    for d in subdirs:
        errores.append(f"{nombre}: subcarpeta no permitida '{d}'")

    prompt = carpeta / "system_prompt.md"
    if prompt.exists() and not prompt.read_text(encoding="utf-8").strip():
        errores.append(f"{nombre}: system_prompt.md esta vacio")

    memoria = carpeta / "memory_store.json"
    if memoria.exists():
        try:
            if not isinstance(json.loads(memoria.read_text(encoding="utf-8")), dict):
                errores.append(f"{nombre}: memory_store.json debe ser un objeto JSON")
        except json.JSONDecodeError as e:
            errores.append(f"{nombre}: memory_store.json no es JSON valido: {e}")

    config = carpeta / "config.yaml"
    if config.exists():
        try:
            datos = parse_yaml_plano(config.read_text(encoding="utf-8"))
        except ValueError as e:
            errores.append(f"{nombre}: config.yaml {e}")
        else:
            for clave, (tipo, ok, desc) in CONFIG_SCHEMA.items():
                if clave not in datos:
                    errores.append(f"{nombre}: config.yaml falta '{clave}' ({desc})")
                elif isinstance(datos[clave], bool) or not isinstance(datos[clave], tipo) or not ok(datos[clave]):
                    errores.append(f"{nombre}: config.yaml '{clave}' invalido, se esperaba {desc}")
            for clave in sorted(set(datos) - set(CONFIG_SCHEMA)):
                errores.append(f"{nombre}: config.yaml clave desconocida '{clave}'")
    return errores


def cmd_estructura():
    errores = []
    if not AGENTES.is_dir():
        return ["falta la carpeta agents/"]

    owners, e = cargar_owners()
    errores += e
    registrados = set((owners or {}).get("agents", {}) or {})

    carpetas = []
    for p in sorted(AGENTES.iterdir()):
        if p.is_file():
            if p.name not in ("owners.json", "README.md"):
                errores.append(f"agents/: archivo no permitido en la raiz '{p.name}'")
            continue
        if p.name == "_template":
            errores += validar_carpeta(p)
            continue
        if not PATRON_CARPETA.match(p.name):
            errores.append(f"agents/{p.name}: el nombre debe seguir 'agent-<nombre>' en minusculas")
            continue
        carpetas.append(p.name)
        errores += validar_carpeta(p)

    for c in carpetas:
        if owners is not None and c not in registrados:
            errores.append(f"agents/{c}: no esta registrada en agents/owners.json")
    for c in sorted(registrados - set(carpetas)):
        errores.append(f"agents/owners.json: '{c}' no tiene carpeta en agents/")

    # Dependencias bloqueadas: todo manifiesto requiere su lockfile al lado.
    for manifiesto, locks in LOCKFILES.items():
        for m in RAIZ.rglob(manifiesto):
            if any(x in m.parts for x in (".git", "node_modules", ".venv")):
                continue
            if not any((m.parent / l).exists() for l in locks):
                errores.append(f"{m.relative_to(RAIZ)}: falta archivo de bloqueo ({' o '.join(locks)})")
    return errores


def cmd_rama(rama):
    if rama in ("main", "master"):
        return [f"no se trabaja directo en '{rama}'; crea una rama feature/<nombre>-<tarea>"]
    if not PATRON_RAMA.match(rama):
        return [
            f"rama '{rama}' no cumple la convencion <tipo>/<nombre>-<tarea> "
            "(tipo: feature|fix|docs|chore|refactor|test; minusculas y guiones). "
            "Ej: feature/ana-memoria-inicial"
        ]
    return []


def cmd_aislamiento(autor, base):
    owners, errores = cargar_owners()
    if errores:
        return errores
    if autor in owners["admins"]:
        print(f"'{autor}' es administradora: sin restriccion de carpeta.")
        return []

    cambiados = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=RAIZ, capture_output=True, text=True, check=True,
    ).stdout.split()
    propias = [c for c, u in owners["agents"].items() if str(u).lower() == autor.lower()]
    if not propias:
        return [f"'{autor}' no tiene carpeta asignada en agents/owners.json; pide a la administradora que la registre"]

    permitidos = tuple(f"agents/{c}/" for c in propias)
    fuera = [f for f in cambiados if not f.startswith(permitidos)]
    return [f"'{autor}' solo puede modificar {', '.join(permitidos)}; archivo fuera de su carpeta: {f}" for f in fuera]


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    cmd, args = argv[0], argv[1:]
    if cmd == "estructura" and not args:
        errores = cmd_estructura()
    elif cmd == "rama" and len(args) == 1:
        errores = cmd_rama(args[0])
    elif cmd == "aislamiento" and len(args) == 2:
        errores = cmd_aislamiento(*args)
    else:
        print(__doc__)
        return 1

    for e in errores:
        print(f"ERROR: {e}")
    if not errores:
        print(f"OK: {cmd}")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
