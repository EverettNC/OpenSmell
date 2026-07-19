#!/usr/bin/env bash
# OpenSmell Notice Package — one-command reproduce
# Run from anywhere; resolves OpenSmell repo root automatically.
# Screening-support sim only. Not clinical validation.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

echo ""
echo "  ════════════════════════════════════════════"
echo "  OpenSmell — Notice Package Reproduce"
echo "  Repo root: $ROOT"
echo "  ════════════════════════════════════════════"
echo ""

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found"
  exit 1
fi

echo "── 1/3  Unit + integration tests ──"
python3 -m unittest test_open_smell2 test_alert_integration -q
echo "  Tests: OK"
echo ""

echo "── 2/3  Seeded short inject (alzheimers, 80 cycles) ──"
python3 opensmell_test_loop.py \
  --cycles 80 \
  --inject alzheimers \
  --inject-rate 0.5 \
  --speed turbo \
  --seed 42
echo ""

echo "── 3/3  Claim lint ──"
if [[ -f scripts/claim_lint.py ]]; then
  python3 scripts/claim_lint.py
else
  echo "  (claim_lint.py not found — skip)"
fi

echo ""
echo "  ════════════════════════════════════════════"
echo "  Reproduce complete."
echo "  Live inventory: see NOTICE_PACKAGE/docs/opensmell_engine_truth.json"
echo "  Scorecard:      NOTICE_PACKAGE/docs/SCORECARD.md"
echo "  Methods:        NOTICE_PACKAGE/01_METHODS.md"
echo "  ════════════════════════════════════════════"
echo "  Reminder: simulation / screening-support only."
echo "  Not FDA-approved. Not a clinical diagnostic."
echo ""
