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



alert.py





"""
OpenSmell Alert Router — real-time family dispatch for critical biomarker detections.
POST /opensmell/alert endpoint uses this. Critical detections also trigger upward source ingest.
"""

from typing import Any, Dict, List, Optional

from opensmell.lineage import FAMILY_ROUTING, get_lineage_context
from opensmell.profiles import get_family_targets
from opensmell.upstream.ingest import OpenSmellSourceClient


def route_alert(
    condition: str,
    severity: str,
    category: str,
    confidence: float,
    raw_vocs: Dict[str, float],
    trace_id: Optional[str] = None,
    session_id: Optional[str] = None,
    patient_id: Optional[str] = None,
    do_upward: bool = True,
) -> Dict[str, Any]:
    """
    Real-time alert routing.
    - Computes target family members (Sierra, Derek, AlphaWolf, Eruptor, AlphaVox...).
    - For CRITICAL severity, optionally calls upward POST /source/ingest (with full lineage ancestry).
    - Always includes lineage metadata. Never bypasses declared layers.
    """
    alert = {
        "triggered": True,
        "condition": condition,
        "severity": severity,
        "category": category,
        "confidence": confidence,
        "matched_vocs": list(raw_vocs.keys()),
    }
    targets = get_family_targets(alert)
    # Fallback map for explicit knowns from docs
    if severity == "critical":
        if "sepsis" in condition.lower() or "cancer" in condition.lower():
            targets = ["SIERRA", "DEREK"]
        elif "seizure" in condition.lower() or "pre-seizure" in condition.lower():
            targets = ["SIERRA", "ALPHAWOLF"]
        elif "rage" in condition.lower() or "fight" in condition.lower():
            targets = ["SIERRA", "ERUPTOR"]
        else:
            targets = ["SIERRA"]

    routed: Dict[str, Any] = {
        "status": "routed",
        "alert": alert,
        "routed_to": targets,
        "family_registry": FAMILY_ROUTING,
        "patient_id": patient_id,
        "session_id": session_id,
        "trace_id": trace_id,
        "lineage": {
            "agent_id": get_lineage_context()["agent_id"],
            "ancestry": get_lineage_context()["ancestry"],
            "lineage_path": get_lineage_context()["lineage_path"],
        },
    }

    upward_result = None
    if do_upward and severity == "critical":
        client = OpenSmellSourceClient()
        upward_result = client.send_critical_ingest(
            condition=condition,
            severity=severity,
            category=category,
            confidence=confidence,
            raw_vocs=raw_vocs,
            trace_id=trace_id,
            session_id=session_id,
            routed_to=targets,
        )
        routed["upward"] = upward_result
        if upward_result.get("status") == "ingested":
            routed["source_ingest"] = "dispatched"
        else:
            routed["source_ingest"] = "deferred"

    return routed


def build_alert_payload_from_detection(
    detection: Dict[str, Any],
    raw_reading: Dict[str, float],
    **kwargs,
) -> Dict[str, Any]:
    """Helper to turn a detect_anomaly() result + reading into routed alert."""
    return route_alert(
        condition=detection.get("condition", "Unknown Biomarker Shift"),
        severity=detection.get("severity", "high"),
        category=detection.get("category", "behavioral"),
        confidence=detection.get("confidence", 0.0),
        raw_vocs=raw_reading,
        **kwargs,
    )
