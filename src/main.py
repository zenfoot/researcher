"""
Entry point of the application; initiates the orchestration agent.

This script starts the AI Scientist system by creating an instance of the
AdaptiveOrchestrationAgent and running the main workflow.
"""


from agents.adaptive_orchestration_agent import AdaptiveOrchestrationAgent

def main():
    orchestrator = AdaptiveOrchestrationAgent()
    orchestrator.run_workflow()

if __name__ == "__main__":
    main()