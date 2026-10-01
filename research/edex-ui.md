# eDEX-UI: revisit notes

Research checked 2026-10-01. Nothing installed or selected as a permanent fork.

## What it is

eDEX-UI is an installed desktop utility application: a fullscreen terminal emulator and system monitor built with Electron. It uses HTML/CSS/JavaScript internally but is not a hosted website or an operating system. It has real terminal sessions, CPU/RAM/network panels, a file browser, a globe, an on-screen keyboard, and optional sound effects.

The original explicitly cites TRON Legacy's boardroom sequence and credits Arscan's ENCOM Globe. This connects it to the same author behind the user's separate ENCOM boardroom fork. Its theme/CSS support fits the accepted black, cyan, soft-white, and orange direction.

Original: https://github.com/GitSquared/edex-ui
Final release: v2.2.8, 2021-10-18; repository archived 2021-10-22. The author described maintenance/refactoring costs and moving on to other work: https://github.com/GitSquared/edex-ui/releases/tag/v2.2.8

## Continuations investigated

| Repository | Evidence at review time | Assessment |
| --- | --- | --- |
| https://github.com/andreas-hartmann/xdex-ui | September 2026 commits and successful packaging workflows; Electron 43.2.0 in source; explicitly Linux-tested/supported; no GitHub Releases returned | First candidate to investigate on Omarchy; lightly maintained, not audited or benchmarked here |
| https://github.com/tianlingmc/edex-ui-plus | Windows v1.2.0 released 2026-07-18; Electron 43, xterm 6, preload bridge | Relevant Windows base, but main/index.js creates the terminal WebSocket without explicit loopback binding, origin validation, or authentication before accepting terminal commands; review/fix before regular use |
| https://github.com/dldvk9999/edex-ui | v2.4.0 released 2026-08-22; multiple-platform downloads, theme editor/plugins/split panes; package still specifies Electron 12 | Recent features do not imply runtime modernization; release notes say split panes were not GUI-tested |
| https://github.com/ippitenin/EDEX-macOS | Source v2.4.3, Electron 43, native Apple Silicon, recent work through 2026-10-01 Shanghai time; no GitHub Releases returned | macOS-specific, not a fit merely because Omarchy runs on Mac hardware; useful hardening notes with acknowledged limitations |
| https://github.com/theelderemo/eDEX-UI-security-patched | WebSocket-origin patch; October 2025 commits; Linux release assets | Older continuation worth consulting for fixes |
| https://github.com/josephkehan-prog/edex-ui-modern | One June 2026 modernization commit beyond upstream; Electron 33; no releases | Insufficient history to establish sustained maintenance |

The original has a published WebSocket hijacking / command-execution advisory: https://github.com/GitSquared/edex-ui/security/advisories/GHSA-q8xc-f2wf-ffh9 (CVE-2023-30856). Source checks above are not complete security audits. Recheck commits, releases, dependencies, and advisories when returning; none of the forks was run or performance-tested during this research.

## Tablet direction

The user likes the touchscreen keyboard and the film-like idea of a tablet ENCOM console.

- A Raspberry Pi tablet project documents eDEX-UI: https://hackaday.io/project/178372-pi-tablet-mk1
- The original developer explained that desktop eDEX was not designed for Android: https://github.com/GitSquared/edex-ui/discussions/1058
- The security-patched fork links to https://github.com/theelderemo/Edex-UI-android, but both GitHub page/API access failed (API 404) at review time. Its present implementation/availability could not be verified.
- No maintained native iPad port was found. Electron targets desktop platforms: https://www.electronjs.org/docs/latest/

Possible future adaptation: tablet renders a touch-friendly ENCOM interface and terminal locally; the Omarchy host supplies actual shell sessions and system statistics through an authenticated connection. This is an architectural proposal, not a verified existing eDEX feature. It would need a mobile/browser-compatible frontend and secure backend integration; it is not achieved by simply opening the Electron app in Safari. Rendering locally does not itself provide Mosh-style prediction or client-side Bash syntax highlighting.

When revisiting: choose desktop utility versus tablet control console first, inspect the candidate fork's terminal access boundary, then benchmark idle CPU, memory, and input response before investing in a custom theme.
