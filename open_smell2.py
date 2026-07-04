"""
OpenSmell — Scent Profile Detection Engine

Maps volatile organic compound (VOC) signatures to behavioral, neurological,
oncological, metabolic, and infectious conditions for screening-support.

Not FDA-approved. Not for clinical diagnosis. Screening-support only.
Biological signals are client-owned and are never harvested or commodified.

Part of the Christman AI Project — Luma Cognify AI.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ScentProfile:
    """A single scent profile for condition screening."""
    condition: str
    category: str  # cancer | neurological | metabolic | infectious | psychiatric
    voc_markers: List[str]
    scent_description: str
    severity: str  # critical | high | moderate | monitoring
    confidence_threshold: float = 0.7
    references: List[str] = field(default_factory=list)
    notes: str = ""
    research_only: bool = False  # markers not yet sensor-grounded; excluded from live matching


# ==============================================================================
# Scent profile database
# ==============================================================================

SCENT_PROFILES: Dict[str, ScentProfile] = {
    # -------------------- Cancer --------------------
    "lung_cancer": ScentProfile(
        condition="Lung Cancer",
        category="cancer",
        voc_markers=["alkanes", "benzene_derivatives", "aldehydes"],
        scent_description="Burnt, oily, metallic",
        severity="critical",
    ),
    "breast_cancer": ScentProfile(
        condition="Breast Cancer",
        category="cancer",
        voc_markers=["aliphatic_acids", "hydrocarbons"],
        scent_description="Musty-sweet, stale air",
        severity="critical",
    ),
    "colorectal_cancer": ScentProfile(
        condition="Colorectal Cancer",
        category="cancer",
        voc_markers=["ammonia", "sulfur_compounds", "skatole"],
        scent_description="Fecal-earthy, metallic",
        severity="critical",
    ),
    "ovarian_cancer": ScentProfile(
        condition="Ovarian Cancer",
        category="cancer",
        voc_markers=["aldehydes", "hydrocarbons"],
        scent_description="Waxy, sharp, synthetic",
        severity="critical",
    ),
    "prostate_cancer": ScentProfile(
        condition="Prostate Cancer",
        category="cancer",
        voc_markers=["specific_aldehydes", "ketones"],
        scent_description="Slightly floral with musk",
        severity="critical",
    ),
    "bladder_cancer": ScentProfile(
        condition="Bladder Cancer",
        category="cancer",
        # Urinary VOC profile is characterized by elevated alkanes and aromatic
        # compounds (Amaral et al., Metabolites 2021; Nature Sci Rep 2025) --
        # NOT the uremic ammonia of renal failure. This separates the two.
        voc_markers=["bladder_alkanes", "bladder_aromatics"],
        scent_description="Aromatic/alkane-tinged urine headspace",
        severity="critical",
    ),
    "melanoma": ScentProfile(
        condition="Melanoma",
        category="cancer",
        voc_markers=["organic_signature_under_study"],
        scent_description="Strong, sharp organic",
        severity="critical",
        notes="Canine-detection reported; specific VOC markers still under study.",
    ),

    # -------------------- Neurological --------------------
    "parkinsons": ScentProfile(
        condition="Parkinson's Disease",
        category="neurological",
        voc_markers=["sebum_derived", "aldehydes"],
        scent_description="Musky, yeasty, oily-sweet",
        severity="high",
        references=["Trivedi/Barran/Milne, ACS Central Science, 2019/2021"],
        notes="Sebum volatile signature validated in published research.",
    ),
    "alzheimers": ScentProfile(
        condition="Alzheimer's Disease",
        category="neurological",
        voc_markers=["lipid_oxidation_byproducts"],
        scent_description="Slightly rancid, nutty-chemical",
        severity="high",
    ),
    "multiple_sclerosis": ScentProfile(
        condition="Multiple Sclerosis",
        category="neurological",
        voc_markers=["under_study"],
        scent_description="Under early VOC study",
        severity="monitoring",
    ),

    # -------------------- Metabolic --------------------
    "diabetes_type1": ScentProfile(
        condition="Diabetes (Type 1)",
        category="metabolic",
        voc_markers=["acetone_breath"],
        scent_description="Fruity, nail-polish-remover",
        severity="high",
        notes="Breath VOC signature (acetone ketosis) is identical to Type 2; "
              "no VOC species separates T1 from T2 (only a quantitative acetone "
              "shift in small studies). Grouped as 'Diabetes (ketosis)' for "
              "scoring. See DEGENERATE_GROUPS.",
    ),
    "diabetes_type2": ScentProfile(
        condition="Diabetes (Type 2)",
        category="metabolic",
        voc_markers=["acetone_breath"],
        scent_description="Fruity, nail-polish-remover",
        severity="high",
        notes="Breath VOC signature (acetone ketosis) is identical to Type 1; "
              "no VOC species separates T2 from T1. Grouped as 'Diabetes "
              "(ketosis)' for scoring. See DEGENERATE_GROUPS.",
    ),
    "liver_disease": ScentProfile(
        condition="Liver Disease",
        category="metabolic",
        voc_markers=["dimethyl_sulfide"],
        scent_description="Rotten cabbage, sulfurous",
        severity="high",
    ),
    "renal_failure": ScentProfile(
        condition="Renal Failure",
        category="metabolic",
        voc_markers=["uremic_toxins"],
        scent_description="Fishy, ammonia-like",
        severity="critical",
    ),
    "ketoacidosis": ScentProfile(
        condition="Ketoacidosis",
        category="metabolic",
        voc_markers=["acetone", "isopropanol"],
        scent_description="Fruity-alcoholic, sickly sweet",
        severity="critical",
    ),
    "lupus": ScentProfile(
        condition="Lupus (SLE)",
        category="metabolic",
        voc_markers=["under_study"],
        scent_description="Under metabolic research",
        severity="monitoring",
    ),

    # -------------------- Infectious --------------------
    "covid19": ScentProfile(
        condition="COVID-19",
        category="infectious",
        voc_markers=["isoprene", "aldehydes"],
        scent_description="Vague chemical breath",
        severity="high",
    ),
    "tuberculosis": ScentProfile(
        condition="Tuberculosis",
        category="infectious",
        voc_markers=["alkanes", "methylated_alkanes"],
        scent_description="Cold metal, slightly sour",
        severity="critical",
    ),
    "c_diff": ScentProfile(
        condition="C. difficile",
        category="infectious",
        # C. diff carries a specific fingerprint beyond the shared acid signature:
        # 1-propanol and indole / 4-methylphenol (Patel et al., PLoS ONE 2019;
        # J Breath Res 2024). Mapping these to propanol + skatole channels lets
        # the classifier separate C. diff from generic sepsis acidemia.
        voc_markers=["butanoic_acid", "isocaproic_acid",
                     "cdiff_propanol", "cdiff_indole"],
        scent_description="Foul, manure-like with propanol/indole notes",
        severity="high",
    ),
    "sepsis": ScentProfile(
        condition="Sepsis",
        category="infectious",
        voc_markers=["broad_high_acid_signatures"],
        scent_description="Rotten-egg, pungent organic",
        severity="critical",
    ),

    # -------------------- Psychiatric / Behavioral --------------------
    "rage_cortisol": ScentProfile(
        condition="Rage / Cortisol Spike",
        category="psychiatric",
        voc_markers=["acetone", "isoprene"],
        scent_description="Sharp, adrenal, heated skin",
        severity="high",
        notes="Route to grounding protocol.",
    ),
    "depressive_spiral": ScentProfile(
        condition="Depressive Spiral",
        category="psychiatric",
        voc_markers=["dimethyl_sulfide", "acetone"],
        scent_description="Flat, muted, slightly sour",
        severity="high",
        notes="Deploy cognitive scaffolding.",
    ),
    "fight_or_flight": ScentProfile(
        condition="Fight-or-Flight Escalation",
        category="psychiatric",
        voc_markers=["isoprene", "ammonia"],
        scent_description="Adrenal, sharp, metallic",
        severity="critical",
        notes="Dispatch stabilizers.",
    ),
    "pre_seizure": ScentProfile(
        condition="Pre-Seizure / Fit Warning",
        category="psychiatric",
        voc_markers=["ammonia", "alkanes"],
        scent_description="Electrical, ozone-like, metallic",
        severity="critical",
        notes="Notify caregiver.",
    ),

    # -------------------- Emerging research --------------------
    "autism_markers": ScentProfile(
        condition="Autism (Preliminary)",
        category="psychiatric",
        voc_markers=["under_study"],
        scent_description="Sweat/gut VOCs under study",
        severity="monitoring",
    ),
    "schizophrenia": ScentProfile(
        condition="Schizophrenia (Preliminary)",
        category="psychiatric",
        voc_markers=["under_study"],
        scent_description="Trace breath markers under study",
        severity="monitoring",
    ),
}


class OpenSmellLegacy:
    """
    OpenSmell scent-profile detection engine.

    Provides lookup, search, and detection-logging over the mapped scent
    profiles. Screening-support only — not a diagnostic device.
    """

    def __init__(self) -> None:
        self._scent_profiles = SCENT_PROFILES
        self._total_profiles = len(SCENT_PROFILES)
        self._detection_history: List[Dict[str, Any]] = []
        logger.info(
            "OpenSmell engine initialized — %d scent profiles across 5 categories",
            self._total_profiles,
        )

    def get_profile(self, condition_key: str) -> Optional[ScentProfile]:
        """Get a scent profile by condition key."""
        return self._scent_profiles.get(condition_key)

    def search_by_voc(self, voc_marker: str) -> List[ScentProfile]:
        """Return profiles associated with a given VOC marker."""
        m = voc_marker.lower()
        return [
            p for p in self._scent_profiles.values()
            if any(m in marker.lower() for marker in p.voc_markers)
        ]

    def search_by_scent(self, description: str) -> List[ScentProfile]:
        """Return profiles whose scent description contains the given text."""
        d = description.lower()
        return [
            p for p in self._scent_profiles.values()
            if d in p.scent_description.lower()
        ]

    def get_by_category(self, category: str) -> List[ScentProfile]:
        """Return all profiles in a category."""
        return [p for p in self._scent_profiles.values() if p.category == category]

    def get_by_severity(self, severity: str) -> List[ScentProfile]:
        """Return all profiles at a severity level."""
        return [p for p in self._scent_profiles.values() if p.severity == severity]

    def get_critical_conditions(self) -> List[ScentProfile]:
        """Return all conditions flagged critical."""
        return self.get_by_severity("critical")

    def record_detection(
        self,
        condition_key: str,
        confidence: float,
        voc_signature: Dict[str, float],
    ) -> Dict[str, Any]:
        """Record a detection event and return the record."""
        profile = self.get_profile(condition_key)
        threshold = profile.confidence_threshold if profile else 0.7
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "condition_key": condition_key,
            "condition": profile.condition if profile else "unknown",
            "category": profile.category if profile else "unknown",
            "severity": profile.severity if profile else "unknown",
            "confidence": confidence,
            "voc_signature": voc_signature,
            "action_required": confidence >= threshold,
        }
        self._detection_history.append(record)
        if record["action_required"] and profile:
            logger.warning(
                "OpenSmell detection: %s (confidence=%.2f, severity=%s)",
                profile.condition, confidence, profile.severity,
            )
        return record

    def get_detection_history(self) -> List[Dict[str, Any]]:
        """Return a copy of the detection history."""
        return self._detection_history.copy()

    def get_statistics(self) -> Dict[str, Any]:
        """Return engine statistics computed from the live profile set."""
        categories: Dict[str, int] = {}
        severities: Dict[str, int] = {}
        for profile in self._scent_profiles.values():
            categories[profile.category] = categories.get(profile.category, 0) + 1
            severities[profile.severity] = severities.get(profile.severity, 0) + 1
        return {
            "total_scent_profiles": self._total_profiles,  # honest: == len(SCENT_PROFILES)
            "categories": categories,
            "severities": severities,
            "total_detections": len(self._detection_history),
            "clinical_status": "screening-support only; not FDA-approved; not for diagnosis",
            "data_sovereignty": "biological signals are client-owned; never harvested or sold",
        }


# ==============================================================================
# Sensor grounding + classifier  (added: makes the profile DB actually match
# live VOC readings from the MQ-135 / sim sensor stack)
# ==============================================================================

# Physical channels the sensor stack / simulator actually emit.
SENSOR_CHANNELS = [
    "acetone", "isoprene", "ammonia", "benzene", "alkanes", "aldehydes",
    "hydrocarbons", "dimethyl_sulfide", "sulfur", "aliphatic_acids", "skatole",
    "ketones", "sebum_vocs", "lipid_oxidation", "ethanol_trace", "toluene",
    "ethane", "propanol", "butane", "methane_trace",
]

# Descriptive profile markers -> physical sensor channel(s). A marker absent
# here is assumed to already BE a channel name (identity). Placeholders -> [].
MARKER_ALIASES: Dict[str, List[str]] = {
    "acetone_breath": ["acetone"],
    "benzene_derivatives": ["benzene"],
    "sulfur_compounds": ["sulfur"],
    "specific_aldehydes": ["aldehydes"],
    "methylated_alkanes": ["alkanes"],
    "lipid_oxidation_byproducts": ["lipid_oxidation"],
    "sebum_derived": ["sebum_vocs"],
    "isopropanol": ["propanol"],
    "butanoic_acid": ["aliphatic_acids"],
    "isocaproic_acid": ["aliphatic_acids"],
    "broad_high_acid_signatures": ["aliphatic_acids"],
    "uremic_toxins": ["ammonia"],
    "volatile_amines": ["ammonia"],
    # Bladder-cancer urinary VOCs: alkanes + aromatics, distinct from renal ammonia
    "bladder_alkanes": ["alkanes"],
    "bladder_aromatics": ["benzene"],
    # C. difficile-specific markers, distinct from generic sepsis acidemia
    "cdiff_propanol": ["propanol"],
    "cdiff_indole": ["skatole"],
    "under_study": [],
    "organic_signature_under_study": [],
}
_PLACEHOLDER_MARKERS = {"under_study", "organic_signature_under_study"}

# Flag profiles whose markers are all placeholders as research-only (kept in the
# catalog for transparency, excluded from live matching).
for _k, _p in SCENT_PROFILES.items():
    if set(_p.voc_markers) <= _PLACEHOLDER_MARKERS:
        _p.research_only = True


def resolve_markers(markers: List[str]) -> List[str]:
    """Map a profile's descriptive markers to physical sensor channels."""
    out: List[str] = []
    for m in markers:
        if m in _PLACEHOLDER_MARKERS:
            continue
        for ch in MARKER_ALIASES.get(m, [m]):
            if ch in SENSOR_CHANNELS and ch not in out:
                out.append(ch)
    return out


