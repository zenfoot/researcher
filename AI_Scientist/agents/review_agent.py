from utils.prompt_templates import PEER_REVIEW_PROMPT

class PeerReviewAgent:
    def __init__(self, llm, improvement_agent):
        self.llm = llm
        self.improvement_agent = improvement_agent

    async def perform_review(self, report):
        prompt = PEER_REVIEW_PROMPT.format(report=report)
        response = self.llm(prompt)
        print(f"Peer Review Feedback:\n{response}")
        await self.improvement_agent.improve_report(report, response)
