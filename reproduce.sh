#!/usr/bin/env bash
# reproduce.sh — Single-command compliance check against example journal specs.
#
# This repository ships the Paper Repo protocol: schemas, example paper repos
# (examples/R13, examples/R14), and the validate_paper.py compliance checker.
# Reproduction here means running the validator against the bundled example
# papers and writing a structured run log to output/logs/.
#
# Conforms to PUBLIC_MIRROR_STANDARD.md v1.0.0.
#
# Usage:
#   ./reproduce.sh                  # Run full validation pass
#   ./reproduce.sh --check-only     # Verify dependencies; do not run validator

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

mkdir -p output/figures output/tables output/logs
LOG_FILE="output/logs/master_run.log"

echo "==================================================" | tee -a "$LOG_FILE"
echo "Pipeline run: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "Repo: $REPO_ROOT" | tee -a "$LOG_FILE"
echo "Git SHA: $(git rev-parse HEAD 2>/dev/null || echo 'not-a-repo')" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"

CHECK_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --check-only) CHECK_ONLY=1 ;;
    *) echo "Unknown flag: $arg"; exit 2 ;;
  esac
done

# 1. Dependency check
echo ">>> Checking dependencies..." | tee -a "$LOG_FILE"
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found" | tee -a "$LOG_FILE"
  exit 1
fi
python3 -c "import yaml" 2>/dev/null || {
  echo "WARN: PyYAML not installed; attempting pip install --user pyyaml" | tee -a "$LOG_FILE"
  python3 -m pip install --user pyyaml 2>&1 | tee -a "$LOG_FILE" || true
}

if [[ "$CHECK_ONLY" == "1" ]]; then
  echo ">>> Check-only mode; exiting before validation." | tee -a "$LOG_FILE"
  exit 0
fi

# 2. Run validator against bundled examples
VALIDATOR="scripts/validate_paper.py"
SPECS_DIR="examples/journal-specs"

if [[ ! -f "$VALIDATOR" ]]; then
  echo "ERROR: validator not found at $VALIDATOR" | tee -a "$LOG_FILE"
  exit 1
fi

echo ">>> Block 1: Validate example R14 paper against bundled journal specs" | tee -a "$LOG_FILE"
if [[ -d examples/R14 && -d "$SPECS_DIR" ]]; then
  for spec in "$SPECS_DIR"/*.yaml; do
    [[ -f "$spec" ]] || continue
    echo "--- spec: $spec" | tee -a "$LOG_FILE"
    python3 "$VALIDATOR" --repo examples/R14 --spec "$spec" 2>&1 | tee -a "$LOG_FILE" || true
  done
else
  echo "SKIP: examples/R14 or $SPECS_DIR not present" | tee -a "$LOG_FILE"
fi

echo ">>> Block 2: Validate example R13 paper against bundled journal specs" | tee -a "$LOG_FILE"
if [[ -d examples/R13 && -d "$SPECS_DIR" ]]; then
  for spec in "$SPECS_DIR"/*.yaml; do
    [[ -f "$spec" ]] || continue
    echo "--- spec: $spec" | tee -a "$LOG_FILE"
    python3 "$VALIDATOR" --repo examples/R13 --spec "$spec" 2>&1 | tee -a "$LOG_FILE" || true
  done
else
  echo "SKIP: examples/R13 or $SPECS_DIR not present" | tee -a "$LOG_FILE"
fi

echo "==================================================" | tee -a "$LOG_FILE"
echo "Pipeline complete: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"
