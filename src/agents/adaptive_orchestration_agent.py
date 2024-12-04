"""
Coordinates the overall workflow among different agents.

The AdaptiveOrchestrationAgent orchestrates the sequence of tasks performed
by various agents, managing the flow from idea generation to report improvement.
"""


import logging
import json

from agents.base_agent import BaseAgent
from agents.user_interaction_agent import UserInteractionAgent
from agents.idea_generation_agent import IdeaGenerationAgent
from agents.idea_reflection_agent import IdeaReflectionAgent
from agents.novelty_evaluation_agent import NoveltyEvaluationAgent
from agents.experiment_planning_agent import ExperimentPlanningAgent
from agents.experiment_design_agent import ExperimentDesignAgent
from agents.experiment_execution_agent import ExperimentExecutionAgent
from agents.data_analysis_agent import DataAnalysisAgent
from agents.plotting_agent import PlottingAgent
from agents.documentation_agent import DocumentationAgent
from agents.reporting_agent import ReportingAgent
from agents.citation_management_agent import CitationManagementAgent
from agents.error_checking_agent import ErrorCheckingAgent
from agents.document_compilation_agent import DocumentCompilationAgent
from agents.review_generation_agent import ReviewGenerationAgent
from agents.improvement_agent import ImprovementAgent
from agents.resource_management_agent import ResourceManagementAgent
from utils.paper_loader import PaperLoader
from models.llm_provider import get_llm


