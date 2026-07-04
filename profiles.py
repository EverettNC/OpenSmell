Skip to main content


OpenSmell — Simulation Validation Brief The Christman AI…


New

Customize
Today

26


Artifacts
Search artifacts…
26 artifacts



▸
Your uploads
16 · 1h ago

opensmell_te
st_loop.py
10m ago · Claude Science




opensm
ell_log.csv
52m ago




lineage.py
52m ago




profiles.py
52m ago




alert.py
52m ago




opensmell_report_20260401
_221230.txt
52m ago




opensmell_report_20260401
_221530.txt
52m ago




opensmell_report_20260401
_224837.txt
52m ago




ope
n_smell.py
52m ago




opensmell_report_20260401
_232349.txt
52m ago




opensmell_report_20260402
_010942.txt
52m ago




opensmell_report_20260401
_223325.txt
52m ago




opensmell_report_20260401
_222405.txt
52m ago




opensmell_report_20260401
_220952.txt
52m ago




opensmell_report_20260402
_113241.txt
52m ago






onboarding-
profile.md
55m ago




▸
OpenSmell VOC Dataset Analysis Pipeline
10 · 1h ago

opensmell2_confusion_matrix.png
opensmell2_confusion
_matrix.png
4m ago · Claude Science




opensmell_calibration.png
opensmell_cali
bration.png
45m ago · Claude Science




opensmell_precision_recall.png
opensmell_precision
_recall.png
45m ago · Claude Science




opensmell_confusion_matrix.png
opensmell_confusion
_matrix.png
45m ago · Claude Science




opensmell2_labeled_exp
eriment.csv
4m ago · Claude Science




opensmell2_per_profile
_recall.csv
4m ago · Claude Science




opensmell_labeled_exp
eriment.csv
45m ago · Claude Science




opensmell_per_profile_
metrics.csv
45m ago · Claude Science










opensmell_validation
_report.md
45m ago · Claude Science




open
_smell2.py
4m ago · Claude Science



profiles.py





"""
OpenSmell Scent Profile Database + Translation Engine
Condensed core set (expandable to 2401+). Logic adapted from opensmell_test_loop.py
for VOC classification, anomaly detection, and alert translation.
"""

from typing import Any, Dict, List, Optional

# SCENT PROFILES (from opensmell_test_loop.py core — behavioral + pathological)
SCENT_PROFILES: Dict[str, Dict[str, Any]] = {
    # Emotional / Behavioral (Phase 1)
    "cortisol_spike": {
        "category": "behavioral",
        "condition": "Stress / Rage Onset",
        "vocs": ["acetone", "isoprene"],
        "alert": True,
        "severity": "high",
    },
    "serotonin_drop": {
        "category": "behavioral",
        "condition": "Depressive Spiral",
        "vocs": ["dimethyl_sulfide", "acetone"],
        "alert": True,
        "severity": "high",
    },
    "adrenaline_surge": {
        "category": "behavioral",
        "condition": "Fight-or-Flight Escalation",
        "vocs": ["isoprene", "ammonia"],
        "alert": True,
        "severity": "critical",
    },
    "neurological_prefit": {
        "category": "behavioral",
        "condition": "Pre-Seizure / Fit Warning",
        "vocs": ["ammonia", "alkanes"],
        "alert": True,
        "severity": "critical",
    },
    "calm_baseline": {
        "category": "behavioral",
        "condition": "Calm / Stable",
        "vocs": ["ethanol_trace", "isoprene"],
        "alert": False,
        "severity": "none",
    },
    # Oncology (Phase 2)
    "lung_cancer": {
        "category": "oncology",
        "condition": "Lung Cancer",
        "vocs": ["alkanes", "benzene", "aldehydes"],
        "alert": True,
        "severity": "critical",
    },
    "breast_cancer": {
        "category": "oncology",
        "condition": "Breast Cancer",
        "vocs": ["aliphatic_acids", "hydrocarbons"],
        "alert": True,
        "severity": "critical",
    },
    "colorectal_cancer": {
        "category": "oncology",
        "condition": "Colorectal Cancer",
        "vocs": ["ammonia", "sulfur", "skatole"],
        "alert": True,
        "severity": "critical",
    },
    "ovarian_cancer": {
        "category": "oncology",
        "condition": "Ovarian Cancer",
        "vocs": ["aldehydes", "hydrocarbons"],
        "alert": True,
        "severity": "critical",
    },
    "prostate_cancer": {
        "category": "oncology",
        "condition": "Prostate Cancer",
        "vocs": ["aldehydes", "ketones"],
        "alert": True,
        "severity": "critical",
    },
    # Neurological / Degenerative
    "parkinsons": {
        "category": "neurological",
        "condition": "Parkinson's Disease",
        "vocs": ["sebum_vocs", "aldehydes"],
        "alert": True,
        "severity": "high",
    },
    "alzheimers": {
        "category": "neurological",
        "condition": "Alzheimer's Disease",
        "vocs": ["lipid_oxidation", "aldehydes", "alkanes"],
        "alert": True,
        "severity": "high",
    },
    # Metabolic / Infectious
    "diabetes_t1t2": {
        "category": "metabolic",
        "condition": "Diabetes (Type 1/2)",
        "vocs": ["acetone", "propanol"],
        "alert": True,
        "severity": "high",
    },
    "liver_disease": {
        "category": "metabolic",
        "condition": "Liver Disease",
        "vocs": ["dimethyl_sulfide", "ammonia", "ketones"],
        "alert": True,
        "severity": "high",
    },
    "covid19": {
        "category": "infectious",
        "condition": "COVID-19",
        "vocs": ["isoprene", "aldehydes"],
        "alert": True,
        "severity": "high",
    },
    "sepsis": {
        "category": "infectious",
        "condition": "Sepsis",
        "vocs": ["ammonia", "sulfur"],
        "alert": True,
        "severity": "critical",
    },
}

