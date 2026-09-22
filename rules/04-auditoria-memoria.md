# Regla 04 — Auditoría y memoria

## Rastro de auditoría
- Todo cambio que afecte dinero, esquema o reglas debe poder responder: **¿quién (qué agente), qué, cuándo y por qué?**
- Los mensajes de commit describen el cambio y la razón. Commits pequeños y con un solo propósito.
- Si un agente propone un asiento o una migración, el resultado del `auditor-cumplimiento` se deja en la descripción del cambio.

## Memoria persistente (estilo ECC)
- Al iniciar sesión se inyecta `memoria/estado-actual.md`. Léelo antes de empezar.
- Al terminar una tarea significativa, ejecuta la skill `cerrar-sesion`:
  - Actualiza `memoria/estado-actual.md` (qué se hizo, qué sigue, bloqueos). Máximo ~40 líneas: resume, no copies transcripciones.
  - Agrega a `memoria/decisiones.md` cualquier decisión de arquitectura nueva, con fecha absoluta (AAAA-MM-DD).
- `memoria/decisiones.md` es append-only, igual que el ledger: si una decisión cambia, agrega una entrada nueva que la reemplace.
- Nunca guardes secretos ni datos personales en `memoria/`.
