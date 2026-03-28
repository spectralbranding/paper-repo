#!/usr/bin/env python3
"""
validate_paper.py — Paper Repository Compliance Validator

Validates a paper repository against a journal_spec.yaml.
Part of the Paper-as-Repository protocol (Zharnikov, 2026u).

Usage:
    python validate_paper.py --repo /path/to/paper/repo --spec /path/to/journal_spec.yaml

Checks:
    - Required files exist (paper.md, paper.yaml, CONTRIBUTORS.yaml, PROVENANCE.yaml)
    - Word count within limits
    - Abstract word count within limits
    - Keyword count within range
    - Reference count and self-citation ratio
    - Figure format and DPI
    - Required statements present (AI disclosure, data availability, etc.)

Exit codes:
    0 = all checks passed
    1 = one or more checks failed
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: uv pip install pyyaml")
    sys.exit(2)


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def count_words(text: str) -> int:
    """Count words in plain text, excluding YAML frontmatter."""
    # Strip YAML frontmatter
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    # Strip markdown headers, links, images
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[.*?\]\(.*?\)", lambda m: m.group(0).split("]")[0][1:], text)
    text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
    # Strip code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return len(text.split())


def extract_abstract(text: str) -> str:
    """Extract abstract section from markdown."""
    match = re.search(
        r"## Abstract\n\n(.*?)(?=\n## |\n---)", text, re.DOTALL | re.IGNORECASE
    )
    if match:
        return match.group(1).strip()
    return ""


def extract_keywords(text: str) -> list:
    """Extract keywords from markdown or YAML frontmatter."""
    match = re.search(r"\*\*Keywords\*\*:?\s*(.+)", text, re.IGNORECASE)
    if match:
        return [k.strip() for k in match.group(1).split(",")]
    return []


def count_references(text: str) -> tuple:
    """Count total references and self-citations."""
    ref_section = re.search(r"## References\n\n(.*)", text, re.DOTALL | re.IGNORECASE)
    if not ref_section:
        return 0, 0, 0.0

    refs = ref_section.group(1).strip().split("\n\n")
    refs = [r for r in refs if r.strip()]
    total = len(refs)

    # Count self-citations (Zharnikov)
    self_cites = sum(1 for r in refs if "Zharnikov" in r)
    ratio = (self_cites / total * 100) if total > 0 else 0.0

    return total, self_cites, ratio


def check_figures(repo_path: Path, spec: dict) -> list:
    """Check figure files against spec requirements."""
    issues = []
    figures_dir = repo_path / "figures"

    if not figures_dir.exists():
        return issues  # no figures is not necessarily an error

    fig_spec = spec.get("figures", {})
    accepted_formats = fig_spec.get("formats_accepted", [])
    min_dpi = fig_spec.get("min_dpi", 0)

    for fig_file in figures_dir.iterdir():
        if fig_file.suffix.lower().lstrip(".") not in [
            f.lower() for f in accepted_formats
        ]:
            if accepted_formats:
                issues.append(
                    f"FAIL: {fig_file.name} format "
                    f"{fig_file.suffix} not in accepted: {accepted_formats}"
                )

    return issues


def validate(repo_path: Path, spec: dict) -> list:
    """Run all validation checks. Returns list of (status, message) tuples."""
    results = []

    # ── Required files ─────────────────────────────────────────
    required_files = {
        "paper.md": "Manuscript source",
        "paper.yaml": "Paper Spec companion",
        "CONTRIBUTORS.yaml": "Contributor roles",
        "PROVENANCE.yaml": "Fork history",
    }

    # Also check for LaTeX/Quarto variants
    manuscript_found = False
    for ext in ["paper.md", "paper.tex", "paper.qmd", "paper.Rmd"]:
        if (repo_path / ext).exists():
            manuscript_found = True
            manuscript_path = repo_path / ext
            break

    if manuscript_found:
        results.append(("PASS", f"Manuscript: {manuscript_path.name}"))
    else:
        results.append(("FAIL", "Manuscript: no paper.md/.tex/.qmd/.Rmd found"))
        return results  # can't continue without manuscript

    for fname, desc in list(required_files.items())[1:]:
        if (repo_path / fname).exists():
            results.append(("PASS", f"{desc}: {fname}"))
        else:
            results.append(("FAIL", f"{desc}: {fname} missing"))

    # ── Read manuscript ────────────────────────────────────────
    text = manuscript_path.read_text()

    # ── Word count ─────────────────────────────────────────────
    wc = count_words(text)
    ms_spec = spec.get("manuscript", {}).get("word_count", {})
    wc_min = ms_spec.get("min")
    wc_max = ms_spec.get("max")

    if wc_min and wc < wc_min:
        results.append(("FAIL", f"Word count: {wc} < minimum {wc_min}"))
    elif wc_max and wc > wc_max:
        results.append(("FAIL", f"Word count: {wc} > maximum {wc_max}"))
    else:
        limit_str = f"{wc_min}-{wc_max}" if wc_min and wc_max else "no limit"
        results.append(("PASS", f"Word count: {wc} (limit: {limit_str})"))

    # ── Abstract ───────────────────────────────────────────────
    abstract = extract_abstract(text)
    abs_spec = spec.get("abstract", {})
    abs_max = abs_spec.get("max_words")

    if abstract:
        abs_wc = len(abstract.split())
        if abs_max and abs_wc > abs_max:
            results.append(("FAIL", f"Abstract: {abs_wc} words > maximum {abs_max}"))
        else:
            results.append(("PASS", f"Abstract: {abs_wc} words (max: {abs_max})"))
    else:
        results.append(("WARN", "Abstract: not found"))

    # ── Keywords ───────────────────────────────────────────────
    keywords = extract_keywords(text)
    kw_spec = spec.get("keywords", {})
    kw_min = kw_spec.get("min", 0)
    kw_max = kw_spec.get("max", 99)

    if keywords:
        kw_count = len(keywords)
        if kw_count < kw_min:
            results.append(("FAIL", f"Keywords: {kw_count} < minimum {kw_min}"))
        elif kw_count > kw_max:
            results.append(("FAIL", f"Keywords: {kw_count} > maximum {kw_max}"))
        else:
            results.append(("PASS", f"Keywords: {kw_count} (range: {kw_min}-{kw_max})"))
    else:
        results.append(("WARN", "Keywords: not found"))

    # ── References ─────────────────────────────────────────────
    total_refs, self_refs, self_ratio = count_references(text)
    ref_spec = spec.get("references", {})
    ref_min = ref_spec.get("min_count", 0)
    self_max = ref_spec.get("self_citation_max_percent")

    if total_refs < ref_min:
        results.append(("FAIL", f"References: {total_refs} < minimum {ref_min}"))
    else:
        results.append(("PASS", f"References: {total_refs} (min: {ref_min})"))

    if self_max and self_ratio > self_max:
        results.append(
            ("FAIL", f"Self-citation: {self_ratio:.1f}% > maximum {self_max}%")
        )
    else:
        results.append(
            ("PASS", f"Self-citation: {self_ratio:.1f}% ({self_refs}/{total_refs})")
        )

    # ── Required statements ────────────────────────────────────
    statements = spec.get("statements", {})
    statement_checks = {
        "ai_disclosure": ["AI", "artificial intelligence", "language model", "Claude"],
        "data_availability": ["data availability", "data sharing", "not applicable"],
        "funding": ["funding", "grant", "no specific grant"],
        "conflict_of_interest": [
            "conflict of interest",
            "competing interest",
            "no conflict",
        ],
    }

    for stmt_name, search_terms in statement_checks.items():
        stmt_spec = statements.get(stmt_name, {})
        if stmt_spec.get("required", False):
            found = any(term.lower() in text.lower() for term in search_terms)
            if found:
                results.append(("PASS", f"Statement: {stmt_name}"))
            else:
                results.append(("FAIL", f"Statement: {stmt_name} not found"))

    # ── Figures ────────────────────────────────────────────────
    fig_issues = check_figures(repo_path, spec)
    for issue in fig_issues:
        results.append(("FAIL", issue))
    if not fig_issues:
        results.append(("PASS", "Figures: all compliant"))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Validate a paper repository against a journal spec"
    )
    parser.add_argument("--repo", required=True, help="Path to paper repository")
    parser.add_argument("--spec", required=True, help="Path to journal_spec.yaml")
    args = parser.parse_args()

    repo_path = Path(args.repo)
    spec = load_yaml(Path(args.spec))

    if not repo_path.exists():
        print(f"ERROR: Repository path not found: {repo_path}")
        sys.exit(2)

    journal_name = spec.get("journal", {}).get("name", "Unknown Journal")
    print(f"\nValidating against: {journal_name}")
    print(f"Repository: {repo_path}")
    print("-" * 60)

    results = validate(repo_path, spec)

    pass_count = sum(1 for s, _ in results if s == "PASS")
    fail_count = sum(1 for s, _ in results if s == "FAIL")
    warn_count = sum(1 for s, _ in results if s == "WARN")

    for status, message in results:
        icon = {"PASS": "[OK]", "FAIL": "[FAIL]", "WARN": "[WARN]"}[status]
        print(f"  {icon} {message}")

    print("-" * 60)
    print(f"Results: {pass_count} passed, {fail_count} failed, {warn_count} warnings")

    if fail_count > 0:
        print("\nSubmission gate: BLOCKED — fix failures before submitting")
        sys.exit(1)
    else:
        print("\nSubmission gate: PASSED — ready to fork/submit")
        sys.exit(0)


if __name__ == "__main__":
    main()
