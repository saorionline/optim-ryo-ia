# Regla 01 — Conducta y determinismo

## Qué hacer
- Trabaja solo con datos presentes en el repositorio, en la base de datos o entregados por el operador. Si algo falta (tasa, cuenta, moneda, regla de redondeo), **detente y pregunta**.
- Antes de escribir código que mueva dinero, escribe el plan: qué cuentas se afectan, montos por moneda y comprobación de que cada `transaction_id` suma cero.
- Usa siempre tipos exactos: `NUMERIC(36,18)` en SQL, `Decimal` en Python, `decimal.js`/`big.js` en JS/TS. **Prohibido `float`/`double`/`Number` para montos o tasas.**
- Redondeo explícito y documentado: a los `decimals` de la moneda destino, con el modo indicado en `memoria/decisiones.md`. Si aún no hay modo definido, pregunta.
- Las conversiones usan una tasa con **fuente, par y sello de tiempo** conocidos. Nunca una tasa "aproximada" ni recordada.
- Los procesos deben ser reproducibles: mismo input + misma secuencia ⇒ mismo resultado. No uses `NOW()` ni aleatoriedad dentro de la lógica de emparejamiento o liquidación; recibe el tiempo y la secuencia como parámetros.

## Qué no hacer
- No "arregles" un descuadre ajustando un monto a mano para que cuadre.
- No agregues dependencias, servicios externos ni APIs de tasas sin aprobación.
- No afirmes que algo funciona sin haberlo verificado (tests, consulta o ejecución). Si no se pudo verificar, dilo.

## Tests mínimos para código financiero
- Caso feliz que cuadra.
- Asiento descuadrado ⇒ debe ser rechazado.
- Saldo que quedaría negativo ⇒ debe ser rechazado.
- Redondeo en el límite de decimales de cada moneda involucrada.
