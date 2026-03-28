# Research as Repository: A Git-Native Protocol for Scientific Knowledge Production

**Dmitry Zharnikov**

Working Paper — March 2026

---

## Abstract

Scientific papers are written, submitted, reviewed, revised, and published through a pipeline that has no specification, no version control, no contributor traceability, and no machine-readable provenance. This is a conceptual protocol proposal, not a report of an implemented system. This paper proposes a protocol that treats every research paper as a version-controlled repository — the single source of truth (SSOT) for its content, its contributor history, and its evaluation lifecycle. The protocol introduces four structural innovations: (1) fork-based submission, where submitting a paper to a journal creates a cryptographically linked frozen snapshot that the editor owns and the author cannot modify; (2) blinding-as-function, where reviewer anonymization is a configurable system property rather than a manual author action; (3) provenance-by-design, where the existence of every fork is permanently recorded in the author's repository and visible to all subsequent forks; and (4) collections-as-users, where preprint servers, journals, and institutional repositories are registered users on a shared platform who accept frozen forks into curated collections. The protocol makes the full research lifecycle — from first draft through peer review through publication through post-publication correction — machine-readable, contributor-traceable, and structurally transparent. When combined with the Paper Spec standard (Zharnikov, 2026t), which specifies what a paper claims, the repository protocol specifies how the paper was built, evaluated, and decided upon. Together, they make the research pipeline auditable by both humans and machines.

**Keywords**: scientific publishing, version control, peer review, research infrastructure, open science, provenance, specification

---

## 1. Introduction

### 1.1 The Document Assumption

The global scientific publishing system processes approximately 3 million papers per year (UNESCO, 2021) through a pipeline built on a single assumption: a paper is a document. A PDF file. A static artifact transmitted from author to editor to reviewer to publisher. Every tool in the pipeline — manuscript submission portals, editorial management systems, reviewer interfaces, typesetting workflows — treats the paper as an opaque binary object that moves between mailboxes.

This assumption was adequate when papers were physically printed and mailed. It is now the binding constraint on every reform the scientific community has attempted in the past two decades.

Open access reforms change *who can read* the document. They do not change the document. Preprint servers change *when* the document becomes available. They do not change its structure. Registered reports change *what sequence* the document follows. They do not change how it is tracked. Post-publication review adds commentary *about* the document. It does not integrate with the document's own history.

Each reform addresses one dimension of the publishing problem while leaving the document assumption intact. The result is a system that has been incrementally improved on six dimensions simultaneously — access, timing, sequence, commentary, data sharing, reproducibility — without any reform touching the structural foundation that constrains all of them.

Software engineering faced the same problem in the 1990s. Source code was treated as a collection of files transmitted between developers via email, FTP, or shared drives. Every collaboration problem — tracking changes, attributing contributions, managing parallel versions, reverting errors — was solved ad hoc. The solution was not incremental improvement of file-sharing tools. It was a structural reconception: source code is not a collection of files. It is a *repository* — a versioned, branched, contributor-attributed, cryptographically auditable history of every change ever made.

Git (Torvalds, 2005) implemented this reconception. Within a decade, it became the universal infrastructure for collaborative software development. GitHub (2008) added the social and collaboration layer: forking, pull requests, issue tracking, and visibility. The combination transformed software from an opaque craft practice into a transparent, auditable, contributor-traceable engineering discipline.

This paper proposes the same structural reconception for scientific papers. A paper is not a document. It is a repository. The submission process is not a file transfer. It is a fork. Peer review is not an email exchange. It is a set of attributed commits on a review branch. Publication is not a format conversion. It is a tagged release with a minted DOI.

### 1.2 What the Protocol Replaces

The current pipeline has five structural gaps that are difficult to address within the document paradigm:

**Gap 1: No version history.** A submitted manuscript has no auditable record of how it was written. The editor sees a finished product. The twenty drafts, the deleted sections, the data re-analyses, the contributor who rewrote Section 4 — all invisible. When questions arise about research integrity, the only evidence is the authors' word and whatever files happen to be on their hard drives.

**Gap 2: No contributor traceability.** CRediT (Contributor Roles Taxonomy) added contributor roles to published papers in 2014. But CRediT is a self-reported annotation attached to the final document. It has no connection to the actual work. There is no mechanism to verify that the person listed as "Methodology" actually wrote the methods section. The contribution record is a claim, not a proof.

**Gap 3: No submission provenance.** When an author submits to Journal A, Journal B has no way to know. Dual submission policies rely entirely on author honesty. When a paper is rejected by three journals and accepted by the fourth, the fourth journal's editor has no access to the prior reviews. The same paper is re-reviewed from scratch at each venue — a massive duplication of expert labor.

**Gap 4: No review attribution.** Peer reviewers contribute substantive intellectual work — identifying errors, suggesting improvements, catching methodological flaws. Their contributions are acknowledged in a single generic sentence ("We thank the anonymous reviewers") and then erased. A reviewer who saves a paper from a fatal statistical error receives the same credit as one who submits a two-sentence review: none.

**Gap 5: No machine interface.** The entire pipeline is human-readable only. A PDF cannot be queried, diff'd, branched, or programmatically analyzed without lossy conversion. AI tools that could assist with literature review, consistency checking, or cross-paper analysis must first solve the extraction problem — converting unstructured text back into structured data — before doing any useful work.

The protocol proposed here closes all five gaps by replacing the document assumption with a repository assumption. The paper becomes a Git repository. Submission becomes a fork. Review becomes a branch. Publication becomes a release. Every operation is versioned, attributed, and machine-readable by construction.

### 1.3 Relationship to Prior Work

The Paper Spec standard (Zharnikov, 2026t) addresses Gap 5 by defining a machine-readable YAML companion file (`paper.yaml`) that captures what a paper claims, what would falsify those claims, and what the paper depends on. Paper Spec is the *specification layer* — it declares the paper's epistemic content in structured form.

**Paper Spec in brief.** The Paper Spec standard (Zharnikov, 2026t) defines a YAML companion file (`paper.yaml`) with five structural elements: (1) typed claims with unique identifiers and dependency links; (2) methodology description with reproducibility requirements; (3) acceptance criteria — what would confirm each claim and, critically, what would falsify it; (4) a dependency graph linking claims to prior work with criticality flags; and (5) submission history tracking venue, decision, and revision scope. The standard is published as an open repository with 20 worked examples from published research (github.com/spectralbranding/paper-spec). The present protocol treats `paper.yaml` as one file in the repository structure; Paper Spec defines its internal schema.

The present protocol is the *process layer* — it specifies how the paper is built, submitted, reviewed, and published. Paper Spec and Research-as-Repository compose: `paper.yaml` travels with the repository, is versioned alongside the manuscript, and is included in every fork. Together, they make both the content and the lifecycle of a paper fully machine-readable.

The Registered Reports format (Chambers, 2013) addresses the sequence problem by splitting peer review into pre-data and post-data stages. The present protocol subsumes Registered Reports as a special case: a Stage 1 submission is a fork at a specific commit; Stage 2 is a subsequent fork from a later commit in the same repository. The fork chain records the two-stage structure automatically.

DORA (San Francisco Declaration on Research Assessment, 2012), the Leiden Manifesto (Hicks et al., 2015), and CoARA (Coalition for Advancing Research Assessment, 2022) all advocate for multi-dimensional research evaluation. The present protocol provides the infrastructure that makes multi-dimensional evaluation tractable: when every contribution, every review, and every decision is recorded in structured form, evaluation can query specific dimensions rather than collapsing to scalar proxies.

