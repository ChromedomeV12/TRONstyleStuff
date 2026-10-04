param(
    [string]$UserData = (Join-Path $env:APPDATA 'FlowLauncher'),
    [string]$FlowExe
)
$ErrorActionPreference = 'Stop'
$taskSettingsPath = Join-Path $UserData 'Settings\Settings.json'
$taskSource = Join-Path $PSScriptRoot 'TRON.xaml'
if (-not (Test-Path -LiteralPath $taskSettingsPath)) { throw 'Flow settings were not found. Pass -UserData for a portable profile.' }
[void][xml](Get-Content -LiteralPath $taskSource -Raw)
$taskInitial = Get-Content -LiteralPath $taskSettingsPath -Raw | ConvertFrom-Json
if ($null -eq $taskInitial.Theme) { throw 'Settings do not contain a Theme preference.' }
$taskProcesses = @(Get-Process Flow.Launcher -ErrorAction SilentlyContinue)
if ($taskProcesses.Count -gt 1) { throw 'Multiple Flow instances found; close them before installing.' }
if (-not $FlowExe -and $taskProcesses.Count) { $FlowExe = $taskProcesses[0].Path }
if (-not $FlowExe) {
    $taskApp = Get-ChildItem (Join-Path $env:LOCALAPPDATA 'FlowLauncher') -Directory -Filter 'app-*' |
        Sort-Object { [version]($_.Name.Substring(4)) } -Descending | Select-Object -First 1
    if ($taskApp) { $FlowExe = Join-Path $taskApp.FullName 'Flow.Launcher.exe' }
}
if (-not $FlowExe -or -not (Test-Path -LiteralPath $FlowExe)) { throw 'Flow executable not found. Pass -FlowExe.' }
$taskBackup = Join-Path $UserData ('ThemeBackups\TRON-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
New-Item -ItemType Directory -Path $taskBackup -Force | Out-Null
$taskTarget = Join-Path $UserData 'Themes\TRON.xaml'
if (Test-Path -LiteralPath $taskTarget) { Copy-Item -LiteralPath $taskTarget -Destination (Join-Path $taskBackup 'TRON.xaml') }
New-Item -ItemType Directory -Path (Split-Path $taskTarget) -Force | Out-Null
Copy-Item -LiteralPath $taskSource -Destination $taskTarget -Force

# Flow 2.1.4's main-window OnClosing saves settings and disposes plugins.
# WM_CLOSE follows that normal path; no forced process termination is used.
if ($taskProcesses.Count) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Text;
public static class TronFlowWindow {
    public delegate bool Callback(IntPtr hwnd, IntPtr arg);
    [DllImport("user32.dll")] public static extern bool EnumWindows(Callback fn, IntPtr arg);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hwnd, out uint pid);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hwnd, StringBuilder text, int count);
    [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr hwnd, uint msg, IntPtr wp, IntPtr lp);
    public static IntPtr Find(uint pid) {
        IntPtr result = IntPtr.Zero;
        EnumWindows((hwnd, arg) => { uint found; GetWindowThreadProcessId(hwnd, out found);
            if(found == pid) { var title=new StringBuilder(512); GetWindowText(hwnd,title,512);
                if(title.ToString()=="Flow.Launcher" || title.ToString()=="Flow Launcher") { result=hwnd; return false; } }
            return true;
        }, IntPtr.Zero);
        return result;
    }
}
'@
    $taskWindow = [TronFlowWindow]::Find($taskProcesses[0].Id)
    if ($taskWindow -eq [IntPtr]::Zero) { throw 'Could not locate Flow main window. Quit Flow from its tray menu and run this installer again.' }
    [void][TronFlowWindow]::PostMessage($taskWindow, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero)
    if (-not $taskProcesses[0].WaitForExit(15000)) { throw 'Flow is still shutting down; settings were not changed. Retry after it exits.' }
}
$taskPreviousText = $null
try {
    # Read again after graceful exit so its final saved preferences are preserved.
    $taskPreviousText = [IO.File]::ReadAllText($taskSettingsPath)
    $taskBefore = $taskPreviousText | ConvertFrom-Json
    Copy-Item -LiteralPath $taskSettingsPath -Destination (Join-Path $taskBackup 'Settings.json')
    $taskPattern = '"Theme"\s*:\s*"(?:[^"\\]|\\.)*"'
    if ([regex]::Matches($taskPreviousText, $taskPattern).Count -ne 1) { throw 'Expected one Theme property; no settings edited.' }
    $taskNextText = [regex]::Replace($taskPreviousText, $taskPattern, '"Theme": "TRON"')
    $taskAfter = $taskNextText | ConvertFrom-Json
    if ($taskAfter.Theme -ne 'TRON') { throw 'Theme selection verification failed.' }
    [IO.File]::WriteAllText($taskSettingsPath, $taskNextText, [Text.UTF8Encoding]::new($false))
    if ((Get-FileHash -LiteralPath $taskSource).Hash -ne (Get-FileHash -LiteralPath $taskTarget).Hash) { throw 'Installed XAML differs from source.' }
    Write-Host "Installed and selected TRON. Previous theme: $($taskBefore.Theme)"
    Write-Host "Backup: $taskBackup"
} catch {
    if ($null -ne $taskPreviousText) { [IO.File]::WriteAllText($taskSettingsPath, $taskPreviousText, [Text.UTF8Encoding]::new($false)) }
    throw
} finally {
    Start-Process -FilePath $FlowExe -WindowStyle Hidden
}
