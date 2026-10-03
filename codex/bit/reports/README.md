# Validation evidence

These are retained outputs from the published 2026-10-02 build. Absolute local paths were replaced with `original-build`; judgments, measurements and warnings were retained. They are historical evidence, not a claim that a fresh server sheet was downloaded.

- `standard-frames.json`: bundled extracted-frame inspection.
- `chroma-cleanup.json`: the one cleanup pass, preserving alpha.
- `direction-continuity.json` and `direction-semantics.json`: measured continuity and labeled visual observations.
- `blind-review-*.json` and `blind-validation.json`: all three isolated reviews and their actual strict-majority result.
- `motion-review.json`: independent standard-state review, including limitations and correction of a display-only false alarm.
- `quality.json`: bundled final quality result, with reviewed warnings.
- `local-reproduction.json`: current repository source/asset verification and exact published-atlas rebuild evidence. Source-strip parity includes the same transparent-RGB clearing used during strip composition.

`tools/verify.py` reruns the bundled structural, continuity and quality tools against the exact retained atlas, using the recorded semantic evidence for unchanged pixels. It also renders and compares both local idle profiles. New output is written to ignored `build/verification/` rather than rewriting this historical record. A new visual design or deployment requires fresh applicable review; local reproduction is not native-service preflight.

## Validated replacement

`replacement/` contains the 2026-10-03 full replacement's actual bundled structural/quality reports, native read-only preflight, frame inspection, one-pass chroma cleanup, shared idle registration, source/pixel provenance, exact-atlas GIF comparisons and visual observations. Local paths are normalized to `replacement-build` or `original-build`.

The look pixels are unchanged, so the historical three isolated reviews above remain the evidence. `replacement/blind-validation.json` is the bundled validator rerun over those existing verdicts, not a claim that new reviewers were used. `replacement/reproduction.json` records the independent repository rebuild and verification of this exact replacement.

These reports record pre-deployment validation. The replacement was subsequently created and activated in ChatGPT Work; private lifecycle receipts are kept outside Git. It remains uninstalled in Codex desktop. Native preflight and offline reproduction do not substitute for the separate desktop runtime or installation workflow.
