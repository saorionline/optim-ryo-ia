# SessionStart - inyecta la memoria del proyecto en el contexto de Claude.
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$estado = Join-Path $root 'memoria\estado-actual.md'

Write-Output '=== MEMORIA DEL PROYECTO DIVISAS (memoria/estado-actual.md) ==='
if (Test-Path $estado) {
    Get-Content -Raw -Encoding UTF8 $estado | Write-Output
} else {
    Write-Output 'Sin memoria previa. Crea memoria/estado-actual.md con la skill cerrar-sesion al terminar.'
}
Write-Output 'Recuerda: reglas en rules/, decisiones en memoria/decisiones.md, usa la skill cerrar-sesion al terminar.'
