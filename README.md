# Researcher Project

This project leverages LangChain to...

## Getting Started

This project requires Python 3.12.3.  We recommend setting up a virtual environment before installing dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Installing Dependencies

```pip install -r requirements.txt```

```pip install langchain langchain-anthropic```

### Optional Dependeencies

For serving the application (if applicable)
```pip install "langserve[all]"```

For using the LangChain CLI (if applicable)
```pip install langchain-cli```

## LangSmith Tracing (Optional, but Recommended)

LangSmith provides valuable tracing and debugging capabilities. To enable it:

Set Environment Variables:

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=pr-sparkling-passing-86
```

(For Windows, use `set` instead of `export`.) Consider using a `.env` file to manage these sensitive variables.

(If using a `.env` file): Install python-dotenv and load the variables:

```bash
pip install python-dotenv
```

And in your Python code:

```bash
from dotenv import load_dotenv
load_dotenv()
```

## Usage



## Examples



## Tutorials and Resources

[How to install LangChain packages](https://python.langchain.com/docs/how_to/installation/)

[Build a simple LLM application with chat models and prompt templates](https://python.langchain.com/docs/tutorials/llm_chain/)

## Contriibutting




## License

