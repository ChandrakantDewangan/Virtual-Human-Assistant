class IntentDetector:
    def __init__(self):
        # In a real scenario, this could be a call to an LLM
        self.action_keywords = ["open", "click", "type", "submit", "fill", "update", "create", "delete", "run"]
        self.goal_keywords = ["complete", "finish", "manage", "organize", "handle"]

    def classify(self, user_input):
        user_input_lower = user_input.lower()

        # Check for goal-driven intent
        if any(keyword in user_input_lower for keyword in self.goal_keywords):
            return "Goal-driven"

        # Check for actionable intent
        if any(keyword in user_input_lower for keyword in self.action_keywords):
            return "Actionable"

        # Default to informational
        return "Informational"
