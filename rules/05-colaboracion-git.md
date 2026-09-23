# Regla 05 — Colaboración en el repositorio

Fuente: *guia-equipo-remoto-agentes-ia* y `CONTRIBUTING.md`.

## Qué hacer
- Trabaja siempre en una rama `<tipo>/<nombre>-<tarea>` creada desde `main` actualizado. Si estás en `main`, crea la rama antes de editar.
- En ramas de colaboradores, modifica solo `agents/agent-<nombre>/` del autor según `agents/owners.json`.
- Si cambias `system_prompt.md` o `config.yaml` de un agente, sube `prompt_version`. Mantén `seed` fija.
- Ejecuta `python scripts/validar_agentes.py estructura` antes de dar un cambio por terminado.
- Todo cambio llega a `main` por Pull Request con *Squash and merge*.

## Qué no hacer
- No hagas commit ni push a `main`; no uses `--force`, `--no-verify` ni reescribas historial publicado.
- No modifiques `.github/`, `.claude/`, `rules/`, `agents/owners.json` ni carpetas de otros agentes salvo que la administradora lo pida explícitamente.
- No agregues dependencias sin su archivo de bloqueo.
