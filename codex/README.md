# TRON for Codex desktop

The accepted ENCOM palette, exported on 2026-09-30. Optional cyan outlines and rounded double window frames are provided separately in [divider-test](divider-test/README.md).

| Role | Color |
| --- | --- |
| Background | `#000000` |
| Accent | `#00EEEE` |
| Text and main titles | `#D8E1DD` |
| Skill accent | `#FF8C1A` |
| Added lines | `#6FC0BA` |
| Removed lines | `#FF8595` |

The ENCOM boardroom revision restores a pure black base and the reference project's exact neon cyan, concentrating color in accents instead of tinting the entire app navy. Contrast is 75, stronger than the initial 60 but gentler than the navy revision's 85. Added-line accents use ENCOM teal. Text and main titles remain the softer white, while skill accents remain vivid orange. Windows remain opaque, and the existing fonts are preserved, including Hack Nerd Font Mono for code. Codex generates raised surfaces and borders from these base settings; this import cannot assign arbitrary cyan outlines to every panel.

The built-in **Codex** code preset supplies orange variables and constants, alongside cyan, green, purple, and red syntax colors. The theme picker may still display “Codex”; this is the syntax preset's name. This import format does not define custom syntax token colors, individual heading colors, inline highlight colors, or a custom display name. Those Obsidian details are therefore not an exact port. Yellow is not introduced in the custom app palette.

## Import or restore

Open Settings with **Ctrl+,**, then **Appearance**. Under the dark theme's **Import** control, paste the entire contents of `TRON.txt`. Select Dark if necessary. If the currently open app has not refreshed from the saved settings, importing applies the same palette through the app's controls.

To restore the navy wallpaper revision, import `previous-navy-tron.txt`. The initial TRON version is in `previous-tron.txt`, and the original Tokyo Night appearance is in `previous-tokyo-night.txt`. Use these theme-only restores to avoid overwriting other settings changed later. Personal backups and installation records remain in the original local workspace.

The `.json` files are readable representations of the share payloads; the `.txt` files include the required `codex-theme-v1:` prefix. `desktop-settings.toml` is a reference excerpt, not a replacement for your complete config.

## Verification and sources

Import fields and supported preset IDs were checked against the locally installed app, version 26.928.1915.0. The generated TOML parses successfully. Only the dark chrome palette and dark code preset changed; light appearance, fonts, and all unrelated settings were compared and preserved.

[Official appearance settings documentation](https://learn.chatgpt.com/docs/reference/settings) describes custom colors, fonts, and theme sharing. The exact share schema was verified in the installed app's theme importer.
