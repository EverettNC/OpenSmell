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
        voc_markers=["volatile_amines"],
        scent_description="Ammonia-tinged, acrid",
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
    ),
    "diabetes_type2": ScentProfile(
        condition="Diabetes (Type 2)",
        category="metabolic",
        voc_markers=["acetone_breath"],
        scent_description="Fruity, nail-polish-remover",
        severity="high",
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
        voc_markers=["butanoic_acid", "isocaproic_acid"],
        scent_description="Foul, manure-like",
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


__all__ = ["OpenSmellLegacy", "ScentProfile", "SCENT_PROFILES"]
