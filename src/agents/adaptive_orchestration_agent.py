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

        # Generate idea
        idea_json, response = self.idea_agent.generate_idea()
        msg_history = [{"role": "assistant", "content": response}]

        # Reflect on idea
        for current_round in range(1, self.idea_agent.num_reflections + 1):
            reflection_agent = IdeaReflectionAgent(
                idea_json=idea_json,
                current_round=current_round,
                num_reflections=self.idea_agent.num_reflections
            )
            idea_json_new, response = reflection_agent.reflect_on_idea(msg_history)
            if idea_json_new:
                idea_json = idea_json_new
            msg_history.append({"role": "assistant", "content": response})
            if "I am done" in response:
                break

        print(f"Final Idea after reflection:\n{json.dumps(idea_json, indent=2)}")

        # Evaluate novelty
        novelty_agent = NoveltyEvaluationAgent(
            idea=idea_json,
            task_description=self.idea_agent.task_description,
            code_snippet=self.idea_agent.code_snippet,
            num_rounds=5  # or any suitable number
        )
        novelty_decision = novelty_agent.evaluate_novelty()
        print(f"Novelty Evaluation Result: {novelty_decision}")

        # Proceed based on novelty decision
        if novelty_decision == "Novel":
            # Continue with experiment design, execution, etc.
            pass
        else:
            print("Idea is not novel. Generating a new idea.")
            # Optionally, loop back to generate a new idea

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


# simplified from "Putting It All Together" section of LangChain Evaluation document, perhaps useful for evaluation...

class AdaptiveOrchestrationAgent:
    def __init__(self):
        self.idea_generator = IdeaGenerationAgent(domain="Your Domain")
        self.novelty_evaluator = NoveltyEvaluationAgent()
        self.experiment_planner = None
        self.experiment_executor = ExperimentExecutionAgent()
        self.data_analyzer = DataAnalysisAgent()
        self.reporter = None
        self.citation_manager = None
        self.error_checker = None
        self.document_compiler = DocumentCompilationAgent()
        self.review_generator = ReviewGenerationAgent()
        self.improvement_agent = ImprovementAgent()

    def run(self):
        # Idea Generation
        ideas = self.idea_generator.generate_ideas()
        print(f"Generated Ideas: {ideas}")

        # Novelty Evaluation
        novel_ideas = [idea for idea in ideas if self.novelty_evaluator.evaluate_novelty(idea)]
        if not novel_ideas:
            print("No novel ideas found.")
            return
        selected_idea = novel_ideas[0]
        print(f"Selected Idea: {selected_idea}")

        # Experiment Planning
        self.experiment_planner = ExperimentPlanningAgent(selected_idea)
        experiment_plan = self.experiment_planner.design_experiment()
        print(f"Experiment Plan:\n{experiment_plan}")

        # Experiment Execution
        results = self.experiment_executor.execute(experiment_plan)
        print(f"Experiment Results:\n{results}")

        # Data Analysis
        analysis = self.data_analyzer.analyze(results)
        print(f"Data Analysis:\n{analysis}")

        # Reporting
        self.reporter = ReportingAgent(selected_idea, analysis)
        report_path = self.reporter.create_report()

        # Citation Management
        self.citation_manager = CitationManagementAgent(report_path)
        self.citation_manager.add_citations()

        # Error Checking
        self.error_checker = ErrorCheckingAgent()
        self.error_checker.check_and_fix_errors(report_path)

        # Document Compilation
        self.document_compiler.compile(report_path, output_dir='outputs')

        # Review Generation
        review = self.review_generator.generate_review(report_path)
        print(f"Peer Review:\n{review}")

        # Report Improvement
        improved_report = self.improvement_agent.improve_report(report_path, review)
        print(f"Improved Report:\n{improved_report}")

        # Final Compilation
        # Save improved report and compile