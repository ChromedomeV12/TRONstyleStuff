# TRON divider session test

The outer frame now has 12 px rounded corners, with concentric 8 px corners on the inset frame. Both were verified in the live app with unchanged layout and pointer input passing through.

The ENCOM shell revision adds a continuous cyan frame around the client area with a second, dimmer line inset 4 px. The sidebar divider and chat header also have a quieter parallel rule. These fixed decorative frames ignore pointer input and do not change layout. Live checks on 2026-09-30 confirmed full cyan coverage on all four window edges, unchanged surface geometry/text colors, and one injected stylesheet. The outer frame is 70% cyan and the inner frame 24% cyan; edit `TRON-dividers.css` to adjust them.

This small local helper uses the same runtime CSS approach as community theme injectors. It does not install or run Theme Inject, patch Codex, alter the saved TRON theme, create startup tasks, or add a background service.

Save any unsent drafts and finish running tasks. Fully exit Codex, then double-click **Start-TRON.cmd**. The launcher opens the installed app visibly with a debugging endpoint on 127.0.0.1:9339, waits up to 45 seconds for a chat surface, adds one stylesheet, and exits. The command window can then be closed. Keep the endpoint local: it permits control of the renderer.

The stylesheet adds a 1 px cyan overlay along the full open sidebar edge, a cyan rule under the chat header, a cyan composer outline that strengthens on focus, sidebar section rules, code-block frames, and cyan colors for existing app borders. Opacity varies by role so the main divider stays strongest. The overlays ignore pointer input. The sidebar overlay replaces the original inset shadow, which could be covered by child surfaces. It has no animations, images, blur, polling, observers, or layout changes. The injector uses Node's built-in facilities and has no package dependencies. Normal CSS rendering and the app's debugging endpoint still have some cost; no live CPU/RAM benchmark has been performed.

The style remains in the current document through ordinary chat navigation. A renderer reload, app restart, or newly opened app window can require running `node inject.cjs` again. Launch through Start-TRON.cmd each time you want the test after a full restart. There is no automatic persistent injection.

Use **Restore-dividers.cmd** to remove this helper's stylesheet without restarting. Fully exit and reopen Codex using its normal shortcut to also close the debugging endpoint. If the helper cannot identify the app shell, it fails without changing installed files.

Selectors were checked against installed Codex 26.928.1915.0. The revised overlay was applied to the live app on 2026-09-30. A narrow screenshot of the sidebar edge showed cyan in all 1,160 captured rows. Its computed height matched the full sidebar height, and pointer events were disabled. Fixture checks also verified unchanged text/layout, repeat application, collapse behavior, and exact stylesheet removal. Future fresh launches still use the launcher described above.

The additional header, composer, section, and code-block accents were also applied and their computed styles checked in the live app. Their text color remained `#D8E1DD`, and the measured surface sizes were unchanged.

Theme Inject's source runs a persistent asset server/bridge and a health check every 10 seconds; its runtime also includes DOM observation and optional effects. See [launcher.rs](https://github.com/codecnmc/codex-theme-inject/blob/clean-version/src/launcher.rs) and [runtime lifecycle](https://github.com/codecnmc/codex-theme-inject/blob/clean-version/assets/runtime/lifecycle.js). Those components are not used here.
