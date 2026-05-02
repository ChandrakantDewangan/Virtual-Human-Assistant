class Thinker:
    def __init__(self):
        self.risk_keywords = ["delete", "overwrite", "remove", "wipe"]

    def analyze(self, intent, user_input):
        user_input_lower = user_input.lower()
        risk_level = "low"

        if any(keyword in user_input_lower for keyword in self.risk_keywords):
            risk_level = "high"

        return {
            "intent": intent,
            "risk": risk_level,
            "context": "general",
            "needs_human_confirmation": risk_level == "high"
        }