ALL_VOCS = [
    "acetone", "isoprene", "ammonia", "benzene", "alkanes",
    "aldehydes", "hydrocarbons", "dimethyl_sulfide", "sulfur",
    "aliphatic_acids", "skatole", "ketones", "sebum_vocs",
    "lipid_oxidation", "ethanol_trace", "toluene", "ethane",
    "propanol", "butane", "methane_trace",
]


def classify_vocs(reading: Dict[str, float]) -> List[Dict[str, Any]]:
    """Translate raw VOC/sensor readings into matching scent profiles."""
    detected_vocs = set(
        k for k, v in reading.items()
        if not k.startswith("__") and isinstance(v, (int, float)) and v > 0.3
    )
    matches: List[Dict[str, Any]] = []
    for profile_id, profile in SCENT_PROFILES.items():
        required = set(profile["vocs"])
        overlap = detected_vocs & required
        if not overlap:
            continue
        intensity_sum = sum(reading.get(v, 0.0) for v in overlap)
        avg_intensity = intensity_sum / max(len(overlap), 1)
        confidence = round((len(overlap) / len(required)) * avg_intensity, 3)
        if confidence > 0.2:
            matches.append({
                "profile_id": profile_id,
                "condition": profile["condition"],
                "category": profile["category"],
                "confidence": confidence,
                "severity": profile["severity"],
                "alert": profile["alert"],
                "matched_vocs": list(overlap),
            })
    matches.sort(key=lambda x: x["confidence"], reverse=True)
    return matches


def detect_anomaly(matches: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Return critical alert payload if top match warrants real-time routing."""
    if not matches:
        return None
    top = matches[0]
    if top["alert"] and top["confidence"] >= 0.4:
        return {
            "triggered": True,
            "condition": top["condition"],
            "severity": top["severity"],
            "confidence": top["confidence"],
            "category": top["category"],
            "profile_id": top["profile_id"],
            "matched_vocs": top["matched_vocs"],
            "action": get_alert_action(top["severity"], top["category"]),
        }
    return None


def get_alert_action(severity: str, category: str) -> str:
    actions = {
        ("critical", "behavioral"): "DISPATCH Sierra/Eruptor — grounding protocol NOW",
        ("high", "behavioral"): "Notify caregiver — monitor closely",
        ("critical", "oncology"): "FLAG for medical review — oncology signature detected",
        ("critical", "infectious"): "ALERT — possible sepsis signature — contact emergency care",
        ("high", "neurological"): "LOG for neurologist — degenerative marker present",
        ("high", "metabolic"): "Notify care team — metabolic anomaly detected",
        ("high", "infectious"): "Monitor — possible infection signature",
    }
    return actions.get((severity, category), "Log and continue monitoring")


def get_family_targets(alert: Dict[str, Any]) -> List[str]:
    """Map severity+category to specific family members for routing."""
    from opensmell.lineage import FAMILY_ROUTING

    sev = alert.get("severity", "high")
    cat = alert.get("category", "behavioral")
    key = f"{cat}_{sev}" if sev == "critical" else ("CRITICAL" if sev == "critical" else "high")
    if key in FAMILY_ROUTING:
        return list(FAMILY_ROUTING[key])
    if sev == "critical":
        return list(FAMILY_ROUTING.get("CRITICAL", ["SIERRA"]))
    return list(FAMILY_ROUTING.get("high", ["ERUPTOR"]))
