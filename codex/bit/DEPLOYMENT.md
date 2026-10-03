# Deployment status

As of 2026-10-03, the full replacement is **active in ChatGPT Work, but not installed in Codex desktop**. `assets/replacement/spritesheet.png` contains the approved ±3° idle revision. The original atlas remains in `assets/published/` for comparison and recovery.

## Codex desktop: separate installation remains blocked

The user requested Codex desktop installation before explicitly selecting the ChatGPT Pets app for the subsequent replacement. Desktop's bundled `hatch-pet` skill requires `load_workspace_dependencies` before running its scripts and explicitly says to stop when that runtime is unavailable. The creation session did not expose that tool, so desktop packaging and activation stopped. No desktop `pet.json` package was installed. The skill does not document a user-facing procedure that guarantees the missing tool will become available.

Do not substitute ChatGPT Work pet controls for this desktop target. Resume installation only in an environment with the required desktop workflow available, using the validated source and exact atlas as inputs and completing any desktop-specific checks. This repository's offline Work Pets reproduction commands do not satisfy or bypass that runtime requirement.

## ChatGPT Work: replacement completed

The original custom Bit was successfully created in ChatGPT Work on 2026-10-02. The retained published atlas is the exact upload snapshot from that creation.

Subsequent attempts to fetch the stored sheet returned HTTP 403, including explicitly authorized fresh-link retries after deselection and an app restart. Those attempts stopped; the denial was not bypassed. The replacement was built from retained, approved source, not a newly downloaded server sheet.

After the user explicitly selected the Pets app, the earlier authorized delete-and-replace request was completed there. The exact validated replacement atlas passed native preflight again, was uploaded as a new custom Bit, and was selected successfully. The old pet record and stored sheet were then deleted. A complete roster readback confirmed the replacement active and the old entry absent. Private lifecycle receipts are retained outside Git.

This was a new pet created from approved local source, not a successful retry of the denied old-sheet download. It does not resolve or substitute for the separate desktop installation requirement.

## Publication scope

Publishing the source branch does not deploy a pet. The repository contains artwork, offline rendering/validation tools and sanitized QA, not private pet IDs, Library IDs, signed URLs, installation records or credentials. None of its Python tools makes network requests or changes a pet selection.
