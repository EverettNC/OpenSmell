"""
OpenSmell Biological Simulation Engine
The Christman AI Project — Luma Cognify AI
Author: Everett Christman + Claude (grounding board)

Replaces flat random VOC generation with biologically realistic distributions.
"""

import random
import math
from collections import defaultdict

def lognormal_voc(mean_log=0.0, sigma=0.8, clip_min=0.01, clip_max=1.0):
    raw = math.exp(random.gauss(mean_log, sigma))
    return round(min(max(raw / (raw + 1), clip_min), clip_max), 3)

VOC_COVARIANCE_GROUPS = [
    {"members": ["isoprene", "acetone", "ethane"],        "correlation": 0.65},
    {"members": ["ammonia", "dimethyl_sulfide", "sulfur"], "correlation": 0.70},
    {"members": ["lipid_oxidation", "aldehydes", "alkanes"],  "correlation": 0.72},
    {"members": ["acetone", "propanol", "ketones"],        "correlation": 0.75},
    {"members": ["skatole", "sulfur", "ammonia"],          "correlation": 0.55},
]

DIURNAL_PHASES = {
    "morning":   {"description": "Post-sleep, fasting state", "elevated": ["acetone", "isoprene", "ketones"], "suppressed": ["ethanol_trace", "sulfur"], "multiplier": 1.35},
    "afternoon": {"description": "Post-meal, active metabolism", "elevated": ["ammonia", "dimethyl_sulfide"], "suppressed": ["ketones", "acetone"], "multiplier": 1.0},
    "evening":   {"description": "Late day, metabolic wind-down", "elevated": ["hydrocarbons", "alkanes"], "suppressed": ["isoprene"], "multiplier": 0.9},
    "night":     {"description": "Sleep-adjacent, low metabolic rate", "elevated": ["lipid_oxidation", "sebum_vocs"], "suppressed": ["ammonia", "isoprene"], "multiplier": 0.75},
}

def get_diurnal_phase():
    return random.choices(["morning", "afternoon", "evening", "night"], weights=[25, 40, 25, 10])[0]

def generate_patient_baseline(all_vocs):
    baseline = {}
    for voc in all_vocs:
        if random.random() < 0.15:
            baseline[voc] = round(random.uniform(0.15, 0.35), 3)
        else:
            baseline[voc] = round(random.uniform(0.01, 0.12), 3)
    return baseline

BACKGROUND_NOISE_VOCS = ["toluene", "ethane", "butane", "methane_trace", "ethanol_trace", "propanol"]

def inject_biological_noise(reading):
    num_noise = random.randint(1, 4)
    noise_vocs = random.sample(BACKGROUND_NOISE_VOCS, k=min(num_noise, len(BACKGROUND_NOISE_VOCS)))
    for voc in noise_vocs:
        existing = reading.get(voc, 0.0)
        noise_level = lognormal_voc(mean_log=-1.5, sigma=0.5)
        reading[voc] = round(min(existing + noise_level, 1.0), 3)
    return reading

def apply_covariance(reading, all_vocs):
    for group in VOC_COVARIANCE_GROUPS:
        members = group["members"]
        correlation = group["correlation"]
        elevated = [v for v in members if reading.get(v, 0) > 0.4]
        if not elevated:
            continue
        anchor_level = max(reading.get(v, 0) for v in elevated)
        for voc in members:
            if voc not in elevated and voc in all_vocs:
                current = reading.get(voc, 0.05)
                shift = (anchor_level - current) * correlation * random.uniform(0.3, 0.8)
                reading[voc] = round(min(current + shift, 1.0), 3)
    return reading

def bio_simulate_sensor_reading(all_vocs, scent_profiles, inject_profile=None, inject_rate=0.25, patient_baseline=None):
    if patient_baseline is None:
        patient_baseline = generate_patient_baseline(all_vocs)
    phase_key = get_diurnal_phase()
    phase = DIURNAL_PHASES[phase_key]
    reading = {}
    for voc in all_vocs:
        base = patient_baseline.get(voc, 0.05)
        variation = lognormal_voc(mean_log=-0.5, sigma=0.7)
        intensity = round(min(base + variation * 0.4, 1.0), 3)
        if voc in phase["elevated"]:
            intensity = round(min(intensity * phase["multiplier"] * random.uniform(1.1, 1.4), 1.0), 3)
        elif voc in phase["suppressed"]:
            intensity = round(intensity * random.uniform(0.4, 0.7), 3)
        reading[voc] = intensity
    reading["__phase__"] = phase_key
    reading["__phase_desc__"] = phase["description"]
    reading = inject_biological_noise(reading)
    reading = apply_covariance(reading, all_vocs)
    injected_key = None
    def _profile_channels(profile):
        if isinstance(profile, dict):
            return profile.get("vocs", profile.get("channels", []))
        if isinstance(profile, (list, tuple)):
            return list(profile)
        return []
    if inject_profile and inject_profile in scent_profiles:
        if random.random() < inject_rate:
            for voc in _profile_channels(scent_profiles[inject_profile]):
                reading[voc] = round(random.uniform(0.55, 0.95), 3)
            injected_key = inject_profile
            reading["__injected__"] = inject_profile
    elif not inject_profile and random.random() < inject_rate:
        injected_key = random.choice(list(scent_profiles.keys()))
        for voc in _profile_channels(scent_profiles[injected_key]):
            reading[voc] = round(random.uniform(0.55, 0.95), 3)
        reading["__injected__"] = injected_key
    reading["__injected_key__"] = injected_key
    return reading
