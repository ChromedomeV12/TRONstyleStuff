$ErrorActionPreference = 'Stop'
try {
    $nodePath = (Get-Command node -ErrorAction Stop).Source
    if (Get-Process ChatGPT -ErrorAction SilentlyContinue) {
        throw 'Close all Codex/ChatGPT desktop windows and let the app exit before starting this test. This launcher will not close them for you.'
    }
    $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, 9339)
    try { $listener.Start() } finally { $listener.Stop() }
    $package = Get-AppxPackage -Name 'OpenAI.Codex' | Sort-Object Version -Descending | Select-Object -First 1
    if (-not $package) { throw 'The OpenAI.Codex Windows package was not found.' }
    $appPath = Join-Path $package.InstallLocation 'app\ChatGPT.exe'
    if (-not (Test-Path -LiteralPath $appPath -PathType Leaf)) { throw 'Codex executable was not found.' }
    # This is the interactive app the user is opening, so its window must be visible.
    Start-Process -FilePath $appPath -ArgumentList '--remote-debugging-address=127.0.0.1','--remote-debugging-port=9339' -WindowStyle Normal
    & $nodePath (Join-Path $PSScriptRoot 'inject.cjs')
    if ($LASTEXITCODE -ne 0) { throw 'Divider injection failed. Restart Codex normally to return to its usual launch mode.' }
    Write-Host 'TRON dividers applied. The injector has exited. Restart Codex normally to undo.'
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
