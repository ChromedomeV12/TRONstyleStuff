# TRON for SumatraPDF

A native theme for SumatraPDF 3.6 / 3.6.1. Uses the ENCOM palette without app patches, injected CSS, or a special launcher.

| Role | Color |
| --- | --- |
| Main surface | `#050E14` |
| Controls / sidebar | `#0B202B` |
| UI text | `#D8E1DD` |
| Links / progress accent | `#78DDFF` |
| Text selection / search result highlight | `#FF8C1A` |

PDF page colors and images retain their existing settings. Annotation colors are unchanged; the orange selection is temporary UI highlighting, not an edit to the PDF.

## Install

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Install-TRON.ps1
```

The installer updates `%LOCALAPPDATA%\SumatraPDF\SumatraPDF-settings.txt`. For a portable installation pass `-SettingsPath` with that copy's settings file. It backs up the original file beside it, adds or updates only the TRON theme, selects it, and sets the selection/search color. Other themes, PDF colors, annotations, shortcuts, file history, and reading positions are preserved. Re-running does not duplicate the theme. The installed theme loads with ordinary SumatraPDF launches.

Sumatra watches its settings file. If an open window does not refresh, reopen the app; you can also select **Settings → Theme → TRON**, or **Ctrl+K → Set theme 'TRON'**. If `UseSysColors = true` is enabled in another installation, system colors may override custom colors; disable it to use the theme.

For manual setup, add the entry in `TRON.theme.txt` inside the existing `Themes [ ... ]` array, set `Theme = TRON`, and optionally set `SelectionColor = #FF8C1A` inside `FixedPageUI`.

To revert, select your previous theme and restore your previous selection color (the stock value is `#f5fc0c`). A full backup restore also restores the history/settings from that point in time; prefer the two-field revert if you have used the reader since installation.

## Version limits

SumatraPDF 3.6.1 exposes four base theme colors and the control-coloring switch. It derives many tab, hover, and border colors internally. Arbitrary neon outlines and separately colored tab titles are not available through this version's native theme settings. Newer online documentation lists additional fields and smart document recoloring that are not part of 3.6.1; this preset deliberately uses the installed version's supported fields.

References: [3.6 settings](https://www.sumatrapdfreader.org/settings/settings3-6), [3.6.1 theme implementation](https://github.com/sumatrapdfreader/sumatrapdf/blob/3.6.1rel/src/Theme.cpp), [current theme documentation](https://www.sumatrapdfreader.org/docs/Customize-theme-colors).
