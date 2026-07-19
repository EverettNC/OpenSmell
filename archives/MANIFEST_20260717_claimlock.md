# OpenSmell Claim-Lock Correction Archive

**Project:** OpenSmell (The Christman AI Project / Luma Cognify AI)  
**Archive ID:** 20260717_claimlock_precorrection  
**Created:** 2026-07-17  
**Reason:** Claim-lock pass removed inflated profile counts (e.g. 2,401 / 2400+) and aligned outbound language with `opensmell_engine_truth.json` (21 live profiles). Past versions are preserved here. Nothing is erased.

## Cardinal rules applied

1. **Never erase the past** — prior file text is stored under `git_HEAD_before_claimlock/` and `existing_bak_files/`.
2. **Never use stubs / truncated / placeholders** — this archive is complete file bodies only.
3. **Corrections are additive** — current corrected snapshot is also stored under `post_claimlock_snapshot/`.

## Layout

| Path | Contents |
|------|----------|
| `git_HEAD_before_claimlock/` | Full file bodies from OpenSmell `git HEAD` immediately before claim-lock working-tree edits |
| `existing_bak_files/` | On-disk `.bak` / `.polluted.bak` already in the OpenSmell tree |
| `post_claimlock_snapshot/` | Corrected files + new claim-lock docs as of archive time |
| `meta/MANIFEST.md` | This document |
| `meta/FILE_LIST.txt` | Path listing with byte sizes |
| `meta/SHA256SUMS.txt` | Checksums of every archived file |

## Files recovered from git HEAD

- OPENSMELL_VIDEO_SCRIPT.md
- README.md
- lineage.py
- open_smell.py
- open_smell_human.py
- opensmell_test_loop.py
- opensmell_test_loopV2.py
- profiles.py

## What changed (summary)

- Inflated “2,401 / 2400+ profiles” language → **21 live profiles** (truth-locked)
- New: CLAIM_LOCK.md, SCORECARD.md, INTENDED_USE.md, LICENSE_CLARITY.md, scripts/claim_lint.py, regulatory docs
- Simulation metrics only; not clinical accuracy; not FDA-approved

## Restore example

```bash
# Restore one file’s pre-correction body into a working copy (review first)
unzip -p OpenSmell_claimlock_precorrection_20260717.zip \
  git_HEAD_before_claimlock/lineage.py > /tmp/lineage.py.pre
diff -u /tmp/lineage.py.pre /path/to/OpenSmell/lineage.py
```

## Source repo

OpenSmell: https://github.com/EverettNC/OpenSmell  
Storage destination: https://github.com/EverettNC/storage  

