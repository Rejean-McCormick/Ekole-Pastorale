# Ekole Pastorale

**A Catholic pastoral education content repository for the independent, religion-neutral Ekole Core, powered by Kristal Framework v11.**

> **Status:** Local educational prototype, version **0.4** (content baseline **0.3**). **Not approved for public or ecclesiastical publication.** The learner-facing material and teacher guides require theological, pedagogical, safeguarding, and licensing review.

Ekole Pastorale provides an extensible Catholic curriculum rooted in Scripture and the wider Catholic tradition: the Church Fathers and Doctors, saints, virtues, Catholic social teaching, and pastoral practice. It also examines miracles and the mysteries of faith in their own dedicated learning branch.

**Ekole Core remains entirely neutral and standalone.** This repository contains the content and launch integration; it does not fork, vendor, or modify the Ekole engine. Its canonical educational sources are independent Kristals, projected into the `ekole.content-pack/0.1` format consumed by Core.

## At a glance

| Component | Included |
| --- | --- |
| Courses | **32**: 20 in *Message and Living Tradition*, 12 in *Miracles and Mysteries of Faith* |
| Learning pathways | **7**, including thematic and introductory pathways |
| Framework | Kristal **11.0.0-draft.3** |
| Archetype extensions | Candidate **ARK-20** (federated learning unit) and **ARK-21** (witness, virtues, and sources) |
| Canonical workspaces | **32** learning-unit Kristals and **1** Saint Francis of Assisi witness Kristal |
| Reference bridge | Historical A-Kristal-Catho inventory: **38** Doctors of the Church and **138** source references, pinned by artifact hashes; **not yet migrated to v11** |
| Teaching language | **French (fr-CA)**; this README and the GitHub Wiki are in English |
| Publication status | **Draft / not approved** |

## Quick start

