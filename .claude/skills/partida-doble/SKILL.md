---
name: partida-doble
description: Checklist obligatorio para crear, modificar o revisar cualquier movimiento de dinero (asientos, conversiones de divisas, liquidación de órdenes, comisiones, reversos). Úsalo antes de escribir código o SQL que afecte ledger_entries, accounts u orders.
---

# Partida doble — flujo de trabajo

## 1. Describe la operación
- Tipo (`TRADE_SETTLEMENT`, `FX_CONVERSION`, `FEE_ACCRUAL`, `DEPOSIT`, `WITHDRAWAL`, `REVERSAL`…).
- Cuentas afectadas, cada una con su moneda.
- Tasa usada (par, valor, fuente, fecha/hora) si hay conversión.

## 2. Arma la tabla del asiento
| transaction_id | account_id | moneda | amount | entry_type |
|---|---|---|---|---|
| T1 | cuenta USD del cliente | USD | −1000.00 | FX_CONVERSION |
| T1 | cuenta USD de la tesorería | USD | +1000.00 | FX_CONVERSION |
| T1 | cuenta COP de la tesorería | COP | −4,000,000.00 | FX_CONVERSION |
| T1 | cuenta COP del cliente | COP | +4,000,000.00 | FX_CONVERSION |

*(Ejemplo ilustrativo: la tasa real siempre sale de la fuente definida.)*

## 3. Verifica antes de escribir código
- [ ] Suma por moneda dentro del `transaction_id` = **0 exacto**.
- [ ] Ningún `balance` ni `locked_balance` queda negativo.
- [ ] Montos redondeados a los `decimals` de su moneda, con el modo de redondeo acordado.
- [ ] Ningún activo involucrado está `HALTED`.
- [ ] Si viene de una orden: `filled_qty` nuevo ≤ `quantity`, y el saldo bloqueado se libera o consume correctamente.

## 4. Implementa
- Todo en **una sola transacción** de base de datos.
- `UPDATE accounts ... WHERE account_id = :id AND version = :v` e incrementa `version`; si afecta 0 filas, aborta y reintenta.
- Solo `INSERT` en `ledger_entries`.

## 5. Prueba
- Caso que cuadra ⇒ se acepta.
- Caso descuadrado ⇒ la base de datos lo rechaza.
- Saldo negativo ⇒ se rechaza.
- Redondeo en el límite de decimales.

## 6. Revisión
Pide a `auditor-cumplimiento` que revise el cambio antes de darlo por terminado.
