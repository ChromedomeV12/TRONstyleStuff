# TRON desktop skin and launcher

## Daily launch

Run `Install-Shortcut.ps1` to install one managed Start-menu shortcut named **ChatGPT**. It replaces the previous user-created `ChatGPT.lnk`, backs up and removes `ChatGPT TRON.lnk`, and consolidates an existing Desktop copy if present. It does not create another Desktop shortcut. Backups are under `%LOCALAPPDATA%\TRONstyleStuff\ChatGPT\backups`.

The shortcut has the running app's `com.openai.codex` AppUserModelID, allowing Windows to group the launcher with ChatGPT. Unpin the previous taskbar entry once, then pin **ChatGPT** from the Start-menu shortcut. Pinning the running packaged app directly can create a pin that bypasses the helper. The registered Windows package entry still exists; this installer does not modify the package or its registration. One managed launcher plus the running app is the intended maximum of two entries; native taskbar grouping needs visual confirmation on the user's Windows session.

The shortcut opens PowerShell hidden and resolves the current installed app package on every cold launch. It selects an available loopback port instead of assuming 9339 is free. A per-user mutex prevents overlapping launcher runs. When ChatGPT is already running, the launcher reuses only a debugging listener owned by ChatGPT, reapplies CSS, and restores its window. If that session has no usable endpoint, it restores the window and records the limitation without closing the app or showing an error dialog. One full quit and launch through the managed shortcut enables CSS for subsequent launches.

The injector accepts the app shell before a main chat surface exists, so opening Settings or the home screen does not require waiting for a chat. It uses Node's built-in facilities, injects one stylesheet, and exits. There is no resident helper, service, startup task, binary patch, or downloaded runtime dependency. Patched Node 22.23.4+, 24.22.1+, or 26.12.1+ (within the same major) must be available on the launcher's PATH; see the collection's [runtime setup](../../README.md#nodejs-utilities). Logs and the session port stay outside Git in the installation directory.

A renderer reload, new app window, normal package launch, or automatic update restart may bypass or discard the CSS. Click the managed shortcut to reapply when a usable endpoint is present. Fully automatic recovery across every launch route would require an additional persistent mechanism. The native saved TRON color theme is separate and unchanged.

## Skin

`TRON-dividers.css` provides cyan sidebar/header dividers, a composer outline, section rules, code-block frames, and concentric outer-window outlines. Corners are rounded at 12 px outside and 8 px inside. Decorative overlays ignore pointer input and do not change layout. The stylesheet has no animations, polling, blur, or images.

Use `Restore-dividers.cmd` from this source directory to remove the injected stylesheet. It reads the recorded session port, falling back to the older 9339 endpoint. Fully quit and reopen through the normal packaged app to also close the debugging endpoint. Keep debugging bound to loopback: it permits renderer control.

## Validation and limits

The revised scripts parse successfully. Shortcut identity writing was exercised under PowerShell 7 and Windows PowerShell 5.1. Installed shortcut readback confirms `com.openai.codex` and one managed Start-menu ChatGPT shortcut. Injector fixture checks cover applying before a chat exists, idempotent replacement, removal, and rejection of nonlocal or wrong-port WebSocket endpoints. Existing-session restoration without a usable endpoint was tested without closing user work. A full cold launch and native taskbar grouping remain unverified during the active chat.

The unchanged stylesheet was previously checked live for continuous sidebar coverage, window-edge outlines, unchanged text/layout, and pointer pass-through. Future app DOM changes may require maintenance. No CPU/RAM benchmark has been performed.
