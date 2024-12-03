"""
Creates comprehensive research reports in LaTeX format.

This agent compiles the findings into a structured report, adhering
to academic standards and formatting guidelines.
"""


from models.llm_provider import get_llm

class ReportingAgent:
    def __init__(self):
        self.llm = get_llm()

    def create_report(self, idea, experiment_details, analysis_results):
        prompt = f"Write a comprehensive scientific report based on the following information:\nIdea: {idea}\nExperiment Details: {experiment_details}\nAnalysis Results: {analysis_results}\nThe report should include an abstract, introduction, methodology, results, discussion, and conclusion."
        report = self.llm.predict(prompt)
        return report