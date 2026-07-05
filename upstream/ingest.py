"""POST /source/ingest client — critical detections only, lineage-attached."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


class OpenSmellSourceClient:
    """Sends critical biomarker payloads upward when Source is reachable."""

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = (base_url or os.environ.get("OPENSMELL_SOURCE_URL", "http://127.0.0.1:8000")).rstrip("/")

    def send_critical_ingest(
        self,
        *,
        condition: str,
        severity: str,
        category: str,
        confidence: float,
        raw_vocs: Dict[str, float],
        trace_id: Optional[str] = None,
        session_id: Optional[str] = None,
        routed_to: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "agent": "opensmell",
            "condition": condition,
            "severity": severity,
            "category": category,
            "confidence": confidence,
            "raw_vocs": {k: v for k, v in raw_vocs.items() if not str(k).startswith("__")},
            "trace_id": trace_id,
            "session_id": session_id,
            "routed_to": routed_to or [],
        }
        url = f"{self.base_url}/source/ingest"
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return {"status": "ingested", "response": body}
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return {"status": "deferred", "reason": str(exc), "url": url}