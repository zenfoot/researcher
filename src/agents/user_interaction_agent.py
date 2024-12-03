"""
Manages interactions with the user.

This agent handles any required input or communication with the user,
facilitating user-guided decisions within the system.
"""


from langchain.agents import AgentExecutor
from langchain.chains import ConversationChain
from models.llm_provider import get_llm
from memory.memory_manager import ConversationBufferMemory

class UserInteractionAgent:
    def __init__(self):
        self.llm = get_llm()
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.conversation = ConversationChain(
            llm=self.llm, 
            memory=self.memory, 
            verbose=True
        )

    def engage_user(self):
        print("Welcome to the AI Scientist System!")
        while True:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            response = self.conversation.predict(input=user_input)
            print(f"AI: {response}")