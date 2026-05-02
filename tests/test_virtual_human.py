from src.virtual_human import VirtualHuman
from src.intent_detector import IntentDetector
from src.thinker import Thinker
from src.planner import Planner

class MockExecutor:
    def execute(self, plan, context_data=None):
        return "Mock executed"

def test_virtual_human_loop():
    vh = VirtualHuman(
        intent_detector=IntentDetector(),
        thinker=Thinker(),
        planner=Planner(),
        executor=MockExecutor()
    )

    result = vh.run("Open google.com")
    assert result == "Mock executed"
    assert len(vh.memory) == 1
    assert vh.memory[0]['intent'] == "Actionable"

def test_virtual_human_high_risk():
    vh = VirtualHuman(
        intent_detector=IntentDetector(),
        thinker=Thinker(),
        planner=Planner(),
        executor=MockExecutor()
    )

    vh.run("delete all files")
    assert vh.memory[0]['intent'] == "Actionable"
    # Thinker should identify high risk for 'delete'
    # In VirtualHuman we don't have special logic yet for high risk but it should be in the memory
