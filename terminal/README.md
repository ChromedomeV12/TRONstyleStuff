# TRON Legacy terminal configuration

The accepted palette and input roles, collected without changing existing installations. Windows Terminal supplies the ANSI palette; each shell controls its own syntax highlighting. SSH hosts require their own shell configuration.

## Windows Terminal and PowerShell

Merge the object in `TRON-Legacy.json` into your Windows Terminal settings' `schemes` array and select **TRON Legacy** for the desired profiles. Do not replace your complete settings file with this scheme object.

Keep `TRON-Colors.ps1` in a stable location and dot-source it from your interactive PowerShell profile. It sets PSReadLine colors. The optional `starship.toml` is the accepted Windows prompt configuration; merge its colors with your own configuration if you have other customizations.

On PowerShell 7.2+, this fragment also makes `Get-ChildItem` directory names bold cyan on the terminal's normal background. PowerShell's default blue directory background collides with this palette's blue default foreground, otherwise producing unreadable solid blocks. This changes only the directory formatting role; aliases, other file styles, and the terminal palette are preserved. After updating the installed fragment, open a new PowerShell tab or dot-source the fragment once in the current tab.

Cross-environment check on 2026-10-03: Ubuntu's `ls --color=auto` uses `01;34` (bold blue foreground) for ordinary directories. The SSH/Mosh host's `ls` alias runs `eza`, which also emits blue foreground without a background for ordinary directories. The ordinary-directory and `/tmp` samples did not reproduce the PowerShell collision. Ubuntu retains its standard special-permission directory backgrounds. No shared ANSI palette or Linux configuration change was needed for this fix.

| Input role | Color |
| --- | --- |
| Commands and keywords | #6FC3DF |
| Default input, strings, parameters, variables, members | #D8E1DD |
| Numbers and types | #FF8C1A |
| Operators | #8892A0 |
| Comments and predictions | #667D94 |
| Search emphasis | #FFE600 |
| Errors | #FF6B4A |
| Selected input | #D8E1DD on #183C66 |

PSReadLine does not expose a separate punctuation color; punctuation follows the containing token. Starship uses a blue directory and success arrow, soft-white Git branch, orange Git status, and coral failure symbol.

## Ubuntu / Bash

`linux/blesh-init.sh` contains the minimal ble.sh color configuration. Automatic suggestions, filename highlighting, and automatic completion menus are disabled. The startup fragments expect ble.sh at `~/.local/share/tron-blesh/ble-nightly/ble.sh` and the color configuration at `~/.config/tron/blesh-init.sh`; ble.sh itself is not vendored.

The original setup uses `linux/bashrc-header.sh` before interactive initialization and `linux/bashrc-footer.sh` at the end of `.bashrc`, after an existing non-interactive guard where applicable. These are fragments to merge once, not replacements for the whole `.bashrc`.

These fragments intentionally remove Windows drive directories from the interactive WSL PATH, before and after startup, to avoid slow executable discovery. Linux paths remain. This reflects the accepted setup where bare-name lookup of Windows executables was not needed; inspect the fragments before adopting them on a different machine. They do not modify `/etc/wsl.conf`.

`TRON_BASH_HIGHLIGHT=0 bash` skips the add-on in a child shell; that shell still inherits its parent's current PATH. Existing fastfetch and Ubuntu Starship configurations are not included or modified. Personal backup paths and installation records remain in the original local workspace.

The recorded PTY trial in `linux/performance-trial.md` measured typing at about 14-15 ms median and 29-31 ms p95. These are historical measurements, not a guarantee for another machine.

## Remote SSH / Mosh shells

The add-on and color configuration must also exist on the remote host. The local Ubuntu `.bashrc` does not configure the Bash process running there.

Use `linux/remote-bashrc-header.sh` before the remote prompt/key-binding initialization and `linux/remote-bashrc-footer.sh` at the end of its `.bashrc`. These fragments use the same ble.sh and color-config paths as above and **do not filter PATH**. Keep the existing interactive-shell guard and login-profile handling. Back up `.bashrc` before merging; do not append duplicate hooks.

The remote Omarchy setup was checked on 2026-10-01: Bash 5.3.15, Mosh server 1.4.0, existing Omarchy/Starship initialization preserved. Interactive login-shell tests confirmed blue commands, soft-white strings, command execution, working fzf registration, the opt-out switch, and identical PATH with/without the add-on. Approximate server-side PTY typing response was 17 ms median and 28 ms maximum; this excludes network latency.

Reconnect after installing. Existing remote shells retain their old initialization. Mosh's predicted local echo can briefly show a character before the remote highlighter recolors it. Mosh 1.4.0 added true-color support; older versions may render the RGB palette differently. See [Mosh](https://mosh.org/) and [ble.sh installation instructions](https://github.com/akinomyoga/ble.sh#13-set-up-bashrc).
