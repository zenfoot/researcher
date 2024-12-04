from utils.prompt_templates import EXPERIMENT_DESIGN_PROMPT

class ExperimentDesignAgent:
    def __init__(self, llm, experiment_execution_agent):
        self.llm = llm
        self.experiment_execution_agent = experiment_execution_agent

    async def design_experiment(self, idea_json):
        prompt = EXPERIMENT_DESIGN_PROMPT.format(
            idea_title=idea_json.get("Title", ""),
            idea_experiment=idea_json.get("Experiment", ""),
            max_runs=3,
            baseline_results="Baseline results data."
        )
        response = self.llm(prompt)
        print(f"Experiment Design Plan:\n{response}")
        await self.experiment_execution_agent.execute_experiment(response)
