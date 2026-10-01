# TRONstyleStuff

This is the canonical source collection for the user's TRON customizations. Work in the relevant application folder; preserve existing installed behavior and accepted color roles. The earlier workspaces and exports are historical copies.

Visual direction: ENCOM boardroom, black/blue-black surfaces, prominent blue/cyan outlines, rounded corners where needed, soft-white main titles, cyan smaller headings, orange more often than yellow for small accents. Terminal ordinary input and strings are soft white; commands/keywords blue.

Keep personal profiles, installation manifests, backup paths, browser data, debug logs, and credentials out of Git. Existing deployment and installed theme locations are separate from this repository.

VLC: run `python tools/build_visualizations.py`, `python tools/build_skin.py`, and `python tools/test_timed_playlist.py` from `vlc/` after relevant changes. Preserve playback, resizing, seeking, and visualization behavior.

ENCOM is a Git submodule of the existing ChromedomeV12/encom-boardroom fork, with independent history, upstream relationship, and deployment. Follow its nested AGENTS.md and preserve the original animations. Make and publish ENCOM changes in its own repository; update the collection's submodule pointer separately when appropriate. Do not replace it with a vendored source copy.

Wallpapers: `wallpapers/outputs/shanghai-tron-uprising.png` is the accepted full-resolution 28% variation image. Do not regenerate or replace it incidentally when adjusting documentation or other applications.

Bash: preserve the accepted minimal ble.sh configuration and startup performance. The PATH filtering in the fragments is intentional for this user's WSL setup.
