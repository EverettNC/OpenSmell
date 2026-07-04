# OpenSmell — Biomarker Specificity & Classifier Validation

**The Christman AI Project / Luma Cognify AI** · synthetic-data R&D
Screening-support only. Not FDA-approved. Not a clinical device. Not deployed.
Every figure below is closed-loop simulation output, **not clinical accuracy.**

---

## What this round did

The prior round scaled the profile library from 16 to 26 conditions. Accuracy
on labeled synthetic data *dropped* from 79% to 43.8% — a real, expected result:
adding profiles that share VOC channels, without adding *discriminating* markers,
makes conditions collide. This round fixed that with literature-grounded
biomarkers and a specificity-aware confidence score.

## Headline (labeled synthetic data, 63,000 injected cycles)

| Stage | Top-1 accuracy |
|-------|----------------|
| 16-profile baseline | 79.3% |
| 26 profiles, no discriminating markers | 43.8% |
| **26 profiles + literature markers + specificity score** | **78.8%** |

Accuracy recovered to baseline **while covering 5 more live conditions**.
Confidence–correctness correlation flipped from **negative** (most-confident =
least-accurate) to **+0.39**. Background false-alert rate at the 0.7 alert
threshold dropped from ~24% to **~0%**.

These are self-consistency numbers on a closed-loop simulator (the same
signatures drive injection and scoring). They measure classifier separability,
**not clinical sensitivity/specificity.**

## The three degenerate pairs

Before this round, three profile pairs resolved to a single identical sensor
channel — physically indistinguishable, one twin always at 0% recall:

| Pair | Was | Fix | Grounding |
|------|-----|-----|-----------|
| Bladder cancer vs. Renal failure | both `{ammonia}` | bladder → `{alkanes, benzene}`, renal stays `{ammonia}` | Urinary VOC panels: bladder cancer elevates alkanes + aromatics, distinct from uremic ammonia (Metabolites 2021; Sci Rep 2025) |
| C. difficile vs. Sepsis | both `{aliphatic_acids}` | c_diff adds `{propanol, skatole}` | C. diff carries 1-propanol + indole/4-methylphenol (PLoS ONE 2019; J Breath Res 2024) |
| Diabetes T1 vs. T2 | both `{acetone}` | **not faked** — grouped as one class | No VOC species separates T1 from T2; both are acetone ketosis. Only a quantitative acetone shift exists in small studies. |

**Diabetes T1/T2 was deliberately NOT given a fabricated discriminator.**
Inventing a marker to lift the accuracy number would make the device
confidently wrong in the field. Instead it is declared inseparable
(`DEGENERATE_GROUPS`) and scored at the group level: the honest claim is
"detects diabetic ketosis," not "tells T1 from T2."

## The specificity-aware confidence score

Old: `confidence = coverage × mean_intensity`. A 1-channel profile
(tuberculosis = `{alkanes}`) always tied at coverage 1.0 and won on raw
intensity — stealing detections from multi-channel conditions and firing on
single-channel noise.

New: `confidence = min(1, coverage × mean_intensity × √matched / √max_sig_len)`.
The √matched term rewards profiles that explain *more* of the signal, so lung
cancer (`{alkanes, benzene, aldehydes}`) beats TB when all three fire, and lone
high channels no longer clear the alert bar.

## Honest limitations

- Synthetic self-consistency numbers, not clinical accuracy. Real breath-VOC
  screening tops out ~85–94% sensitivity/specificity on actual samples.
- Remaining single-channel profiles (renal, sepsis, alzheimers, bladder) still
  confuse with conditions that superset their signature — see the confusion
  matrix. Each needs its own discriminating marker before it is reliable.
- The MQ-135 sensor stack does not literally resolve "benzene" vs "indole" as
  named species; channel names are proxies for cross-sensitive response bands.
  Real-sample validation is required before any of this maps to biology.

## Tests

22 unit tests pass (`python -m unittest test_open_smell2`), including 6 new
guards that lock in: bladder/renal separation, C.diff/sepsis separation,
diabetes grouping (not faked), specificity ranking, confidence bounding, and
single-channel background rejection.