class AdaptiveOrchestrationAgent(BaseAgent):
    """Orchestrates the entire AI Scientist workflow by coordinating agents."""

    def __init__(self, domain: str = None, num_ideas: int = 3):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.domain = domain
        self.num_ideas = num_ideas
        self.llm = get_llm()
        self.initialize_agents()

    def initialize_agents(self):
        """Initializes all the agents used in the workflow."""
        self.logger.info("Initializing agents.")
        self.user_agent = UserInteractionAgent()
        self.idea_agent = IdeaGenerationAgent(domain=self.domain, num_ideas=self.num_ideas)
        # IdeaReflectionAgent will be instantiated during the reflection phase
        self.novelty_agent = NoveltyEvaluationAgent()
        self.resource_manager = ResourceManagementAgent()
        self.data_analysis_agent = DataAnalysisAgent()
        self.citation_manager = CitationManagementAgent()
        self.error_checker = ErrorCheckingAgent()
        self.document_compilation_agent = DocumentCompilationAgent()
        self.review_generation_agent = ReviewGenerationAgent()
        self.improvement_agent = ImprovementAgent()
        # Agents initialized as None will be created as needed
        self.experiment_design_agent = None
        self.experiment_planning_agent = None
        self.experiment_execution_agent = None
        self.reporting_agent = None
        self.plotting_agent = None
        self.documentation_agent = None

    def run(self):
        """Executes the full AI Scientist workflow."""
        try:
            # User Interaction
            self.gather_user_input()

            # Idea Generation and Reflection
            ideas = self.generate_and_refine_ideas()

            # Novelty Evaluation
            novel_idea = self.evaluate_novelty(ideas)
            if not novel_idea:
                self.logger.warning("No novel ideas found. Exiting workflow.")
                return

            # Experiment Design
            experiment_plan = self.design_experiment(novel_idea)

            # Resource Allocation
            self.resource_manager.allocate_resources()

            # Experiment Planning
            experiment_script = self.plan_experiment(novel_idea)

            # Experiment Execution
            execution_output = self.execute_experiment(experiment_script)

            # Data Analysis
            analysis_results = self.analyze_data(execution_output)

            # Plotting
            self.plot_results(execution_output)

            # Documentation
            self.document_experiment(execution_output)

            # Reporting
            report_path = self.generate_report(novel_idea, analysis_results)

            # Citation Management
            self.manage_citations(report_path)

            # Error Checking
            self.check_errors(report_path)

            # Document Compilation
            compiled_report = self.compile_document(report_path)

            # Peer Review Simulation
            review = self.generate_review(compiled_report)

            # Report Improvement
            improved_report_path = self.improve_report(report_path, review)

            # Final Compilation
            final_compiled_report = self.compile_document(improved_report_path)

            # Resource Monitoring
            self.resource_manager.monitor_resources()

            self.logger.info("Workflow completed successfully.")
        except Exception as e:
            self.logger.exception(f"Workflow failed: {e}")

    def gather_user_input(self):
        """Gathers input from the user."""
        if not self.domain:
            self.domain = input("Please specify the research domain: ")
        if not self.num_ideas:
            self.num_ideas = int(input("How many ideas would you like to generate? "))
        self.logger.info(f"User selected domain: {self.domain}, number of ideas: {self.num_ideas}")

    def generate_and_refine_ideas(self):
        """Generates and refines research ideas."""
        ideas = self.idea_agent.generate_ideas()
        if not ideas:
            self.logger.error("No ideas were generated.")
            return []
        self.logger.info(f"Generated {len(ideas)} ideas.")

        # Reflection Phase
        idea_json = {"Ideas": ideas}
        msg_history = []
        num_reflections = self.idea_agent.num_reflections if hasattr(self.idea_agent, 'num_reflections') else 3

        for current_round in range(1, num_reflections + 1):
            reflection_agent = IdeaReflectionAgent(
                idea_json=idea_json,
                current_round=current_round,
                num_reflections=num_reflections
            )
            idea_json_new, response = reflection_agent.reflect_on_ideas(msg_history)
            if idea_json_new:
                idea_json = idea_json_new
            msg_history.append({"role": "assistant", "content": response})
            if "I am done" in response:
                break

        self.logger.info(f"Final Idea after reflection:\n{json.dumps(idea_json, indent=2)}")
        return idea_json.get("Ideas", [])

    def evaluate_novelty(self, ideas):
        """Evaluates the novelty of generated ideas."""
        novel_ideas = []
        for idea in ideas:
            is_novel = self.novelty_agent.evaluate_novelty(idea)
            if is_novel:
                novel_ideas.append(idea)
        if not novel_ideas:
            self.logger.warning("No novel ideas found after evaluation.")
            return None
        selected_idea = novel_ideas[0]
        self.logger.info(f"Selected novel idea: {selected_idea}")
        return selected_idea

    def design_experiment(self, idea):
        """Designs an experiment based on the selected idea."""
        self.experiment_design_agent = ExperimentDesignAgent(idea)
        experiment_plan = self.experiment_design_agent.design_experiment()
        self.logger.info(f"Experiment plan created:\n{experiment_plan}")
        return experiment_plan

    def plan_experiment(self, idea):
        """Plans the experiment execution."""
        self.experiment_planning_agent = ExperimentPlanningAgent(
            idea_title=idea.get('Title', 'Untitled'),
            idea_description=idea.get('Description', ''),
            max_runs=5,
            baseline_results="Baseline results data"
        )
        planning_response = self.experiment_planning_agent.plan_experiments()
        self.logger.info(f"Experiment planning response:\n{planning_response}")
        return planning_response  # Assuming this is the experiment script or relevant command

    def execute_experiment(self, experiment_script):
        """Executes the planned experiment."""
        folder_name = "experiment_folder"
        self.experiment_execution_agent = ExperimentExecutionAgent(folder_name=folder_name)
        current_iter = 0
        run_num = 1
        max_iters = 4

        while run_num <= self.experiment_planning_agent.max_runs:
            if current_iter >= max_iters:
                self.logger.warning("Maximum iterations reached during experiment execution.")
                break
            return_code, next_prompt = self.experiment_execution_agent.run_experiment(run_num)
            if return_code == 0:
                self.logger.info(f"Experiment run {run_num} completed successfully.")
                current_iter = 0
                run_num += 1
            else:
                self.logger.error(f"Experiment run {run_num} failed.")
                current_iter += 1
                # Adjust experiment based on feedback
                adjustment_response = self.llm.predict(next_prompt)
                self.logger.debug(f"LLM adjustment response: {adjustment_response}")
                if 'ALL_COMPLETED' in adjustment_response:
                    break

        execution_output = self.experiment_execution_agent.get_results()
        return execution_output

    def analyze_data(self, execution_output):
        """Analyzes the data from experiment execution."""
        analysis_results = self.data_analysis_agent.analyze_data(execution_output)
        self.logger.info(f"Data analysis results:\n{analysis_results}")
        return analysis_results

    def plot_results(self, execution_output):
        """Generates plots based on the analysis results."""
        self.plotting_agent = PlottingAgent(data=execution_output)
        self.plotting_agent.modify_and_run_plot()
        self.logger.info("Plots generated successfully.")

    def document_experiment(self, execution_output):
        """Updates experimental notes and documentation."""
        self.documentation_agent = DocumentationAgent(data=execution_output)
        self.documentation_agent.update_notes()
        self.logger.info("Experiment documentation updated.")

    def generate_report(self, idea, analysis_results):
        """Generates the research report in LaTeX format."""
        self.reporting_agent = ReportingAgent(idea, analysis_results)
        report_path = self.reporting_agent.run()
        self.logger.info(f"Report generated at {report_path}.")
        return report_path

    def manage_citations(self, report_path):
        """Manages citations within the report."""
        self.citation_manager.run(report_path)
        self.logger.info("Citations integrated into the report.")

    def check_errors(self, report_path):
        """Checks and corrects errors in the LaTeX document."""
        self.error_checker.run(report_path)
        self.logger.info("Errors checked and corrected in the report.")

    def compile_document(self, report_path):
        """Compiles the LaTeX report into a PDF document."""
        output_dir = 'outputs'
        compiled_pdf_path = self.document_compilation_agent.run(report_path, output_dir)
        if compiled_pdf_path:
            self.logger.info(f"Document compiled successfully: {compiled_pdf_path}")
        else:
            self.logger.error("Document compilation failed.")
        return compiled_pdf_path

    def generate_review(self, compiled_pdf_path):
        """Generates a peer review of the compiled report."""
        paper_loader = PaperLoader()
        paper_text = paper_loader.load_paper(compiled_pdf_path)
        review = self.review_generation_agent.run(paper_text)
        self.logger.info(f"Generated review:\n{json.dumps(review, indent=2)}")
        return review

    def improve_report(self, report_path, review):
        """Improves the report based on the review feedback."""
        improved_report_path = self.improvement_agent.run(report_path, review)
        self.logger.info(f"Report improved and saved at {improved_report_path}.")
        return improved_report_path