import sys
from src.virtual_human import VirtualHuman
from src.intent_detector import IntentDetector
from src.thinker import Thinker
from src.planner import Planner
from src.manual_executor import SyncManualExecutor

def main():
    # Initialize components
    intent_detector = IntentDetector()
    thinker = Thinker()
    planner = Planner()
    executor = SyncManualExecutor()

    vh = VirtualHuman(
        intent_detector=intent_detector,
        thinker=thinker,
        planner=planner,
        executor=executor
    )

    print("========================================")
    print("   Virtual Human Assistant (Phase 1)    ")
    print("========================================")

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        vh.run(user_input)
    else:
        while True:
            try:
                user_input = input("\nHow can I help you today? (Type 'exit' to quit): ")
                if user_input.lower() in ['exit', 'quit']:
                    break

                vh.run(user_input)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
