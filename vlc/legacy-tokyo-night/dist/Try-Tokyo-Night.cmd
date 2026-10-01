@echo off
setlocal
set "VLC_EXE=%ProgramFiles%\VideoLAN\VLC\vlc.exe"
if not exist "%VLC_EXE%" set "VLC_EXE=%ProgramFiles(x86)%\VideoLAN\VLC\vlc.exe"
if not exist "%VLC_EXE%" (
  echo VLC was not found. Open VLC Preferences and select the VLT file manually.
  pause
  exit /b 1
)
set "PREVIEW_CONFIG=%TEMP%\vlc-tokyo-night-preview-%RANDOM%-%RANDOM%.ini"
if exist "%APPDATA%\vlc\vlcrc" (copy /y "%APPDATA%\vlc\vlcrc" "%PREVIEW_CONFIG%" >nul) else (type nul > "%PREVIEW_CONFIG%")
start "" "%VLC_EXE%" --no-one-instance --config="%PREVIEW_CONFIG%" --intf=skins2 --skins2-last="%~dp0Tokyo-Night-Dark.vlt" %*
