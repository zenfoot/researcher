IDEA_PROMPT = """
Your goal is to generate a novel research idea based on the user input.
User Input: {user_input}
Here are the ideas that have already been generated: {prev_ideas}
Respond in JSON format: [Name, Title, Experiment, Interestingness, Feasibility, Novelty]
"""

NOVELTY_PROMPT = """
Check if this idea is novel compared to existing literature:
Idea Description: {idea_description}
Respond with 'Decision made: novel.' or 'Decision made: not novel.'
"""

EXPERIMENT_DESIGN_PROMPT = """
Your goal is to design experiments for the idea '{idea_title}'.
Experiment Description: {idea_experiment}
Baseline Results: {baseline_results}
You can run up to {max_runs} experiments. Provide a detailed experiment plan in JSON format.
"""

DATA_ANALYSIS_PROMPT = """
Analyze the following experimental results:
{results}
Summarize key findings, provide insights, and interpret the data.
"""

REPORT_COMPILATION_PROMPT = """
Write a research paper based on the following analysis:
{analysis}
Use the standard research paper structure and provide the output in LaTeX format.
"""

PEER_REVIEW_PROMPT = """
You are reviewing the following research paper:
{report}
Provide constructive feedback including strengths, weaknesses, and suggestions.
"""

IMPROVEMENT_PROMPT = """
Improve the following research paper based on this review:
Review: {review}
Original Paper: {report}
Provide the revised version in LaTeX format.
"""
