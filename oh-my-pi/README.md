# TRON for Oh-My-Pi

Native **Oh-My-Pi (`omp`) coding-agent** theme. This is separate from the [original Pi theme](../pi/) and from any terminal prompt engine.

Adapted from the bundled `dark-abyss` theme's role layout, compared with `dark-tokyo-night`, `dark-cyberpunk`, and `obsidian`. The dark surfaces and cyan framing follow this collection's ENCOM palette; warm colors are confined to syntax, warnings, and small status elements. Source reference: Oh-My-Pi package 17.4.2's `src/modes/theme/defaults/dark-abyss.json`. Its MIT license and copyright notices are retained in [LICENSE](LICENSE).

| Role | TRON color |
| --- | --- |
| Active frames, headings, horizontal rules | Cyan `#00EEEE` |
| Normal frames, links, keywords, operators, paths | Blue `#6FC3DF` |
| Body text, tool titles/output, variables, strings | Soft white `#D8E1DD` |
| Functions, numbers, inline code, warnings, dirty Git/cost indicators | Orange `#FF8C1A` |
| Types / Python mode | Lavender `#B6A4D8` |
| Success / additions | Green `#65D6A6` |
| Failure / removals | Coral `#FF6B4A` |
| Selected rows | Dark navy `#183C66` |
| Pending / successful / failed tool panels | `#07151D` / `#102824` / `#321C1F` |

The success panel retains the accepted dark-green cue. Thinking borders progress through blue/cyan rather than warm colors. Oh-My-Pi exposes one Markdown-heading color, so all heading levels share cyan; tool titles and body text stay white. The terminal controls the main canvas background. This theme adds no animations, CSS injection, shell hooks, or extra startup processes, and it leaves the user's symbol preset alone.

## Install in WSL Ubuntu

Run `python3 install.py` from this directory. The native Oh-My-Pi executable defaults to `~/.bun/bin/omp`; pass `--omp /path/to/omp` for another location. The agent directory defaults to `PI_CODING_AGENT_DIR` or `~/.omp/agent`; pass `--agent-dir /path/to/agent` when needed.

The installer copies `TRON.json` into `themes/`, backs up the existing configuration and any previous TRON file under `backups/tron-<timestamp>/`, and uses `omp config set theme.dark TRON` to select it. Light-mode selection remains unchanged. Named profiles require selecting the matching agent directory and config environment.

Restart Oh-My-Pi to load the saved selection, or choose **TRON** under `/settings` → Appearance → Dark Theme. No terminal restart or Bash reload is required. To revert, use `omp config set theme.dark dark-abyss` (the previous Ubuntu choice), or choose the former theme in Settings. The original built-in themes remain installed.

## Verification

Installed and selected in Oh-My-Pi 18.10.3. Its native config command read back `TRON`. Parsed settings before/after differ only at `theme.dark`; light selection and all unrelated preferences match. `.bashrc` remains byte-identical, preserving Starship and ble.sh.

The installed source package's 17.4.2 runtime schema/loader validated the JSON and rendered all 67 foreground/background roles in truecolor. This source-package check is distinct from the newer standalone executable; full visual review inside the 18.10.3 TUI remains to be done. Language capture and individual tool renderer behavior may affect where colors appear.

References: [official Oh-My-Pi theming guide](https://github.com/can1357/oh-my-pi/blob/main/docs/theme.md), [current theme schema](https://github.com/can1357/oh-my-pi/blob/main/packages/tui/src/theme/theme-schema.json).
