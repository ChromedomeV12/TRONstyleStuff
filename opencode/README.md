# TRON for OpenCode v2

Native dark theme for the **OpenCode terminal client**, named **TRON**. Adapted from the complete built-in `opencode` v2 theme at release `v2.0.27`, with its MIT license retained in [LICENSE](LICENSE).

This uses the v2 `base`/`dark` token-tree format and `cli.json` settings. It is not a v1 `theme`/`defs` file or a `tui.json` installation. References: [v2 theme guidance](https://dev.opencode.ai/v2/docs/cli/theme), [pinned default theme](https://github.com/anomalyco/opencode/blob/v2.0.27/packages/tui/src/theme/assets/v2/opencode.json), [pinned native schema](https://github.com/anomalyco/opencode/blob/v2.0.27/packages/theme/src/tui/schema.ts).

| Role | Color |
| --- | --- |
| Main canvas / raised panels | `#050E14` / `#0B202B` |
| Borders / active links | Blue `#6FC3DF` / cyan `#78DDFF` |
| Markdown headings / horizontal rules | Cyan `#00EEEE` |
| Text, titles, variables, ordinary strings | Soft white `#D8E1DD` |
| Keywords / operators | Blue `#6FC3DF` |
| Functions, numbers, inline code, strong emphasis, warnings | Orange `#FF8C1A` |
| Types | Lavender `#B6A4D8` |
| Success / additions | Green `#65D6A6` |
| Errors / removals | Coral `#FF6B4A` |
| Focused and selected actions | Dark navy `#183C66`, white text |

The theme includes the full semantic tree, dark hue scales, dialog surfaces, action states, forms, Markdown, syntax, and diff roles. Added/removed diff backgrounds and changed-word highlights use dark green/red fills rather than bright blocks. Yellow remains available in its hue scale but is not assigned to common syntax or warnings. Repeated agent colors start with cyan, then orange. No additional plugin, shell hook, or background process is required.

The theme is dark-only. The installer explicitly selects dark mode; selecting light mode with this theme still falls back to the dark palette as documented by OpenCode. The TUI's native layout determines where borders are drawn; this is not CSS injection or a desktop/web theme.

## Install

Run `python3 install.py` on Linux/WSL, or `python install.py` on Windows. The default config directory is `$XDG_CONFIG_HOME/opencode` or `~/.config/opencode`; use `--config-dir /path/to/opencode` when needed.

The installer backs up the existing `cli.json` and any existing TRON theme under `backups/tron-<timestamp>/`, copies [TRON.json](TRON.json) into `themes/`, and changes only `theme.name` to `TRON` and `theme.mode` to `dark`. It expects standard JSON in `cli.json`; it does not rewrite provider/model settings in `opencode.json` or `opencode.jsonc`.

Restart OpenCode after installation. Alternatively, run `/themes` and select **TRON**, or press Ctrl+P → Open settings → Theme. A project-local theme of the same name can override the global file.

To revert, restore the backed-up `cli.json`, or select the previous theme (`tokyonight` in the checked installations). Existing built-ins are unchanged.

## Validation

Validated with the exact `ThemeDocument` schema from OpenCode v2.0.27 and its pinned Effect 4.0.1 dependency. All color references resolve without cycles. Checked syntax/Markdown colors, focused/selected/pressed action pairs, and normal/highlighted diff pairs have at least 4.84:1 contrast. This is a static palette check, not a full TUI accessibility audit.

Installed copies match the source in Windows and WSL Ubuntu, both running OpenCode v2.0.27. Parsed CLI settings differ only in the selected theme name/mode. Provider configuration, Oh-My-Pi settings, and existing shell files were checked unchanged. Full visual review in a running OpenCode TUI remains pending.

## Original logo colors

Run `python3 install-logo-colors.py` on WSL/Linux or `python install-logo-colors.py` on Windows. This installs a CLI-only plugin under `plugins/tron-logo-colors/` and appends its path to `cli.json.plugins`, with a backup of the previous settings. Restart OpenCode normally to load it.

The plugin recolors OpenCode's existing logo in place: the first word uses Legacy blue `#6FC3DF`, the second cyan `#00EEEE`, and the original inset shadows receive corresponding dark blue/cyan fills. Every letter, text node, layout group, and responsive arrangement remains native. It does not create replacement artwork or alter ordinary text colors.

OpenCode v2.0.27 has no dedicated logo palette setting. The plugin recognizes its exact original logo structure and changes only the matched text nodes' foreground/background colors. If an update changes that structure, it leaves the native logo alone. Colors are restored on cleanup or when leaving the home screen. It uses existing frame events and skips settled nodes, with no additional timer, renderer dependency, service, or binary patch.

Verified using the native renderer for identical characters/layout, shadows, composer preservation, and cleanup, followed by a real WSL OpenCode startup. Installed in Windows and WSL with both TRON theme files preserved. To remove it, delete its path from `cli.json.plugins` and remove `plugins/tron-logo-colors/`, then restart; the TRON theme can remain selected.
