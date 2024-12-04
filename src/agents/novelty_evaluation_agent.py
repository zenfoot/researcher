"""
Evaluates the novelty of ideas against existing literature.

Using LLMs and external databases, this agent determines whether a research
idea is novel or has been previously explored.
"""


# from agents.knowledge_management_agent import KnowledgeManagementAgent
# from models.llm_provider import get_llm

# class NoveltyEvaluationAgent:
#     def __init__(self):
#         self.llm = get_llm()
#         self.km_agent = KnowledgeManagementAgent()

#     def evaluate_novelty(self, idea):
#         similar_docs = self.km_agent.query(idea)
#         if not similar_docs:
#             return True  # Novel idea
#         # Further evaluation using LLM
#         prompt = f"Assess the novelty of the following idea considering existing research:\nIdea: {idea}\nSimilar Research: {similar_docs}\nIs this idea novel? Yes or No. Provide justification."
#         response = self.llm.predict(prompt)
#         return "Yes" in response


from langchain.prompts import PromptTemplate
from models.llm_provider import get_llm
from utils.api_clients import SemanticScholarAPI
import json

class NoveltyEvaluationAgent:
    def __init__(self, idea, task_description, code_snippet, num_rounds):
        self.llm = get_llm()
        with open('src/prompts/novelty_system_message.txt', 'r') as f:
            self.novelty_system_message = f.read()
        with open('src/prompts/novelty_prompt.txt', 'r') as f:
            self.novelty_prompt = f.read()
        self.idea = idea
        self.task_description = task_description
        self.code_snippet = code_snippet
        self.num_rounds = num_rounds
        self.api_client = SemanticScholarAPI()

    def evaluate_novelty(self):
        msg_history = []
        last_query_results = ""
        for current_round in range(1, self.num_rounds + 1):
            prompt = self.novelty_prompt.format(
                current_round=current_round,
                num_rounds=self.num_rounds,
                idea=json.dumps(self.idea, indent=2),
                last_query_results=last_query_results
            )
            system_message = self.novelty_system_message.format(
                num_rounds=self.num_rounds,
                task_description=self.task_description,
                code=self.code_snippet
            )
            response = self.llm.predict(prompt, system_message=system_message, chat_history=msg_history)
            thought, decision, query = self.parse_response(response)
            if decision:
                return decision
            if query:
                papers = self.api_client.search_papers(query)
                last_query_results = self.format_papers(papers)
            msg_history.append({"role": "assistant", "content": response})
        return "Novelty evaluation inconclusive."

    def parse_response(self, text):
        # Parse THOUGHT, decision (if any), and Query from JSON
        thought = ""
        decision = None
        query = None
        try:
            thought = text.split('THOUGHT:\n')[1].split('RESPONSE:')[0].strip()
            if "Decision made: novel." in thought:
                decision = "Novel"
            elif "Decision made: not novel." in thought:
                decision = "Not Novel"
            json_str = text.split('RESPONSE:\n```json')[1].split('```')[0].strip()
            response_json = json.loads(json_str)
            query = response_json.get("Query", "")
        except Exception as e:
            print(f"Error parsing response: {e}")
        return thought, decision, query

    def format_papers(self, papers):
        # Format papers for the LLM
        paper_strings = []
        for i, paper in enumerate(papers):
            paper_strings.append(
                f"""{i+1}: {paper['title']}. {', '.join(author['name'] for author in paper['authors'])}. {paper.get('venue', 'Unknown Venue')}, {paper.get('year', 'n.d.')}.\nNumber of citations: {paper.get('citationCount', 0)}\nAbstract: {paper.get('abstract', 'No abstract available.')}"""
            )
        return "\n\n".join(paper_strings)


# from models.llm_provider import get_llm
# from utils.api_clients import SemanticScholarAPI

# class NoveltyEvaluationAgent:
#     def __init__(self):
#         self.llm = get_llm()
#         self.s2_api = SemanticScholarAPI()

#     def evaluate_novelty(self, idea):
#         papers = self.s2_api.search_papers(idea)
#         if not papers:
#             return True
#         else:
#             # Further evaluation with LLM
#             prompt = f"Assess the novelty of the idea '{idea}' considering the following papers:\n"
#             for paper in papers:
#                 prompt += f"- {paper['title']} by {', '.join([author['name'] for author in paper['authors']])}\n"
#             prompt += "Is the idea still considered novel? Yes or No."
#             response = self.llm.predict(prompt)
#             return 'Yes' in response