"""Unit tests for open_smell2.py — sensor-grounded classifier + profile DB."""

import unittest

from open_smell2 import (
    OpenSmellLegacy,
    PROFILE_SIGNATURES,
    SCENT_PROFILES,
    classify,
    classify_top,
    resolve_markers,
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
        reading = {"alkanes": 0.85, "benzene": 0.80, "aldehydes": 0.75, "isoprene": 0.1}
        matches = classify(reading, top_n=10)
        keys = {m["profile_key"] for m in matches}
        self.assertIn("lung_cancer", keys)
        self.assertEqual(matches[0]["profile_key"], "tuberculosis")

    def test_diabetes_acetone_detection(self):
        reading = {"acetone": 0.9, "isoprene": 0.1}
        matches = classify(reading, top_n=10)
        keys = {m["profile_key"] for m in matches}
        self.assertTrue(keys & {"diabetes_type1", "diabetes_type2", "rage_cortisol"})

    def test_no_match_below_threshold(self):
        reading = {"isoprene": 0.05, "ethane": 0.08}
        self.assertEqual(classify(reading), [])

    def test_metadata_keys_ignored(self):
        reading = {"__injected__": "lung_cancer", "__patient__": {"age": 70}, "benzene": 0.80, "aldehydes": 0.75}
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

    def test_record_detection_threshold(self):
        engine = OpenSmellLegacy()
        record = engine.record_detection("covid19", 0.85, {"isoprene": 0.85})
        self.assertTrue(record["action_required"])

    def test_search_by_voc(self):
        engine = OpenSmellLegacy()
        hits = engine.search_by_voc("acetone")
        self.assertGreater(len(hits), 0)


class TestLoopIntegration(unittest.TestCase):
    def test_inject_alias_resolves(self):
        from opensmell_test_loop import resolve_inject_profile
        self.assertEqual(resolve_inject_profile("diabetes_t1t2"), "diabetes_type1")

    def test_classify_vocs_delegates_to_engine(self):
        from opensmell_test_loop import classify_vocs
        reading = {"lipid_oxidation": 0.88, "isoprene": 0.1}
        matches = classify_vocs(reading)
        self.assertTrue(any(m["profile_id"] == "alzheimers" for m in matches))

    def test_injection_profiles_match_engine(self):
        from opensmell_test_loop import INJECTION_PROFILES
        self.assertEqual(set(INJECTION_PROFILES), set(PROFILE_SIGNATURES))


if __name__ == "__main__":
    unittest.main(verbosity=2)
