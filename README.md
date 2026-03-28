# Paper Repo: A Git-Native Protocol for Scientific Publishing

A paper is not a document. It is a repository.

**Paper Repo** defines a protocol for managing scientific papers as version-controlled repositories — with fork-based submission, automated compliance gates, attributed reviewer commits, and provenance chains that make the full research lifecycle machine-readable.

## The Problem

Scientific publishing routes knowledge production through administrative checkpoints: formatting manuscripts, uploading to portals, manually blinding, re-reviewing papers rejected elsewhere. These activities consume editorial and author labor without creating knowledge.

The root cause: the system treats a paper as a static document (a PDF) rather than a living repository with history, contributors, branches, and provenance.

## The Protocol

| Feature | What it does |
|---|---|
| **Paper repository** | Every paper is a Git repo with structured metadata (paper.yaml, CONTRIBUTORS.yaml, PROVENANCE.yaml) |
| **Fork-based submission** | Submitting to a journal creates a frozen, cryptographically linked fork |
| **Compliance gate** | Journal publishes `journal_spec.yaml`; validator checks compliance before fork is accepted |
| **Blinding as function** | Reviewer anonymization is automated per journal config, not manual |
| **Reviewer attribution** | Reviews are typed commits on branches — creating portable reviewer portfolios |
| **Provenance by design** | Every fork is irrevocably recorded; dual submission becomes structurally detectable |
| **Collections as users** | Journals, preprint servers, archives are users who accept forks into curated collections |
| **Hybrid submission** | Git-linked submission coexists with traditional upload (like ORCID linking) |
| **Federation** | No central platform — any institution runs its own server |

## Repository Structure

A compliant paper repository:

```
paper/
  paper.md                  # Manuscript source (Markdown, LaTeX, or Quarto)
  paper.yaml                # Claims, methods, falsification conditions (Paper Spec)
  CONTRIBUTORS.yaml         # Contributor roles verified against commit history
  PROVENANCE.yaml           # Fork history, submission records
  DATA_MANIFEST.yaml        # Links to external data archives (DOI + checksum)
  LICENSE                   # Content license (CC-BY-4.0 recommended)
  figures/                  # Generated figures
  analysis/                 # Code, scripts, notebooks
```

See [Paper Spec](https://github.com/spectralbranding/paper-spec) for the `paper.yaml` schema.

## Quick Start

### Validate a paper against a journal spec

```bash
python scripts/validate_paper.py --repo /path/to/paper --spec examples/journal_spec_jm.yaml
```

Output:
```
Validating against: Journal of Marketing
Repository: /path/to/paper
------------------------------------------------------------
  [OK]   Manuscript: paper.md
  [OK]   Word count: 9,217 (limit: page-based)
  [OK]   Abstract: 187 words (max: 200)
  [FAIL] References: self-citation 27.3% > maximum 25%
  [OK]   Statement: ai_disclosure
------------------------------------------------------------
Results: 5 passed, 1 failed
Submission gate: BLOCKED — fix failures before submitting
```

### Create a paper repository

```bash
mkdir my-paper && cd my-paper && git init
# Copy template files:
cp /path/to/paper-repo/templates/* .
# Edit paper.md, paper.yaml, CONTRIBUTORS.yaml
# Validate: python validate_paper.py --repo . --spec journal_spec.yaml
```

## Schemas

| Schema | Purpose |
|---|---|
| [`schemas/journal_spec.yaml`](schemas/journal_spec.yaml) | Journal submission requirements (46 field categories from 15 real journals) |
| [`schemas/paper_repo.yaml`](schemas/paper_repo.yaml) | Paper repository structure specification |

## Examples

| Example | What it demonstrates |
|---|---|
| [`examples/journal_spec_jm.yaml`](examples/journal_spec_jm.yaml) | Real Journal of Marketing spec from actual submission |
| [`examples/R13_CONTRIBUTORS.yaml`](examples/R13_CONTRIBUTORS.yaml) | Contributor attribution from a real paper |
| [`examples/R13_PROVENANCE.yaml`](examples/R13_PROVENANCE.yaml) | Fork history: Zenodo preprint + QSS submission |
| [`examples/R14/`](examples/R14/) | **This protocol's own paper** — self-referential implementation |

## This Paper Eats Its Own Dogfood

The research paper proposing this protocol ([R14](examples/R14/paper.md)) is itself structured as a compliant paper repository. Its `paper.yaml` contains 7 typed claims with falsification conditions. Its `CONTRIBUTORS.yaml` lists 4 contributors (1 human + 3 AI tools). Its `PROVENANCE.yaml` will be populated as the paper is submitted to venues.

## Relationship to Paper Spec

[Paper Spec](https://github.com/spectralbranding/paper-spec) defines WHAT a paper claims (`paper.yaml` schema).
Paper Repo defines HOW a paper is managed (repository structure, fork protocol, compliance gate).

They compose: `paper.yaml` is one file in the paper repository. Paper Spec validates the content; Paper Repo validates the process.

## Research Paper

Zharnikov, D. (2026u). Paper as Repository: A Git-Native Protocol for Scientific Publishing. Working Paper.

## Related

- [Paper Spec](https://github.com/spectralbranding/paper-spec) — Machine-readable standard for scientific claims
- [Spectral Brand Theory](https://spectralbranding.com) — The research program this protocol emerged from
- [Organizational Schema Theory](https://orgschema.com) — Test-driven business design (the OST value-stream lens informs this protocol)

## License

MIT
