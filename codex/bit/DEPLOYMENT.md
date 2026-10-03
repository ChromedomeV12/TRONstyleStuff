# Deployment status

As of 2026-10-03, the full replacement is **approved and validated, but not installed or activated**. `assets/replacement/spritesheet.png` contains the approved ±3° idle revision. The original atlas remains in `assets/published/` for comparison and recovery.

## Codex desktop: current requested target

The user's latest installation request names Codex desktop. Its bundled `hatch-pet` skill requires `load_workspace_dependencies` before running its scripts and explicitly says to stop when that runtime is unavailable. The creation session did not expose that tool, so desktop packaging and activation stopped. No desktop `pet.json` package was installed. The skill does not document a user-facing procedure that guarantees the missing tool will become available.

Do not substitute ChatGPT Work pet controls for this desktop target. Resume installation only in an environment with the required desktop workflow available, using the validated source and exact atlas as inputs and completing any desktop-specific checks. This repository's offline Work Pets reproduction commands do not satisfy or bypass that runtime requirement.

## ChatGPT Work: separate existing pet

The original custom Bit was successfully created in ChatGPT Work on 2026-10-02. The retained published atlas is the exact upload snapshot from that creation.

Subsequent attempts to fetch the stored sheet returned HTTP 403, including explicitly authorized fresh-link retries after deselection and an app restart. Those attempts stopped; the denial was not bypassed. The replacement was built from retained, approved source, not a newly downloaded server sheet. Native sprite-sheet preflight passed, but no replacement upload session, new pet record, deletion or activation followed. The existing Work pet remains untouched by replacement preparation.

These are distinct blockers: the desktop workflow lacks its mandated runtime tool; the previous Work stored-sheet download was denied. Resolving either one does not prove the other is resolved.

## Publication scope

Publishing the source branch does not deploy a pet. The repository contains artwork, offline rendering/validation tools and sanitized QA, not private pet IDs, Library IDs, signed URLs, installation records or credentials. None of its Python tools makes network requests or changes a pet selection.