### 1.4 The Value Stream: Knowledge Development as the Core Process

Existing reform proposals — and the platforms that implement them — share a common limitation: they optimize individual stations on the publishing production line without examining the production line itself.

Manubot (Himmelstein et al., 2019) improves authoring. COAR Notify improves cross-platform notification. ORKG (Auer, 2019) improves indexing. Signposting improves machine discovery. Each addresses one gap. None asks the structural question: *what is the value stream of scientific knowledge production, and which activities on the production line are value-creating versus waste?*

Lean manufacturing (Ohno, 1988) distinguishes between value-creating activities (those the customer would pay for) and muda (waste — activities that consume resources but do not create value). Applied to scientific publishing:

**Value-creating activities** (the knowledge production process):
- Formulating hypotheses
- Designing experiments and analyses
- Collecting and analyzing data
- Writing arguments and interpretations
- Peer evaluation of claims (the intellectual substance of review)
- Integrating new knowledge into the existing corpus

**Non-value-creating activities** (administrative process around the value stream):
- Formatting manuscripts to journal specifications
- Uploading files through submission portals
- Manually blinding manuscripts
- Re-reviewing papers rejected elsewhere (duplicate expert labor)
- Converting between file formats (LaTeX to DOCX to JATS XML to PDF)
- Tracking submission status through email
- Manually entering metadata into multiple platforms
- Negotiating copyright transfer agreements

In many disciplines and at many journals, the current system routes the value stream *through* the administrative process. A researcher cannot share a finding with the community without first navigating formatting requirements, submission portals, and editorial management systems that were designed for publisher convenience, not knowledge flow. The administrative burden is not adjacent to the value stream — it is woven into it, forcing every knowledge-creating act to pass through non-value-creating checkpoints.

The Research-as-Repository protocol restructures this relationship. The value stream flows continuously in the author's repository: writing, analyzing, versioning, collaborating. The administrative functions — submission, blinding, review assignment, publication, indexing — are *services that operate on the repository* rather than *checkpoints the repository must pass through*. A fork is a service call, not a format conversion. Blinding is a function, not a manual task. Publication is a tag, not a production pipeline.

This is the Organizational Schema Theory (OST) principle applied to science: specify the process first, then derive the organizational structure from the process — not the other way around (Zharnikov, 2026i). This process-before-structure principle has antecedents in business process reengineering (Hammer & Champy, 1993), Lean thinking (Womack & Jones, 1996), and service-oriented architecture. OST formalizes it for organizational design; the present protocol applies it to scholarly communication. Current scientific publishing derives its processes from its organizational structure (journals define formats, timelines, and workflows; researchers conform). The protocol inverts this: the knowledge development process defines the requirements; journals, preprint servers, and review systems are services that fulfill those requirements.

## 1.5 Related Work

Several platforms and standards address subsets of the gaps identified above. None integrates all five into a unified protocol.

| System | Version control | Fork-based submission | Compliance gate | Reviewer attribution | Provenance chain | Collections as users | Adoption level | Key limitation |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| Manubot (Himmelstein et al., 2019) | Full (Git-native) | No | No | No | No | No | ~500 papers | Authoring only, no submission/review |
| JOSS (Katz et al., 2018) | Full (GitHub) | Yes (PR-based) | Partial (checklist) | Yes (GitHub handles) | No | No | ~3,000 papers | Software papers only |
| Octopus.ac (Freeman, 2021) | Partial (platform) | No | No | Yes (reviews as publications) | Partial (linked modules) | No | Pilot (2022-) | Proprietary platform, not Git-native |
| OJS/PKP (Willinsky, 2005) | No | No | Partial (checklist) | No | No | No | 25,000+ journals | No version control, no structured review |
| COAR Notify | No | No | No | No | Partial (notifications) | Partial (cross-platform) | Pilot (2023-) | Notification only, no manuscript management |
| Signposting | No | No | No | No | No | Partial (typed links) | Growing adoption | Discovery only, no workflow |
| CryptSubmit (Gipp et al., 2017) | No | No | No | No | Yes (blockchain) | No | Prototype (2017) | Timestamping only, no full lifecycle |
| PubPub (MIT Media Lab) | Partial (web-native) | No | No | No | Partial (versions) | No | ~200 communities | Web-native, not Git-native |
| **This protocol** | **Full (Git-native)** | **Yes** | **Yes (CI/CD)** | **Yes (typed commits)** | **Yes (fork chain)** | **Yes** | Proposal | No implementation yet |

Manubot is the closest predecessor for the authoring layer — it implements Git-native collaborative writing with CI/CD rendering (Himmelstein et al., 2019). The present protocol extends this pattern from authoring to the full submission-review-publication lifecycle. JOSS implements review-as-GitHub-issues for software papers; the present protocol generalizes this to all disciplines with structured reviewer commits rather than free-form issue comments. Octopus decomposes papers into modular linked units with open review — sharing the modular philosophy but using a proprietary platform rather than Git repositories. Overlay journals (e.g., Discrete Analysis on arXiv) already implement a lightweight version of "collections as users" by curating papers hosted on preprint servers.

The protocol's contribution is not any single feature but the integration: a unified Git-native lifecycle where authoring, compliance, submission, blinding, review, provenance, and publication are operations on a single versioned repository.

---

## 2. The Protocol

The protocol maps the scientific publishing lifecycle onto a CI/CD (Continuous Integration / Continuous Delivery) pipeline — the same architecture that transformed software from artisanal craft to engineered discipline. In software CI/CD, every code change triggers automated validation, testing, and deployment. In the paper protocol, every stage of the knowledge lifecycle triggers analogous automated operations:

```
AUTHOR REPO (Continuous Integration)
    |
    |-- commit: writing, analysis, revision
    |   → CI: paper.yaml schema validation
    |   → CI: reference completeness check
    |   → CI: figure quality verification
    |   → CI: internal consistency (claims match data)
    |
    |-- fork request to journal (Delivery Gate)
    |   → GATE: journal_spec.yaml compliance
    |   → GATE: blinding automation
    |   → GATE: provenance chain verification
    |   → GATE: AI pre-submission advisory (scope, novelty, coverage)
    |   |
    |   PASS → fork created, enters review pipeline
    |   FAIL → author sees exact failures, fixes locally, retries
    |
    |-- review pipeline (Continuous Review)
    |   → reviewer branches created
    |   → commits: structured review comments
    |   → editorial merge: decision commit
    |
    |-- acceptance (Release)
    |   → tagged release with DOI
    |   → badge from journal collection
    |   → provenance record closed
    |   → AI-native index updated (ORKG, Semantic Scholar)
    |
    |-- post-publication (Continuous Monitoring)
        → dependency alerts (cited paper retracted/updated)
        → correction commits (errata as patches)
        → community forks (post-publication review)
```

Each stage has automated checks (the CI), human judgment points (the review), and structural artifacts (the provenance chain). The protocol does not automate science — it automates a significant fraction of the administrative overhead that currently consumes editorial and author labor, so that human attention is reserved for the intellectual work that only humans can do.

### 2.1 The Paper Repository

A paper repository is a Git repository with the following structure:

```
paper/
  paper.md              # Manuscript (Markdown SSOT)
  paper.yaml            # Paper Spec (claims, methods, dependencies)
  data/                 # Data files, analysis scripts
  figures/              # Generated figures
  CONTRIBUTORS.yaml     # Contributor roles (verified, not self-reported)
  PROVENANCE.yaml       # Fork history, submission records
  LICENSE               # Content license
  .paperrc              # Repository configuration
```

