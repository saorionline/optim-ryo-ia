# `agents/` — Agentes aislados por colaborador

Cada colaborador tiene **una sola carpeta** `agents/agent-<nombre>/` y trabaja **exclusivamente** dentro de ella. La CI rechaza cualquier Pull Request de une colaborador que toque archivos fuera de su carpeta.

> No confundir con `.claude/agents/`, que son los subagentes del arnés de Claude del proyecto y solo los modifica la administradora.

## Estructura obligatoria

```text
agents/agent-<nombre>/
  ├── system_prompt.md    # Reglas del agente (no vacío)
  ├── memory_store.json   # Memoria local (objeto JSON válido)
  ├── config.yaml         # model, prompt_version, temperature, seed, max_tokens
  └── README.md           # Opcional
```

No se permiten otros archivos ni subcarpetas.

## Alta de une colaborador (solo administradora)

1. Copiar `agents/_template/` a `agents/agent-<nombre>/`.
2. Registrar la carpeta en `agents/owners.json`: `"agent-<nombre>": "<usuario-github>"`.
3. Añadir la línea correspondiente en `.github/CODEOWNERS`.
4. Abrir PR, pasar CI y hacer *Squash and merge*.

## Determinismo

- `seed` fija y `temperature` entre 0 y 1 (recomendado `0`).
- Cualquier cambio en `system_prompt.md` o `config.yaml` sube `prompt_version` (X.Y.Z).

Validar localmente antes de subir:

```bash
python scripts/validar_agentes.py estructura
```
