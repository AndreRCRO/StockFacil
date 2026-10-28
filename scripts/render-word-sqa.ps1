# Exportación de documento a PDF mediante Word instalado, sin mostrar ventanas.
param([string]$InputPath, [string]$OutputPath)
$ErrorActionPreference = 'Stop'
$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $document = $word.Documents.Open($InputPath, $false, $true, $false)
    $document.ExportAsFixedFormat($OutputPath, 17)
    Write-Output "Word exportó PDF para revisión visual: $OutputPath"
} finally {
    if ($document) { $document.Close(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($document) }
    if ($word) { $word.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word) }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
