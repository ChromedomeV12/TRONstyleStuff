TRON for Zen Browser
====================
Target verified: Zen 1.22.3b on Windows.

Blue-black panels, blue/cyan controls, cyan dividers, a rounded double window
outline, soft-white text, and orange for small active/matched/media states.
Container identity colors retain their distinct meanings.

userChrome.css styles the browser UI. userContent.css only styles built-in
about: pages, including settings and the new-tab page. Ordinary websites
keep their own colors. The frame is pointer-transparent. No added animations,
blur filters, JavaScript injection, extension, or companion background process.

Installed using Zen's documented CSS support:
https://docs.zen-browser.app/guides/live-editing

Apply changes by fully quitting and reopening Zen. Existing tabs/session
remain under Zen's normal session handling; the installer does not close it.
Custom stylesheets were already enabled in this profile, so no browser
preferences, binaries, or generated Zen Mods files were changed.

Installation
------------
Install-TRON.ps1 -ProfilePath '<your Zen profile folder>'
Use about:support to locate the profile folder. This installer is designed
for replacing an existing userChrome.css/userContent.css theme. It verifies
the stylesheet preference, saves timestamped copies, then verifies file hashes.
installation.json records the actual profile and backup location.

To restore the previous Tokyo Night theme, run Restore-Previous-Theme.ps1,
then fully quit and reopen Zen. It stops if the installed CSS was edited
after installation, so later customizations are not silently overwritten.

Validation
----------
Tested in a separate, empty Zen profile: actual computed colors for browser
chrome, selected tabs, URL field focus, menus, and settings; compact-mode
toggle; pointer-transparent window frame; unchanged colors on a test web page.
Screenshots were captured from that profile, not from private browsing data.
These checks do not cover every extension, workspace gradient, or future Zen
release. CSS selectors may need updating after major browser UI changes.
