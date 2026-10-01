# Project TODO

## Current priority: performance and compatibility

- [x] Replace tiny background tiles that caused excessive drawing during resize.
- [x] Remove the redundant idle background layer.
- [x] Check player and playlist resizing, maximize/restore, and seek-bar alignment in VLC.
- [x] Confirm resize responsiveness in normal use after reloading the optimized skin (confirmed by user).
- Prefer VLC's existing controls, dialogs, menus, and rendering features. Preserve the horizontal menu row.

## Simple DJ features

- [x] Investigate crossfades: native playlist transitions are cuts; document Mixxx Auto DJ for overlapping fades.
- [x] Expose VLC's native equalizer and preamp through Audio and Tools; document bass boost.
- [x] Add a timed XSPF playlist helper with per-track start/stop points; verify options in VLC.
- [x] Assess a two-player companion: defer a custom engine in favor of a dedicated DJ application for reliable mixing. See docs/audio.md.

## Audio visualization customization

- [x] Add blue Waves and cyan Orbit on the TRON background without branding, captions, or emojis.
- [x] Use the installed projectM plugin; verify loading, visible animation and embedded rendering during resize in VLC 3.0.23 on Windows.
- [x] Document preset selection, customization, disabling and restoring the previous preset path.
- [x] Fix black edges in wide visualization windows and background darkening during preset transitions; verify rendered RGB against `#050e14`.
- [x] Smooth motion between audio blocks with native preset equations; observe Waves above the user's 30 FPS target and reduce unnecessary feedback mesh work.

## Follow-up validation

- [ ] User feedback on visualization appearance and equalizer controls.
- [ ] Test Linux Skins2/projectM compatibility; currently only Windows is verified.

## TRON adaptation

- [x] Blue-black panels, double cyan borders, blue controls and orange active states.
- [x] Recolor Waves and Orbit while preserving the smoothing equations.
- [x] Validate player/playlist resize and seek alignment at 960, 1440, and 1920 pixels.
- [x] Verify live visualizations and equalizer, and refresh actual VLC screenshots.
- [ ] User feedback on TRON styling.
