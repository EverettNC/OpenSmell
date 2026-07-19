# OpenSmell — Sensor Truth (MQ-135 class research)

**The Christman AI Project / Luma Cognify AI**  
**Started:** 2026-07-19  
**Status:** Research in progress — **not** clinical validation  
**Hardware class:** MQ-135 metal-oxide (MOS) gas sensor module + MCU  
**Law:** Channel names in software are **proxy labels**, not GC-MS species IDs.

---

## 1. Why this document exists

OpenSmell’s software library uses **20 named channels** (acetone, isoprene, ammonia, benzene, …).  
A single MQ-135 does **not** chemically resolve those twenty species as independent analytes.

This document states:

1. What the MQ-135 **physically** is  
2. How OpenSmell’s **software channels** relate (honestly)  
3. What experiments we must run next  
4. What we will **never** claim until measured  

Without this file, labs cannot take us seriously — and we would be lying by implication.

---

## 2. Physical sensor: MQ-135 (datasheet-grounded)

### 2.1 Operating principle

- **Metal-oxide semiconductor (MOS / SnO₂-class)** chemoresistor.  
- Heater elevates sensing layer temperature; gas adsorption changes **surface resistance**.  
- Module typically exposes: **VCC, GND, AOUT** (analog voltage via load divider) and sometimes DOUT (threshold).  
- Arduino path: `analogRead(A0)` → relative intensity, **not** ppm without calibration.

### 2.2 Datasheet-stated sensitivities (typical Hanwei / clone MQ-135)

Public datasheets for MQ-135 commonly state sensitivity toward:

| Family | Datasheet examples |
|--------|-------------------|
| Ammonia / NH₃ | Primary calibration suggestion often **100 ppm NH₃** |
| Alcohols | Calibration option **~50 ppm alcohol** |
| Benzene vapor | Listed among sensitive targets |
| Sulfides / smoke / “air quality” blends | Broad response |
| CO₂ | Appears on sensitivity curves but **MQ-135 is a poor CO₂ meter** in practice |

**Critical datasheet notes (standard MQ-135 technical data):**

- Resistance **differs by gas type and concentration** — sensitivity adjustment is required.  
- Curves are typically at fixed **T / RH** (e.g. ~20 °C, ~65% RH); humidity and temperature move Rs strongly.  
- **Ro** is often defined at a reference (e.g. 100 ppm NH₃ in clean air) — without a controlled Ro, “ppm” numbers are fiction.  
- Cross-response is the rule: one analog channel, many gases.

### 2.3 What one MQ-135 cannot do

| Claim | Reality |
|-------|---------|
| “Measures benzene ppm” as a lab would | **False** without multi-sensor + calibration + reference |
| Separates acetone vs isoprene vs aldehydes as independent GC peaks | **False** on one AOUT |
| Immune to alcohol / cleaner interferents | **False** — alcohols and solvents dominate MOS response |
| Stable forever | **False** — warm-up, drift, aging, poisoning |

### 2.4 What one MQ-135 *can* do (useful for OpenSmell)

| Capability | Use |
|------------|-----|
| Continuous relative air-quality / reducing-gas response | Ambient monitoring research |
| Detect **change** from a room baseline | Spike / trend flags |
| Cheap, deployable Station (~$15–25) | Access / LMIC / multi-room research |
| Pair with software **hypothesis profiles** | Screening-support **ideas** for humans to review |

---

## 3. Software channels vs hardware (truth map)

### 3.1 Software model (`open_smell2.SENSOR_CHANNELS`)

Twenty **named** channels drive profile signatures and the bio-simulator.  
They are a **neuro-symbolic / literature-facing vocabulary**, not twenty independent MQ-135 outputs.

### 3.2 Hardware model (current Station)

| Layer | Output |
|-------|--------|
| MQ-135 AOUT | **One** analog voltage (or Rs/Ro-derived scalar after calibration) |
| Optional fan | Sample turnover, not chemistry |
| Optional future multi-MQ pack | Still coarse bands, not GC-MS |

### 3.3 Honest bridging strategies (research tracks)

| Track | Description | Status |
|-------|-------------|--------|
| **A — Scalar + sim library** | Hardware provides one “activity” intensity; software profiles remain literature-facing for **sim and future multi-sensor** work | Current demo reality for pure hardware |
| **B — Time-series features** | Rise time, recovery, heater PWM patterns as weak fingerprints | Research |
| **C — Multi-sensor array** | MQ-135 + MQ-3 (alcohol) + MQ-7 (CO-class) + humidity/temp + electrochemical if justified | Planned research |
| **D — Reference lab** | GC-MS / calibrated mixtures label sessions; train mapping later | Partner path |

**Claim lock:** Until Track C/D produce published maps, UI and papers must say **proxy / screening-support / sim-validated library**, not “detected benzene at X ppm.”

