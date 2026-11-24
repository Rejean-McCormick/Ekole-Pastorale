# Testing and validation — local educational prototype

**Status:** locally maintained testing guide (2026-11-23). This is **not** a recovered `wiki/Testing-and-Validation.md` page, and passing checks **does not** grant public, student-facing or ecclesiastical publication permission.

## Preconditions

- Python **3.10+**; run commands from the `ecole-pastorale/` repository root.
- `kristals/` (32 course workspaces), the separate witness workspace and the two template workspaces must be present.
- A source ZIP may omit derived `build/v9/state-snapshot.json` files. A failed test caused by their absence is not evidence that the canonical input is missing.
- The neutral sibling `../ekole/launcher.py` is required **only** for the cross-repository integration test and Core loading checks.

## Safe local sequence

```bash
python outils/rebuild_local_candidates.py --build
python outils/rebuild_local_candidates.py
python -m unittest discover -s tests -v
```

The first helper invocation regenerates and inspects 35 **local, unpublished** v9 candidate states (32 units, one witness, two templates); the second confirms that the derived states exist. Neither runs a publisher. The helper compares hashes of `canon/` before and after rebuilding; it must refuse a mutation. An optional integration test is skipped when the sibling Core is missing; report that skip rather than calling the integration qualified.

Reproject only after a valid local state exists:

```bash
python outils/projeter_ekole.py
python -m unittest discover -s tests -v
python demarrer_pastorale.py --verifier
```

The final Core check needs the real sibling `ekole/` repository. **Never execute `--edition` or a publishing workflow merely to test compatibility.**

## What the tests establish

- `tests/test_depot_frere.py` checks the derived pack, the **32** teacher courses, the **32** learner projections, **7** pathways and the exact regeneration comparison, including `visuels_themes`.
- `curriculum/visuels-themes.json` is the maintained input for the **12** style definitions (default `aquarelle`); the projector refuses an invalid or missing default.
- `tests/test_pastorale.py` is a permissive Core compatibility test (at least 12 courses and 3 pathways), not a complete 32/7 qualification.
- These checks do not establish theological, safeguarding, pedagogical, licensing, or public-release approval.

If tests fail, keep the current source and derived outputs intact for diagnosis; do not remove `visuels_themes` from `pack.json` simply to make a generated comparison pass.
