#!/usr/bin/env python3
"""Closed-loop labeled synthetic experiment for open_smell2 classifier."""

from __future__ import annotations

import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from open_smell2 import (
    PROFILE_SIGNATURES,
    SCENT_PROFILES,
    SENSOR_CHANNELS,
    classify_top,
    same_group,
)
from opensmell_bio_sim import bio_simulate_sensor_reading, generate_patient_baseline

CYCLES_PER_PROFILE = 3000
RNG = random.Random(42)
INJECTION_PROFILES = {k: {"vocs": v} for k, v in PROFILE_SIGNATURES.items()}
PATIENT_BASELINE = generate_patient_baseline(SENSOR_CHANNELS)


def synthetic_reading(profile_key: str) -> dict[str, float]:
    """Biologically realistic labeled injection (closed-loop, always inject)."""
    return bio_simulate_sensor_reading(
        SENSOR_CHANNELS,
        INJECTION_PROFILES,
        inject_profile=profile_key,
        inject_rate=1.0,
        patient_baseline=PATIENT_BASELINE,
    )


def run() -> None:
    rows: list[dict[str, str | float | int]] = []
    per_profile_hits: Counter[str] = Counter()
    per_profile_total: Counter[str] = Counter()
    conf_correct: list[tuple[float, int]] = []

    for true_key in sorted(PROFILE_SIGNATURES):
        prof = SCENT_PROFILES[true_key]
        for _ in range(CYCLES_PER_PROFILE):
            reading = synthetic_reading(true_key)
            top = classify_top(reading)
            pred_key = top["profile_key"] if top else ""
            confidence = top["confidence"] if top else 0.0
            exact = int(pred_key == true_key)
            group = int(same_group(pred_key, true_key)) if pred_key else 0
            per_profile_total[true_key] += 1
            if group:
                per_profile_hits[true_key] += 1
            if top:
                conf_correct.append((confidence, exact))
            rows.append({
                "true_key": true_key,
                "true_condition": prof.condition,
                "pred_key": pred_key,
                "pred_condition": SCENT_PROFILES[pred_key].condition if pred_key else "",
                "confidence": confidence,
                "exact_correct": exact,
                "group_correct": group,
            })

    total = len(rows)
    exact_acc = sum(int(r["exact_correct"]) for r in rows) / total
    group_acc = sum(int(r["group_correct"]) for r in rows) / total

    if conf_correct:
        mean_c = sum(c for c, _ in conf_correct) / len(conf_correct)
        mean_correct = sum(e for _, e in conf_correct) / len(conf_correct)
        cov = sum((c - mean_c) * (e - mean_correct) for c, e in conf_correct) / len(conf_correct)
        std_c = math.sqrt(sum((c - mean_c) ** 2 for c, _ in conf_correct) / len(conf_correct))
        std_e = math.sqrt(sum((e - mean_correct) ** 2 for _, e in conf_correct) / len(conf_correct))
        corr = cov / (std_c * std_e) if std_c and std_e else 0.0
    else:
        corr = 0.0

    bg_alerts = 0
    bg_total = 5000
    for _ in range(bg_total):
        reading = {ch: round(RNG.uniform(0.03, 0.35), 3) for ch in SENSOR_CHANNELS}
        top = classify_top(reading)
        if top and top["confidence"] >= 0.7:
            bg_alerts += 1
    bg_false_rate = bg_alerts / bg_total

    out_csv = Path("opensmell2_labeled_experiment.csv")
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    recall_csv = Path("opensmell2_per_profile_recall.csv")
    with recall_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["profile_key", "condition", "n_channels", "group_recall"])
        for key in sorted(per_profile_total, key=lambda k: per_profile_hits[k] / per_profile_total[k]):
            recall = per_profile_hits[key] / per_profile_total[key]
            w.writerow([
                key,
                SCENT_PROFILES[key].condition,
                len(PROFILE_SIGNATURES[key]),
                round(recall, 3),
            ])

    print(f"Profiles: {len(PROFILE_SIGNATURES)}")
    print(f"Cycles:   {total}")
    print(f"Top-1 accuracy (exact): {exact_acc:.1%}")
    print(f"Top-1 accuracy (group): {group_acc:.1%}")
    print(f"Confidence-correctness correlation: {corr:+.3f}")
    print(f"Background false-alert rate @0.7: {bg_false_rate:.1%}")
    print(f"Wrote {out_csv} and {recall_csv}")

    for target in ("renal_failure", "sepsis"):
        c: Counter[str] = Counter()
        for r in rows:
            if r["true_key"] == target:
                c[str(r["pred_key"])] += 1
        print(f"\n{target} confusion:")
        for k, v in c.most_common(5):
            print(f"  {k}: {v/ per_profile_total[target]:.1%}")


if __name__ == "__main__":
    run()