"""
Analyzes experimental data and extracts meaningful insights.

The agent processes the collected data, performing statistical analyses
and interpreting results to draw conclusions.
"""


# from models.llm_provider import get_llm

# class DataAnalysisAgent:
#     def __init__(self):
#         self.llm = get_llm()

#     def analyze_data(self, data):
#         prompt = f"Analyze the following data and summarize the key findings:\n{data}"
#         response = self.llm.predict(prompt)
#         return response


from models.llm_provider import get_llm

class DataAnalysisAgent:
    def __init__(self):
        self.llm = get_llm()

    def analyze(self, data):
        prompt = f"Analyze the following data and provide insights:\n{data}"
        analysis = self.llm.predict(prompt)
        return analysis