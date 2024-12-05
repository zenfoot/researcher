"""
Entry Point Module for Researcher System
========================================

This module serves as the main entry point for the Researcher application. It initializes and 
runs the orchestration agent that coordinates the system's workflows.

Module Structure:
----------------
- Imports the AdaptiveOrchestrationAgent from the agents package
- Defines a main() function as the entry point
- Includes standard Python idiom for script execution

Functions:
---------
main()
    Initializes and runs the orchestration workflow.
    
    Returns:
        None
    
    Side Effects:
        - Creates an instance of AdaptiveOrchestrationAgent
        - Executes the main workflow through the orchestrator, initiating various processes
        - May raise exceptions if the workflow encounters errors (consider implementing error handling)

Usage:
-----
The script can be run directly:
    $ python main.py

Or imported and used in other modules:
    from main import main
    main()

Expected Output:
---------------
Upon successful execution, the user can expect to see output indicating the progress of the 
workflow, including steps completed and any results generated.

Dependencies:
------------
- agents.adaptive_orchestration_agent.AdaptiveOrchestrationAgent
"""

import logging
import os
from agents.adaptive_orchestration_agent import AdaptiveOrchestrationAgent

# Configure logging level from environment variable or default to INFO
logging_level = os.getenv('LOGGING_LEVEL', 'INFO').upper()
logging.basicConfig(level=logging_level)

def main() -> None:
    """
    Initialize and run the Researcher system's main workflow.
    
    Creates an instance of the AdaptiveOrchestrationAgent and executes
    its primary workflow sequence.
    
    Args:
        None
        
    Returns:
        None
        
    Side Effects:
        Initiates the orchestration agent and its associated processes
    """
    orchestrator = AdaptiveOrchestrationAgent()
    try:
        logging.info("Starting the orchestration agent.")
        orchestrator.run()
        logging.info("Orchestration agent finished successfully.")
    except ValueError as ve:
        logging.error(f"Value error occurred: {ve}")
    except IOError as ioe:
        logging.error(f"I/O error occurred: {ioe}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()