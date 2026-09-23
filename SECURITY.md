# 🔐 Política de seguridad

## Reportar una vulnerabilidad

**No abras un issue público ni lo comentes en Discord.** Repórtalo de forma privada:

1. En GitHub: pestaña **Security → Report a vulnerability** ([enlace directo](https://github.com/saorionline/optim-ryo-ia/security/advisories/new)).
2. Si no está disponible, escribe directamente a la administradora (@saorionline).

Incluye: qué encontraste, cómo reproducirlo y qué impacto crees que tiene. Recibirás respuesta en un máximo de 72 horas.

## Qué cuenta como vulnerabilidad

- Secretos (tokens, llaves, `.env`) subidos al repositorio o a una PR.
- Un prompt o memoria de agente que permita inyección de instrucciones desde contenido externo.
- Cualquier forma de saltarse las protecciones de `main` o los checks de CI.
- Lógica que permita modificar el libro mayor fuera del flujo de contra-asientos.

## Si subiste un secreto por error

Avisa de inmediato a la administradora: el secreto se **revoca y rota**; borrarlo en un commit nuevo no basta porque queda en el historial.
