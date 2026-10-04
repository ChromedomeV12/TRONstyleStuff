# TRON for Pi

Native Pi coding-agent theme, named **TRON** in the theme selector. No extension, CSS injection, or additional startup process.

| Role | Color |
| --- | --- |
| Reading text, tool titles, variables, strings | Soft white `#D8E1DD` |
| Active borders, Markdown headings, horizontal rules | Neon cyan `#00EEEE` |
| Normal borders, links, keywords, list markers | Blue `#6FC3DF` |
| Functions, numbers, inline code, warnings, Bash-mode border | Orange `#FF8C1A` |
| Types | Lavender `#B6A4D8` |
| Success / additions | Green `#65D6A6` |
| Errors / removals | Coral `#FF6B4A` |
| Search matches | Yellow `#FFD166` with dark text |

Thinking-level borders progress through blue and cyan; high reasoning levels do not turn the whole editor yellow. Function names are orange so adjacent blue keywords and functions are easy to distinguish. Code strings and ordinary text stay soft white. Green, red, and yellow retain specific status/search meanings.

Pi exposes one Markdown heading color, so all heading levels share cyan. Tool titles are soft white. The terminal controls the main canvas and unstyled input foreground; use the existing TRON Legacy terminal palette (`#0D1117` background, soft-white foreground). Pi's theme controls message/tool panel backgrounds and HTML export backgrounds, not the terminal's global palette.

Completed tool panels, including edit diffs, use the blue-black `successBg` (`#101E29`). The earlier green `#102824` filled the entire successful-tool container: it was our `toolSuccessBg` role, not an unchangeable terminal color. Verified in Pi 1.0.2's `tool-execution.js`, where pending/error/success select their respective background roles. Changing `toolDiffAdded` affects text, not this panel. Separately, Pi's `diff.js` renders changed words with inverse video; those small highlight blocks swap foreground/background and have no independent theme background role. This theme leaves Pi's renderer intact and retains green/coral added/removed text.

## Install or update

With Python 3, from this directory:

```powershell
python install.py
```

The installer respects `PI_CODING_AGENT_DIR`, or defaults to `~/.pi/agent`. It writes `themes/TRON.json` and sets only the `theme` preference to `TRON`. It saves the original settings and any existing TRON file under the target profile's `backups/tron-<timestamp>/` first. Models, providers, packages, and credentials are not changed.

For another profile, pass `--agent-dir /path/to/.pi/agent`. A remote Pi process needs installation on that host; this installer affects only the specified local profile.

For an already running Pi session, use `/reload`, then `/settings` → Theme → **TRON**. A newly launched session reads the saved selection. Pi watches the active user theme file for later edits.

Manual install: copy `TRON.json` to `~/.pi/agent/themes/TRON.json`, then select TRON in `/settings`. File and theme names must match, including case on Linux.

## Restore

Choose your previous theme through `/settings` (the existing Windows profile used `omarchy-tokyonight`). The installer keeps that theme file intact. The saved settings backup is also available if needed; restoring the full file will restore all preferences to their installation-time values.

## Compatibility

Based on the Pi 0.87.1 profile and validated against its official JSON schema, including all required colors and the optional scrollbar, search, and maximum-thinking roles. Uses six-digit RGB values and variable references for compatibility. Terminal truecolor support gives the intended palette; 256-color terminals approximate it.

References: [Pi theme documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/themes.md), [0.87.1 schema](https://github.com/earendil-works/pi/blob/v0.87.1/packages/coding-agent/src/modes/interactive/theme/theme-schema.json).
