# Coder Agent

An AI-powered autonomous code generation system that takes natural language prompts and generates complete, structured projects with multiple files and proper dependencies.

## Overview

Coder Agent uses a multi-agent architecture powered by LangGraph and Google's Gemini 2.5 Flash to:
1. **Plan** - Convert user requirements into a structured project plan
2. **Architect** - Break down the plan into sequential implementation tasks
3. **Code** - Execute each task using a ReAct agent with file system tools

## Features

- 🤖 **Autonomous Code Generation** - Describe what you want, get a complete project
- 📁 **Project Management** - Organized project structure in `generated_projects/`
- 🔄 **Multi-Agent Pipeline** - Planner → Architect → Coder workflow
- 🛠️ **Tool-Using Agent** - Coder agent uses tools to read, write, and navigate files
- 🔗 **Dependency Resolution** - Automatically orders tasks to handle dependencies
- 📊 **Structured Output** - Uses Pydantic models for type-safe agent outputs

## Architecture

```
User Prompt → Planner Agent → Architect Agent → Coder Agent (loops) → Complete Project
                    ↓               ↓                  ↓
                  Plan         Task Plan        File Implementation
```

### Agents

1. **Planner Agent** (`planner_agent`)
   - Generates project name
   - Creates project plan with tech stack, features, and file structure
   - Initializes project directory

2. **Architect Agent** (`architect_agent`)
   - Converts plan into sequential implementation tasks
   - Ensures proper task ordering for dependency resolution
   - Provides detailed task descriptions with context

3. **Coder Agent** (`coder_agent`)
   - ReAct agent with file system tools
   - Implements each task sequentially
   - Maintains consistency across files
   - Loops until all tasks are completed

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Prerequisites

- Python 3.13+
- uv package manager
- Google API Key (for Gemini)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd coder
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

### Interactive Mode

Run the agent interactively:

```bash
python main.py
```

You'll be prompted to enter your project description:
```
Enter your project prompt: Build a colorful modern todo app in HTML, CSS and JS
```

### Example Prompts

- "Build a colorful modern todo app in HTML, CSS and JS"
- "Create a Python Flask REST API with SQLite database for a blog"
- "Make a React dashboard with charts for sales data"
- "Build a CLI tool in Python for file encryption"

## Project Structure

```
coder/
├── agent/
│   ├── graph.py          # LangGraph workflow definition
│   ├── prompts.py        # Agent system prompts
│   ├── states.py         # Pydantic state models
│   └── tools.py          # File system tools and project management
├── generated_projects/   # Output directory for generated projects
├── main.py              # CLI entry point
├── pyproject.toml       # uv project configuration
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Generated Projects

All generated projects are saved in the `generated_projects/` directory with sanitized names based on your prompt and a unique hash:

```
generated_projects/
├── build_a_colorful_abc123/
├── create_a_python_def456/
└── make_a_react_789012/
```

## Development

### Running with Debug Output

The agent includes verbose logging by default. You'll see:
- 📁 Project initialization messages
- 📋 Task plan summaries
- 🔨 Current task being worked on
- ✅ Completion status

### Modifying Agents

Each agent can be customized by editing:
- **Prompts**: `agent/prompts.py`
- **State Models**: `agent/states.py`
- **Tools**: `agent/tools.py`
- **Graph Flow**: `agent/graph.py`

### Adding New Tools

Add tools to the coder agent in `agent/tools.py` using the `@tool` decorator:

```python
@tool
def your_custom_tool(param: str) -> str:
    """Tool description for the LLM."""
    # Implementation
    return result
```

## Configuration

### LLM Model

Change the model in `agent/graph.py`:

```python
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
```

Supported models:
- `gemini-2.5-flash` (default, fast)
- `gemini-2.5-pro` (more capable)


## Troubleshooting

### "No project initialized" Error
Make sure the planner agent runs first in the workflow.

### File Write Errors
The agent can only write within the project root for security. All paths are validated.

### API Rate Limits
If you hit rate limits, consider:
- Using a different model
- Adding delays between requests
- Increasing recursion limit to allow more retries

## Dependencies

Key dependencies (managed by uv):
- `langgraph` - Agent workflow orchestration
- `langchain-google-genai` - Google Gemini integration
- `pydantic` - Data validation and settings
- `python-dotenv` - Environment variable management

See `pyproject.toml` for the complete list.


## Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) by LangChain
- [Google Gemini](https://ai.google.dev/) for LLM capabilities
- [uv](https://github.com/astral-sh/uv) for Python package management