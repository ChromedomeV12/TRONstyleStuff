# TRON for Zed

An ENCOM boardroom adaptation of [Bret Comnes' Tron Legacy theme](https://github.com/bcomnes/zed-theme-tron-legacy), based on upstream commit `3fd2b39d7a0769d5842e23d182f9a4a88bc6e634`. Its MIT license is retained in [LICENSE](LICENSE). The theme selector displays **TRON**.

The original dark variant supplies the UI and syntax coverage. This adaptation replaces gray surfaces with blue-black, makes dividers and focus borders cyan, uses soft-white text, and replaces lime accents with orange or cyan. Opaque surfaces avoid wallpaper-dependent contrast. Selections use dark navy rather than a bright cyan fill.

| Role | Color |
| --- | --- |
| Editor | `#050E14` |
| Side panels / elevated surfaces | `#07151D` / `#0B202B` |
| Text, variables, ordinary strings | `#D8E1DD` |
| Keywords, operators, namespaces, tags | `#6FC3DF` |
| Focus borders, active icons, links, cursor | `#78DDFF` |
| Functions, constructors, numeric literals, escapes | `#FF8C1A` |
| Types, regex, special variables | `#C594C5` |
| Comments | `#819BA7` |
| Success / additions | `#50D6C6` |
| Errors / removals | `#FF6B4A` |

Yellow is limited to the existing terminal bright-yellow slot and a later collaboration cursor. Language grammars determine which syntax captures appear; a theme cannot control their frequency. The integrated terminal uses the collection's accepted [ANSI palette](../terminal/TRON-Legacy.json); shell input highlighting remains controlled by the shell.

## Install

On Windows, run `pwsh -File ./install.ps1` from this directory. It backs up your settings and any previous local TRON theme, installs the JSON, and selects dark TRON while retaining your light-theme choice and other settings. It does not install extensions, change fonts, or modify keybindings.

Alternatively, copy [TRON.json](TRON.json) into `%APPDATA%/Zed/themes/` on Windows or `~/.config/zed/themes/` on Linux/macOS. Reload Zed, open the theme selector with Ctrl+K Ctrl+T (Cmd+K Cmd+T on macOS), and choose TRON. These are [Zed's native local-theme locations](https://zed.dev/docs/themes#local-themes).

To revert, select the previous theme or restore the settings backup beside `settings.json`. The original extension can coexist with this local theme.

## Validation

Validated as JSON against Zed's official v0.2.0 theme schema. Current upstream style keys absent from that schema are retained. All 45 syntax colors have at least 6.65:1 contrast on the editor background; soft-white text on the selected-row background has 8.38:1 contrast. These are opaque palette checks, not a full accessibility audit. Installed copy and unrelated-settings preservation are checked by the installer. Native visual review inside Zed remains necessary; this is a native color theme and does not add custom CSS geometry, glow, or double outlines.
