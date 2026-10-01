# Bash highlighting performance trial — 2026-09-30

Status: enabled after the user confirmed Windows executable lookup is not needed. Interactive Bash filters Windows-drive PATH entries before and after startup. The original `.bashrc` backup and personal installation records remain in the original local workspace. Starship, fastfetch, Windows Terminal, and `/etc/wsl.conf` remain unchanged.

Final full-profile test, with Linux PATH and fzf integration: startup 546–614 ms (baseline 250–283 ms); typing median 14–15 ms; p95 29–31 ms; maximum 33.1 ms. The earlier 1.5-second first-key pause was absent. Both `the Linux home directory` and the Windows-mounted workspace were tested. These are approximate PTY timings, not physical keyboard-to-screen measurements.

The results below document the earlier investigation before PATH filtering was authorized.

Test: Python PTY, Bash 5.2, the existing Starship prompt, home directory and a Windows-mounted workspace. Normal Windows machine/user PATH was reconstructed to exclude extra Codex tool-runtime paths. Each key's terminal output was collected until a 25 ms quiet interval; that interval was subtracted. These are approximate output-response measurements, not physical keyboard-to-screen latency. Terminal-query replies were simulated. A few short command lines do not cover every interactive workload.

Results with normal PATH and minimal ble.sh colors (no automatic suggestions, filename highlighting, or automatic menus):

- Baseline startup: approximately 0.24–0.27 seconds.
- Baseline typing median: approximately 0.7 ms.
- Add-on startup with deferred fzf integration: approximately 0.66–0.73 seconds.
- Add-on typing median: approximately 15 ms; 95th percentile approximately 38–40 ms.
- First-key pause: approximately 1.5–1.6 seconds. Loading fzf and the completion module before the prompt did not eliminate it.
- Blue command and white string ANSI output were observed.

A separate bare-shell control with only Linux directories in PATH had a typing median of 18.3 ms, p95 of 35.3 ms, and maximum of 38.9 ms. This suggests Windows-path lookup overhead is significant, but that control omitted the normal profile and is not proof that a full-profile installation with a reduced PATH is ready.

No PATH reduction was installed: it could affect Windows executable discovery from Ubuntu. An experimental highlighting-only PATH wrapper did not resolve the delay and was not installed either.

Benchmarker: `work/benchmark-bash.py` in the task workspace. Source guidance: https://github.com/akinomyoga/ble.sh/issues/96 and the runtime's `doc/contrib/integration/fzf.md`.
