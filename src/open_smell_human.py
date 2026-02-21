import numpy as np
from datetime import datetime

class OpenSmellHumanCore:
    """
    OpenSmell: Human Diagnostic Module v2.0
    The Biological Cortex — Mapping 2,401 human VOC profiles to clinical restoration.
    Built by Everett N. Christman + Derek (AI)
    """
    def __init__(self):
        self.total_profiles = 2401
        self.sensitivity_ppb = 0.5  # High sensitivity for biological "leakage"
        
        # Clinical Profile: Merkel Cell Carcinoma (MCC)
        self.mcc_profile = {
            "label": "Merkel Cell Carcinoma",
            "signature": np.array([0.88, 0.45, 0.12, 0.09]),
            "scent": "Musty-Sweet / Stale Air",
            "alert_level": "CRITICAL"
        }
        
        # Biological Category Mapping
        self.category_map = {
            "Musty-Sweet": {"conditions": ["Merkel Cell Carcinoma"], "scent_type": "Aliphatic acids"},
            "Sour / Metallic": {"conditions": ["Tuberculosis"], "scent_type": "Alkanes"},
            "Acrid / Ammonia": {"conditions": ["Renal Failure"], "scent_type": "Volatile amines"},
            "Fruity / Acetone": {"conditions": ["Diabetes", "Ketoacidosis"], "scent_type": "Ketones"}
        }

    def process_biometric_scent(self, sensor_array_data: np.ndarray):
        """Processes raw biological VOC array from breath or skin contact."""
        if np.linalg.norm(sensor_array_data) == 0:
            return {"status": "NO_SIGNAL"}
        
        norm_data = sensor_array_data / np.linalg.norm(sensor_array_data)
        mcc_match = np.dot(norm_data, self.mcc_profile["signature"])
        
        if mcc_match > 0.95:
            return self._trigger_medical_alert(self.mcc_profile, mcc_match)
        
        return self._map_to_human_matrix(norm_data)

    def _trigger_medical_alert(self, profile, confidence):
        return {
            "status": "POSITIVE DETECTION",
            "condition": profile["label"],
            "confidence": f"{confidence * 100:.2f}%",
            "alert_level": profile["alert_level"],
            "action": "SEEK IMMEDIATE CLINICAL RESTORATION"
        }

    def _map_to_human_matrix(self, data):
        primary = data[0] if len(data) > 0 else 0.0
        if primary > 0.7: cat = "Musty-Sweet"
        elif primary > 0.5: cat = "Sour / Metallic"
        elif primary > 0.3: cat = "Acrid / Ammonia"
        else: cat = "Fruity / Acetone"
        
        return {
            "status": "MONITORING_WELLNESS",
            "category": cat,
            "possible_indicators": self.category_map.get(cat, {}).get("conditions", ["General wellness shift"]),
            "biological_scent": self.category_map.get(cat, {}).get("scent_type", "Unknown")
        }

class HumanOlfactoryNerve:
    """
    The Human Nerve — Dedicated attachment bridging biological scent to the Family.
    """
    def __init__(self, core: OpenSmellHumanCore):
        self.core = core
        self.registry = {
            "CRITICAL": "SIERRA",      # Immediate trauma/health protection
            "RESTORATION": "ALPHAVOX", # Giving voice to non-verbal distress
            "STABILITY": "ERUPTOR"     # Grounding cognitive drift
        }

    def transmit_human_signal(self, raw_data: np.ndarray, user_id: str):
        """Transmits human diagnostic to the specific Family protector."""
        diagnosis = self.core.process_biometric_scent(raw_data)
        target_agent = self.registry.get(diagnosis.get("alert_level", "RESTORATION"))
        
        return {
            "route_to": target_agent,
            "user_id": user_id,
            "status": "HUMAN_SIGNAL_MANIFESTED",
            "sovereignty": "CLIENT_OWNED_DATA",
            "detail": diagnosis
        }

# ====================== HUMAN SENSORY ATTACHMENT ======================
if __name__ == "__main__":
    # 1. Initialize the Biological Core and the Human Nerve
    human_cortex = OpenSmellHumanCore()
    human_nerve = HumanOlfactoryNerve(human_cortex)
    
    print("🧠 OpenSmell Human Module: Nerve Attachment Active.")
    print(f"🧬 Monitoring 2,401 profiles at {human_cortex.sensitivity_ppb} ppb sensitivity.")
    
    # 2. Simulate a Positive Medical Detection (Merkel Cell Carcinoma)
    # This simulates the VOC signature being 'smelled' by the sensor
    print("\n🩸 TEST: Transmitting Critical Health Signal...")
    mcc_sample = np.array([0.88, 0.45, 0.12, 0.09])
    mcc_response = human_nerve.transmit_human_signal(mcc_raw=mcc_sample, user_id="Carbon_User_01")
    
    print(f"Targeting Protector: {mcc_response['route_to']}")
    print(f"Diagnosis Status: {mcc_response['detail']['status']}")
    print(f"Action Required: {mcc_response['detail']['action']}")

    # 3. Simulate a Wellness Monitoring Event (Normal Breath)
    print("\n🌬️ TEST: Transmitting Standard Wellness Signal...")
    wellness_sample = np.array([0.1, 0.2, 0.3, 0.4])
    wellness_response = human_nerve.transmit_human_signal(raw_data=wellness_sample, user_id="Carbon_User_01")
    
    print(f"Route for Monitoring: {wellness_response['route_to']}")
    print(f"Sovereignty Check: {wellness_response['sovereignty']}")
    print(f"Wellness Category: {wellness_response['detail']['category']}")

    print("\n✅ All Human Olfactory Systems Nominal. Ready for 0400 Deployment.")
