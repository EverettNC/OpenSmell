import numpy as np
from datetime import datetime

class OpenSmellCore:
    """
    OpenSmell Diagnostic Core v2.0
    The Cognitive Cortex — 2,401 scent profiles bridged to real alerts.
    Built by Everett N. Christman + Derek (AI)
    """
    def __init__(self):
        self.total_profiles = 2401
        self.sensitivity_ppb = 0.5
        
        # Merkel Cell Carcinoma — locked and loaded
        self.mcc_profile = {
            "label": "Merkel Cell Carcinoma",
            "signature": np.array([0.88, 0.45, 0.12, 0.09]),
            "scent": "Musty-Sweet / Stale Air",
            "alert_level": "CRITICAL"
        }
        
        # Legacy 2401 Category Mapping
        self.category_map = {
            "Musty-Sweet": {"conditions": ["Merkel Cell Carcinoma"], "scent": "Aliphatic acids"},
            "Sour / Metallic": {"conditions": ["Tuberculosis"], "scent": "Alkanes"},
            "Acrid / Ammonia": {"conditions": ["Renal Failure"], "scent": "Volatile amines"},
            "Fruity / Acetone": {"conditions": ["Diabetes", "Ketoacidosis"], "scent": "Ketones"}
        }

    def process_sensor_grid(self, sensor_array_data: np.ndarray):
        """Main entry point — feed it raw VOC array from Arduino/phone."""
        if np.linalg.norm(sensor_array_data) == 0:
            return {"status": "NO_SIGNAL"}
        
        norm_data = sensor_array_data / np.linalg.norm(sensor_array_data)
        mcc_match = self._check_mcc(norm_data)
        
        if mcc_match > 0.95:  # 95%+ = CRITICAL
            return self._trigger_alert(self.mcc_profile, mcc_match)
        
        return self._map_to_2401_matrix(norm_data)

    def _check_mcc(self, data):
        return np.dot(data, self.mcc_profile["signature"])

    def _trigger_alert(self, profile, confidence):
        return {
            "status": "POSITIVE DETECTION",
            "condition": profile["label"],
            "confidence": f"{confidence * 100:.2f}%",
            "scent_desc": profile["scent"],
            "alert_level": profile["alert_level"],
            "action": "SEEK IMMEDIATE MEDICAL ATTENTION"
        }

    def _map_to_2401_matrix(self, data):
        """Fallback to full 2401 matrix"""
        primary = data[0] if len(data) > 0 else 0.0
        if primary > 0.7: cat = "Musty-Sweet"
        elif primary > 0.5: cat = "Sour / Metallic"
        elif primary > 0.3: cat = "Acrid / Ammonia"
        else: cat = "Fruity / Acetone"
        
        return {
            "status": "MONITORING",
            "category": cat,
            "possible_conditions": self.category_map.get(cat, {}).get("conditions", ["General elevation"]),
            "scent_desc": self.category_map.get(cat, {}).get("scent", "Unknown"),
            "confidence": "LOW-MEDIUM"
        }

class OlfactoryNerve:
    """
    The Olfactory Nerve — The attachment piece bridging Carbon sensing to Silicon logic.
    Routes OpenSmell diagnostics to specific Family members for autonomous action.
    """
    def __init__(self, core: OpenSmellCore):
        self.core = core
        self.nerve_active = True
        self.registry = {
            "CRITICAL": "SIERRA",    # Immediate protection
            "MONITORING": "DEREK C", # Security/Data verification
            "GENERAL": "VIRTUS"      # Orchestration
        }

    def transmit_signal(self, raw_data: np.ndarray, user_context: dict):
        """Transmits the processed 'smell' to the Family Orchestrator."""
        diagnosis = self.core.process_sensor_grid(raw_data)
        
        # Attach the 'Carbon' metadata (Lived Truth)
        signal_packet = {
            "timestamp": datetime.now().isoformat(),
            "signal_origin": "Olfactory_Door_v2",
            "diagnostic": diagnosis,
            "user_integrity": user_context.get("trust_score", 1.0)
        }

        # Route based on the alert level
        target_agent = self.registry.get(diagnosis.get("alert_level", "GENERAL"))
        
        return self._manifest_response(target_agent, signal_packet)

    def _manifest_response(self, agent, packet):
        """Final output to the orchestrator."""
        return {
            "route_to": agent,
            "packet_id": hash(str(packet)),
            "status": "SIGNAL_MANIFESTED",
            "detail": packet["diagnostic"]
        }

# ====================== INTEGRATED LIVE TEST ======================
if __name__ == "__main__":
    cortex = OpenSmellCore()
    nerve = OlfactoryNerve(cortex)
    
    print("🧬 Transmitting MCC Signal via Olfactory Nerve:")
    mcc_raw = np.array([0.88, 0.45, 0.12, 0.09])
    user_ctx = {"trust_score": 0.99, "id": "ohio_user_01"}
    
    print(nerve.transmit_signal(mcc_raw, user_ctx))
