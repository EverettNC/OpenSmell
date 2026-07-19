# OpenSmell — SaMD / Device Classification Memo (Draft)

**Version:** 0.1 draft — 2026-07-17  
**Author framing:** Internal technical memo for counsel and regulatory consultant  
**Status:** Not a formal submission. Not a determination of class.

---

## 1. Purpose

Sketch how OpenSmell may be viewed under US FDA software as a medical device (SaMD) concepts and EU MDR, so Q-Sub questions are concrete. Final classification requires counsel and, if pursued, FDA feedback.

## 2. Product under analysis

| Layer | Description |
|-------|-------------|
| Software | VOC profile matching, confidence scores, alerts, audit logs |
| Hardware (optional) | Low-cost metal-oxide gas sensor path (MQ-135 class) + MCU |
| Claims today | Screening-support / investigational; **not** diagnosis; **not** FDA-approved |
| Evidence today | Closed-loop simulation; no multi-site human clinical performance study in this repo |

## 3. US FDA — working sketch

### 3.1 Is it a device?

If marketed for use in diagnosis, cure, mitigation, treatment, or prevention of disease, software and/or sensor system may be a device. OpenSmell’s **current intended use** is written to stay in **screening-support / research** framing. Expanding to clinical decision claims increases device regulatory burden.

### 3.2 SaMD risk framing (IMDRF-style, qualitative)

| Factor | OpenSmell today | Notes |
|--------|-----------------|-------|
| Significance of information | Inform / drive clinical management if misused as diagnosis | Must remain “inform” via labeling |
| State of healthcare situation | Non-serious → serious depending on profile (e.g. sepsis vs mood proxy) | Multi-indication increases complexity |
| Preferred near-term posture | Narrow investigational / RUO packaging + Q-Sub before broad claims | Aligns with aggressive path without illegal marketing |

### 3.3 Likely engagement path

1. **Q-Submission** — ask classification, evidence expectations, multi-indication strategy.  
2. Evidence generation on **narrow first indication** while sim covers all 21.  
3. Possible **De Novo** or **510(k)** only if predicate/logic and data support — undetermined until Q-Sub feedback.  
4. Do **not** claim 510(k) cleared or De Novo granted until true.

## 4. EU MDR — working sketch

| Topic | Sketch |
|-------|--------|
| Software | MDR applies to software with medical purpose when CE-marked as device |
| Near-term | Research use / non-CE investigational paths with ethics approval may apply before CE |
| Class | Indication-dependent; multi-disease oncology claims tend higher class |
| Partner | Notified Body engagement only after intended use locked and clinical plan funded |

## 5. Multi-indication strategy

Simultaneous **marketing** of all 21 conditions as clinical claims is high risk and high cost. Recommended:

- **Inventory:** all 21 live in software and sim scorecard (truthful capability surface).  
- **Regulatory claims:** sequence evidence waves (metabolic/psych → infectious → neuro → oncology) as in the institutional plan.  
- **Labeling:** only cleared/authorized indications appear as clinical claims; others remain research.

## 6. Hardware

MQ-135-class sensors are **not** treated here as GC-MS equivalents. Any device file must describe **cross-sensitive response bands** and environmental confounders (humidity, interferents, ambient VOCs).

## 7. Cybersecurity and privacy

On-prem default, client-owned data, optional cryptographic hardening (including post-quantum libraries where used) should be described in future premarket cybersecurity documentation. Not a medical claim.

## 8. Open questions for Q-Sub

See `q_sub_outline.md`.

## 9. Revision history

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-07-17 | Initial full memo |

---

© 2025–2026 The Christman AI Project. All Rights Reserved.
