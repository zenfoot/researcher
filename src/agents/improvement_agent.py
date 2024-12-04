"""
Improves the research report based on review feedback.

This agent modifies the original report by incorporating reviewer suggestions,
enhancing clarity, and addressing identified issues.
"""


# from models.llm_provider import get_llm

# class ImprovementAgent:
#     def __init__(self):
#         self.llm = get_llm()

#     def improve_report(self, report, feedback):
#         prompt = f"Based on the following feedback, improve the scientific report.\nReport:\n{report}\nFeedback:\n{feedback}\nProvide the revised report."
#         improved_report = self.llm.predict(prompt)
#         return improved_report


from models.llm_provider import get_llm
from prompts import load_prompt
import json

class ImprovementAgent:
    def __init__(self):
        self.llm = get_llm()
        self.improvement_prompt = load_prompt('improvement_prompt.txt')

    def improve_report(self, report, review):
        prompt = self.improvement_prompt.format(report=report, review=json.dumps(review))
        improved_report = self.llm.predict(prompt)
        return improved_report


# from models.llm_provider import get_llm

# class ImprovementAgent:
#     def __init__(self):
#         self.llm = get_llm()

#     def improve_report(self, report, review):
#         prompt = f"Based on the following review, improve the research paper:\nReview:\n{review}\nPaper:\n{report}"
#         improved_report = self.llm.predict(prompt)
#         return improved_report