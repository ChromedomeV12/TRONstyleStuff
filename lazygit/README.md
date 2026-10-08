# TRON for Lazygit

Native Lazygit colors: cyan focused borders, muted blue inactive borders, soft-white text, orange change/search accents, and a dark navy selected row. Explicit RGB colors prevent the terminal's pale ANSI blue from becoming an unreadable selection background. The selected row uses soft white so file names and status text stay readable.

Merge the `gui.theme` block from [TRON.yml](TRON.yml) into your existing Lazygit configuration. Preserve other options. For an empty configuration, copy the file directly.

- Windows: `%LOCALAPPDATA%\lazygit\config.yml`
- Linux/WSL: `~/.config/lazygit/config.yml`

Run `lazygit --print-config-dir` to confirm the location. Restart Lazygit after editing. Each remote host has its own configuration; installing locally does not install it over SSH.

This changes Lazygit's UI without changing the terminal palette or shell highlighting. Theme keys were checked against Lazygit 0.66.0 and the [official configuration documentation](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md#highlighting-the-selected-line).
