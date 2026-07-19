# OpenSmell — Hardware Station SOP

**The Christman AI Project / Luma Cognify AI**  
**Station goal:** low-cost continuous VOC **proxy** sensing for research and screening-support software  
**Not a cleared medical device. Not GC-MS.**

---

## 1. Bill of materials (approximate USD)

| Component | Approx. cost | Notes |
|-----------|--------------|--------|
| Arduino Nano or Uno R3 class MCU | ~$8–12 | USB serial to host |
| MQ-135 gas sensor module | ~$3–5 | Cross-sensitive VOC module |
| 5V active draw fan (small) | ~$2–4 | Improves sample turnover; PWM optional on D9 |
| Jumper wires | ~$2–4 | Female–male as needed |
| USB cable | ~$2 | Host connection |
| **Typical total** | **~$15–25** | Hobby / research build |

Optional later: multi-sensor pack, humidity sensor, sealed manifold — not required for first software reproduce (sim mode needs **no** hardware).

---

## 2. Wiring (no soldering required for first bring-up)

```
MQ-135 VCC  → Arduino 5V
MQ-135 GND  → Arduino GND
MQ-135 AOUT → Arduino A0
```

Optional fan:

```
Fan + / MOSFET drive ← Arduino D9 (PWM) via appropriate driver
Fan GND → common ground
```

**Do not** power high-current fans directly from a logic pin without a transistor/MOSFET and flyback diode.

---

## 3. Firmware / serial path

Intended path:

1. Upload Arduino sketch that samples A0 and streams readings over USB serial (project may ship `opensmell_sensor.ino` when present; if missing, any sketch that emits stable analog samples is acceptable for hardware experiments).  
2. Host Python process reads serial, normalizes to channel intensities or a raw proxy vector, then calls `open_smell2.classify()`.  
3. Simulation path (default for this notice pack): **no Arduino** — `opensmell_test_loop.py` + `opensmell_bio_sim.py`.

Hardware mode dependencies (when used):

```bash
pip install pyserial colorama
```

---

## 4. Warm-up and operating notes

| Step | Guidance |
|------|----------|
| Power-on warm-up | MQ-series sensors often need minutes of heat-up before stable resistance; discard early samples |
| Baseline | Capture ambient baseline in the same room geometry before interpreting spikes |
| Airflow | Fan on → more turnover; fan off → slower response, different baseline |
| Humidity / temperature | Strong confounders for MOS sensors; log them if available |
| Contaminants | Alcohols, cleaners, smoke will dominate — log environment |
| Poisoning / aging | MOS sensors drift; batch-mark hardware and re-baseline |

---

## 5. QC checklist (every station)

Before any research session:

- [ ] Wiring verified (VCC / GND / AOUT only on intended pins)  
- [ ] USB enumerates; serial port opens at expected baud  
- [ ] Warm-up completed (time logged)  
- [ ] Ambient baseline captured and stored  
- [ ] Fan state recorded (on/off, PWM duty if used)  
- [ ] Software version / git commit of `open_smell2.py` recorded  
- [ ] Claim lock understood: proxy channels, not species IDs  
- [ ] No diagnostic language in logs or UI  

Fail loud if:

- Serial disconnect mid-session  
- Readings stuck at rail (0 or max) for sustained period  
- Sensor not warming (if heater supply failed)  

---

## 6. Calibration philosophy (honest)

| Level | What it is | Status in this pack |
|-------|------------|---------------------|
| L0 | Software sim only | **Available now** via `reproduce.sh` |
| L1 | Ambient + known interferent response (alcohol swab near sensor, etc.) | Partner / lab exercise |
| L2 | Known VOC mixture headspace vs channel map | **Planned** — sensor truth step |
| L3 | Human breath/skin under IRB | **Not in this pack** — research path |

Until L2/L3 exist, **do not** claim calibrated clinical performance.

---

## 7. Data handling on station

- Default: **local CSV audit trail** on the host  
- Client / site owns data  
- No automatic upload to Christman servers in the open research path  
- If cloud is used later, only under explicit contract and consent  

---

## 8. Safety

- 5V electronics only for this BOM; follow basic lab electrical safety  
- Not for use in explosive atmospheres or as a life-support monitor  
- Not a fire, gas-leak, or CO detector certification path  

---

## 9. Cost and access intent

The Station is intentionally **cheap** so screening-support research is not locked to capital equipment. Serious chemistry still needs reference methods (GC-MS, standardized breath collection). OpenSmell’s role is continuous **proxy** monitoring + honest classification software — not replacing reference labs.

---

© 2025–2026 The Christman AI Project. All Rights Reserved.