**Requirements:** Python 3.10 or later and a compatible copy of [Ekole Core](#repository-layout). No third-party Python package is required to launch the Core provided with this project. Development and optional schema-validation tools may have additional dependencies.

Place the repositories side by side. Keep the directory name `ecole-pastorale` exactly as shown; it is the content-pack identifier used by the launcher.

```text
workspace/
├── ekole/             # Standalone, content-neutral engine
├── ekole-quebec/      # Optional, separate education content
└── ecole-pastorale/   # This repository
```

**Windows:** double-click `LANCER_PASTORALE.bat` from `ecole-pastorale/`.

**macOS / Linux:**

```bash
cd ecole-pastorale
./lancer-pastorale.sh
```

Before starting the servers, you can validate content loading:

```bash
python3 demarrer_pastorale.py --verifier
```

The default learner portal runs at **http://127.0.0.1:21153/**. The teacher/editor application uses port **21154**, and the launcher displays its private access URL in the terminal. Keep the terminal open while the servers run; use **Ctrl+C** to stop them.

To launch without automatically opening a browser:

```bash
python3 demarrer_pastorale.py --sans-navigateur
```

To select a different Core checkout or custom ports:

```bash
python3 demarrer_pastorale.py --core ../ekole --port 8875 --port-editeur 8876
```

The launcher also accepts `--sans-editeur` (learner portal only), `--edition` (enable local editor changes), and the `EKOLE_CORE_PATH` environment variable. The editor is read-only by default.

For full setup, Windows commands, and troubleshooting, see [Getting Started](docs/INSTALLATION_REPO_FRERE.md).

## Two independent learning branches, one Catholic identity

The curriculum deliberately distinguishes **what Jesus and the Catholic tradition teach** from **the accounts of miracles and the mysteries of faith**. A learner can follow the first branch without being required to complete or assent to the second branch first. This is a **pedagogical distinction**, not a denial of Catholic beliefs.

1. **Message and Living Tradition (20 courses):** biblical reading, love, forgiveness, justice, poverty and solidarity, prayer, the Doctors of the Church, saints and virtues, social teaching, and responsible pastoral accompaniment.
2. **Miracles and Mysteries of Faith (12 courses):** Gospel signs, healings, Cana, the feeding of the multitude, the virginal conception, Christ's Resurrection, witness accounts, attributed miracles, faith and science, and ecclesial discernment.

The Resurrection is treated as central to Catholic faith; it is not presented as interchangeable with a later devotional miracle claim. Textual, historical, theological, and pastoral registers are kept distinguishable. Both branches permit thoughtful discussion and respect for learners who have questions or doubts.

All 32 courses are currently structured **teaching drafts**, not a complete accredited curriculum. See the [Curriculum](docs/CURRICULUM.md) and [Editorial Principles](docs/GOUVERNANCE_ET_ETHIQUE.md).

## Repository layout

```text
ecole-pastorale/
├── README.md                      # English repository overview
├── docs/                          # Local curriculum, governance, installation and architecture notes
├── pack.json                      # Ekole content-pack manifest (generated)
├── curriculum/visuels-themes.json # Maintained source for 12 visual styles
├── cours/                         # 32 teacher-oriented course JSON files (generated)
├── publications/eleve/            # 32 learner views (generated, not approved)
├── kristals/                      # 32 canonical Kristal v11 course workspaces
├── kristals-temoins/              # Witness Kristal (Saint Francis of Assisi)
├── extension-arketype/            # Candidate ARK-20 / ARK-21 overlays and installers
├── federation/                    # Historical Catho reference bridge and candidates
├── curriculum/                    # Derived curriculum index
├── contracts/                     # Experimental native editorial JSON Schemas
├── outils/                        # Projector, catalog generator, and reference audit
├── tests/                         # Integration and repository tests
├── docs/                          # Internal design and historical working notes
├── demarrer_pastorale.py          # Launches the sibling Ekole Core
├── LANCER_PASTORALE.bat           # Windows launcher
└── lancer-pastorale.sh            # macOS / Linux launcher
```

### Sources of truth versus generated outputs

- **Canonical teaching content:** `kristals/<slug>/canon/domain/pedagogie/unite.json`, together with each Kristal's registered v11 semantic resources and its v9 state commitment.
- **Witness content:** `kristals-temoins/francois-assise/`, maintained independently of the course on Saint Francis.
- **Visual style source:** `curriculum/visuels-themes.json` defines the 12 visual styles and their default, separately from the canonical teaching material. The projector validates and includes this configuration in the generated `pack.json`.
- **Generated Ekole projection:** root `pack.json`, `cours/`, `publications/eleve/`, and `provenance-derivation.json`. **Do not hand-edit these generated files.**
- **Historical reference bridge:** `federation/catho-legacy-bridge.json` links exact legacy artifact hashes. It is not proof of v11 identity equivalence.

For the design boundaries, see [Architecture](docs/DECISIONS_ARCHITECTURE.md), [Kristal v11](docs/MIGRATION_CATHO_V11.md), and [Arketypes](docs/MIGRATION_CATHO_V11.md).

## Validation and regeneration

Rebuild the derived local v9 states first when working from a source snapshot (which can omit `build/v9/`), then run the tests:

```bash
python3 outils/rebuild_local_candidates.py --build
python3 outils/rebuild_local_candidates.py
python3 -m unittest discover -s tests -v
```

The sibling Ekole Core integration test is skipped when Core is unavailable; that skip is not evidence of integration success. Tests do not authorize publication. See [Testing and Validation](docs/TESTING_AND_VALIDATION.md).

Check that the sibling Core can load the exported pack:

```bash
python3 demarrer_pastorale.py --verifier
```

Regenerate Ekole-derived artifacts from the existing, validated Kristal states:

```bash
python3 outils/projeter_ekole.py
```

**When the canonical content of a course changes,** first review the edits and rebuild its v9 state commitment; then run the projector. Example for `lire-bible`:

```bash
python3 kristals/lire-bible/tools/kristal.py check-v11 kristals/lire-bible
python3 kristals/lire-bible/tools/kristal.py check kristals/lire-bible
python3 kristals/lire-bible/tools/kristal.py build-v9 kristals/lire-bible
python3 outils/projeter_ekole.py
python3 demarrer_pastorale.py --verifier
```

The projector is designed to reject changed canonical files that no longer match their pinned build state. Successful technical checks **do not** mean the material has been approved doctrinally or cleared for release.

See [Authoring and Projection](docs/DECISIONS_ARCHITECTURE.md) and [Testing and Validation](docs/TESTING_AND_VALIDATION.md).

## Publication, safety, and limitations

- **No ecclesiastical approval is claimed.** Appropriate ecclesial review is required if the school seeks an official Catholic mandate or recognition.
- **Do not publish learner views yet.** They are explicitly marked as unapproved prototypes; the teacher-only rubric is not included in learner exports.
- **Safeguarding is mandatory:** no coerced disclosure, no pressure to forgive abuse, no substitution of religious claims for medical care, and no misleading claim about the recognition of a miracle.
- **References and rights need review:** verify Scriptural citations, translations, historical sources, biographies, third-party images, and applicable licenses.
- **Catho migration is incomplete:** the 38-Doctor/138-reference inventory is historical and hash-pinned, not an automatically trusted semantic crosswalk.
- **Repository licensing:** no repository-level license was provided in this snapshot; do not assume permission to redistribute its contents.

Read [Governance and Safeguarding](docs/GOUVERNANCE_ET_ETHIQUE.md) before editing, teaching, or publishing.

## Documentation

The historical set of 11 local `wiki/*.md` pages is **not present in the 2026-11-23 code snapshot**. New [documentation home](docs/DOCUMENTATION_HOME.md), [testing guide](docs/TESTING_AND_VALIDATION.md), and [Wiki publication policy](docs/WIKI_PUBLICATION_POLICY.md) are maintained as local replacements for three missing topics—not recovered copies of the old Wiki. See [Wiki gaps and source guide](docs/WIKI_GAPS.md); an external GitHub Wiki has not been verified or published by this overlay.

## Relationship to Ekole

**Ekole Core + this content repository = Ekole Pastorale.**

Ekole Core is a general-purpose learning platform and can also load other content packs (such as Ekole Québec). The Catholic curriculum, branch definitions, citations, and saints belong to this content repository and its Kristals, **not** to the Core engine. No Catholic-specific code must be introduced into Ekole Core to run this school.
## Final-system integration reference (Branch 06)

The [English education-boundary specification](docs/FINAL_SYSTEM_EDUCATION_ALIGNMENT.md) describes implemented safety checks, local test instructions, cross-owner responsibilities and still-unapproved interfaces. It does **not** assert a deployed Orgo/Moodle workflow.
