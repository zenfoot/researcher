"""
Handles citations and bibliographic references in reports.

The agent manages the inclusion of relevant literature references,
ensuring proper citation formats.
"""


from models.llm_provider import get_llm
from prompts import load_prompt
from utils.api_clients import SemanticScholarAPI
import json

class CitationManagementAgent:
    def __init__(self, draft_path):
        self.llm = get_llm()
        self.draft_path = draft_path
        self.citation_system_message = load_prompt('citation_system_message.txt')
        self.citation_first_prompt = load_prompt('citation_first_prompt.txt')
        self.citation_second_prompt = load_prompt('citation_second_prompt.txt')
        self.aider_prompt_format = load_prompt('aider_prompt_format.txt')
        self.api_client = SemanticScholarAPI()

    def integrate_citations(self, total_rounds=20):
        msg_history = []
        for current_round in range(1, total_rounds + 1):
            with open(self.draft_path, 'r') as f:
                draft = f.read()
            # First prompt
            first_prompt = self.citation_first_prompt.format(
                draft=draft,
                current_round=current_round,
                total_rounds=total_rounds
            )
            response = self.llm.predict(
                first_prompt,
                system_message=self.citation_system_message.format(total_rounds=total_rounds),
                chat_history=msg_history
            )
            msg_history.append({'role': 'assistant', 'content': response})
            if 'No more citations needed' in response:
                break
            # Parse response
            json_output = self.extract_json(response)
            if not json_output:
                continue
            query = json_output.get('Query')
            if not query:
                continue
            # Search for papers
            papers = self.api_client.search_papers(query)
            papers_str = self.format_papers(papers)
            # Second prompt
            second_prompt = self.citation_second_prompt.format(
                papers=papers_str,
                current_round=current_round,
                total_rounds=total_rounds
            )
            response = self.llm.predict(
                second_prompt,
                system_message=self.citation_system_message.format(total_rounds=total_rounds),
                chat_history=msg_history
            )
            msg_history.append({'role': 'assistant', 'content': response})
            if 'Do not add any' in response:
                continue
            # Parse response
            json_output = self.extract_json(response)
            if not json_output:
                continue
            selected_indices = json.loads(json_output.get('Selected', '[]'))
            description = json_output.get('Description')
            if not selected_indices or not description:
                continue
            # Add citations to draft
            self.add_citations_to_draft(papers, selected_indices, description)

    def extract_json(self, text):
        # Implement logic to extract JSON from the response
        try:
            json_str = text.split('```json')[1].split('```')[0]
            return json.loads(json_str)
        except (IndexError, json.JSONDecodeError):
            return None

    def format_papers(self, papers):
        # Format papers into a string for the prompt
        paper_strings = []
        for i, paper in enumerate(papers):
            paper_strings.append(
                f"""{i}: {paper['title']}. {', '.join(author['name'] for author in paper['authors'])}. {paper.get('venue', 'Unknown Venue')}, {paper.get('year', 'n.d.')}.
Abstract: {paper.get('abstract', 'No abstract available.')}"""
            )
        return "\n\n".join(paper_strings)

    def add_citations_to_draft(self, papers, selected_indices, description):
        # Extract bibtex entries
        bib_entries = []
        for idx in selected_indices:
            bib_entry = papers[idx].get('bibtex')
            if bib_entry:
                bib_entries.append(bib_entry)
        # Update references.bib and LaTeX draft
        pass  # Implement file I/O to add bib entries and update the draft