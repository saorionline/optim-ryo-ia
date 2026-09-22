# Registro de decisiones (append-only)

> No edites entradas anteriores. Si una decisión cambia, agrega una nueva que indique a cuál reemplaza.

## 2026-09-22 — Arnés base inspirado en ECC
- Decisión: el agente de Claude trabaja con reglas siempre cargadas (`rules/`), agentes con herramientas mínimas (`.claude/agents/`), skills de dominio, hook gateguard y memoria en `memoria/`.
- Motivo: `GuiaOptimizacion..md` y el repositorio https://github.com/affaan-m/ecc.

## 2026-09-22 — Núcleo de 4 tablas
- Decisión: assets, accounts, ledger_entries (doble partida, append-only) y orders, según `TablasDeDesarrollo..md`.
- Motivo: determinismo, aislamiento por cuenta/moneda y auditoría inmutable.

## 2026-09-22 — Aritmética exacta
- Decisión: montos y tasas en `NUMERIC(36,18)` / `Decimal`; prohibido `float`.
- Motivo: evitar errores de redondeo en operaciones de alta materialidad.