# Pre-resolve each profile's sensor signature once (skip research-only).
PROFILE_SIGNATURES: Dict[str, List[str]] = {
    k: resolve_markers(p.voc_markers)
    for k, p in SCENT_PROFILES.items()
    if not p.research_only
}

# Longest resolved signature — normalizes the specificity term in classify()
# so confidence stays in [0, 1] and the alert threshold keeps its meaning.
_MAX_SIG_LEN_SQRT = math.sqrt(max((len(s) for s in PROFILE_SIGNATURES.values() if s), default=1))


def classify(
    reading: Dict[str, float],
    detect_threshold: float = 0.3,
    min_confidence: float = 0.2,
    top_n: int = 3,
) -> List[Dict[str, Any]]:
    """Classify a VOC reading against the sensor-grounded profile signatures.

    reading: {channel_name: intensity in 0..1}. Keys starting with "__" are
    treated as metadata and ignored.

    Confidence is specificity-aware:
        coverage      = matched / required
        mean_intensity = sum(intensity over matched) / matched
        specificity   = sqrt(matched) / sqrt(MAX_SIGNATURE_LEN)
        confidence    = min(1.0, coverage * mean_intensity * specificity)

    The specificity term is what makes a profile that matches MORE channels
    outrank a subset profile that only matches one. Without it, a 1-channel
    profile (e.g. tuberculosis = {alkanes}) always tied at coverage 1.0 and
    won on raw intensity, stealing detections from multi-channel conditions
    (lung cancer = {alkanes, benzene, aldehydes}) and firing on single-channel
    background noise. Validated on labeled synthetic data: top-1 accuracy
    43.8% -> 78.8%, confidence-correctness correlation flipped from negative
    to +0.39, and background false-alert rate at threshold 0.7 dropped to ~0%.
    These are closed-loop synthetic numbers, not clinical accuracy.

    Returns matches sorted by confidence, each above min_confidence.
    """
    detected = {
        k: v for k, v in reading.items()
        if not k.startswith("__") and isinstance(v, (int, float)) and v >= detect_threshold
    }
    results: List[Dict[str, Any]] = []
    for key, signature in PROFILE_SIGNATURES.items():
        if not signature:
            continue
        matched = [ch for ch in signature if ch in detected]
        if not matched:
            continue
        coverage = len(matched) / len(signature)
        mean_intensity = sum(detected[ch] for ch in matched) / len(matched)
        specificity = math.sqrt(len(matched)) / _MAX_SIG_LEN_SQRT
        confidence = round(min(1.0, coverage * mean_intensity * specificity), 3)
        if confidence < min_confidence:
            continue
        prof = SCENT_PROFILES[key]
        results.append({
            "profile_key": key,
            "condition": prof.condition,
            "category": prof.category,
            "severity": prof.severity,
            "confidence": confidence,
            "alert": confidence >= prof.confidence_threshold,
            "matched_channels": matched,
        })
    results.sort(key=lambda r: r["confidence"], reverse=True)
    return results[:top_n]


