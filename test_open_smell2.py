"""Unit tests for open_smell2.py — sensor-grounded classifier + profile DB."""

import unittest

from open_smell2 import (
    DEGENERATE_GROUPS,
    OpenSmellLegacy,
    PROFILE_SIGNATURES,
    SCENT_PROFILES,
    classify,
    classify_top,
    resolve_markers,
    same_group,
)


class TestResolveMarkers(unittest.TestCase):
    def test_acetone_breath_alias(self):
        self.assertEqual(resolve_markers(["acetone_breath"]), ["acetone"])

    def test_placeholder_markers_skipped(self):
        self.assertEqual(resolve_markers(["under_study"]), [])

    def test_lung_cancer_signature(self):
        sig = resolve_markers(SCENT_PROFILES["lung_cancer"].voc_markers)
        self.assertEqual(sorted(sig), ["aldehydes", "alkanes", "benzene"])


class TestProfileSignatures(unittest.TestCase):
    RESEARCH_ONLY = {
        "melanoma", "multiple_sclerosis", "lupus",
        "autism_markers", "schizophrenia",
    }

    def test_research_only_excluded(self):
        for key in self.RESEARCH_ONLY:
            self.assertTrue(SCENT_PROFILES[key].research_only)
            self.assertNotIn(key, PROFILE_SIGNATURES)

    def test_live_profile_count(self):
        live = [k for k, p in SCENT_PROFILES.items() if not p.research_only]
        self.assertEqual(len(PROFILE_SIGNATURES), len(live))


class TestClassify(unittest.TestCase):
    def test_lung_cancer_detection(self):
        reading = {
            "alkanes": 0.85,
            "benzene": 0.80,
            "aldehydes": 0.75,
            "isoprene": 0.1,
        }
        matches = classify(reading, top_n=10)
        keys = {m["profile_key"] for m in matches}
        self.assertIn("lung_cancer", keys)
        lung = next(m for m in matches if m["profile_key"] == "lung_cancer")
        self.assertGreaterEqual(lung["confidence"], 0.2)
        # Specificity-aware confidence: lung cancer matches all 3 of its channels
        # and must outrank tuberculosis, which shares only {alkanes}. (Before the
        # specificity fix, the shorter TB signature wrongly won this reading.)
        self.assertEqual(matches[0]["profile_key"], "lung_cancer")

    def test_diabetes_acetone_detection(self):
        reading = {"acetone": 0.9, "isoprene": 0.1}
        matches = classify(reading, top_n=10)
        keys = {m["profile_key"] for m in matches}
        self.assertTrue(keys & {"diabetes_type1", "diabetes_type2", "rage_cortisol"})

    def test_no_match_below_threshold(self):
        reading = {"isoprene": 0.05, "ethane": 0.08}
        self.assertEqual(classify(reading), [])

    def test_metadata_keys_ignored(self):
        reading = {
            "__injected__": "lung_cancer",
            "__patient__": {"age": 70},
            "benzene": 0.80,
            "aldehydes": 0.75,
        }
        top = classify_top(reading)
        self.assertIsNotNone(top)
        self.assertEqual(top["profile_key"], "lung_cancer")

    def test_alzheimers_lipid_oxidation(self):
        reading = {"lipid_oxidation": 0.88, "isoprene": 0.1}
        top = classify_top(reading)
        self.assertIsNotNone(top)
        self.assertEqual(top["profile_key"], "alzheimers")


class TestOpenSmellLegacy(unittest.TestCase):
    def test_statistics(self):
        engine = OpenSmellLegacy()
        stats = engine.get_statistics()
        self.assertEqual(stats["total_scent_profiles"], len(SCENT_PROFILES))
        self.assertIn("cancer", stats["categories"])
        self.assertEqual(stats["total_detections"], 0)

    def test_record_detection_threshold(self):
        engine = OpenSmellLegacy()
        record = engine.record_detection("covid19", 0.85, {"isoprene": 0.85})
        self.assertTrue(record["action_required"])
        self.assertEqual(len(engine.get_detection_history()), 1)

    def test_search_by_voc(self):
        engine = OpenSmellLegacy()
        hits = engine.search_by_voc("acetone")
        self.assertGreater(len(hits), 0)


