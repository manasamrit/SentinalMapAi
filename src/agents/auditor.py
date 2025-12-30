from src.services.gemini_api import GeminiService
from src.utils.mock_data import POLICIES
import time

class PolicyAuditorAgent:
    def __init__(self, gemini_key):
        self.gemini_service = GeminiService(gemini_key)
        self.logs = []

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] [AUDITOR] {message}")

    def audit(self, place_data, osint_data):
        self.logs = []
        self.log("Received case file from Investigator.")
        
        # Step 1: Context Loading
        self.log("Loading Policy Framework: 'Google Maps User Contributed Content Policy'...")
        # (In a real app, we might dynamically select policies, here we use the static set)
        
        # Step 2: Reasoning
        self.log("Step 2: Sending data to Gemini Pro for reasoning...")
        analysis = self.gemini_service.analyze_policy_compliance(place_data, osint_data, POLICIES)
        self.log("Analysis Complete.")
        
        return analysis
