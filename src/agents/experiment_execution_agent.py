"""
Agent responsible for executing experiments and collecting data.

This agent takes an experimental plan and runs the necessary procedures to
gather data, handling errors and timeouts as necessary.
"""


# class ExperimentExecutionAgent:
#     def __init__(self):
#         pass

#     def execute_experiment(self, experiment_plan):
#         # Simulate experiment execution
#         print("Executing experiment...")
#         # Placeholder for actual execution logic
#         results = "Simulated experimental results."
#         return results


from models.llm_provider import get_llm
import subprocess
import os
import shutil
import json

class ExperimentExecutionAgent:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.llm = get_llm()
        # Load prompts
        with open('src/prompts/experiment_failure_prompt.txt', 'r') as f:
            self.failure_prompt_template = f.read()
        with open('src/prompts/experiment_completion_prompt.txt', 'r') as f:
            self.completion_prompt_template = f.read()
        with open('src/prompts/run_timeout_prompt.txt', 'r') as f:
            self.timeout_prompt_template = f.read()
        self.max_stderr_output = 1500  # As per the code

    def run_experiment(self, run_num, timeout=7200):
        cwd = os.path.abspath(self.folder_name)
        # Copy code for versioning
        shutil.copy(
            os.path.join(self.folder_name, "experiment.py"),
            os.path.join(self.folder_name, f"run_{run_num}.py"),
        )
        # Command to run
        command = [
            "python",
            "experiment.py",
            f"--out_dir=run_{run_num}",
        ]
        try:
            result = subprocess.run(
                command, cwd=cwd, stderr=subprocess.PIPE, text=True, timeout=timeout
            )
            if result.stderr:
                print(result.stderr)
            if result.returncode != 0:
                # Experiment failed
                if os.path.exists(os.path.join(cwd, f"run_{run_num}")):
                    shutil.rmtree(os.path.join(cwd, f"run_{run_num}"))
                stderr_output = result.stderr
                if len(stderr_output) > self.max_stderr_output:
                    stderr_output = "..." + stderr_output[-self.max_stderr_output:]
                next_prompt = self.failure_prompt_template.format(stderr_output=stderr_output)
            else:
                # Experiment succeeded
                with open(os.path.join(cwd, f"run_{run_num}", "final_info.json"), "r") as f:
                    results = json.load(f)
                results_summary = {k: v["means"] for k, v in results.items()}
                next_prompt = self.completion_prompt_template.format(
                    run_num=run_num,
                    results=results_summary
                )
            return result.returncode, next_prompt
        except subprocess.TimeoutExpired:
            # Experiment timed out
            if os.path.exists(os.path.join(cwd, f"run_{run_num}")):
                shutil.rmtree(os.path.join(cwd, f"run_{run_num}"))
            next_prompt = self.timeout_prompt_template.format(timeout=timeout)
            return 1, next_prompt