class TestLoopIntegration(unittest.TestCase):
    def test_inject_alias_resolves(self):
        from opensmell_test_loop import resolve_inject_profile
        self.assertEqual(resolve_inject_profile("diabetes_t1t2"), "diabetes_type1")
        self.assertEqual(resolve_inject_profile("alzheimers"), "alzheimers")

    def test_classify_vocs_delegates_to_engine(self):
        from opensmell_test_loop import classify_vocs
        reading = {"lipid_oxidation": 0.88, "isoprene": 0.1}
        matches = classify_vocs(reading)
        self.assertTrue(any(m["profile_id"] == "alzheimers" for m in matches))

    def test_injection_profiles_match_engine(self):
        from opensmell_test_loop import INJECTION_PROFILES
        self.assertEqual(set(INJECTION_PROFILES), set(PROFILE_SIGNATURES))
        for key, spec in INJECTION_PROFILES.items():
            self.assertEqual(spec["vocs"], PROFILE_SIGNATURES[key])


class TestSpecificityAndDegeneracy(unittest.TestCase):
    """Locks in the biomarker-specificity fixes so they can't silently regress."""

    def test_bladder_renal_separated(self):
        # Bladder cancer (alkanes+aromatics) must NOT resolve to the same
        # signature as renal failure (ammonia). Previously both were {ammonia}.
        bladder = set(resolve_markers(SCENT_PROFILES["bladder_cancer"].voc_markers))
        renal = set(resolve_markers(SCENT_PROFILES["renal_failure"].voc_markers))
        self.assertTrue(bladder.isdisjoint(renal))

    def test_cdiff_separated_from_sepsis(self):
        # C. diff carries propanol + skatole (indole) on top of the acid signature.
        cdiff = set(resolve_markers(SCENT_PROFILES["c_diff"].voc_markers))
        sepsis = set(resolve_markers(SCENT_PROFILES["sepsis"].voc_markers))
        self.assertNotEqual(cdiff, sepsis)
        self.assertIn("propanol", cdiff)
        self.assertIn("skatole", cdiff)

    def test_diabetes_grouped_not_faked(self):
        # T1/T2 share an identical acetone signature by biology; they must be
        # declared inseparable, not given a fabricated discriminating marker.
        self.assertEqual(
            resolve_markers(SCENT_PROFILES["diabetes_type1"].voc_markers),
            resolve_markers(SCENT_PROFILES["diabetes_type2"].voc_markers),
        )
        self.assertTrue(same_group("diabetes_type1", "diabetes_type2"))
        self.assertFalse(same_group("diabetes_type1", "ketoacidosis"))
        self.assertIn("diabetes_ketosis", DEGENERATE_GROUPS)

    def test_specificity_multichannel_beats_subset(self):
        # A reading matching all of lung cancer's channels must rank lung cancer
        # above tuberculosis, which shares only {alkanes}.
        reading = {"alkanes": 0.85, "benzene": 0.80, "aldehydes": 0.75}
        top = classify_top(reading)
        self.assertEqual(top["profile_key"], "lung_cancer")

    def test_confidence_bounded(self):
        # Specificity term must never push confidence above 1.0.
        reading = {ch: 1.0 for ch in PROFILE_SIGNATURES["lung_cancer"]}
        for match in classify(reading, top_n=10):
            self.assertLessEqual(match["confidence"], 1.0)

    def test_single_channel_noise_stays_low(self):
        # One moderately-high channel should not clear a 0.7 alert on its own,
        # thanks to the specificity normalization (background-rejection guard).
        reading = {"ammonia": 0.6}
        top = classify_top(reading)
        if top is not None:
            self.assertLess(top["confidence"], 0.7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
