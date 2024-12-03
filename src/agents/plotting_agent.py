"""
Generates plots and visualizations from experimental data.

This agent creates visual representations of data to aid in analysis
and inclusion in reports.
"""


from models.llm_provider import get_llm
import subprocess
import os

class PlottingAgent:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.llm = get_llm()
        with open('src/prompts/plotting_instructions_prompt.txt', 'r') as f:
            self.plotting_prompt_template = f.read()
        self.max_iterations = 4

    def modify_and_run_plot(self):
        current_iter = 0
        next_prompt = self.plotting_prompt_template
        while True:
            response = self.llm.predict(next_prompt)
            # Assume LLM modifies plot.py in the folder
            return_code, next_prompt = self.run_plotting()
            current_iter += 1
            if return_code == 0 or current_iter >= self.max_iterations:
                break

    def run_plotting(self, timeout=600):
        cwd = os.path.abspath(self.folder_name)
        command = [
            "python",
            "plot.py",
        ]
        try:
            result = subprocess.run(
                command, cwd=cwd, stderr=subprocess.PIPE, text=True, timeout=timeout
            )
            if result.stderr:
                print(result.stderr)
            if result.returncode != 0:
                # Plotting failed
                next_prompt = f"Plotting failed with the following error {result.stderr}"
            else:
                # Plotting succeeded
                next_prompt = ""
            return result.returncode, next_prompt
        except subprocess.TimeoutExpired:
            # Plotting timed out
            next_prompt = f"Plotting timed out after {timeout} seconds"
            return 1, next_prompt