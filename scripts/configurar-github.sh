#!/usr/bin/env bash
# Aplica en GitHub la gobernanza de la guia-equipo-remoto-agentes-ia.
# Requiere GitHub CLI autenticado como administradora: gh auth login
# Idempotente: se puede volver a ejecutar para re-sincronizar.
set -euo pipefail

REPO="${1:-saorionline/optim-ryo-ia}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
RULESET="$RAIZ/.github/rulesets/proteccion-main.json"

echo "==> Ajustes del repositorio $REPO (solo Squash and merge, borrar rama al fusionar)"
gh api -X PATCH "repos/$REPO" \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=false \
  -F delete_branch_on_merge=true \
  -F allow_auto_merge=false \
  -f squash_merge_commit_title=PR_TITLE \
  -f squash_merge_commit_message=PR_BODY >/dev/null

echo "==> Ruleset 'proteccion-main'"
ID="$(gh api "repos/$REPO/rulesets" --jq '.[] | select(.name=="proteccion-main") | .id')"
if [ -n "$ID" ]; then
  gh api -X PUT "repos/$REPO/rulesets/$ID" --input "$RULESET" >/dev/null
  echo "    actualizado (id $ID)"
else
  gh api -X POST "repos/$REPO/rulesets" --input "$RULESET" >/dev/null
  echo "    creado"
fi

echo "==> Reporte privado de vulnerabilidades"
gh api -X PUT "repos/$REPO/private-vulnerability-reporting" >/dev/null || \
  echo "    (no disponible para este repo; activarlo en Settings > Code security)"

echo "Listo. Revisa: https://github.com/$REPO/settings/rules"
