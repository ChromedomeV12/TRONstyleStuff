# TRON / ENCOM for Oh My Posh

A compact, two-line prompt with cyan framing, blue paths, soft-white branch names, and orange Git changes and slow-command duration. Failed commands turn the prompt red and display the exit code. Yellow appears only for a root session. Transparent segments preserve the terminal's accepted blue-black background. Ordinary command input remains controlled by ble.sh; this theme does not change syntax highlighting or ANSI colors.

```text
╭─[ENCOM]─[~/dev/project]─[main ●~1] │ 2.1s
╰─❯ echo "hehe"
```

This original configuration was informed by the official `nordtron` outlined frame, `atomic` two-line structure, and the `blueish` and `clean-detailed` segment arrangements. It does not copy their theme files. References: [bundled theme catalog](https://ohmyposh.dev/docs/themes), [configuration](https://ohmyposh.dev/docs/configuration/general), [Git](https://ohmyposh.dev/docs/segments/scm/git).

## Install in Ubuntu

Install the native Linux Oh My Posh executable in `~/.local/bin` following the [official Linux installation guide](https://ohmyposh.dev/docs/installation/linux). Avoid invoking the Windows executable from WSL. Then run `python3 install.py` from this directory and open a new Ubuntu terminal.

The installer replaces one existing Starship initialization block, leaving all other Bash startup content intact. It backs up `.bashrc` and any previous TRON OMP configuration in `~/.config/tron/backups/`. The initialization uses an absolute executable path and a local configuration; it performs no theme downloads on shell startup. The Starship binary/configuration remain available for rollback. ble.sh loading, highlighting, attach order, PATH filtering, and fastfetch are unchanged.

For a temporary fallback, open a new shell using `TRON_PROMPT=starship bash`. To fully revert, restore the backed-up `.bashrc`. Do not source a new prompt engine into an existing initialized shell: open a fresh shell instead.

## Performance and scope

Only local path, Git, exit status, root status, and command duration are collected. Git status is enabled with a 150 ms segment timeout; repository size and filesystem affect its cost. There are no cloud/network segments, language-runtime probes, right prompt, battery checks, automatic updates, or transient prompt. No Nerd Font is required for the Unicode frame and symbols.

This installs only in the current Linux home. Windows PowerShell, other WSL distributions, and SSH/Mosh hosts have independent prompt setups.

Verified in Ubuntu with native Oh My Posh 31.8.0: official schema validation, successful/failed command rendering, untracked Git state, duration formatting, and a fresh interactive PTY with ble.sh 0.4.0-nightly. OMP initializes without duplicate Starship hooks. Seven warm render samples had medians of 19.7 ms in the home directory and 20.1 ms in a small dirty Git repository, with maxima of 22.3/23.4 ms; the previous Starship home median was 18.0 ms. These measure prompt-render processes, not typing or total shell startup. Large repositories and Windows-mounted filesystems can cost more; the Git segment can disappear if its timeout is reached.
