# OpenSmell — Intended Use & Prohibited Claims

**The Christman AI Project / Luma Cognify AI**  
**Document version:** 1.0 — 2026-07-17  
**Status:** Screening-support / investigational software description  
**Not a marketing brochure.**

---

## Intended use (current)

OpenSmell is **screening-support software** that:

1. Accepts VOC-related sensor channel readings (hardware or simulation)  
2. Matches those readings against a fixed set of **literature-grounded, sensor-proxy profiles**  
3. Logs matches, confidence scores, and optional alerts for review by a human  
4. May optionally route alerts to other Christman AI Family systems for **care support workflows** (not diagnosis)

**Intended users (near-term):** researchers, developers, care-organization innovation teams, and institutional partners under research or investigational protocols.

**Intended setting:** laboratory, research pilot, or controlled care-research environment — not as a standalone diagnostic in routine clinical care.

---

## What OpenSmell is not

| Not | Why |
|-----|-----|
| **Not FDA-approved** | No clearance or approval has been obtained |
| **Not a clinical diagnostic device** | Does not establish, rule out, or confirm disease |
| **Not a substitute for a clinician** | Humans retain decision authority |
| **Not a claim of clinical accuracy** | Published metrics to date are **simulation / synthetic** unless a later study states otherwise |
| **Not a data-harvest product** | Client owns biological signals; never sold |

---



## Allowed claims (when true and sourced)

- Inventory: 21 live / 26 catalog / 5 research_only / 20 channels  
- Simulation metrics as measured in `VALIDATION.md`, `BIOMARKER_SPECIFICITY.md`, `SCORECARD.md`  
- “Screening-support,” “investigational,” “research use,” “not for diagnosis”  
- Hardware BOM approximate cost and wiring  
- Client data sovereignty and Dignity Clause  
- That a regulatory / clinical evidence path is **being prepared** (not completed)  

---

## Labeling snippet (copy for demos and packages)

> OpenSmell is screening-support software. Not FDA-approved. Not for clinical diagnosis.  
> Current performance figures are from closed-loop simulation unless otherwise stated.  
> Sensor channel names are response-band proxies. Client owns all biological data.

---

## Device system description (high level)

| Element | Description |
|---------|-------------|
| Software | `open_smell2.py` classifier, alert router, audit CSV logging |
| Hardware (optional) | Arduino-class MCU + MQ-135-class gas sensor + optional draw fan |
| Data | Local logs; client-controlled; no sale of biometrics |
| Optional link | Christman AI Family alert routing (research / care-support context) |

Regulatory class, Q-Sub content, and risk file live under `regulatory/` when those drafts exist.

---

## Contact

**Everett Nathaniel Christman**  
Founder — The Christman AI Project  
Operating under Luma Cognify AI  

© 2025–2026 The Christman AI Project. All Rights Reserved.  
