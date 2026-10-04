# TRON desktop skin and launcher

## Daily launch

Run `Install-Shortcut.ps1` once to install **ChatGPT TRON** on the Desktop and in the Start menu. It copies the launcher, CSS, injector, and cyan icon to `%LOCALAPPDATA%\TRONstyleStuff\ChatGPT`, so ordinary launches do not depend on this checkout. Run the installer again after updating these source files. Existing managed files and same-named shortcuts are backed up under the destination's `backups/` folder.

Use **ChatGPT TRON** instead of the normal app shortcut. Right-click its Start-menu entry and pin it to the taskbar if desired; unpin the old normal launcher yourself. Pin the launcher entry, not the running app's normal icon. Windows may still group the running app under its original identity and show the original icon there; the cyan icon identifies our launcher and does not replace packaged app resources.

The shortcut starts PowerShell hidden, opens the app, injects the skin once, and exits. There is no command-window pause, resident watcher, or startup task. Failures show a small dialog. Successful runs overwrite `launcher.log` in the installation directory. Clicking the shortcut while an already-themed session is running reapplies the CSS and restores its main window. If the app is running without the debugging endpoint, the launcher asks you to quit it first; it never closes your work.

Verified 2026-10-04: both installed shortcut targets and icons; successful launch through the actual Desktop shortcut against the running app; one-shot injector completion. A full quit/relaunch was not performed during the active chat. The app path is resolved from the installed Windows package each launch, but changed DOM selectors in a future update may still require CSS/injector maintenance.

## Skin behavior

The outer frame now has 12 px rounded corners, with concentric 8 px corners on the inset frame. Both were verified in the live app with unchanged layout and pointer input passing through.

The ENCOM shell revision adds a continuous cyan frame around the client area with a second, dimmer line inset 4 px. The sidebar divider and chat header also have a quieter parallel rule. These fixed decorative frames ignore pointer input and do not change layout. Live checks on 2026-09-30 confirmed full cyan coverage on all four window edges, unchanged surface geometry/text colors, and one injected stylesheet. The outer frame is 70% cyan and the inner frame 24% cyan; edit `TRON-dividers.css` to adjust them.

This small local helper uses the same runtime CSS approach as community theme injectors. It does not install or run Theme Inject, patch Codex, alter the saved TRON theme, create startup tasks, or add a background service.

For the first themed launch, save any unsent drafts, finish running tasks, and fully quit the normal app. Open **ChatGPT TRON**, or use **Start-TRON.cmd** directly for troubleshooting. The launcher opens the installed app visibly with a debugging endpoint on 127.0.0.1:9339, waits up to 45 seconds for a chat surface, adds one stylesheet, and exits. The command script now pauses only after errors. Keep the endpoint local: it permits control of the renderer.

The stylesheet adds a 1 px cyan overlay along the full open sidebar edge, a cyan rule under the chat header, a cyan composer outline that strengthens on focus, sidebar section rules, code-block frames, and cyan colors for existing app borders. Opacity varies by role so the main divider stays strongest. The overlays ignore pointer input. The sidebar overlay replaces the original inset shadow, which could be covered by child surfaces. It has no animations, images, blur, polling, observers, or layout changes. The injector uses Node's built-in facilities and has no package dependencies. Normal CSS rendering and the app's debugging endpoint still have some cost; no live CPU/RAM benchmark has been performed.

The style remains in the current document through ordinary chat navigation. A renderer reload or newly opened app window may need another click on **ChatGPT TRON**. After a full restart, launch through that shortcut. Automatic update restarts, app links, and normal app shortcuts can bypass the helper. There is no automatic persistent injection.

Use **Restore-dividers.cmd** to remove this helper's stylesheet without restarting. Fully exit and reopen Codex using its normal shortcut to also close the debugging endpoint. If the helper cannot identify the app shell, it fails without changing installed files.

Selectors were checked against installed Codex 26.928.1915.0. The revised overlay was applied to the live app on 2026-09-30. A narrow screenshot of the sidebar edge showed cyan in all 1,160 captured rows. Its computed height matched the full sidebar height, and pointer events were disabled. Fixture checks also verified unchanged text/layout, repeat application, collapse behavior, and exact stylesheet removal. Future fresh launches still use the launcher described above.

The additional header, composer, section, and code-block accents were also applied and their computed styles checked in the live app. Their text color remained `#D8E1DD`, and the measured surface sizes were unchanged.

Theme Inject's source runs a persistent asset server/bridge and a health check every 10 seconds; its runtime also includes DOM observation and optional effects. See [launcher.rs](https://github.com/codecnmc/codex-theme-inject/blob/clean-version/src/launcher.rs) and [runtime lifecycle](https://github.com/codecnmc/codex-theme-inject/blob/clean-version/assets/runtime/lifecycle.js). Those components are not used here.