The manuscript (`paper.md`) is the single source of truth. All renderings — PDF, DOCX, HTML, JATS XML — are generated from it. The repository contains the generating function, not the rendered output.

The protocol does not mandate Markdown specifically. Any plain-text, diff-friendly format serves as the SSOT: Markdown, LaTeX, Quarto, or R Markdown. The essential requirement is that the source format is version-controllable (plain text, not binary) and renderable to multiple outputs. Fields that predominantly use LaTeX (physics, mathematics) or Word (biomedical, humanities) would require either format bridging tools or a GUI abstraction layer that presents the Git operations through a familiar editing interface — analogous to how GitHub Desktop made Git accessible to non-engineers.

JATS XML (Journal Article Tag Suite) is the dominant machine-readable format for published articles. The protocol does not replace JATS — it generates JATS as one rendering output from the repository source. The submission gate (Section 2.3) can include JATS validation as a compliance check. The relationship is: the repository stores the source; JATS is one of several delivery formats the CI pipeline produces.

**The two-layer architecture: text in Git, data in archives.** Scientific papers across all disciplines produce two categories of artifacts: text-based artifacts (manuscripts, code, analysis scripts, small structured data) and binary/large artifacts (microscopy images, genomic sequences, medical imaging, satellite data, audio recordings, simulation outputs). Git handles the first category natively. It handles the second category poorly — storing full copies of every version of every binary file makes repositories impractically large.

The protocol adopts the same architecture that software engineering uses for code and assets: the repository stores the text layer; large data lives in linked external archives.

```
Paper repository (Git — text layer)
    paper.md / paper.tex         Manuscript source
    paper.yaml                   Claims, methods, dependencies
    analysis/                    Code, scripts, notebooks
    figures/                     Generated figures (SVG, small PNG)
    CONTRIBUTORS.yaml            Contributor roles
    PROVENANCE.yaml              Fork history
    DATA_MANIFEST.yaml           Links to external data

External data archives (linked by DOI)
    Zenodo, Dryad, Figshare      General-purpose
    GenBank                      Genomic sequences
    PDB                          Protein structures
    EMPIAR                       Cryo-EM maps
    Dataverse                    Social science datasets
    PANGAEA                      Earth science data
```

`DATA_MANIFEST.yaml` in the repository declares every external data dependency with its DOI, checksum, and access conditions:

```yaml
data_manifest:
  - id: "microscopy-dataset"
    description: "Confocal microscopy images, 47 samples"
    archive: "Zenodo"
    doi: "10.5281/zenodo.XXXXXXX"
    size_gb: 12.4
    format: "TIFF (16-bit, 2048x2048)"
    checksum_sha256: "a1b2c3..."
    access: public

  - id: "patient-records"
    description: "De-identified clinical trial data, N=340"
    archive: "Dryad"
    doi: "10.5061/dryad.XXXXXXX"
    size_gb: 0.3
    format: "CSV"
    checksum_sha256: "d4e5f6..."
    access: restricted    # requires DUA
```

This separation is not a limitation of the protocol — it is the correct architecture. The Zenodo-GitHub integration already implements this pattern: code in GitHub, data in Zenodo, linked by DOI. The protocol formalizes the linkage with checksums and access metadata so that the data manifest is part of the reproducibility chain.

For figures, the protocol favors generated figures: analysis scripts in the repository produce figures from data at build time, the same way CI/CD generates build artifacts from source code. A figure that is generated from a script in the repository is reproducible by construction. A figure that is a binary file in the repository is reproducible only if the reader trusts that it matches the claimed analysis. Fields where figures must be hand-drawn or photographed (art history, field biology, clinical medicine) store the figure files directly — Git handles moderate-sized images (under ~10MB each) adequately, and Git LFS extends this to larger files when needed.

**CONTRIBUTORS.yaml** records every person who contributed to the repository, verified by their commit history:

```yaml
contributors:
  - name: "Alice Chen"
    orcid: "0000-0001-2345-6789"
    roles: [conceptualization, methodology, writing-original]
    commits: 847
    first_commit: 2025-06-15
    last_commit: 2026-03-20

  - name: "Bob Martinez"
    orcid: "0000-0002-3456-7890"
    roles: [data-curation, formal-analysis]
    commits: 312
    first_commit: 2025-09-01
    last_commit: 2026-02-14

  - name: "Claude (Anthropic)"
    type: ai_tool
    roles: [writing-review, consistency-checking]
    commits: 0  # AI contributions tracked via author commits
    disclosure: "Used for manuscript preparation and mathematical verification"
```

Roles follow CRediT taxonomy but are *verified against commit history*: a contributor listed as "Methodology" must have commits touching the methods section. The verification can be automated.

### 2.2 Fork-Based Submission and the Hybrid Flow

The protocol does not require journals to abandon their existing submission systems. It defines a **hybrid flow** that integrates with current portals:

**Traditional flow** (unchanged): Author uploads .docx/.pdf through ScholarOne, Editorial Manager, or OJS. The portal handles metadata. Nothing changes for authors or editors who prefer the current approach.

**Git-linked flow** (new option): Author links their paper repository to the submission portal — the same way ORCID accounts are linked today. The portal handles metadata (manuscript type, keywords, suggested reviewers, cover letter). The repository handles the manuscript. On submission, the portal creates a fork from the linked repository and runs the compliance gate.

```
ScholarOne / Editorial Manager / OJS
    |
    |-- Step 1: Author fills metadata form (unchanged)
    |-- Step 2: Author either:
    |   (a) uploads .docx/.pdf [traditional]  OR
    |   (b) links git repo + selects commit [git-linked]
    |
    |-- Step 3 (git-linked only):
    |   Portal creates fork → runs journal_spec validation
    |   If PASS: submission completes
    |   If FAIL: author sees failures, fixes locally, retries
    |
    |-- Step 4: Editor receives compliant manuscript
    |   (from either flow — identical from editor's perspective)
```

This hybrid approach has three adoption advantages. First, it requires no changes to the editorial side — editors see the same manuscript regardless of submission path. Second, it piggybacks on existing OAuth infrastructure (if ScholarOne can link an ORCID, it can link a GitHub account). Third, it creates a gradual migration path: early adopters use the git-linked flow; others continue uploading files. The portal supports both indefinitely.

For journals that support the git-linked flow, submitting a paper creates a **fork** — a frozen, cryptographically linked snapshot of the repository at a specific commit.

```
AUTHOR REPO                          JOURNAL FORK
    |                                     |
    |--- commit a1b2c3 ----[fork]-------> |  frozen at a1b2c3
    |                                     |  owned by editor
    |    (author continues working)       |  author cannot modify
    |                                     |
```

The fork operation:

1. **Creates** a read-only copy of the repository at the specified commit
2. **Transfers ownership** to the journal editor
3. **Records** the fork in the author's `PROVENANCE.yaml` (irrevocable)
4. **Strips** or anonymizes contributor identities per the journal's blinding policy
5. **Generates** rendered outputs (PDF, DOCX) from the SSOT for the editorial workflow

The author **cannot modify** the fork after creation. They can:
- **Revoke** the fork (withdrawing the submission) — the revocation is recorded in provenance
- **Continue working** on their main branch — the fork is a snapshot, not a lock
- **Create additional forks** to other journals — but each new fork carries the full provenance chain, making the existing fork visible

