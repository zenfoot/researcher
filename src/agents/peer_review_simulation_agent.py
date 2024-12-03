"""
Simulates peer reviews for the research paper.

This agent mimics the peer review process, providing feedback
to improve the quality of the research report.
"""


from models.llm_provider import get_llm

class PeerReviewSimulationAgent:
    def __init__(self):
        self.llm = get_llm()

    def review_report(self, report):
        prompt = f"Conduct a peer review of the following scientific report. Provide constructive feedback, pointing out strengths and areas for improvement.\nReport:\n{report}"
        feedback = self.llm.predict(prompt)
        return feedback