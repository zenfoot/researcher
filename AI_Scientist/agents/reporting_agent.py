from utils.prompt_templates import REPORT_COMPILATION_PROMPT

class ReportingAgent:
    def __init__(self, llm, peer_review_agent):
        self.llm = llm
        self.peer_review_agent = peer_review_agent

    async def compile_report(self, analysis):
        prompt = REPORT_COMPILATION_PROMPT.format(analysis=analysis)
        response = self.llm(prompt)
        print("Report compiled.")
        await self.peer_review_agent.perform_review(response)