### 2.3 The Submission Gate: Compliance as CI/CD

In the current system, a significant fraction of editorial labor is consumed by non-compliant submissions. Manuscripts arrive with wrong fonts, incorrect reference styles, figures at inadequate resolution, abstracts exceeding word limits, and missing ethics declarations. Editors desk-reject or return these papers, wasting both editorial time and author time. The author reformats and resubmits — sometimes multiple rounds — before the paper ever reaches a reviewer. This is administrative overhead (muda in lean terminology): labor that creates no knowledge.

In the repository protocol, each journal publishes a **submission specification** — a machine-readable document that defines its compliance requirements:

```yaml
# journal_spec.yaml — published by the journal, readable by the author's toolchain
journal:
  name: "Journal of Marketing"
  submission_spec_version: "2026.1"

manuscript:
  format: markdown              # source format
  word_count:
    min: 5000
    max: 12000
    includes: [body]
    excludes: [abstract, references, appendices, tables, figure_captions]
  abstract:
    max_words: 200
    structure: null              # null = flowing | structured = IMRaD headings
  keywords:
    min: 4
    max: 6
  sections_required: [introduction, literature_review, methodology, results, discussion, conclusion]

references:
  style: apa7
  self_citation_max_percent: 25
  min_count: 20
  doi_required: true            # every reference must have a DOI or URL

figures:
  format: [png, svg, tiff]
  min_dpi: 300
  max_file_size_mb: 10
  color_mode: [rgb, cmyk]       # grayscale required for print? specify here
  captions_required: true

tables:
  format: [csv, markdown]       # no embedded Excel
  max_count: 10

ethics:
  ai_disclosure_required: true
  data_availability_required: true
  conflict_of_interest_required: true
  funding_statement_required: true

blinding:
  mode: double-blind
  # ... (detailed blinding config as in Section 2.4)

review:
  type: double-blind            # double-blind | single-blind | open
  suggested_reviewers:
    min: 3
    max: 5
  cover_letter_required: true
```

**The fork operation runs the spec as a validation pipeline before the fork is accepted.** This is the CI/CD model applied to paper submission:

```
AUTHOR REPO
    |
    |--- author requests fork to "Journal of Marketing"
    |
    |--- GATE: journal_spec.yaml validation runs locally
    |    |
    |    |-- [CHECK] Word count: 9,217 ✓ (within 5,000-12,000)
    |    |-- [CHECK] Abstract: 187 words ✓ (≤200)
    |    |-- [CHECK] Keywords: 5 ✓ (4-6)
    |    |-- [CHECK] References: 42, all with DOIs ✓
    |    |-- [CHECK] Self-citation: 19% ✓ (≤25%)
    |    |-- [CHECK] Figures: 3 PNG, all 300+ DPI ✓
    |    |-- [CHECK] AI disclosure: present ✓
    |    |-- [CHECK] Data availability: present ✓
    |    |-- [CHECK] Cover letter: present ✓
    |    |-- [CHECK] paper.yaml: valid schema ✓
    |    |
    |    ALL CHECKS PASSED → fork created
    |
    |--- JOURNAL FORK (compliant by construction)
```

If any check fails, the fork is **not created**. The author sees exactly which requirements are unmet, fixes them in their repository, and retries. The email exchange, desk rejection, and reformatting cycle is eliminated. The journal never sees a non-compliant manuscript.

**This inverts the current compliance model.** Currently:

1. Author guesses at formatting requirements from a 15-page "Instructions for Authors" PDF
2. Author manually formats the manuscript
3. Author submits
4. Editorial assistant checks compliance (days to weeks)
5. Paper returned for formatting fixes (another round trip)
6. Author reformats, resubmits
7. Eventually reaches editor for substantive evaluation

In the repository protocol:

1. Journal publishes `journal_spec.yaml` (machine-readable, unambiguous)
2. Author runs `paper validate --spec journal_spec.yaml` locally
3. All failures shown instantly with exact fix instructions
4. Author fixes in their repo, re-runs validation
5. When all checks pass, fork is created — paper arrives at editor fully compliant

**The author-facing pre-submission layer.** The validation pipeline can include optional AI-assisted checks that run before the gate:

```yaml
# Optional pre-submission AI checks (author-facing, advisory only)
pre_submission:
  scope_check:
    enabled: true
    description: "Does this paper match the journal's stated scope?"
    method: "Compare paper.yaml claims against journal's published topic list"
    blocking: false   # advisory — author decides

  novelty_signal:
    enabled: true
    description: "How does this paper relate to recent publications in this journal?"
    method: "Compare paper.yaml claims against last 2 years of journal's published papers"
    blocking: false

  reference_coverage:
    enabled: true
    description: "Are key works in this field cited?"
    method: "Check paper.yaml dependencies against known citation graphs"
    blocking: false

  statistical_review:
    enabled: true
    description: "Are sample sizes, tests, and effect sizes reported per journal standards?"
    method: "Parse methodology section for reporting completeness"
    blocking: false
```

These AI checks are **advisory, not blocking**. They help the author assess fit before investing in the submission. A researcher can see: "Your paper's claims overlap 72% with Journal X's scope but only 31% with Journal Y's — consider submitting to X first." This replaces the current guesswork of reading "Instructions for Authors" and hoping.

**Implementability.** Every check in the gate is technically straightforward:

| Check | Implementation | Difficulty |
|---|---|---|
| Word count | Parse Markdown, count tokens by section | Trivial |
| Abstract length | Parse frontmatter or delimited section | Trivial |
| Reference style | Lint against CSL style definition (CSL already exists for every major style) | Moderate — CSL libraries exist |
| Figure format/DPI | Read image metadata (Pillow, ImageMagick) | Trivial |
| Self-citation ratio | Count author-name matches in reference list | Easy |
| DOI completeness | Check each reference for DOI field | Easy |
| AI disclosure presence | Check for required section heading or YAML field | Trivial |
| Scope matching (AI) | Embed paper abstract + journal scope, compute similarity | Moderate — embedding models exist |
| Reference coverage (AI) | Compare citation list against field's citation graph | Moderate — Semantic Scholar API |
| Statistical reporting (AI) | Parse methods section for reporting standards | Hard — but tools like statcheck exist |

The hard checks (scope matching, reference coverage, statistical reporting) are advisory and optional. The blocking checks are all automatable with existing tools. No new AI research is needed — only integration.

**Consequences.** When every submission arrives fully compliant:

- **Editors** spend zero time on formatting desk rejections — 100% of their time goes to substantive evaluation
- **Authors** never wait weeks to learn their margins were wrong — they know in seconds
- **Reviewers** never receive papers missing basic elements — every paper has all required sections, disclosures, and metadata
- **The system** eliminates an entire class of muda: the formatting-rejection-resubmission cycle

This is the specification principle: what can be specified should be automated. Human judgment is reserved for what cannot be specified — the intellectual evaluation of the paper's contribution.

### 2.4 Blinding as a System Function

Current blinding requires authors to manually remove their names, anonymize self-citations, and hope that no identifying information leaks through. This is error-prone, labor-intensive, and structurally unverifiable.

In the repository protocol, blinding is a **configurable system function** applied to the fork at creation time. The journal specifies its blinding policy as a parameter:

```yaml
# Journal configuration
blinding:
  mode: double-blind          # single-blind | double-blind | open
  strip_author_names: true
  strip_affiliations: true
  strip_orcids: true
  strip_acknowledgments: true
  preserve_roles: true         # "Author 1 (methodology, formal analysis)"
  anonymize_self_citations: true
  strip_figure_metadata: true  # EXIF data, embedded author info
  strip_funding_sources: false # some journals require this visible
```

