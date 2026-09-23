# 📘 Cómo contribuir

Resumen operativo de la *Guía de Organización: Equipo Remoto con Desarrollo Descentralizado y Agentes de IA*. Estas reglas están **codificadas**: si no se cumplen, Git, la CI o GitHub rechazan el cambio.

## Configuración inicial (una vez por clon)

```bash
git clone git@github.com:saorionline/optim-ryo-ia.git
cd optim-ryo-ia
git config core.hooksPath .githooks
```

El último comando activa los hooks locales que impiden hacer commit o push a `main`.

## Flujo: Planificar → Verificar → Corregir

### 1. Planificar
1. Toda tarea nace como **Issue** (plantilla *Tarea*).
2. Actualiza tu copia y crea una rama:

```bash
git checkout main
git pull origin main
git checkout -b feature/<nombre>-<tarea>
```

**Convención de ramas:** `<tipo>/<nombre>-<tarea>` en minúsculas con guiones.
Tipos: `feature`, `fix`, `docs`, `chore`, `refactor`, `test`. Ej.: `feature/ana-memoria-inicial`, `fix/bruno-parser-json`.

### 2. Ejecutar y verificar
- Edita **solo** tu carpeta `agents/agent-<nombre>/` (ver [agents/README.md](agents/README.md)).
- Valida antes de subir: `python scripts/validar_agentes.py estructura`
- Sube tu rama: `git push origin feature/<nombre>-<tarea>`

La CI (`.github/workflows/gobernanza.yml`) ejecuta:

| Check | Qué verifica |
|---|---|
| `validar-agentes` | Estructura de `agents/`, `config.yaml` (modelo, `seed`, `temperature`, `prompt_version`), JSON de memoria y lockfiles de dependencias |
| `nombre-rama` | Convención de nombre de la rama |
| `aislamiento-pr` | Que la PR solo toque la carpeta del agente asignado a su autor/a en `agents/owners.json` |

### 3. Corregir y consolidar
1. Abre una PR hacia `main` y completa la plantilla.
2. La administradora revisa (CODEOWNERS). Se requiere 1 aprobación y todos los checks en verde.
3. Si hay correcciones: commit en la **misma rama** y `git push`; la PR se actualiza sola.
4. Se fusiona con **Squash and merge**; la rama se borra automáticamente.

## Commits

Mensajes cortos en imperativo describiendo el *qué*: `Agrega memoria inicial del agente ana`. Como se usa *squash*, el título de la PR es el que queda en `main`.

## Lo que está bloqueado

| Acción | Dónde se bloquea |
|---|---|
| Commit en `main` / rama mal nombrada | Hook `pre-commit` |
| Push a `main` | Hook `pre-push` y ruleset de GitHub |
| Force push, borrar `main`, historial no lineal | Ruleset de GitHub |
| Merge sin PR, sin aprobación o con checks en rojo | Ruleset de GitHub |
| Tocar carpetas ajenas o archivos de gobernanza | Check `aislamiento-pr` + CODEOWNERS |
| Dependencias sin lockfile | Check `validar-agentes` |

**Excepción documentada:** la administradora puede fusionar sus **propias** PRs sin segunda aprobación (bypass del ruleset en modo *pull request*). Nunca puede hacer push directo a `main`.

## Dependencias

Si agregas un `package.json`, `pyproject.toml`, `Pipfile` o `Gemfile`, sube también su archivo de bloqueo. Instala siempre desde el lock (`npm ci`, `poetry install --sync`, `bundle install --frozen`).
