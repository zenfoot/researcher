"""
Manages documentation and experimental notes.

The agent ensures that all experimental procedures and observations
are properly documented for transparency and reproducibility.
"""


from models.llm_provider import get_llm

class DocumentationAgent:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.llm = get_llm()
        with open('src/prompts/notes_modification_prompt.txt', 'r') as f:
            self.notes_prompt_template = f.read()

    def update_notes(self):
        prompt = self.notes_prompt_template
        response = self.llm.predict(prompt)
        # Assume LLM modifies notes.txt in the folder
        # No need to handle errors in this case