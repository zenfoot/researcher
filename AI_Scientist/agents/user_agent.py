class UserInteractionAgent:
    def __init__(self):
        self.idea_generation_agent = None

    async def interact_with_user(self):
        print("Hello! Please provide a brief description of the research area or problem you're interested in.")
        user_input = await self.get_user_input()
        await self.idea_generation_agent.generate_idea(user_input)

    async def get_user_input(self):
        user_input = input("User: ")
        return user_input
