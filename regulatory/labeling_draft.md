# OpenSmell — Labeling Draft

**Version:** 0.1 draft — 2026-07-17  
**Applies to:** Software UI, README medical audiences, Science Kit packaging, institutional demos  
**Status:** Draft. Aligns with `../INTENDED_USE.md` and `../CLAIM_LOCK.md`.

---

## 1. Required short label (always visible in medical/institutional contexts)

```
OpenSmell — Screening-support software.
Not FDA-approved. Not for clinical diagnosis.
Performance figures from simulation are not clinical accuracy
unless a specific study is cited as human-sample data.
Sensor channel names are response-band proxies, not GC-MS species IDs.
Client owns all biological data. Never sold.
Live inventory: 21 sensor-grounded profiles (see engine truth).
```

## 2. Required long label (package insert / methods pack)

**Product name:** OpenSmell  
**Manufacturer / developer:** The Christman AI Project / Luma Cognify AI (Everett N. Christman)  

**Description:**  
Software that accepts VOC-related sensor channel readings (from optional low-cost gas sensors or from simulation) and reports similarity scores against a fixed library of literature-grounded profiles. Optional alert routing to other Christman AI Family systems is for care-support workflows under human oversight.

**Intended use:**  
See `INTENDED_USE.md`. Screening-support and investigational research use. Not a substitute for professional medical advice, diagnosis, or treatment.

**Contraindications / do not use for:**  
- Emergency triage as sole decision tool  
- Autonomous diagnosis or treatment orders  
- Any claim of clinical accuracy without a cited human-sample study  

**Warnings:**  
- False positives and false negatives can occur.  
- Environmental VOCs, humidity, sensor aging, and user error affect readings.  
- Diabetes type 1 and type 2 are not separated by VOC on this system; ketosis-class signals may be grouped.  
- Do not interpret confidence scores as probabilities of disease in a patient population until clinical validation is published for that indication.

**Performance summary (simulation only):**  
Cite only numbers from `VALIDATION.md`, `BIOMARKER_SPECIFICITY.md`, and `SCORECARD.md`, each time stating **simulation**.

## 3. Prohibited label language

Do not print or display:

- “Diagnoses [disease]”  
- “FDA approved” / “FDA cleared” / “CE marked” (until true)  
- “2,401 profiles” or any inflated count  
- “Clinically proven” without a specific study citation that is actually clinical  
- “Detects cancer with X% accuracy” using sim numbers without the word simulation  

## 4. UI string examples

**Allowed:**  
`Match: lung_cancer profile · confidence 0.82 · screening-support only · not a diagnosis`

**Forbidden:**  
`Diagnosis: Lung Cancer · 82% certain`

## 5. Versioning

Any change to this labeling draft that weakens warnings or inflates claims requires:

1. Full prior version archived to EverettNC/storage per `ARCHIVE_POLICY.md`  
2. Claim lint pass  
3. Update to INTENDED_USE if scope changes  

## 6. Revision history

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-07-17 | Initial full labeling draft |

---

© 2025–2026 The Christman AI Project. All Rights Reserved.
