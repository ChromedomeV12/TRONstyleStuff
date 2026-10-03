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
