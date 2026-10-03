# Deployment status

As of 2026-10-03:

- An existing custom Bit pet was successfully created on 2026-10-02. `assets/published/spritesheet.png` is the exact retained upload artifact for that creation.
- The user approved the source-only ±3° idle comparison on 2026-10-03. It is **approved, not deployed**.
- Fetching the current stored sheet returned HTTP 403 from an unexpired download link. One explicitly authorized retry after switching away from Bit used a fresh link through the same supported route and returned the same error. The attempts stopped; the denial was not bypassed. No replacement sheet, upload session or pet update was sent.
- The pet's selection was left unchanged. Private pet IDs, Library IDs, signed URLs and installation records are deliberately excluded from this repository.

Before deployment can resume, obtain the current stored sheet through the authorized workflow and verify its relationship to the retained source. Rebuild only the affected idle row where possible, preserve all unaffected states, rerun the applicable bundled QA and native preflight, and show the final encoded motion before mutation. Update the existing custom pet's stable identity; never create a duplicate as a repair. Preserve its active selection unless separately requested otherwise.

Repository publication does not deploy a pet. None of the included Python tools performs network requests or pet mutations.
