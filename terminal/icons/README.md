# ENCOM profile icon

`encom-icon.png` is a transparent 64 x 64 blue/cyan E monogram derived from the boardroom ENCOM wordmark. A single letter remains readable at tab-icon size. Rebuild with `node ../backgrounds/build.cjs` using that builder's dependencies.

In Windows Terminal, press **Ctrl+,**, select a profile such as **PowerShell** under **Profiles**, then expand **Icon**, browse to this PNG, and save. Repeat for other profiles you want branded. This changes the profile's tab and dropdown icon without painting anything over shell or TUI content. It does not change the Windows Terminal taskbar/app icon.

Alternatively, add an `icon` field to the chosen object in `profiles.list` in `settings.json`, using an absolute path to the PNG. Use forward slashes in the path or escape backslashes. To share it, put the field in `profiles.defaults`; existing profile-specific icons take precedence.

Official reference: [Windows Terminal profile icons](https://learn.microsoft.com/en-us/windows/terminal/customize-settings/profile-general#icon).

The background images remain optional; this icon does not require enabling one.
