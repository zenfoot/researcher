from utils.prompt_templates import IDEA_PROMPT

class IdeaGenerationAgent:
    def __init__(self, llm, knowledge_management_agent, novelty_evaluation_agent):
        self.llm = llm
        self.knowledge_management_agent = knowledge_management_agent
        self.novelty_evaluation_agent = novelty_evaluation_agent

    async def generate_idea(self, user_input):
        prev_ideas = self.knowledge_management_agent.get_previous_ideas()
        prev_ideas_string = '\n'.join(prev_ideas) if prev_ideas else 'None'
        prompt = IDEA_PROMPT.format(user_input=user_input, prev_ideas=prev_ideas_string)
        response = self.llm(prompt)
        idea_json = self.extract_idea_json(response)
        self.knowledge_management_agent.store_idea(idea_json)
        await self.novelty_evaluation_agent.evaluate_novelty(idea_json)

    def extract_idea_json(self, text):
        import json, re
        match = re.search(r'NEW IDEA JSON:\s*(\{.*\})', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        else:
            raise ValueError("No JSON found in the idea text")
