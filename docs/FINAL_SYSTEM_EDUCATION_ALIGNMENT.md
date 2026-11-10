# Final-system content-pack qualification — Ékole Pastorale

**Scope:** `FC-11` with source-compatible `ekole.content-pack/0.1` produced from **32** independent pedagogical Kristal units and a separate 3-unit witness/template verification set. The core engine is a separate neutral project; this repository does not publish or fork it.

## Derived state and reproducibility

The SmartDump code archive omits generated, git-ignored `build/v9` state snapshots that the owner projector deliberately verifies. This is **not** evidence that the canonical source was absent or that validation passed. To regenerate from the provided local Kristal tools **without publication or activation**:

```bash
python outils/rebuild_local_candidates.py --build
python outils/rebuild_local_candidates.py
PYTHONPATH=../ekole python -m unittest discover -s tests -v
```

The helper builds exactly 35 local candidates (32 course units + witness + two templates), verifies that `canon/` input hashes remain unchanged and outputs a report asserting `published=false`, `release_authorized=false`. The generated `build/v9` directories are deliberately **not bundled in the source-code patch**: consumers must regenerate and check them under their own exact toolchain.

## Ownership and release safety

The native pastoral Kristals remain `11.0.0-draft.3`-aligned source material. The projected `pack.json` and `cours/` are derived data, not a release authorization; `statut=projet_non_publie` and course status `maquette_non_approuvee` remain unchanged. Ékole Core now filters course bodies from its learner API when `publication_autorisee=false`. Theology, pedagogy, child safety and licensing review are all **separate** requirements before any learner/public publication.

The previously stale pastoral test is aligned with the current generated pack status, and explicitly imports the real sibling Ékole Core rather than importing a nonexistent local `launcher.py`. The source archive remains standalone except for the explicitly declared cross-owner integration test.
