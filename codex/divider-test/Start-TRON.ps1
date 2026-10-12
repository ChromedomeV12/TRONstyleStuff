param([switch]$Quiet)
$ErrorActionPreference = 'Stop'
$taskLogDirectory = Join-Path $env:LOCALAPPDATA 'TRONstyleStuff\ChatGPT'
New-Item -ItemType Directory -Path $taskLogDirectory -Force | Out-Null
$mutex = New-Object Threading.Mutex($false, ('Local\TRON-ChatGPT-' + [Security.Principal.WindowsIdentity]::GetCurrent().User.Value))
$locked = $false
try {
    try { $locked = $mutex.WaitOne(0) } catch [Threading.AbandonedMutexException] { $locked = $true }
    if (-not $locked) { return }
    $package = Get-AppxPackage -Name 'OpenAI.Codex' | Sort-Object Version -Descending | Select-Object -First 1
    if (-not $package) { throw 'The OpenAI.Codex Windows package was not found.' }
    $appPath = Join-Path $package.InstallLocation 'app\ChatGPT.exe'
    if (-not (Test-Path -LiteralPath $appPath -PathType Leaf)) { throw 'ChatGPT executable was not found.' }
    $appProcesses = @(Get-Process ChatGPT -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path -like '*\OpenAI.Codex_*\app\ChatGPT.exe' })
    $port = $null
    $statePath = Join-Path $taskLogDirectory 'debug-session.json'
    if ($appProcesses.Count) {
        # Reuse only a loopback listener owned by this app.
        $candidatePorts = @(9339)
        if (Test-Path -LiteralPath $statePath) {
            try { $candidatePorts += [int](Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json).port } catch { }
        }
        $candidatePorts += @(Get-CimInstance Win32_Process -Filter "Name='ChatGPT.exe'" | Where-Object { $_.ProcessId -in $appProcesses.Id } | ForEach-Object {
            if ($_.CommandLine -match '--remote-debugging-port=(\d+)') { [int]$Matches[1] }
        })
        foreach ($candidate in @($candidatePorts | Select-Object -Unique)) {
            if ($candidate -lt 1024 -or $candidate -gt 65535) { continue }
            $owned = @(Get-NetTCPConnection -State Listen -LocalPort $candidate -ErrorAction SilentlyContinue | Where-Object { $_.LocalAddress -eq '127.0.0.1' -and $_.OwningProcess -in $appProcesses.Id })
            if ($owned.Count) { $port = $candidate; break }
        }
    } else {
        $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 0)
        try { $listener.Start(); $port = $listener.LocalEndpoint.Port } finally { $listener.Stop() }
        @{ port=$port } | ConvertTo-Json | Set-Content -LiteralPath $statePath
        Start-Process -FilePath $appPath -ArgumentList '--remote-debugging-address=127.0.0.1',"--remote-debugging-port=$port" -WindowStyle Normal
    }
    $status = 'Existing app restored. CSS requires one full quit and launch through ChatGPT to enable debugging.'
    if ($port) {
        $nodePath = (Get-Command node -ErrorAction Stop).Source
        $injectOutput = & $nodePath (Join-Path $PSScriptRoot 'inject.cjs') "--port=$port" 2>&1
        if ($LASTEXITCODE -ne 0) { throw ('TRON injection failed. ' + ($injectOutput -join ' ')) }
        $status = 'TRON applied. Injector exited. ' + ($injectOutput -join ' ')
    }
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
    ('{0:o} {1}' -f (Get-Date), $status) | Set-Content -LiteralPath (Join-Path $taskLogDirectory 'launcher.log')
    if (-not $Quiet) { Write-Host $status }
} catch {
    $taskMessage = $_.Exception.Message
    ('{0:o} {1}' -f (Get-Date), $taskMessage) | Set-Content -LiteralPath (Join-Path $taskLogDirectory 'launcher.log')
    if (-not $Quiet) { Write-Warning $taskMessage }
    exit 1
} finally {
    if ($locked) { $mutex.ReleaseMutex() }
    $mutex.Dispose()
}
