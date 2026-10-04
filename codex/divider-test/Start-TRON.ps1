param([switch]$Quiet)
$ErrorActionPreference = 'Stop'
$taskLogDirectory = Join-Path $env:LOCALAPPDATA 'TRONstyleStuff\ChatGPT'
try {
    $nodePath = (Get-Command node -ErrorAction Stop).Source
    $package = Get-AppxPackage -Name 'OpenAI.Codex' | Sort-Object Version -Descending | Select-Object -First 1
    if (-not $package) { throw 'The OpenAI.Codex Windows package was not found.' }
    $appPath = Join-Path $package.InstallLocation 'app\ChatGPT.exe'
    if (-not (Test-Path -LiteralPath $appPath -PathType Leaf)) { throw 'Codex executable was not found.' }
    $appProcesses = @(Get-Process ChatGPT -ErrorAction SilentlyContinue)
    if ($appProcesses.Count) {
        $debugListener = @(Get-NetTCPConnection -State Listen -LocalPort 9339 -ErrorAction SilentlyContinue)
        if (-not $debugListener.Count -or @($debugListener | Where-Object {
            $_.LocalAddress -ne '127.0.0.1' -or $_.OwningProcess -notin $appProcesses.Id
        }).Count) {
            throw 'ChatGPT is already running without the TRON launcher. Save your work, fully quit it from its tray menu, then open ChatGPT TRON. Nothing has been closed automatically.'
        }
    } else {
        $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 9339)
        try { $listener.Start() } finally { $listener.Stop() }
        # This is the interactive app the user requested, so show its window.
        Start-Process -FilePath $appPath -ArgumentList '--remote-debugging-address=127.0.0.1','--remote-debugging-port=9339' -WindowStyle Normal
    }
    $injectOutput = & $nodePath (Join-Path $PSScriptRoot 'inject.cjs') 2>&1
    if ($LASTEXITCODE -ne 0) { throw ('TRON injection failed. ' + ($injectOutput -join ' ')) }
    # Restore the existing main window when the shortcut is clicked again.
    $window = Get-Process ChatGPT -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
    if ($window) {
        Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class TronWindow {
    [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr hWnd, int command);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@
        [void][TronWindow]::ShowWindowAsync($window.MainWindowHandle, 9)
        [void][TronWindow]::SetForegroundWindow($window.MainWindowHandle)
    }
    New-Item -ItemType Directory -Path $taskLogDirectory -Force | Out-Null
    ('{0:o} TRON applied. Injector exited. {1}' -f (Get-Date), ($injectOutput -join ' ')) | Set-Content -LiteralPath (Join-Path $taskLogDirectory 'launcher.log')
    if (-not $Quiet) { Write-Host 'TRON applied. The injector has exited.' }
} catch {
    $taskMessage = $_.Exception.Message
    if ($Quiet) {
        Add-Type -AssemblyName System.Windows.Forms
        [void][System.Windows.Forms.MessageBox]::Show($taskMessage, 'ChatGPT TRON', 'OK', 'Warning')
    } else { Write-Host $taskMessage -ForegroundColor Red }
    exit 1
}
