class VirtualHuman:
    def __init__(self, intent_detector=None, thinker=None, planner=None, executor=None):
        self.intent_detector = intent_detector
        self.thinker = thinker
        self.planner = planner
        self.executor = executor
        self.memory = []

    def run(self, user_input):
        print(f"--- Starting Intelligence Loop ---")
        print(f"User Input: {user_input}")

        # 1. Understand
        intent = self.understand(user_input)
        print(f"Step 1: Understand - Intent identified: {intent}")

        # 2. Think
        analysis = self.think(intent, user_input)
        print(f"Step 2: Think - Analysis: {analysis}")

        # 3. Plan
        plan = self.plan(analysis, intent, user_input)
        print(f"Step 3: Plan - Plan created: {plan}")

        # 4. Act
        # Extract potential URLs for the executor in Phase 1
        url = None
        if "http" in user_input:
            import re
            urls = re.findall(r'(https?://\S+)', user_input)
            if urls:
                url = urls[0]

        result = self.act(plan, context_data={"url": url})
        print(f"Step 4: Act - Action complete: {result}")

        # 5. Verify
        verification = self.verify(result, plan)
        print(f"Step 5: Verify - Status: {verification}")

        # 6. Learn
        self.learn(user_input, intent, plan, result, verification)
        print("Step 6: Learn - Memory stored.")
        print(f"--- Loop Complete ---")

        return result

    def understand(self, user_input):
        if self.intent_detector:
            return self.intent_detector.classify(user_input)
        return "Unknown"

    def think(self, intent, user_input):
        if self.thinker:
            return self.thinker.analyze(intent, user_input)
        return {"risk": "low", "context": "general"}

    def plan(self, analysis, intent, user_input):
        if self.planner:
            return self.planner.create_plan(analysis, intent, user_input)
        return ["Process input"]

    def act(self, plan, context_data=None):
        if self.executor:
            return self.executor.execute(plan, context_data=context_data)
        return "Task performed"

    def verify(self, result, plan):
        # Basic verification logic for Phase 1
        if result:
            return "Verified Successfully"
        return "Verification Failed"

    def learn(self, user_input, intent, plan, result, verification):
        self.memory.append({
            "input": user_input,
            "intent": intent,
            "plan": plan,
            "result": result,
            "verification": verification
        })
