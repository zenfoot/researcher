"""
Coordinates the overall workflow among different agents.

The AdaptiveOrchestrationAgent orchestrates the sequence of tasks performed
by various agents, managing the flow from idea generation to report improvement.
"""


from agents.user_interaction_agent import UserInteractionAgent
from agents.idea_generation_agent import IdeaGenerationAgent
from agents.novelty_evaluation_agent import NoveltyEvaluationAgent
from agents.experiment_design_agent import ExperimentDesignAgent
from agents.experiment_execution_agent import ExperimentExecutionAgent
from agents.data_analysis_agent import DataAnalysisAgent
from agents.reporting_agent import ReportingAgent
from agents.peer_review_simulation_agent import PeerReviewSimulationAgent
from agents.improvement_agent import ImprovementAgent
from agents.resource_management_agent import ResourceManagementAgent

class AdaptiveOrchestrationAgent:
    def __init__(self):
        self.user_agent = UserInteractionAgent()
        self.idea_agent = IdeaGenerationAgent()
        self.novelty_agent = NoveltyEvaluationAgent()
        self.experiment_design_agent = ExperimentDesignAgent()
        self.experiment_execution_agent = ExperimentExecutionAgent()
        self.data_analysis_agent = DataAnalysisAgent()
        self.reporting_agent = ReportingAgent()
        self.peer_review_agent = PeerReviewSimulationAgent()
        self.improvement_agent = ImprovementAgent()
        self.resource_manager = ResourceManagementAgent()

    def run_workflow(self):
        # Engage with the user to gather requirements
        domain = input("Please specify the research domain: ")
        num_ideas = int(input("How many ideas would you like to generate? "))

        # Generate ideas
        ideas = self.idea_agent.generate_ideas(domain, num_ideas)
        print("Generated Ideas:")
        for idx, idea in enumerate(ideas, 1):
            print(f"{idx}. {idea}")

        # Evaluate novelty
        novel_ideas = []
        for idea in ideas:
            is_novel = self.novelty_agent.evaluate_novelty(idea)
            if is_novel:
                novel_ideas.append(idea)
        print("Novel Ideas:")
        for idx, idea in enumerate(novel_ideas, 1):
            print(f"{idx}. {idea}")

        if not novel_ideas:
            print("No novel ideas found. Exiting.")
            return

        # Proceed with the first novel idea
        selected_idea = novel_ideas[0]
        print(f"Selected Idea: {selected_idea}")

        # Design experiment
        experiment_plan = self.experiment_design_agent.design_experiment(selected_idea)
        print(f"Experiment Plan:\n{experiment_plan}")

        # Allocate resources
        self.resource_manager.allocate_resources()

        # Execute experiment
        experimental_data = self.experiment_execution_agent.execute_experiment(experiment_plan)
        print(f"Experimental Data:\n{experimental_data}")

        # Analyze data
        analysis_results = self.data_analysis_agent.analyze_data(experimental_data)
        print(f"Analysis Results:\n{analysis_results}")

        # Write report
        report = self.reporting_agent.create_report(selected_idea, experiment_plan, analysis_results)
        print(f"Generated Report:\n{report}")

        # Simulate peer review
        feedback = self.peer_review_agent.review_report(report)
        print(f"Peer Review Feedback:\n{feedback}")

        # Improve report
        improved_report = self.improvement_agent.improve_report(report, feedback)
        print(f"Improved Report:\n{improved_report}")

        # Monitor resources
        self.resource_manager.monitor_resources()

        print("Workflow completed successfully.")