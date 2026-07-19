#!/usr/bin/env python3
"""Fail if sources reintroduce bloated profile counts without ban context.

Claim lock: CLAIM_LOCK.md · engine: opensmell_engine_truth.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRUTH = json.loads((ROOT / "opensmell_engine_truth.json").read_text())
LIVE = int(TRUTH["metrics"]["live_profiles"])

SKIP_DIR_NAMES = {".git", "__pycache__", ".venv", "venv", "node_modules", "reports"}
SCAN_SUFFIX = {".md", ".py", ".html", ".txt"}
# Files that deliberately document or forbid inflated counts
ALLOWLIST_NAMES = {
    "CLAIM_LOCK.md",
    "VALIDATION.md",
    "BIOMARKER_SPECIFICITY.md",
    "LICENSE_CLARITY.md",
    "SCORECARD.md",
    "INTENDED_USE.md",
    "claim_lint.py",
    "generate_cortex_diagram.py",
    "opensmell_cognitive_cortex.html",
}

BLOATED = re.compile(r"\b2,?401\b|\b2400\+")
BAN_CONTEXT = re.compile(
    r"(?i)(not|never|inflated|false|ban|forbid|do not|don't|replaces|legacy|"
    r"must not|prohibited|without|until true|not production)"
)


def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(p in SKIP_DIR_NAMES for p in path.parts):
            continue
        if path.suffix.lower() not in SCAN_SUFFIX:
            continue
        if path.name.endswith(".bak"):
            continue
        yield path


def line_ok(line: str) -> bool:
    return bool(BAN_CONTEXT.search(line))


def main() -> int:
    issues: list[str] = []
    for path in iter_files():
        if path.name in ALLOWLIST_NAMES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if BLOATED.search(line) and not line_ok(line):
                rel = path.relative_to(ROOT)
                issues.append(f"{rel}:{i}: bloated count without ban context → {line.strip()[:90]}")

    if LIVE != 21:
        issues.append(
            f"engine truth live_profiles={LIVE} "
            f"(update CLAIM_LOCK if this intentional change is real)"
        )

    if issues:
        print("CLAIM LINT FAILED:")
        for item in issues:
            print(f"  · {item}")
        return 1
    print(f"CLAIM LINT OK — live_profiles={LIVE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
