"""Integration tests: classify → detect_anomaly → route_alert threshold chain."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from alert import build_alert_payload_from_detection, route_alert
from open_smell2 import SCENT_PROFILES, classify, classify_top
from opensmell_test_loop import classify_vocs, detect_anomaly

# Reproduces the user's live cycle: multi-VOC background, lung tops at ~0.38
MESSY_BACKGROUND_READING = {
    "benzene": 0.365,
    "alkanes": 0.424,
    "aldehydes": 0.36,
    "hydrocarbons": 0.4,
    "skatole": 0.38,
    "lipid_oxidation": 0.35,
    "ethanol_trace": 0.415,
    "toluene": 0.492,
    "ethane": 0.368,
    "propanol": 0.417,
}


class TestClassifyToAnomalyGate(unittest.TestCase):
    def test_messy_background_matches_but_no_anomaly(self):
        matches = classify_vocs(MESSY_BACKGROUND_READING)
        self.assertTrue(matches)
        top = matches[0]
        self.assertEqual(top["profile_id"], "lung_cancer")
        self.assertLess(top["confidence"], 0.7)
        self.assertFalse(top["alert"])
        self.assertIsNone(detect_anomaly(matches))

    def test_critical_label_without_threshold_is_not_actionable(self):
        top = classify_top(MESSY_BACKGROUND_READING)
        self.assertIsNotNone(top)
        self.assertEqual(top["severity"], "critical")
        self.assertLess(top["confidence"], SCENT_PROFILES["lung_cancer"].confidence_threshold)

    def test_high_confidence_lung_triggers_anomaly(self):
        reading = {ch: 0.05 for ch in MESSY_BACKGROUND_READING}
        reading.update({"alkanes": 0.92, "benzene": 0.88, "aldehydes": 0.86})
        matches = classify_vocs(reading)
        detection = detect_anomaly(matches)
        self.assertIsNotNone(detection)
        self.assertEqual(detection["profile_id"], "lung_cancer")
        self.assertGreaterEqual(detection["confidence"], 0.7)
        self.assertIn("FLAG", detection["action"])


class TestAnomalyToRouterGate(unittest.TestCase):
    def test_route_suppressed_below_threshold(self):
        routed = route_alert(
            condition="Lung Cancer",
            severity="critical",
            category="cancer",
            confidence=0.38,
            raw_vocs=MESSY_BACKGROUND_READING,
            profile_key="lung_cancer",
            do_upward=False,
        )
        self.assertEqual(routed["status"], "suppressed")
        self.assertEqual(routed["reason"], "below_confidence_threshold")
        self.assertEqual(routed["threshold"], 0.7)

    @patch("alert.OpenSmellSourceClient.send_critical_ingest")
    def test_full_pipeline_routes_only_when_earned(self, mock_ingest):
        mock_ingest.return_value = {"status": "deferred", "reason": "test"}

        # Sub-threshold: no detection, no route
        low_matches = classify_vocs(MESSY_BACKGROUND_READING)
        self.assertIsNone(detect_anomaly(low_matches))
        suppressed = route_alert(
            condition="Lung Cancer",
            severity="critical",
            category="cancer",
            confidence=low_matches[0]["confidence"],
            raw_vocs=MESSY_BACKGROUND_READING,
            profile_key="lung_cancer",
            do_upward=True,
        )
        self.assertEqual(suppressed["status"], "suppressed")
        mock_ingest.assert_not_called()

        # High-confidence: detection + route
        reading = {"alkanes": 0.91, "benzene": 0.89, "aldehydes": 0.87, "isoprene": 0.05}
        high_matches = classify_vocs(reading)
        detection = detect_anomaly(high_matches)
        self.assertIsNotNone(detection)
        routed = build_alert_payload_from_detection(
            detection,
            reading,
            do_upward=True,
        )
        self.assertEqual(routed["status"], "routed")
        self.assertIn("SIERRA", routed["routed_to"])
        self.assertIn("DEREK", routed["routed_to"])
        mock_ingest.assert_called_once()

    @patch("alert.OpenSmellSourceClient.send_critical_ingest")
    def test_sepsis_critical_routes_sierra_derek(self, mock_ingest):
        mock_ingest.return_value = {"status": "deferred"}
        reading = {
            "aliphatic_acids": 0.88,
            "ammonia": 0.84,
            "dimethyl_sulfide": 0.81,
        }
        matches = classify_vocs(reading)
        detection = detect_anomaly(matches)
        self.assertIsNotNone(detection)
        self.assertEqual(detection["profile_id"], "sepsis")
        routed = build_alert_payload_from_detection(detection, reading, do_upward=True)
        self.assertEqual(routed["status"], "routed")
        self.assertEqual(routed["routed_to"], ["SIERRA", "DEREK"])


class TestDirectClassifyConsistency(unittest.TestCase):
    def test_classify_alert_flag_matches_threshold(self):
        for reading in (MESSY_BACKGROUND_READING, {"alkanes": 0.9, "benzene": 0.9, "aldehydes": 0.9}):
            for match in classify(reading, top_n=5):
                prof = SCENT_PROFILES[match["profile_key"]]
                if match["confidence"] >= prof.confidence_threshold:
                    self.assertTrue(match["alert"])
                else:
                    self.assertFalse(match["alert"])


if __name__ == "__main__":
    unittest.main(verbosity=2)