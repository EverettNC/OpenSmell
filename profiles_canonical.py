"""
OpenSmell Canonical Profile Registry

Single source of truth for all disease/state profiles in OpenSmell.
Every other module imports profile identity FROM HERE. Do not redefine
profile keys anywhere else — drift between spellings (parkinson vs parkinsons,
four diabetes variants, liver-* autocomplete junk) is exactly what this file exists
to prevent.

Source of record: opensmell_engine_truth.json (21 validated profiles).
NOTE: VOC marker lists are NOT stored here — this registry is identity only
(key, condition, category, severity, channels). Markers live in the engine.
"""
from __future__ import annotations

__all__ = ["PROFILES", "ALIASES", "canonical_key", "get_profile", "all_keys"]


# The 21 canonical profiles. Category-sorted. This list IS the registry.
PROFILES: dict[str, dict] = {
    'bladder_cancer': {
        "condition": 'Bladder Cancer',
        "category": 'cancer',
        "severity": 'critical',
        "channels": ['alkanes', 'benzene'],
    },
    'breast_cancer': {
        "condition": 'Breast Cancer',
        "category": 'cancer',
        "severity": 'critical',
        "channels": ['aliphatic_acids', 'hydrocarbons'],
    },
    'colorectal_cancer': {
        "condition": 'Colorectal Cancer',
        "category": 'cancer',
        "severity": 'critical',
        "channels": ['ammonia', 'sulfur', 'skatole'],
    },
    'lung_cancer': {
        "condition": 'Lung Cancer',
        "category": 'cancer',
        "severity": 'critical',
        "channels": ['alkanes', 'benzene', 'aldehydes'],
    },
    'ovarian_cancer': {
        "condition": 'Ovarian Cancer',
        "category": 'cancer',
        "severity": 'critical',
        "channels": ['aldehydes', 'hydrocarbons'],
    },
    'prostate_cancer': {
        "condition": 'Prostate Cancer',
        "category": 'cancer',
        "severity": 'critical',
        "channels": ['aldehydes', 'ketones'],
    },
    'c_diff': {
        "condition": 'C. difficile',
        "category": 'infectious',
        "severity": 'high',
        "channels": ['aliphatic_acids', 'propanol', 'skatole'],
    },
    'covid19': {
        "condition": 'COVID-19',
        "category": 'infectious',
        "severity": 'high',
        "channels": ['isoprene', 'aldehydes'],
    },
    'sepsis': {
        "condition": 'Sepsis',
        "category": 'infectious',
        "severity": 'critical',
        "channels": ['aliphatic_acids', 'ammonia', 'dimethyl_sulfide'],
    },
    'tuberculosis': {
        "condition": 'Tuberculosis',
        "category": 'infectious',
        "severity": 'critical',
        "channels": ['alkanes'],
    },
    'diabetes_type1': {
        "condition": 'Diabetes (Type 1)',
        "category": 'metabolic',
        "severity": 'high',
        "channels": ['acetone'],
    },
    'diabetes_type2': {
        "condition": 'Diabetes (Type 2)',
        "category": 'metabolic',
        "severity": 'high',
        "channels": ['acetone'],
    },
    'ketoacidosis': {
        "condition": 'Ketoacidosis',
        "category": 'metabolic',
        "severity": 'critical',
        "channels": ['acetone', 'propanol'],
    },
    'liver_disease': {
        "condition": 'Liver Disease',
        "category": 'metabolic',
        "severity": 'high',
        "channels": ['dimethyl_sulfide'],
    },
    'renal_failure': {
        "condition": 'Renal Failure',
        "category": 'metabolic',
        "severity": 'critical',
        "channels": ['ammonia', 'dimethyl_sulfide', 'toluene'],
    },
    'alzheimers': {
        "condition": "Alzheimer's Disease",
        "category": 'neurological',
        "severity": 'high',
        "channels": ['lipid_oxidation'],
    },
    'parkinsons': {
        "condition": "Parkinson's Disease",
        "category": 'neurological',
        "severity": 'high',
        "channels": ['sebum_vocs', 'aldehydes'],
    },
    'depressive_spiral': {
        "condition": 'Depressive Spiral',
        "category": 'psychiatric',
        "severity": 'high',
        "channels": ['dimethyl_sulfide', 'acetone'],
    },
    'fight_or_flight': {
        "condition": 'Fight-or-Flight Escalation',
        "category": 'psychiatric',
        "severity": 'critical',
        "channels": ['isoprene', 'ammonia'],
    },
    'pre_seizure': {
        "condition": 'Pre-Seizure / Fit Warning',
        "category": 'psychiatric',
        "severity": 'critical',
        "channels": ['ammonia', 'alkanes'],
    },
    'rage_cortisol': {
        "condition": 'Rage / Cortisol Spike',
        "category": 'psychiatric',
        "severity": 'high',
        "channels": ['acetone', 'isoprene'],
    },
}


# Every known messy spelling seen across the repo -> its one true key.
# Add new drift here the moment you see it, never a new PROFILES entry.
ALIASES: dict[str, str] = {
    'ad': 'alzheimers',
    'alzheimer': 'alzheimers',
    'alzheimers_disease': 'alzheimers',
    'alzheimers_lipid_oxidation': 'alzheimers',
    'c_difficile': 'c_diff',
    'cdiff': 'c_diff',
    'clostridium_difficile': 'c_diff',
    'cortisol_rage': 'rage_cortisol',
    'covid': 'covid19',
    'covid_19': 'covid19',
    'depression': 'depressive_spiral',
    'depressive': 'depressive_spiral',
    'diabetes': 'diabetes_type2',
    'diabetes_acetone_detection': 'diabetes_type1',
    'diabetes_ketosis': 'ketoacidosis',
    'diabetes_t1': 'diabetes_type1',
    'diabetes_t1t2': 'diabetes_type1',
    'diabetes_t2': 'diabetes_type2',
    'diabetes_type_1': 'diabetes_type1',
    'diabetes_type_2': 'diabetes_type2',
    'dka': 'ketoacidosis',
    'flight_or_fight': 'fight_or_flight',
    'kidney': 'renal_failure',
    'kidney_failure': 'renal_failure',
    'liver': 'liver_disease',
    'liver_cancellation': 'liver_disease',
    'liver_cancer': 'liver_disease',
    'liverability': 'liver_disease',
    'livered': 'liver_disease',
    'livermore': 'liver_disease',
    'livery': 'liver_disease',
    'lung_cancer_detection': 'lung_cancer',
    'lung_cancer_signature': 'lung_cancer',
    'panic': 'fight_or_flight',
    'parkinson': 'parkinsons',
    'parkinsons_disease': 'parkinsons',
    'pd': 'parkinsons',
    'pre_seizure_state': 'pre_seizure',
    'rage': 'rage_cortisol',
    'renal': 'renal_failure',
    'sars_cov_2': 'covid19',
    'seizure': 'pre_seizure',
    'tb': 'tuberculosis',
    'type1_diabetes': 'diabetes_type1',
    'type2_diabetes': 'diabetes_type2',
}


def canonical_key(name: str) -> str | None:
    """Normalize any profile name to its canonical key, or None if unknown."""
    if not name:
        return None
    k = name.strip().lower().replace("-", "_").replace(" ", "_")
    if k in PROFILES:
        return k
    return ALIASES.get(k)


def get_profile(name: str) -> dict | None:
    """Return the canonical profile dict for any spelling, or None if unknown."""
    k = canonical_key(name)
    return PROFILES[k] | {"key": k} if k else None


def all_keys() -> list[str]:
    """All 21 canonical keys, sorted."""
    return sorted(PROFILES)
