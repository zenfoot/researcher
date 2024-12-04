import unittest
from agents.idea_generation_agent import IdeaGenerationAgent

class TestIdeaGenerationAgent(unittest.TestCase):
    def test_generate_ideas(self):
        agent = IdeaGenerationAgent(domain="Physics", num_ideas=3)
        ideas = agent.generate_ideas()
        self.assertEqual(len(ideas), 3)

if __name__ == '__main__':
    unittest.main()