from utils.prompt_templates import NOVELTY_PROMPT

class NoveltyEvaluationAgent:
    def __init__(self, llm, experiment_design_agent):
        self.llm = llm
        self.experiment_design_agent = experiment_design_agent

    async def evaluate_novelty(self, idea_json):
        prompt = NOVELTY_PROMPT.format(idea_description=idea_json.get('Experiment', ''))
        response = self.llm(prompt)
        if 'Decision made: novel' in response:
            await self.experiment_design_agent.design_experiment(idea_json)
        else:
            print("Idea is not novel. Generate a new idea.")
