from utils.prompt_templates import DATA_ANALYSIS_PROMPT

class DataAnalysisAgent:
    def __init__(self, llm, reporting_agent):
        self.llm = llm
        self.reporting_agent = reporting_agent

    async def analyze_data(self, execution_results):
        prompt = DATA_ANALYSIS_PROMPT.format(results=execution_results)
        response = self.llm(prompt)
        print(f"Data Analysis Results:\n{response}")
        await self.reporting_agent.compile_report(response)
