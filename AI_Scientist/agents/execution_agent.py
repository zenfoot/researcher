class ExperimentExecutionAgent:
    def __init__(self, data_analysis_agent):
        self.data_analysis_agent = data_analysis_agent

    async def execute_experiment(self, experiment_plan_text):
        print("Executing experiments...")
        # Simulate experiment execution
        execution_results = f"Execution results for experiment plan:\n{experiment_plan_text}"
        print("Execution completed.")
        await self.data_analysis_agent.analyze_data(execution_results)
