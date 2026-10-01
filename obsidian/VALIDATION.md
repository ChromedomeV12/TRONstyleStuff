# Validation · 0.3.4 · ENCOM edition

Completed on 29 September 2026:

- Manifest JSON parsed; name equals the theme directory name.
- Browser mockup rendered in installed Microsoft Edge via Playwright at 1480px and 390px widths.
- Desktop screenshot visually inspected; mobile screenshot checked separately.
- Browser reported no JavaScript errors.
- No horizontal document overflow at 390px.
- Reading/source preview switch and its pressed state work.
- Quiet toggle changes the glow variable to `none`.
- Mono-note toggle switches the note font stack to Inconsolata with local monospace fallbacks.
- Controls dialog opens and closes with Escape.
- Nine text/accent colors tested on four base surfaces: 36 pairs, all at least 4.5:1. Lowest ratio 5.72:1.
- Rendered color checks passed for title, H2/H3, bold text, tags, inline code, strings, numbers, and highlighted text.
- Corrected preview-only syntax span classes so code colors render through the intended token selectors.

These checks validate the package and the browser mockup. They do not establish native Obsidian compatibility, full WCAG conformance, or compatibility with every community plugin.

## Native checks still needed

- [ ] Activate Tron Grid in an Obsidian vault in Dark mode.
- [ ] Read Sample note.md in Reading view and Live Preview.
- [ ] Inspect source mode, code blocks, list markers, internal/external links, and highlights.
- [ ] Check file explorer, properties, quick switcher, command palette, settings, search, and menus.
- [ ] Check graph view, Canvas, backlinks, and outline in the actual app.
- [ ] Check the optional Style Settings controls if that plugin is installed.
- [ ] Check native mobile layout and touch controls if mobile use is desired.
- [ ] Confirm default appearance returns after choosing another theme.

## Installation and recovery update

Tron Grid was subsequently installed in the user's Economics vault. An incorrect hidden-window launch made the loaded vault inaccessible through its normal visible window. The exact Tokyo Night appearance backup was restored, and the existing Obsidian window was revealed without terminating the app. The user confirmed the vault was usable again.

The installed Tokyo Night theme was compared with Tron Grid: both have the standard `manifest.json` + `theme.css` layout, matching theme/folder names, and CSS-variable styling. No structural mismatch was found that explains the incident. Tokyo Night was selected at recovery. Before the later v0.3 file update, the vault already selected Tron Grid; that update preserved the appearance settings byte-for-byte, backed up v0.2, and verified the installed v0.3 files by SHA-256. No application launch or restart was performed for the v0.3 update. Native rendering of Tron Grid remains unverified. Codex appearance settings were not changed.
