# Estado actual — actualizado 2026-09-22

## Hecho recientemente
- Creado el arnés base del agente: `CLAUDE.md`, `rules/` (4 reglas), `.claude/agents/` (5 agentes), `.claude/skills/` (partida-doble, cerrar-sesion), hooks gateguard y session-start, y esta memoria.
- Modelo de datos núcleo definido en `H:\WarriorRain\Optimizacion-IA-Ryo\TablasDeDesarrollo..md`: assets, accounts, ledger_entries, orders.

## En curso
- Nada todavía: aún no hay código ni esquema SQL.

## Siguiente paso
- Definir con el operador las preguntas pendientes de abajo.
- Crear la primera migración SQL de las 4 tablas con sus CHECK, FOREIGN KEY y un trigger que impida UPDATE/DELETE en ledger_entries y valide el cuadre por transaction_id.

## Bloqueos / preguntas para el operador
- ¿Qué monedas se van a soportar al inicio (USD, EUR, COP, USDC…)?
- ¿Modo de redondeo por defecto (HALF_EVEN / HALF_UP)?
- ¿Fuente oficial de tasas de cambio?
- ¿Lenguaje/stack de la aplicación (Python, TypeScript…)?
