# OpenSmell — Risk Management File (Draft)

**Document type:** ISO 14971-style risk file skeleton  
**Version:** 0.1 draft — 2026-07-17  
**Device/system:** OpenSmell screening-support software + optional MQ-135-class sensor hardware  
**Intended use reference:** `../INTENDED_USE.md`  
**Status:** Draft for internal and counsel review. Not validated clinical risk acceptance.

---

## 1. Scope

This file identifies foreseeable hazards arising from use (and reasonably foreseeable misuse) of OpenSmell as **screening-support / investigational** software, with or without the low-cost gas sensor path. It does **not** accept residual risk for a marketed diagnostic indication — no such indication is claimed.

## 2. System description

| Element | Description |
|---------|-------------|
| Classifier | `open_smell2.py` — 21 live profiles, confidence scoring, alert threshold default 0.7 |
| Logging | Per-cycle CSV audit trail |
| Alerts | Optional routing to Christman AI Family members (care-support context) |
| Hardware (optional) | Arduino-class MCU + MQ-135-class sensor + optional draw fan |
| Data | Client-owned; no sale of biometrics |

## 3. Intended users and environments

- Researchers and institutional pilot teams under protocol  
- Care-organization innovation teams in supervised research settings  
- Not intended as standalone diagnostic decision-maker in routine clinical care  

## 4. Hazard analysis (initial)

Severity scale (draft): **S1** negligible · **S2** minor delay/annoyance · **S3** temporary harm or major false pathway · **S4** serious harm · **S5** catastrophic (death/permanent severe harm).  
Probability (draft qualitative): **P1** rare · **P2** occasional · **P3** probable · **P4** frequent — **to be replaced with data when pilots exist**.

| ID | Hazard | Foreseeable sequence | Harm | S | P (qual) | Risk controls (design / info / procedure) |
|----|--------|----------------------|------|---|----------|-------------------------------------------|
| H01 | False positive high-severity alert (e.g. cancer, sepsis) | Sim or sensor noise triggers match ≥0.7; user treats as diagnosis | Anxiety, unnecessary care seeking, mistrust | S3 | P2–P3 in field until proven | Intended-use labeling; prohibited diagnostic claims; human review required; conservative threshold; SCORECARD collision disclosure |
| H02 | False negative on true metabolic crisis (e.g. ketoacidosis) | User relies on OpenSmell instead of clinical assessment | Delayed care | S4–S5 | Unknown in field | Explicit “not a diagnostic”; no replace-emergency-care language; fail-loud on sensor disconnect |
| H03 | Sensor channel misinterpretation as named chemistry | User believes “benzene channel” = GC-MS benzene | Wrong scientific or clinical conclusion | S3 | P3 if overclaimed | Proxy-band disclaimer in CLAIM_LOCK, INTENDED_USE, UI |
| H04 | Inflated capability claims (historical 2401 profiles) | Partner over-trusts system | Institutional and patient harm via misuse | S3 | Controlled by claim lock | CLAIM_LOCK + claim_lint; archive past language in storage |
| H05 | Alert fatigue | High alert rate in continuous monitoring | Ignored true alerts | S3–S4 | P2–P3 | Per-site threshold tuning; alert rate metrics; human acknowledgment path |
| H06 | Privacy breach of VOC/log data | Unencrypted share, wrong cloud, secondary use | Dignity harm, discrimination risk | S3–S4 | P1–P2 | Client ownership; local-first; no harvest business model; Enterprise terms |
| H07 | Degenerate diabetes T1/T2 treated as separated | UI shows T1 vs T2 as distinct diagnoses | Clinical confusion | S3 | P2 if UI lies | Group scoring honesty; SCORECARD notes |
| H08 | Family auto-routing without human oversight | Automated “intervention” treated as medical order | Inappropriate action | S3–S4 | P2 | Research/care-support framing; human-in-loop policy for pilots |
| H09 | Hardware failure (fan, sensor poison, humidity) silent | Readings drift; classifier still emits confidence | Misleading outputs | S3 | P2 | Fail-loud on disconnect/drift (implementation requirement); QC SOP |
| H10 | Use in LMIC without local clinical pathway | Screening signal with no referral path | Harm from action or inaction | S3–S4 | P2 if scaled early | Access program only with local partner protocol |

## 5. Risk evaluation policy (draft)

Until real-sample and pilot data exist:

- No residual risk is accepted for **diagnostic** use — diagnostic use is **out of scope**.  
- Research use residual risk is acceptable only with: protocol, informed framing, human review, and claim lock.  
- Any marketed claim requires this file to be rewritten with measured rates and formal acceptance.

## 6. Production / post-market (future)

When pilots run: complaint handling, CAPA, versioned software releases, and update of probability columns from observed alert and error rates.

## 7. Open questions for counsel / clinical advisor

1. Preferred US product code / classification pathway for multi-indication screening-support software + sensor.  
2. Whether research-only labeling (RUO) is the correct near-term wrapper for institutional kits.  
3. BAA / HIPAA scope when only research logs are held on-prem at the client site.

## 8. Revision history

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-07-17 | Initial full draft (not a stub index) |

---

© 2025–2026 The Christman AI Project. All Rights Reserved.
