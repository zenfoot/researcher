class KnowledgeManagementAgent:
    def __init__(self):
        self.knowledge_base = []

    def store_idea(self, idea_json):
        self.knowledge_base.append(idea_json)
        print("Idea stored.")

    def get_previous_ideas(self):
        return [f"Name: {idea.get('Name')}, Title: {idea.get('Title')}" for idea in self.knowledge_base]
