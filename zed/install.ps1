param([string]$ConfigDir = (Join-Path $env:APPDATA 'Zed'))
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'TRON.json'
$settingsPath = Join-Path $ConfigDir 'settings.json'
$text = if (Test-Path -LiteralPath $settingsPath) { [IO.File]::ReadAllText($settingsPath) } else { '{}' }
$before = ConvertFrom-Json -InputObject $text -AsHashtable
$themePattern = '"theme"\s*:\s*(\{[^{}]*\}|"[^"\r\n]*")'
$matchesFound = [regex]::Matches($text, $themePattern)
if ($matchesFound.Count -gt 1) { throw 'Multiple theme entries found; merge the theme setting manually to avoid changing a nested override.' }
$light = if ($before.theme -is [System.Collections.IDictionary] -and $before.theme.light) { $before.theme.light } else { 'One Light' }
$theme = @{mode='dark'; dark='TRON'; light=$light}
$replacement = '"theme": ' + ($theme | ConvertTo-Json -Compress)
if ($matchesFound.Count -eq 1) {
    $match = $matchesFound[0]
    $updated = $text.Substring(0,$match.Index) + $replacement + $text.Substring($match.Index+$match.Length)
} else {
    # Inserting first avoids modifying trailing commas or existing comments.
    $brace = $text.IndexOf('{')
    if ($brace -lt 0) { throw 'Settings must be a JSON object.' }
    $separator = if ($before.Count) { ',' } else { '' }
    $updated = $text.Insert($brace+1, "`n  $replacement$separator`n")
}
$after = ConvertFrom-Json -InputObject $updated -AsHashtable
foreach ($key in $before.Keys | Where-Object { $_ -ne 'theme' }) {
    if (($before[$key] | ConvertTo-Json -Depth 100 -Compress) -ne ($after[$key] | ConvertTo-Json -Depth 100 -Compress)) { throw "Unrelated setting changed: $key" }
}
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null
if (Test-Path -LiteralPath $settingsPath) { Copy-Item -LiteralPath $settingsPath -Destination "$settingsPath.before-tron-$stamp.bak" }
$themeDir = Join-Path $ConfigDir 'themes'
New-Item -ItemType Directory -Path $themeDir -Force | Out-Null
$destination = Join-Path $themeDir 'TRON.json'
if (Test-Path -LiteralPath $destination) { Copy-Item -LiteralPath $destination -Destination "$destination.before-tron-$stamp.bak" }
Copy-Item -LiteralPath $source -Destination $destination -Force
[IO.File]::WriteAllText($settingsPath,$updated,[Text.UTF8Encoding]::new($false))
if ((Get-FileHash -LiteralPath $source).Hash -ne (Get-FileHash -LiteralPath $destination).Hash) { throw 'Installed theme differs from source.' }
Write-Output "Installed and selected TRON in $ConfigDir. Other settings and the light-theme choice were preserved."
