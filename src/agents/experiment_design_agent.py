"""
Designs detailed experimental procedures and setups.

This agent develops comprehensive experiment designs, including protocols,
equipment setups, and step-by-step procedures.
"""


from models.llm_provider import get_llm

class ExperimentDesignAgent:
    def __init__(self):
        self.llm = get_llm()

    def design_experiment(self, idea):
        prompt = f"Design an experiment to test the following idea:\n{idea}\nProvide detailed methodology, required resources, and expected outcomes."
        response = self.llm.predict(prompt)
        return response