# Paper Repo: A Git-Native Protocol for Scientific Knowledge Production

A research program is not a sequence of documents. It is a repository. Papers are not the research — they are renders of the research at specific points on its timeline, shared with the scientific community so findings can be confirmed and knowledge can accumulate.

**Paper Repo** defines a protocol for managing scientific research as version-controlled repositories. The protocol optimizes the knowledge production process, not the paper. Individual papers are tagged releases — frozen snapshots forked to journals for community review — with automated compliance gates, attributed reviewer commits, and provenance chains that make the full research lifecycle machine-readable.

## Core Concept

| Level | Meaning |
|---|---|
| **Research program** | Repository — the single source of truth, evolving over time |
| **Paper** | Render of the research at a point on its timeline — a frozen snapshot, a communication event |
| **Fork** | Sharing that render with a journal for confirmation |
| **Publication** | Merge — the community's confirmation that the findings join the shared knowledge base |

This maps onto the same rendering problem pattern that appears across domains: a specification is rendered into an expression, which is then evaluated by observers. In SBT: brand specification → signals → perception cloud. In OST: organizational schema → operations → performance metrics. In Paper Repo: research repository → paper → community evaluation (peer review). Same structure, different substrates.

## The Problem

Scientific publishing routes knowledge production through administrative checkpoints: formatting manuscripts, uploading to portals, manually blinding, re-reviewing papers rejected elsewhere. These activities consume editorial and author labor without creating knowledge.

The root cause: the system treats a paper as a static document (a PDF) rather than a living repository with history, contributors, branches, and provenance.

## The Protocol

| Feature | What it does |
|---|---|
| **Research repository** | Every research program is a Git repo; papers are tagged releases with structured metadata (paper.yaml, CONTRIBUTORS.yaml, PROVENANCE.yaml) |
| **Fork-based submission** | A fork request to a journal creates a frozen, cryptographically linked fork |
| **Compliance gate** | Journal publishes `journal_spec.yaml`; validator checks compliance before fork request is processed |
| **Blinding as function** | Reviewer anonymization is automated per journal config, not manual |
| **Reviewer attribution** | Reviews are typed commits on branches — creating portable reviewer portfolios |
| **Provenance by design** | Every fork is irrevocably recorded; dual submission becomes structurally detectable |
| **Collections as users** | Journals, preprint servers, archives are collection users who curate forks |
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
python scripts/validate_paper.py --repo /path/to/paper --spec examples/journal-specs/journal_spec_jm.yaml
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
| [`examples/journal-specs/`](examples/journal-specs/) | Journal submission specs (machine-readable requirements) |
| [`examples/R13/`](examples/R13/) | Paper Spec paper — contributor attribution + fork history (Zenodo + QSS) |
| [`examples/R14/`](examples/R14/) | **This protocol's own paper** — full self-referential implementation (paper.md + paper.yaml + all artifacts) |

## Privacy: The Hash Is Always Public, the Content Need Not Be

Open science and confidentiality are not mutually exclusive. A commit hash is a tamper-evident fingerprint — publishing the hash establishes that the work in this exact form existed at this exact moment, signed by this exact author, without revealing what the work is.

This is **commit-reveal**: priority and provenance established immediately, content disclosure under the author's control.

| Disclosure mode | What is public | What stays private |
|---|---|---|
| Solo private + hash anchors | Commit hashes (timestamped + signed) | Full content until author chooses to release |
| Consortium shared private branch | Periodic hash anchors | Branch contents — visible only to members |
| Hybrid public-private repo | `paper.yaml`, references, public commit graph | `.wiki/`, raw data, draft branches |
| Embargoed disclosure | Hash at time *t* | Content until *t + n*; hash proves no editing during embargo |
| Standard open science | Everything | Nothing |

Years from now, in the event of a priority dispute, the researcher reveals the contents and any party can recompute the hash to verify the disclosed file matches the previously published anchor. Most academics assume git-native research forces them to choose between confidentiality and credit. Cryptographic commit-reveal gives them both.

For misconduct prevention, this is the structural alternative to centralized institutional databanks: a scientist's reputation is the verifiable history of their commits. There is no need to "report" misconduct at the moment of an employment transition — the misconduct, if it occurred, is visible at the granularity of the commit graph. Fabrication cannot retroactively edit a signed, hashed commit without breaking the chain.

## AI Traceability by Design

Git doesn't just track your work. It tracks your AI's work too.

Every AI-assisted edit in a paper repository becomes a commit with metadata: the tool used, the model version, and what changed. When Claude rewrites Section 3, that's a commit. When Gemini generates a figure, that's a commit. The contribution is recorded not because the author declared it on a form, but because the system recorded it.

This solves the AI disclosure problem that journals are currently addressing with honor-system checkboxes. In a paper repository, AI contribution is structurally transparent and auditable by construction. The `CONTRIBUTORS.yaml` file maps every contributor (human and AI) to their verified commit history.

## This Paper Eats Its Own Dogfood

The research paper proposing this protocol ([R14](examples/R14/paper.md)) is itself structured as a compliant paper repository. Its `paper.yaml` contains 7 typed claims with falsification conditions. Its `CONTRIBUTORS.yaml` lists 4 contributors (1 human + 3 AI tools). Its `PROVENANCE.yaml` will be populated as fork requests are made to venues.

## Relationship to Paper Spec

[Paper Spec](https://github.com/spectralbranding/paper-spec) defines WHAT a paper claims (`paper.yaml` schema).
Paper Repo defines HOW a paper is managed (repository structure, fork protocol, compliance gate).

They compose: `paper.yaml` is one file in the paper repository. Paper Spec validates the content; Paper Repo validates the process.

## Research Paper

Zharnikov, D. (2026u). Research as Repository: A Git-Native Protocol for Scientific Knowledge Production. Working Paper.

## Related

- [Paper Spec](https://github.com/spectralbranding/paper-spec) — Machine-readable standard for scientific claims
- [Spectral Brand Theory](https://spectralbranding.com) — The research program this protocol emerged from
- [Organizational Schema Theory](https://orgschema.com) — Test-driven business design (the OST value-stream lens informs this protocol)

## License

MIT