The system applies these rules automatically when generating the reviewer-facing version of the fork. The original fork retains all identity information (for the editor's use); the reviewer-facing view is a projection that suppresses the specified fields.

This offers several structural advantages over manual blinding:
- **Complete**: every field is covered, including figure metadata, code comments, and embedded document properties that authors routinely forget
- **Configurable**: different journals apply different policies without requiring authors to re-blind for each venue
- **Verifiable**: the blinding function is deterministic and auditable — an author cannot "accidentally" leave identifying information visible
- **Reversible**: after the review decision, the editor can lift the blind selectively (e.g., revealing author identity to reviewers who request it post-decision)

### 2.5 Review as Attributed Commits

The editor creates a **review branch** for each reviewer on the journal fork:

```
JOURNAL FORK
    |
    |--- main (frozen manuscript)
    |
    |--- review/reviewer-1
    |    |-- commit: "Section 3 methodology critique" (2026-04-01)
    |    |-- commit: "Statistical test recommendation" (2026-04-01)
    |    |-- commit: "Minor: typos and formatting" (2026-04-02)
    |    └-- commit: "RECOMMENDATION: major revision" (2026-04-05)
    |
    |--- review/reviewer-2
    |    |-- commit: "Theoretical framework assessment" (2026-04-03)
    |    └-- commit: "RECOMMENDATION: accept with minor" (2026-04-07)
    |
    └--- editorial/decision
         └-- commit: "DECISION: revise and resubmit" (2026-04-10)
```

Each reviewer's branch is a complete, timestamped, attributed record of their review. The commit history shows:
- **When** the reviewer worked (timestamps)
- **What** they reviewed (which sections, which claims)
- **How deeply** they engaged (number of commits, lines of commentary)
- **What they recommended** (final commit on the branch)

The reviewer's identity on the branch is controlled by the editor:
- **Open review**: real name and ORCID visible
- **Single-blind**: reviewer identity visible to editor only; authors see "Reviewer 1"
- **Pseudonymous**: reviewer has a persistent pseudonym across reviews at this journal

### 2.6 Reviewer Ownership and Portable Review History

A reviewer's account belongs to the reviewer, not the journal. When a reviewer completes a review, their branch on the journal fork is linked to their personal profile. Over time, the reviewer accumulates a **review portfolio**:

```yaml
# Reviewer profile (owned by reviewer, not journal)
review_history:
  total_reviews: 47
  journals: ["Nature", "Science", "PNAS", "JM", "QSS"]
  avg_depth: 12.3 commits per review
  specializations: [methodology, statistics, theory]

  # Individual reviews — visibility controlled by reviewer
  reviews:
    - journal: "Nature"
      year: 2026
      decision: "accept"
      depth: 18 commits
      visible: true     # reviewer chose to make this public

    - journal: "JM"
      year: 2026
      decision: "reject"
      depth: 7 commits
      visible: false    # reviewer chose to keep private
```

The reviewer controls which individual reviews are public, but aggregate statistics (total count, average depth, journal list) are always visible. This creates verifiable review reputation without requiring full transparency.

**Consequences for reviewer incentives:**
- **Depth is measurable**: A reviewer who writes 18 commits of substantive critique is visibly different from one who writes 2 commits of vague praise
- **Quality is portable**: A reviewer's track record follows them across journals — a strong review history at Nature signals credibility to QSS
- **Credit is structural**: Hiring committees and grant panels can query a candidate's review portfolio alongside their publication record
- **Accountability is implicit**: A reviewer who consistently gives superficial reviews has a visible pattern — not because anyone punished them, but because the data structure records it

### 2.7 Provenance by Design

Every fork creates an irrevocable record in the author's `PROVENANCE.yaml`:

```yaml
provenance:
  forks:
    - id: "fork-001"
      target: "Journal of Marketing"
      target_type: journal
      created: 2026-03-20T14:00:00Z
      source_commit: a3f7c2e
      status: returned       # active | returned | revoked
      decision: rejected
      decision_date: 2026-03-28
      decision_public: false  # author controls visibility
      reviewers: 3
      review_depth: 847       # total comment lines

    - id: "fork-002"
      target: "Journal of Advertising Research"
      target_type: journal
      created: 2026-04-05T10:00:00Z
      source_commit: b4e8d3f  # different commit — paper was revised
      status: active
      decision: null
      prior_forks_visible: true  # JAR editor can see fork-001 exists
```

**Critical property**: The `forks` list is append-only. An author cannot delete a fork record. This means:

1. **Dual submission becomes structurally detectable within the protocol.** If fork-001 has `status: active`, any new fork carries this information. The receiving editor sees that another fork is active.

2. **Rejection history is optionally transparent.** The *existence* of fork-001 is always visible to subsequent fork recipients. The *decision* (rejected) is visible only if the author sets `decision_public: true`. An author can reveal their rejection history to demonstrate thoroughness, or keep it private.

3. **Review labor is preserved.** When a paper moves from Journal A (rejected) to Journal B, Journal B's editor can see that three reviewers spent 847 lines of commentary on the paper. The editor can (with author consent and reviewer consent) request access to those reviews — reducing duplicate labor. This requires a three-way consent protocol: author agrees to share, original editor agrees to release, and original reviewers agree to transfer their reviews.

### 2.8 Collections as Users

The most radical architectural implication: if every paper is a repository, then preprint servers, journals, and institutional archives are not platforms — they are **users** on a shared platform who curate collections of frozen forks.

```
AUTHOR REPO (the paper)
    |
    |-- fork → "arXiv" user → accepted into arXiv collection
    |   (paper receives arXiv badge + arXiv ID)
    |
    |-- fork → "Zenodo" user → accepted into Zenodo community
    |   (paper receives DOI)
    |
    |-- fork → "Nature" user → enters review workflow
    |   (if accepted: paper receives Nature badge + DOI)
    |
    |-- fork → "MIT Libraries" user → accepted into institutional repo
    |   (paper receives handle)
```

In this architecture:

- **arXiv** is a user account that accepts forks into its collection. Acceptance criteria: formatting compliance, subject classification, basic quality check. The paper gets an arXiv ID badge.
- **Zenodo** is a user account that accepts forks and mints DOIs. Acceptance criteria: metadata completeness.
- **Nature** is a user account that accepts forks into a review workflow. Acceptance criteria: editorial judgment + peer review.
- **SSRN** is a user account that curates working paper collections.

The paper exists once. It lives in the author's repository. Preprint servers, journals, and archives hold frozen forks — snapshots at specific commits, curated into collections with different acceptance criteria and different badges.

This eliminates:
- **Format conversion**: the repository generates whatever output each collection requires
- **Multiple uploads**: fork once, accepted into collection
- **Version fragmentation**: the author's repo is the SSOT; every collection holds a linked snapshot
- **Access barriers**: arXiv endorsement, SSRN account approval, journal submission portals — all replaced by fork requests that carry verifiable provenance

### 2.9 Federation and Local Sovereignty

A critical design constraint: scientists will not entrust their life's work to a centralized platform they do not control. Any protocol that requires a single hosting provider — even a well-intentioned one — replicates the power dynamics of the current publisher oligopoly in a new form.

Git is inherently decentralized. A Git repository is a complete, self-contained history that can be cloned, moved, and operated on without any server. The Research-as-Repository protocol leverages this property through a three-tier architecture:

**Tier 1: Local-first authoring.** The author's repository lives on their own machine. All writing, data analysis, and version history happen locally. No internet connection is required for any authoring operation. The author owns their files — not a platform, not an institution, not a publisher. This is how Git already works for software. No new infrastructure is needed.

**Tier 2: Optional remote hosting.** The author may push their repository to any Git-compatible host: GitHub, GitLab, a university's self-hosted Gitea instance, or a personal server. The choice of host is the author's. The protocol imposes no requirement on where the repository is hosted — only on its structure (the presence of `paper.yaml`, `CONTRIBUTORS.yaml`, `PROVENANCE.yaml`).

Multiple remotes are supported natively by Git. An author can push to their university's GitLab AND to GitHub AND to a personal backup — simultaneously, with no conflict. If one host disappears, the repository survives on the others and on the author's local machine.

**Tier 3: Federated discovery and provenance.**

Fork-based submission requires that the receiving party (a journal, a preprint server) can verify the provenance chain. This does not require a central registry. It requires a **federation protocol** — a way for independent hosts to exchange provenance metadata.

The model is email (SMTP), not social media (Twitter). Email works because any server can send to any other server using a shared protocol. No central authority controls who can send or receive. The Research-as-Repository federation protocol works the same way:

```
Author (hosted on University GitLab)
    |
    |-- fork request --> Journal (hosted on their own OJS+Git)
    |   |
    |   |-- provenance check: query author's remote for PROVENANCE.yaml
    |   |-- verify: no active forks to other journals
    |   |-- accept fork: clone at specified commit
    |
    |-- fork request --> arXiv (hosted on arXiv infrastructure)
        |
        |-- provenance check: same query, same verification
        |-- accept: add to collection, mint identifier
```

Each participant runs their own infrastructure. The protocol specifies the message format (provenance queries, fork requests, decision records) and the verification rules (how to check a provenance chain). No central platform is involved.

**Adoption gradient.** The three tiers allow incremental adoption:

1. **Minimal adoption**: Author uses Git locally for version control. Benefits: full history, contributor tracking, backup. Cost: learning Git (many researchers already use it for code).

2. **Moderate adoption**: Author pushes to a remote host and includes `paper.yaml`. Benefits: structured metadata, machine readability, DOI minting via Zenodo-GitHub integration (already exists). Cost: maintaining the YAML companion.

3. **Full adoption**: Author participates in the federation protocol — submitting via fork, receiving review branches, carrying provenance. Benefits: all five gaps closed. Cost: journals must implement the protocol.

Tier 1 is useful immediately, alone, with no institutional adoption. This is critical: the protocol must deliver value to a single researcher on their laptop before it delivers value to the system.

### 2.10 The AI-Native Layer

When every paper is a repository with structured metadata (`paper.yaml`), machine-readable content (Markdown), and auditable provenance (`PROVENANCE.yaml`), the entire corpus becomes queryable:

**Cross-paper consistency**: An AI agent can detect when Paper B's claims depend on Paper A's results, and Paper A has been retracted or revised. The dependency chain is explicit in `paper.yaml`.

**Real-time literature review**: "Find all papers whose claims depend on Peters (2019) ergodicity framework and have been accepted by a Q1 journal in the last 6 months" — answerable in seconds from structured metadata.

**Language independence**: The repository stores structured claims. An AI can translate the natural-language manuscript while preserving the machine-readable claim structure. A Japanese researcher can read a Brazilian paper's claims in Japanese, verify them against the original structured metadata, and cite the specific claim by ID.

**Change propagation**: When a foundational paper updates a key result, every paper that cites that result can be automatically flagged. The dependency graph is explicit. Currently, citation is a string in a reference list. In the repository protocol, citation is a typed link to a specific claim in a specific version of a specific repository.

**Reviewer assistance**: An AI can pre-screen a fork against the journal's scope, check the `paper.yaml` claims for internal consistency, flag potential conflicts with known results, and prepare a structured briefing for the human reviewer — all before the reviewer opens the manuscript.

---

## 3. Design Principles

### 3.1 Single Source of Truth (SSOT)

The author's repository is the one and only source of truth for the paper. All other representations — PDFs, preprints, published versions, translations — are renderings. If the rendering disagrees with the repository, the repository is correct.

This inverts the current hierarchy, where the published PDF is the canonical version and the author's files are disposable. In the repository protocol, the published version is a tagged release from the repository — one rendering among many, distinguished only by its DOI and journal badge.

### 3.2 Functions by Design

Every feature that the current system implements through policy, the repository protocol implements through structure:

| Current approach | Repository approach |
|---|---|
| Dual submission ban (policy, honor system) | Provenance chain makes active forks visible (structural) |
| Double-blind review (manual anonymization) | Blinding function configurable per journal (automated) |
| CRediT roles (self-reported annotation) | Contributor roles verified against commit history (auditable) |
| Peer review acknowledgment ("We thank...") | Review branches with attributed commits (structural credit) |
| Preprint posting (separate upload to separate platform) | Fork to collection user (same repository, different badge) |
| Retraction (editorial notice on published PDF) | Revert commit in repository + propagated flag to all forks |

### 3.3 Minimal Mandatory Transparency, Maximal Optional Transparency

The protocol distinguishes between information that must always be visible and information whose visibility the participant controls:

**Always visible** (structural integrity):
- That a fork exists (a submission happened)
- That a fork was revoked (a submission was withdrawn)
- Aggregate review statistics (number of reviewers, total depth)
- Contributor roles (but not necessarily identities — blinding may apply)

**Author controls**:
- Whether each fork's decision (accepted/rejected) is public
- Whether the full provenance chain is public or visible only to fork recipients
- Whether post-publication corrections are visible as diffs or only as current state

**Reviewer controls**:
- Whether their identity is revealed on specific reviews
- Which individual reviews appear in their public portfolio
- Aggregate statistics are always visible; individual details are opt-in

**Editor controls**:
- Blinding configuration for the journal fork
- Whether review branches are preserved after decision
- Whether reviews can be transferred to subsequent journals (with reviewer consent)

---

## 4. Implications

### 4.1 For Authors

The paper repository replaces the fragmented workflow of Word documents, email attachments, submission portals, and manual record-keeping with a single versioned repository that serves all purposes:

- **Writing**: collaborative editing with full attribution
- **Submission**: fork to journal (one operation, full provenance)
- **Preprint**: fork to arXiv/Zenodo collection (same operation)
- **Revision**: continue working on main branch; create new fork when ready
- **Publication**: tagged release with DOI
- **Post-publication**: corrections as commits, visible to all fork holders

### 4.2 For Reviewers

Review labor becomes visible, portable, and creditable. The reviewer's work is no longer a private communication between reviewer and editor — it is an attributed intellectual contribution with a verifiable record. This has direct implications for career evaluation: a researcher with a strong review portfolio demonstrates scholarly judgment that publication counts alone cannot capture.

### 4.3 For Editors

The editor gains structured data about every paper in the pipeline: who contributed what, how the paper has been received elsewhere, and what the reviewer community thinks — not as a stack of PDFs in an inbox, but as a queryable graph of repositories, forks, and review branches.

### 4.4 For AI Transparency

One of the most contested questions in contemporary science is the role of AI in research: which parts of a paper were written, analyzed, or suggested by AI tools? Current disclosure mechanisms are text statements ("AI was used for...") that no one can verify. A researcher can declare any level of AI involvement — or none — and the declaration is unfalsifiable.

The repository protocol offers a structural approach to this problem. When AI tools interact with a paper repository, their contributions are commits — the same versioned, timestamped, attributed operations that track human contributions. The `CONTRIBUTORS.yaml` file records each AI tool with its type (`ai_tool`), its specific roles (writing-review, consistency-checking, formal-analysis), and a disclosure statement. The commit history shows exactly which sections were modified in commits attributed to AI-assisted sessions.

This does not fully solve the AI transparency problem — an author can still commit AI-generated text under their own name. But it shifts the default from unverifiable declaration to auditable history. A repository where Claude is listed in CONTRIBUTORS.yaml with 0 commits but the manuscript was written in 3 days raises the same questions a code review would raise: the attribution and the evidence do not match. The git log creates a structural expectation of consistency between declared contributions and observed activity — an expectation that does not exist when the only disclosure is a sentence in the acknowledgments.

### 4.5 For the System

The cumulative effect is that scientific publishing becomes a transparent, auditable, machine-readable graph of knowledge production. The Matthew Effect — where early prestige compounds into career advantage through mechanisms invisible to evaluation systems — becomes measurable. The non-ergodic dynamics of academic careers (Zharnikov, 2026o) become traceable. The specification gap in peer review (Zharnikov, 2026t) becomes closeable.

---

## 5. Limitations and Open Questions

1. **Adoption barrier.** The protocol requires journals, authors, and reviewers to adopt new tooling. The transition cost is non-trivial. A realistic adoption path may begin with a single journal or preprint server implementing the protocol alongside traditional workflows.

2. **No prototype.** This paper proposes a conceptual architecture, not an implementation. A proof-of-concept — implementing the fork gate, blinding function, and reviewer branch model for a single journal — is the necessary validation step. The most realistic first adopter is likely a preprint server (which already accepts structured deposits) or an overlay journal (which already curates externally hosted papers), not a traditional publisher whose business model depends on controlling the manuscript pipeline.

### 5.1 Implementation Roadmap

The protocol's compliance gate has been prototyped. A reference validator (`validate_paper.py`, 290 lines of Python) checks a paper repository against a `journal_spec.yaml` file, validating word count, abstract length, keyword range, reference count, self-citation ratio, figure formats, and required statements (AI disclosure, data availability, funding, conflict of interest). The validator runs locally in under one second and produces a pass/fail report with specific failure messages.

A worked example demonstrates feasibility: the Journal of Marketing's submission requirements have been encoded as `journal_spec_jm.yaml` (130 fields covering manuscript format, blinding rules, figure specifications, math notation rules, and 46 compliance checks derived from actual JM submission guidelines). Running the validator against a paper repository produces output such as:

```
Validating against: Journal of Marketing
Repository: /path/to/paper
------------------------------------------------------------
  [OK]   Manuscript: paper.md
  [OK]   Paper Spec companion: paper.yaml
  [OK]   Word count: 9,217 (limit: page-based)
  [OK]   Abstract: 187 words (max: 200)
  [FAIL] References: self-citation 27.3% > maximum 25%
  [OK]   Statement: ai_disclosure
  [OK]   Figures: all compliant
------------------------------------------------------------
Results: 6 passed, 1 failed, 0 warnings
Submission gate: BLOCKED — fix failures before submitting
```

The author sees the exact failure (self-citation ratio), fixes it in their repository, and re-runs the validator. The entire cycle takes minutes, not the weeks currently consumed by desk-rejection-and-resubmission rounds.

A realistic adoption sequence: (1) a preprint server or overlay journal implements the fork gate as a GitHub Action — this requires only the validator and a `journal_spec.yaml`, both of which exist; (2) an existing editorial management system (OJS is open-source and extensible) adds git-linked submission as an optional flow alongside traditional upload; (3) a funder (e.g., Wellcome Trust, which already mandates open data) requires `PROVENANCE.yaml` for funded papers, creating demand-side pressure. Each step is independently useful and does not require the others.

The companion artifacts — schemas, examples, and validator — are available at the paper's repository and will be published as an open-source package.

**This paper as its own first implementation.** The present paper is authored, versioned, and structured according to the protocol it proposes. The repository contains: `paper.yaml` (7 typed claims with falsification conditions), `CONTRIBUTORS.yaml` (4 contributors including 3 AI tools with disclosure statements), `PROVENANCE.yaml` (fork history — populated as the paper is submitted to venues), `DATA_MANIFEST.yaml` (empty — this is a conceptual paper with no external data), the `journal_spec.yaml` schema, a worked Journal of Marketing example, and the `validate_paper.py` compliance validator. Every claim can be traced to a specific commit. Every contributor's role is verified against the commit log. The paper is its own proof of concept — not a prototype of the full fork-and-review protocol, but a demonstration that the repository structure, metadata schemas, and compliance tooling are functional and internally consistent. The public repository is at github.com/spectralbranding/paper-repo.

### 5.2 Stakeholder Incentives and Barriers

**Publishers.** Traditional publishers derive revenue from controlling the manuscript pipeline — submission portals, typesetting, branding, and access. The protocol disperses this control. Publishers are unlikely first movers. However, society publishers and university presses (which often operate at cost) have weaker lock-in incentives and may value the efficiency gains. Open-access publishers whose revenue comes from APCs rather than pipeline control are natural early adopters — the protocol reduces their operational costs without threatening their business model.

**Editors.** The compliance gate eliminates formatting desk rejections — a direct time savings. The reviewer branch model provides structured data on reviewer engagement — useful for identifying reliable reviewers. Editors benefit immediately from the gate and incrementally from the review model. The hybrid flow (Section 2.2) ensures editors need not change their workflow; they see the same manuscript regardless of submission path.

**Reviewers.** The portable review portfolio creates career credit for an activity that currently generates none. The privacy controls (Section 3.3) allow reviewers to accumulate reputation without revealing specific reviews. The risk is that visible review depth creates pressure to over-invest in each review; the mitigation is that depth metrics are aggregate, not per-review.

**Authors.** The primary adoption barrier is Git literacy (Limitation 3). For authors who already use Git (common in computer science, physics, and computational biology), the protocol offers immediate benefits: version history, contributor traceability, and compliance checking. For authors in Word-dominant fields, the protocol requires a GUI abstraction layer that does not yet exist at production quality.

**Legal and intellectual property.** Reviewer commits on journal forks create intellectual contributions with unclear copyright status under current law. The protocol should specify that all review commits are licensed CC-BY-4.0 at creation time — reviewers retain attribution rights but grant reuse. This requires explicit consent at the point of reviewer invitation, analogous to the copyright transfer agreements authors currently sign.

**Privacy.** The irrevocable provenance chain raises concerns: some authors may not want rejection history visible, even as "existence of fork" without decision outcome. The protocol's current design (existence always visible, outcome optionally visible) is a compromise. An alternative — fully private provenance visible only to fork recipients — weakens the dual-submission prevention. The appropriate default is a community decision that may vary by discipline: clinical research may require full transparency; humanities may prefer privacy. The protocol supports both configurations.

3. **Git literacy.** The majority of researchers outside computer science and engineering have never used Git. Humanities, social sciences, and many natural science fields work primarily in Word processors. The protocol requires a GUI abstraction layer — a "GitHub Desktop for papers" — that presents repository operations (commit, fork, branch) through familiar editing metaphors. Without this, adoption is limited to computationally literate disciplines. The three-tier architecture (Section 2.9) mitigates this: Tier 1 (local Git) benefits only those who already use version control; the full protocol benefits only materialize at Tier 3, which requires broader tool development.

4. **Gaming.** Commit histories can be manufactured. A contributor could inflate their commit count through trivial changes. Mitigation: review branches are created by editors, not authors; and contribution metrics should weight substance (lines changed in methods section) over quantity (total commits).

5. **Privacy.** The always-visible provenance chain reveals submission history, which some authors may consider sensitive. The protocol's "existence visible, outcome optional" compromise attempts to balance structural integrity against author privacy, but the appropriate threshold is a community decision.

6. **Legacy corpus.** The existing body of 50+ million published papers has no repository structure. Retroactive conversion is impractical. The protocol applies to new papers going forward; legacy papers remain in their current form.

7. **Governance.** The protocol is designed as a federated network (Section 2.9), not a centralized platform. Like email, any institution can run its own server. The governance question reduces to: who maintains the protocol specification? Existing models (IETF for internet protocols, W3C for web standards, NISO for information standards) provide precedents. The protocol specification itself can be versioned in a Git repository.

8. **Intellectual property.** When an editor owns a fork and reviewers commit to it, the ownership of review content is unclear under current copyright law. The protocol should specify that review commits are licensed under a standard open license (e.g., CC-BY) at creation time.

---

## 6. Conclusion

The structural gap in scientific publishing is not access, timing, or format. It is the document assumption — the treatment of a paper as a static file rather than a living repository with history, contributors, branches, and provenance.

The Research-as-Repository protocol replaces this assumption with Git-native semantics: papers are repositories, submissions are forks, reviews are attributed commits, and preprint servers are collection users on a shared platform. Every structural problem in the current system — untracked contributions, invisible review labor, unenforceable dual-submission policies, fragmented version histories, and opaque editorial decisions — becomes structurally addressable in principle when the paper is a repository rather than a document.

The protocol does not require new science. It requires applying to scientific publishing the same version-control infrastructure that software engineering adopted two decades ago. The tools exist. The semantics exist. The missing piece is the specification layer — the protocol that maps academic publishing workflows onto repository operations.

This paper proposes the conceptual architecture for that specification. A formal, implementable standard — with normative message schemas, authentication flows, and error handling — is the necessary next step.

---

## References

Borgman, C. L. (2007). *Scholarship in the Digital Age: Information, Infrastructure, and the Internet*. MIT Press.

Chambers, C. D. (2013). Registered Reports: A new publishing initiative at Cortex. *Cortex*, 49(3), 609-610.

cOAlition S. (2018). Plan S: Making full and immediate Open Access a reality. https://www.coalition-s.org/

Coalition for Advancing Research Assessment (CoARA). (2022). Agreement on reforming research assessment.

Hicks, D., Wouters, P., Waltman, L., de Rijcke, S., & Rafols, I. (2015). Bibliometrics: The Leiden Manifesto for research metrics. *Nature*, 520(7548), 429-431.

San Francisco Declaration on Research Assessment (DORA). (2012).

Auer, S., Kovtun, V., Prinz, M., Kasprzik, A., Stocker, M., & Vidal, M. E. (2019). Towards an Open Research Knowledge Graph. *Serials Review*, 45(4). https://doi.org/10.1080/0361526X.2019.1540272

Clark, T., Ciccarese, P. N., & Goble, C. A. (2014). Micropublications: A semantic model for claims, evidence, arguments and annotations in biomedical communications. *Journal of Biomedical Semantics*, 5(28). https://doi.org/10.1186/2041-1480-5-28

Di Cosmo, R., & Zacchiroli, S. (2019). Software Heritage: Why and How to Preserve Software Source Code. arXiv:1909.10760.

Gipp, B., Meuschke, N., & Gernandt, A. (2017). Decentralized Trusted Timestamping using the Crypto Currency Bitcoin. *Proceedings of the ACM/IEEE Joint Conference on Digital Libraries (JCDL)*.

Groth, P., Gibson, A., & Velterop, J. (2010). The Anatomy of a Nanopublication. *Information Services & Use*, 30(1-2), 51-56.

Hammer, M., & Champy, J. (1993). *Reengineering the Corporation: A Manifesto for Business Revolution*. Harper Business.

Himmelstein, D. S., Rubinetti, V., Slochower, D. R., et al. (2019). Open collaborative writing with Manubot. *PLOS Computational Biology*, 15(6), e1007128. https://doi.org/10.1371/journal.pcbi.1007128

Katz, D. S., Barba, L. A., Niemeyer, K. E., & Smith, A. M. (2018). Journal of Open Source Software (JOSS): design and first-year review. *PeerJ Computer Science*, 4, e147.

Lariviere, V., Haustein, S., & Mongeon, P. (2015). The oligopoly of academic publishers in the digital era. *PLOS ONE*, 10(6), e0127502.

Ohno, T. (1988). *Toyota Production System: Beyond Large-Scale Production*. Productivity Press.

Peroni, S., & Shotton, D. (2012). FaBiO and CiTO: Ontologies for describing bibliographic resources and citations. *Journal of Web Semantics*, 17, 33-43. https://doi.org/10.1016/j.websem.2012.08.001

Ram, K. (2013). Git can facilitate greater reproducibility and increased transparency in science. *Source Code for Biology and Medicine*, 8(1), 7.

Robinson, D. C., Hand, J. A., Madsen, M. B., & McKelvey, K. R. (2018). The Dat Project, an open and decentralized research data tool. *Scientific Data*, 5, 180221. https://doi.org/10.1038/sdata.2018.221

Ross-Hellauer, T. (2017). What is open peer review? A systematic review. *F1000Research*, 6, 588. https://doi.org/10.12688/f1000research.11369.2

Tennant, J. P., Dugan, J. M., Graziotin, D., et al. (2017). A multi-disciplinary perspective on emergent and future innovations in peer review. *F1000Research*, 6, 1151.

Soiland-Reyes, S., Sefton, P., Crosas, M., et al. (2022). Packaging research artefacts with RO-Crate. *Data Science*, 5(1), 97-138. https://doi.org/10.3233/DS-210053

Torvalds, L. (2005). Git: Fast version control system.

UNESCO. (2021). UNESCO Science Report: The race against time for smarter development.

van Rooyen, S., Godlee, F., Evans, S., Black, N., & Smith, R. (1999). Effect of open peer review on quality of reviews and on reviewers' recommendations. *BMJ*, 318(7175), 23-27.

Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018. https://doi.org/10.1038/sdata.2016.18

Willinsky, J. (2005). Open Journal Systems: An example of open source software for journal management and publishing. *Library Hi Tech*, 23(4), 504-519.

Womack, J. P., & Jones, D. T. (1996). *Lean Thinking: Banish Waste and Create Wealth in Your Corporation*. Simon & Schuster.

Zharnikov, D. (2026a). Spectral Brand Theory: A multi-dimensional framework for brand perception analysis. Working Paper. https://doi.org/10.5281/zenodo.18945912

Zharnikov, D. (2026i). Organization as specification: A test-driven approach to business design. Working Paper. https://doi.org/10.5281/zenodo.18946043

Zharnikov, D. (2026o). Non-ergodic brand perception: Why cross-sectional brand tracking systematically misrepresents individual trajectories. Working Paper. https://doi.org/10.5281/zenodo.19138860

Zharnikov, D. (2026t). Paper as specification: A machine-readable standard for scientific claims. Working Paper. https://doi.org/10.5281/zenodo.19210037
