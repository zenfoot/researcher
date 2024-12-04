from utils.prompt_templates import IMPROVEMENT_PROMPT

class ImprovementAgent:
    def __init__(self, llm):
        self.llm = llm

    async def improve_report(self, report, review):
        prompt = IMPROVEMENT_PROMPT.format(report=report, review=review)
        response = self.llm(prompt)
        print("Final improved report is ready!")
