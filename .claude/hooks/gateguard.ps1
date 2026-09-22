# Gateguard - hook PreToolUse del proyecto Divisas.
# Bloquea comandos destructivos y pide aprobacion humana para migraciones y push.
# Salida: exit 2 + mensaje en stderr = bloqueo; JSON "ask" en stdout = pedir confirmacion.

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

try {
    $data = [Console]::In.ReadToEnd() | ConvertFrom-Json
} catch {
    exit 0
}

$tool = $data.tool_name
$ti = $data.tool_input

function Block($reason) {
    [Console]::Error.WriteLine("GATEGUARD bloqueo: $reason. Explica al operador que querias hacer; no busques otra forma de hacerlo.")
    exit 2
}

function Ask($reason) {
    $out = @{
        hookSpecificOutput = @{
            hookEventName            = 'PreToolUse'
            permissionDecision       = 'ask'
            permissionDecisionReason = "GATEGUARD: $reason. Requiere aprobacion del operador."
        }
    } | ConvertTo-Json -Depth 5 -Compress
    Write-Output $out
    exit 0
}

# --- Archivos sensibles (Read / Edit / Write) ---
if ($ti.file_path) {
    $p = [string]$ti.file_path
    if ($p -match '(^|[\\/])\.env(\.(?!example$)[^\\/]+)?$') { Block "acceso a archivo de entorno con secretos ($p)" }
    if ($p -match '\.(pem|key|p12|pfx)$') { Block "acceso a archivo de llaves ($p)" }
}

# --- Comandos de shell (Bash / PowerShell) ---
if ($ti.command) {
    $c = [string]$ti.command

    $blocked = @(
        @{ p = '\b(update|delete\s+from)\s+("?public"?\.)?"?ledger_entries\b'; r = 'modificar o borrar ledger_entries (es append-only; usa un contra-asiento)' },
        @{ p = '\btruncate\b';                                        r = 'TRUNCATE de tablas' },
        @{ p = '\bdrop\s+(table|schema|database)\b';                  r = 'DROP de tabla/esquema/base de datos' },
        @{ p = '\bsupabase\s+db\s+reset\b';                           r = 'supabase db reset' },
        @{ p = '\bgit\s+push\b.*(--force|\s-f\b)';                    r = 'git push --force' },
        @{ p = '\bgit\s+reset\s+--hard\b';                            r = 'git reset --hard' },
        @{ p = '\brm\s+-[a-z]*(rf|fr)[a-z]*\b';                       r = 'rm -rf' },
        @{ p = 'Remove-Item\b.*-Recurse';                             r = 'borrado recursivo' }
    )
    foreach ($b in $blocked) {
        if ($c -match "(?i)$($b.p)") { Block $b.r }
    }

    $needsApproval = @(
        @{ p = '\bsupabase\s+(db\s+push|migration\s+(up|repair))\b'; r = 'aplicar migraciones' },
        @{ p = '\b(alter|create)\s+table\b';                       r = 'cambio de esquema' },
        @{ p = '\bgit\s+push\b';                                   r = 'git push' }
    )
    foreach ($a in $needsApproval) {
        if ($c -match "(?i)$($a.p)") { Ask $a.r }
    }
}

exit 0
