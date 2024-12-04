import asyncio
from agents.user_agent import UserInteractionAgent
from agents.idea_agent import IdeaGenerationAgent
from agents.knowledge_agent import KnowledgeManagementAgent
from agents.novelty_agent import NoveltyEvaluationAgent
from agents.experiment_agent import ExperimentDesignAgent
from agents.execution_agent import ExperimentExecutionAgent
from agents.analysis_agent import DataAnalysisAgent
from agents.reporting_agent import ReportingAgent
from agents.review_agent import PeerReviewAgent
from agents.improvement_agent import ImprovementAgent
from langchain import OpenAI

async def main():
    # Initialize LLM
    llm = OpenAI(model_name="gpt-4")
    
    # Initialize agents
    knowledge_management_agent = KnowledgeManagementAgent()
    improvement_agent = ImprovementAgent(llm)
    peer_review_agent = PeerReviewAgent(llm, improvement_agent)
    reporting_agent = ReportingAgent(llm, peer_review_agent)
    data_analysis_agent = DataAnalysisAgent(llm, reporting_agent)
    experiment_execution_agent = ExperimentExecutionAgent(data_analysis_agent)
    experiment_design_agent = ExperimentDesignAgent(llm, experiment_execution_agent)
    novelty_evaluation_agent = NoveltyEvaluationAgent(llm, experiment_design_agent)
    idea_generation_agent = IdeaGenerationAgent(llm, knowledge_management_agent, novelty_evaluation_agent)
    user_interaction_agent = UserInteractionAgent()
    user_interaction_agent.idea_generation_agent = idea_generation_agent

    # Start the interaction
    await user_interaction_agent.interact_with_user()

if __name__ == "__main__":
    asyncio.run(main())
