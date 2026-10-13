# Deployment status

As of 2026-10-13, the full replacement is active in ChatGPT Work and its validated local copy is installed for Codex desktop. `assets/replacement/spritesheet.png` contains the approved ±3° idle revision. The original atlas remains in `assets/published/` for comparison and recovery.

## Codex desktop: local Bit installed

The bundled `hatch-pet` runtime became available. The approved replacement PNG was SHA-256 checked against the retained source, then packaged as a lossless WebP. Codex desktop v2 requires a neutral frame at idle row 0, column 6; the approved first idle frame was copied into this otherwise empty reserved cell. All existing art cells remain pixel-identical. The app's `validate_atlas.py --require-v2` passed without errors or warnings.

The package is at `~/.codex/pets/bit/{pet.json,spritesheet.webp}` and desktop `selected-avatar-id` is `custom:bit`. The previous config is backed up under `~/.codex/backups/bit-local-selection-20261013-155516-209300/`. The app's own loader assigns this package the ID `custom:bit`. A restart may be needed for the running desktop window to reload its pet; visual confirmation in that window remains pending. The ChatGPT Work cloud pet and its stable ID were left intact.

The earlier Work-mode fallback had a separate cause: the desktop's cached cloud Bit artwork URL returned HTTP 404, although its saved selection still named Bit. The local package avoids that artwork route in the desktop pet selector. This does not establish that the cloud artwork URL itself is fixed.

## ChatGPT Work: replacement completed

The original custom Bit was successfully created in ChatGPT Work on 2026-10-02. The retained published atlas is the exact upload snapshot from that creation.

Subsequent attempts to fetch the stored sheet returned HTTP 403, including explicitly authorized fresh-link retries after deselection and an app restart. Those attempts stopped; the denial was not bypassed. The replacement was built from retained, approved source, not a newly downloaded server sheet.

After the user explicitly selected the Pets app, the earlier authorized delete-and-replace request was completed there. The exact validated replacement atlas passed native preflight again, was uploaded as a new custom Bit, and was selected successfully. The old pet record and stored sheet were then deleted. A complete roster readback confirmed the replacement active and the old entry absent. Private lifecycle receipts are retained outside Git.

This was a new pet created from approved local source, not a successful retry of the denied old-sheet download. It does not resolve or substitute for the separate desktop installation requirement.

## Publication scope

Publishing the source branch does not deploy a pet. The repository contains artwork, offline rendering/validation tools and sanitized QA, not private pet IDs, Library IDs, signed URLs, installation records or credentials. None of its Python tools makes network requests or changes a pet selection.
