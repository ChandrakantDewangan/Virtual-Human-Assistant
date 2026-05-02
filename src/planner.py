class Planner:
    def __init__(self):
        pass

    def create_plan(self, analysis, intent, user_input):
        # Basic planning logic for Phase 1
        if intent == "Informational":
            return ["Analyze request", "Formulate answer"]
        elif intent == "Actionable":
            return ["Identify tool", "Execute action", "Verify outcome"]
        elif intent == "Goal-driven":
            return ["Decompose goal", "Step 1: Execute", "Step 2: Verify", "Finalize"]

        return ["Process unknown request"]