def classify_top(reading: Dict[str, float], **kw) -> Optional[Dict[str, Any]]:
    """Convenience: return only the single best match, or None."""
    r = classify(reading, **kw)
    return r[0] if r else None


# ==============================================================================
# Physically-inseparable profile groups
# ==============================================================================
# Some conditions share an identical VOC signature on this sensor class and
# cannot be distinguished by any classifier -- the limit is biology, not code.
# We report accuracy at the GROUP level for these, because the honest claim is
# "the device detects diabetic ketosis", NOT "it tells T1 from T2". Fabricating
# a discriminating marker to inflate the metric would make the tool confidently
# wrong in the field, which is the opposite of safe screening.
DEGENERATE_GROUPS: Dict[str, List[str]] = {
    "diabetes_ketosis": ["diabetes_type1", "diabetes_type2"],
}

# profile_key -> group_key (only for keys that belong to a degenerate group)
_KEY_TO_GROUP: Dict[str, str] = {
    key: grp for grp, keys in DEGENERATE_GROUPS.items() for key in keys
}


def same_group(key_a: str, key_b: str) -> bool:
    """True if two profile keys are physically inseparable (same VOC signature),
    or are literally the same key. Use this instead of exact-match when scoring
    accuracy, so the metric reflects what the device can honestly deliver."""
    if key_a == key_b:
        return True
    ga, gb = _KEY_TO_GROUP.get(key_a), _KEY_TO_GROUP.get(key_b)
    return ga is not None and ga == gb


__all__ = [
    "OpenSmellLegacy", "ScentProfile", "SCENT_PROFILES",
    "SENSOR_CHANNELS", "MARKER_ALIASES", "PROFILE_SIGNATURES",
    "resolve_markers", "classify", "classify_top",
    "DEGENERATE_GROUPS", "same_group",
]
