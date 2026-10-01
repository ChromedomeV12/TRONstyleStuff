# Shanghai TRON wallpapers

Use [outputs/shanghai-tron-uprising.png](outputs/shanghai-tron-uprising.png), the accepted 4704 × 3136 wallpaper. It combines the refined Uprising grade with 28% of the stronger building-color variation, keeping blue/cyan dominant. It is the final image previously called `shanghai-tron-uprising-subtle.png`, subsequently renamed; its pixels match that blend exactly.

![Accepted wallpaper preview](work/uprising-subtle-preview.png)

Suggested matching Windows accent: **#299DB5**. Earlier grades and the stronger building-color version remain in `outputs/` for comparison. JSON files record the original color checks; `work/` contains scripts and preview images.

## Reproducing grades

Install `requirements.txt` with Python. Scripts resolve paths relative to this directory. Original-photo stages require `inputs/source.jpg`; reference-based stages also require the files described in `inputs/README.txt`. The original third-party inputs and the generated NumPy pixel cache are excluded.

Scripts represent successive experiments, not a single automatic build. Inspect the input/output paths of the stage you want before running it. The accepted exported image is preserved without re-encoding during consolidation.

See [source and licensing notes](../PROVENANCE.md).
