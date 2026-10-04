# Install a user-owned launcher, without modifying the app's installed files.
$ErrorActionPreference = 'Stop'
$taskDestination = Join-Path $env:LOCALAPPDATA 'TRONstyleStuff\ChatGPT'
$taskFiles = @('Start-TRON.ps1', 'inject.cjs', 'TRON-dividers.css', 'ChatGPT-TRON.ico')
foreach ($taskFile in $taskFiles) {
    if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot $taskFile))) { throw "Missing launcher asset: $taskFile" }
}
$taskStamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$taskBackup = Join-Path $taskDestination "backups\$taskStamp"
New-Item -ItemType Directory -Path $taskBackup -Force | Out-Null
foreach ($taskFile in $taskFiles) {
    $taskInstalledFile = Join-Path $taskDestination $taskFile
    if (Test-Path -LiteralPath $taskInstalledFile) {
        Copy-Item -LiteralPath $taskInstalledFile -Destination (Join-Path $taskBackup $taskFile)
    }
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot $taskFile) -Destination $taskInstalledFile -Force
}
$taskShell = New-Object -ComObject WScript.Shell
$taskShortcutFolders = @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))
foreach ($taskFolder in $taskShortcutFolders) {
    $taskShortcutPath = Join-Path $taskFolder 'ChatGPT TRON.lnk'
    if (Test-Path -LiteralPath $taskShortcutPath) {
        Copy-Item -LiteralPath $taskShortcutPath -Destination (Join-Path $taskBackup ((Split-Path $taskFolder -Leaf) + '-ChatGPT TRON.lnk'))
    }
    $taskLink = $taskShell.CreateShortcut($taskShortcutPath)
    $taskLink.TargetPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
    $taskLink.Arguments = '-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + (Join-Path $taskDestination 'Start-TRON.ps1') + '" -Quiet'
    $taskLink.WorkingDirectory = $taskDestination
    $taskLink.IconLocation = (Join-Path $taskDestination 'ChatGPT-TRON.ico') + ',0'
    $taskLink.Description = 'Open ChatGPT with the TRON cyan frame and accents'
    $taskLink.WindowStyle = 7
    $taskLink.Save()
    $taskCheck = $taskShell.CreateShortcut($taskShortcutPath)
    if ($taskCheck.Arguments -ne $taskLink.Arguments -or $taskCheck.IconLocation -ne $taskLink.IconLocation) { throw 'Shortcut verification failed' }
    Write-Host "Installed: $taskShortcutPath"
}
Write-Host "Launcher assets: $taskDestination"
Write-Host 'Pin ChatGPT TRON from Start to use this launcher from the taskbar. Original app shortcuts are preserved.'
