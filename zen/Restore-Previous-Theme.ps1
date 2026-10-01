$ErrorActionPreference='Stop'
$manifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'installation.json') -Raw | ConvertFrom-Json
$chrome=Join-Path $manifest.Profile 'chrome'
$backup=(Resolve-Path -LiteralPath $manifest.Backup).Path
$expectedRoot=(Resolve-Path -LiteralPath $chrome).Path.TrimEnd('\')+'\'
if (!$backup.StartsWith($expectedRoot,[StringComparison]::OrdinalIgnoreCase)) { throw 'Unexpected backup location.' }
foreach($record in $manifest.Files) {
    if ($record.Name -notin @('userChrome.css','userContent.css')) { throw 'Unexpected file in manifest.' }
    $target=Join-Path $chrome $record.Name
    $original=Join-Path $backup $record.Name
    if ((Get-FileHash -LiteralPath $target).Hash -ne $record.InstalledHash) { throw "CSS has changed since installation; review $target before restoring." }
    if ((Get-FileHash -LiteralPath $original).Hash -ne $record.OriginalHash) { throw 'Backup integrity check failed.' }
}
foreach($record in $manifest.Files) { Copy-Item -LiteralPath (Join-Path $backup $record.Name) -Destination (Join-Path $chrome $record.Name) -Force }
Write-Output 'Previous theme restored. Fully quit and reopen Zen to apply it.'