### 3.4 Literature markers → software channels

`MARKER_ALIASES` in `open_smell2.py` maps descriptive VOC language to software channel names.  
That mapping is **logical**, not a hardware spectrometer.

---

## 4. Characterization protocol (what we run next)

### Level L0 — Software only (done)

```bash
./NOTICE_PACKAGE/reproduce.sh
```

Sim separability only. See `SCORECARD.md`, `VALIDATION.md`.

### Level L1 — Interferent response (Station, no certified gas)

**Goal:** Prove the Station fails loud and responds to known household interferents in a controlled way.

| Step | Action | Record |
|------|--------|--------|
| 1 | Warm-up ≥ 5–10 min; log T/RH if available | time, baseline mean A0 |
| 2 | Clean-air baseline 5 min | mean, std of A0 |
| 3 | Controlled approach: isopropyl alcohol swab 20 cm, 10 s | peak Δ, recovery time |
| 4 | Acetone nail-polish remover (same geometry) | peak Δ, recovery |
| 5 | Ammonia household cleaner (extreme caution, ventilation) | peak Δ, recovery |
| 6 | Return to baseline | recovery minutes |

**Outputs:** CSV with `timestamp, a0_raw, condition_label, notes`.  
**Not** clinical. **Not** ppm.

### Level L2 — Known mixture / headspace (lab)

**Goal:** Partner lab applies known concentrations or headspace standards.

| Requirement | Detail |
|-------------|--------|
| Reference | Certified cylinder or prepared headspace with stated compounds |
| Environment | Logged T, RH, flow, fan state |
| Sensor batch | Module serial / purchase lot |
| Protocol | Baseline → exposure → recovery; ≥3 repeats |
| Analysis | Response curves; interference matrix; compare to software channel **hypotheses** |

**Outputs:** co-authored sensor-truth table (compound × response), **not** disease accuracy.

### Level L3 — Human samples under ethics

Only under IRB / equivalent. Non-diagnostic. Separate protocol document.

---

## 5. Lab log template (copy per session)

```text
OpenSmell Station L1/L2 log
Date (UTC):
Operator:
MCU:
MQ module lot/ID:
Firmware / git commit:
Warm-up minutes:
Baseline A0 mean/std:
Fan: on/off duty:
Ambient T/RH:
Exposure sequence:
  1) ...
  2) ...
Raw CSV path:
Notes / anomalies:
Claim reminder: proxy sensor, not diagnosis, not FDA-approved.
```

---

## 6. Research questions (active)

1. What is the **minimum multi-sensor set** that can support more than a single activity scalar for OpenSmell’s strongest profiles (e.g. ketosis/acetone-class vs ammonia-class vs alcohol interferent)?  
2. How stable is baseline over 24–72 h continuous?  
3. Does active fan PWM improve recovery enough to justify always-on airflow?  
4. Which software channels are **purely literature placeholders** for multi-sensor future vs tied to plausible MOS bands today?  
5. What L2 partner setup is cheapest that still produces publishable methods (not disease claims)?

---

## 7. Immediate build / lab tasks

| # | Task | Owner pattern |
|---|------|----------------|
| 1 | This document (sensor truth) | Done 2026-07-19 |
| 2 | Optional: Arduino sketch + host logger writing L1 CSV schema | Engineering next |
| 3 | Run L1 interferent session; attach CSV to `reports/sensor_l1/` | Lab / Everett |
| 4 | Outreach using `NOTICE_PACKAGE/` + this file | Everett / partners |
| 5 | Draft multi-MQ BOM for Track C | Engineering after L1 |

---

## 8. What we will not claim after this research

- That software profile names equal physical pure compounds on one MQ-135  
- Clinical sensitivity/specificity from Station-only data  
- “FDA approved” or diagnostic language  
- Inflated live profile counts  

---

## 9. References (starting set)

- Manufacturer technical data sheets for **MQ-135** (Hanwei / equivalent clones): sensitivity curves, Ro definition, T/RH dependence, NH₃ / alcohol calibration suggestions.  
- OpenSmell in-repo: `NOTICE_PACKAGE/02_HARDWARE_STATION.md`, `open_smell2.py`, `CLAIM_LOCK.md`, `VALIDATION.md`.  
- Partner literature on breath VOC / e-nose limitations (cross-sensitivity, humidity) when designing L2.

*(Add DOI / exact datasheet revision as L1/L2 runs complete — do not invent citations.)*

---

## 10. Link to institutional plan

Sensor truth is **Step 1 of “next moves”** after notice package.  
Labs open: `NOTICE_PACKAGE/` + this file.  
Scale and clinical claims wait on L2/L3 evidence.

---

© 2025–2026 The Christman AI Project. All Rights Reserved.
