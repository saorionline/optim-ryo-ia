# Regla 03 — Modelo de datos del núcleo de divisas

Fuente: `TablasDeDesarrollo..md`. Estas 4 tablas son el núcleo; cualquier tabla nueva debe justificarse en `memoria/decisiones.md`.

| Tabla | Propósito | Invariantes clave |
|---|---|---|
| `assets` | Catálogo de monedas/activos (USD, EUR, COP, USDC…) | `symbol` único; `decimals` fijo; `status` ∈ {ACTIVE, HALTED} |
| `accounts` | Una cuenta = un dueño + una moneda | `balance >= 0`; `locked_balance >= 0`; `version` para concurrencia optimista |
| `ledger_entries` | Libro mayor de doble partida | Append-only; `SUM(amount) = 0` por `transaction_id` y moneda |
| `orders` | Órdenes BUY/SELL y su ciclo de vida | `price > 0`; `quantity > 0`; `0 <= filled_qty <= quantity`; `sequence` único y creciente |

## Reglas de negocio
1. **Una moneda por cuenta.** Una conversión USD→COP genera movimientos en al menos dos cuentas de moneda distinta y cada moneda cuadra por separado.
2. **Bloqueo antes de operar.** Al abrir una orden, el monto pasa de `balance` a `locked_balance` en la misma transacción de base de datos.
3. **Liquidación atómica.** Ejecutar una orden = actualizar `orders.filled_qty`, mover saldos y escribir los `ledger_entries` en **una sola transacción**. Si una parte falla, falla todo.
4. **Concurrencia.** Toda actualización de `accounts` usa `WHERE version = :version_leida` e incrementa `version`. Si no afecta filas, reintenta; no sobrescribas.
5. **Activo detenido.** Si `assets.status = 'HALTED'`, no se abren ni ejecutan órdenes en ese activo.
6. **Correcciones.** Un error en el ledger se corrige con un contra-asiento nuevo con `entry_type` explícito (p. ej. `REVERSAL`) que referencia la transacción original.
7. **Las restricciones viven en la base de datos**, no solo en el código: `CHECK`, `FOREIGN KEY`, `UNIQUE` y triggers de cuadre. El código del agente no es la última línea de defensa.

## Pendiente de definir con el operador
- Modo de redondeo por defecto.
- Fuente oficial de tasas de cambio.
- Tablas adicionales de la guía (`reconciliations_log`, `financial_snapshots`) y cuándo incorporarlas.
