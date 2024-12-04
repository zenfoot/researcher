"""
Creates comprehensive research reports in LaTeX format.

This agent compiles the findings into a structured report, adhering
to academic standards and formatting guidelines.
"""


# from models.llm_provider import get_llm

# class ReportingAgent:
#     def __init__(self):
#         self.llm = get_llm()

#     def create_report(self, idea, experiment_details, analysis_results):
#         prompt = f"Write a comprehensive scientific report based on the following information:\nIdea: {idea}\nExperiment Details: {experiment_details}\nAnalysis Results: {analysis_results}\nThe report should include an abstract, introduction, methodology, results, discussion, and conclusion."
#         report = self.llm.predict(prompt)
#         return report


from models.llm_provider import get_llm
from prompts import load_prompt
from utils.latex_utils import generate_latex, compile_latex
import os

class ReportingAgent:
    def __init__(self):
        self.llm = get_llm()
        self.per_section_tips = load_prompt('per_section_tips.txt', as_dict=True)
        self.refinement_prompt = load_prompt('refinement_prompt.txt')
        self.second_refinement_prompt = load_prompt('second_refinement_prompt.txt')
        self.abstract_prompt = load_prompt('abstract_prompt.txt')
        self.section_prompt = load_prompt('section_prompt.txt')
        self.sections = [
            'Introduction',
            'Background',
            'Method',
            'Experimental Setup',
            'Results',
            'Conclusion',
            'Related Work'
        ]
        self.latex_template_path = 'data/latex/template.tex'  # Adjust path as needed

    def create_initial_draft(self, idea):
        # Prepare the LaTeX template
        self.initialize_latex_template(idea)
        
        # Generate Abstract
        self.generate_abstract(idea)
        
        # Generate each section
        for section in self.sections:
            self.generate_section(section)
            self.refine_section(section)
        
        # Second refinement loop
        self.second_refinement()

    def initialize_latex_template(self, idea):
        # Copy template and set the title
        pass  # Implement as needed

    def generate_abstract(self, idea):
        prompt = self.abstract_prompt.format(
            tips=self.per_section_tips['Abstract']
        )
        abstract = self.llm.predict(prompt)
        # Save abstract to LaTeX file
        pass  # Implement saving logic

    def generate_section(self, section):
        prompt = self.section_prompt.format(
            section=section,
            tips=self.per_section_tips.get(section, '')
        )
        content = self.llm.predict(prompt)
        # Append content to LaTeX file
        pass  # Implement saving logic

    def refine_section(self, section):
        prompt = self.refinement_prompt.format(section=section)
        refined_content = self.llm.predict(prompt)
        # Update the LaTeX file with refined content
        pass  # Implement saving logic

    def second_refinement(self):
        # Re-evaluate the title
        title_refinement_prompt = load_prompt('second_refinement_loop_prompt.txt')
        refined_title = self.llm.predict(title_refinement_prompt)
        # Update LaTeX file with refined title
        pass  # Implement saving logic

        # Refine each section again
        for section in self.sections:
            prompt = self.second_refinement_prompt.format(
                section=section,
                tips=self.per_section_tips.get(section, '')
            )
            refined_content = self.llm.predict(prompt)
            # Update LaTeX file with refined content
            pass  # Implement saving logic

    def generate_final_report(self):
        # Compile the LaTeX document
        compile_latex(self.latex_template_path)
        # Handle any compilation errors with ErrorCheckingAgent
        pass


# from models.llm_provider import get_llm
# from prompts import load_prompt
# import os

# class ReportingAgent:
#     def __init__(self, idea, analysis):
#         self.llm = get_llm()
#         self.idea = idea
#         self.analysis = analysis
#         self.latex_template_path = os.path.join('data', 'latex', 'template.tex')

#     def create_report(self):
#         # Generate the report content
#         prompt = f"Write a research paper based on the idea '{self.idea}' and the analysis:\n{self.analysis}"
#         report_content = self.llm.predict(prompt)
#         # Save to LaTeX
#         with open(self.latex_template_path, 'w') as file:
#             file.write(report_content)
#         return self.latex_template_path