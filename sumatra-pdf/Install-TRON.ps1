[CmdletBinding()]
param(
    [string]$SettingsPath = (Join-Path $env:LOCALAPPDATA 'SumatraPDF/SumatraPDF-settings.txt')
)
$ErrorActionPreference = 'Stop'
$SettingsPath = (Resolve-Path -LiteralPath $SettingsPath).Path
$bytes = [IO.File]::ReadAllBytes($SettingsPath)
$hasBom = $bytes.Length -ge 3 -and $bytes[0] -eq 239 -and $bytes[1] -eq 187 -and $bytes[2] -eq 191
$encoding = [Text.UTF8Encoding]::new($hasBom, $true)
$original = [IO.File]::ReadAllText($SettingsPath, $encoding)
$newline = if ($original.Contains("`r`n")) { "`r`n" } else { "`n" }

# Top-level closing brackets in Sumatra's serialized settings have no indent.
# Refuse unexpected layouts instead of replacing an ambiguous section.
function Get-Section([string]$text, [string]$name) {
    $matches = [regex]::Matches($text, '(?ms)^' + [regex]::Escape($name) + '[ \t]*\[[ \t]*\r?\n.*?^\][ \t]*(?=\r?$)')
    if ($matches.Count -ne 1) { throw "Expected one top-level $name section; settings were not changed." }
    return $matches[0]
}
function Replace-Range([string]$text, $match, [string]$replacement) {
    return $text.Substring(0, $match.Index) + $replacement + $text.Substring($match.Index + $match.Length)
}

$themeSource = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'TRON.theme.txt'))
$definition = (($themeSource -split '\r?\n' | Where-Object { $_ -notmatch '^#' }) -join $newline).Trim()
$definition = (($definition -split '\r?\n' | ForEach-Object { '    ' + $_ }) -join $newline)
$themes = Get-Section $original 'Themes'
$entries = [regex]::Matches($themes.Value, '(?ms)^[ \t]+\[[ \t]*\r?\n.*?^[ \t]+\][ \t]*(?=\r?$)')
$tronEntries = @($entries | Where-Object { $_.Value -match '(?mi)^[ \t]+Name[ \t]*=[ \t]*TRON[ \t]*\r?$' })
if ($tronEntries.Count -gt 1) { throw 'Multiple TRON themes found; settings were not changed.' }
if ($tronEntries.Count -eq 1) {
    $newThemes = Replace-Range $themes.Value $tronEntries[0] $definition
} else {
    $closing = $themes.Value.LastIndexOf(']')
    $newThemes = $themes.Value.Substring(0, $closing) + $definition + $newline + $themes.Value.Substring($closing)
}
$updated = Replace-Range $original $themes $newThemes

$themeSetting = [regex]::Matches($updated, '(?m)^Theme[ \t]*=[^\r\n]*')
if ($themeSetting.Count -ne 1) { throw 'Expected one Theme setting; settings were not changed.' }
$updated = Replace-Range $updated $themeSetting[0] 'Theme = TRON'
$fixed = Get-Section $updated 'FixedPageUI'
$selection = [regex]::Matches($fixed.Value, '(?m)^([ \t]+)SelectionColor[ \t]*=[^\r\n]*')
if ($selection.Count -ne 1) { throw 'Expected one selection color; settings were not changed.' }
$newFixed = Replace-Range $fixed.Value $selection[0] ($selection[0].Groups[1].Value + 'SelectionColor = #FF8C1A')
$updated = Replace-Range $updated $fixed $newFixed

# All changes are limited to Themes, Theme, and the transient selection color.
if ($updated -ceq $original) { Write-Output 'TRON is already installed and selected.'; return }
$current = [IO.File]::ReadAllBytes($SettingsPath)
if ([Convert]::ToBase64String($bytes) -cne [Convert]::ToBase64String($current)) {
    throw 'Settings changed during preparation; run the installer again.'
}
$backup = $SettingsPath + '.before-tron-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '.bak'
[IO.File]::WriteAllBytes($backup, $bytes)
$temp = $SettingsPath + '.tron-' + [guid]::NewGuid().ToString('N') + '.tmp'
try {
    [IO.File]::WriteAllText($temp, $updated, $encoding)
    [IO.File]::Replace($temp, $SettingsPath, [NullString]::Value)
} finally {
    if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp }
}
if ([IO.File]::ReadAllText($SettingsPath, $encoding) -cne $updated) {
    throw "Settings changed after installation. A backup is available at $backup"
}
Write-Output 'TRON installed and selected. Document colors, annotations, history, and session settings preserved.'
Write-Output "Backup: $backup"
