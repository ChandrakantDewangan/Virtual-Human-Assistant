from src.intent_detector import IntentDetector

def test_classify_actionable():
    detector = IntentDetector()
    assert detector.classify("open the browser") == "Actionable"
    assert detector.classify("click the button") == "Actionable"
    assert detector.classify("submit the form") == "Actionable"

def test_classify_goal_driven():
    detector = IntentDetector()
    assert detector.classify("manage my daily tasks") == "Goal-driven"
    assert detector.classify("complete the project") == "Goal-driven"

def test_classify_informational():
    detector = IntentDetector()
    assert detector.classify("what is the weather?") == "Informational"
    assert detector.classify("tell me a story") == "Informational"
