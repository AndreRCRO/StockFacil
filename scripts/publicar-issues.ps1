# Ejecuta desde la raíz después de instalar GitHub CLI e iniciar sesión con gh auth login.
$ErrorActionPreference = 'Stop'
$repository = 'AndreRCRO/StockFacil'
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw 'Instala GitHub CLI desde https://cli.github.com y ejecuta gh auth login.'
}
gh auth status
if ($LASTEXITCODE -ne 0) { throw 'Inicia sesión con gh auth login antes de continuar.' }
$existing = gh issue list --repo $repository --state all --limit 100 --json title,number | ConvertFrom-Json
$tasks = Import-Csv -LiteralPath 'docs/Kanban_Tareas.csv'
foreach ($task in $tasks) {
    if ($existing.title -contains $task.Titulo) {
        Write-Output "Ya existe: $($task.Titulo)"
        continue
    }
    $body = @"
Responsable propuesto: $($task.Responsable)
Prioridad: $($task.Prioridad)
Estado técnico local: $($task.Estado)

$($task.Descripcion)

## Criterios de aceptación
$($task.Criterios)

## Evidencias
$($task.Evidencias)

La ejecución asistida no acredita revisión humana. El compañero registra su revisión antes de mover a Terminado.
"@
    $bodyFile = Join-Path ([System.IO.Path]::GetTempPath()) 'stockfacil-issue-body.md'
    Set-Content -LiteralPath $bodyFile -Value $body -Encoding utf8
    gh issue create --repo $repository --title $task.Titulo --body-file $bodyFile
    if ($LASTEXITCODE -ne 0) { throw "No se pudo crear $($task.Titulo). Revisa permisos y reejecuta." }
}
