param([Parameter(Mandatory=$true)][string]$ProfilePath)
$ErrorActionPreference = 'Stop'
$profile = (Resolve-Path -LiteralPath $ProfilePath).Path
$chrome = Join-Path $profile 'chrome'
$prefs = Join-Path $profile 'prefs.js'
if (!(Test-Path -LiteralPath $prefs)) { throw 'Choose the Zen profile folder containing prefs.js.' }
if (!(Select-String -LiteralPath $prefs -SimpleMatch 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);' -Quiet)) {
    throw 'Enable toolkit.legacyUserProfileCustomizations.stylesheets in about:config first.'
}
$names = @('userChrome.css','userContent.css')
foreach ($name in $names) {
    if (!(Test-Path -LiteralPath (Join-Path $PSScriptRoot $name))) { throw "Missing package file: $name" }
}
New-Item -ItemType Directory -Path $chrome -Force | Out-Null
$stamp = [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow,'China Standard Time').ToString('yyyyMMdd-HHmmss')
$backup = Join-Path $chrome ("TRON-backup-" + $stamp)
New-Item -ItemType Directory -Path $backup | Out-Null
$records = @()
foreach ($name in $names) {
    $destination = Join-Path $chrome $name
    if (!(Test-Path -LiteralPath $destination)) { throw "This installer expects the existing theme file: $destination" }
    Copy-Item -LiteralPath $destination -Destination (Join-Path $backup $name)
    $records += [pscustomobject]@{Name=$name;OriginalHash=(Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash;InstalledHash=(Get-FileHash -LiteralPath (Join-Path $PSScriptRoot $name) -Algorithm SHA256).Hash}
}
try {
    foreach ($record in $records) {
        $destination=Join-Path $chrome $record.Name
        Copy-Item -LiteralPath (Join-Path $PSScriptRoot $record.Name) -Destination $destination -Force
        if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $record.InstalledHash) { throw 'Installed CSS verification failed.' }
    }
} catch {
    foreach ($name in $names) { Copy-Item -LiteralPath (Join-Path $backup $name) -Destination (Join-Path $chrome $name) -Force }
    throw
}
$manifest=[pscustomobject]@{Profile=$profile;Backup=$backup;InstalledAtChinaTime=$stamp;Files=$records;BrowserRestartRequired=$true}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'installation.json') -Encoding utf8
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $backup 'installation.json') -Encoding utf8
Write-Output "TRON CSS installed. Original CSS backed up to: $backup"
Write-Output 'Fully quit and reopen Zen when convenient to apply. This script does not restart Zen or alter preferences.'
