"""
Checks for errors in documents and code; ensures quality.

This agent performs validation checks on reports and code,
identifying and correcting errors.
"""


from models.llm_provider import get_llm
from utils.latex_utils import check_latex_errors
from prompts import load_prompt

class ErrorCheckingAgent:
    def __init__(self, draft_path):
        self.llm = get_llm()
        self.draft_path = draft_path
        self.common_errors = load_prompt('common_errors.txt')
        self.refinement_prompt = load_prompt('refinement_prompt.txt')

    def check_and_correct_errors(self):
        errors = check_latex_errors(self.draft_path)
        if errors:
            prompt = f"""Please fix the following LaTeX errors in `template.tex` guided by the output:
{errors}
Make the minimal fix required and do not remove or change any packages.
Pay attention to any accidental uses of HTML syntax, e.g., </end instead of \\end."""
            corrections = self.llm.predict(prompt)
            # Apply corrections to the LaTeX file
            pass  # Implement file I/O to update draft