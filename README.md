# PlanAndReEval

A Python implementation of the Plan-and-Execute AI agent pattern using LangGraph. This system breaks down complex tasks into manageable steps, executes them sequentially, and adapts the plan based on intermediate results.

## Overview

PlanAndReEval implements an intelligent agent that can:
- **Plan**: Generate step-by-step plans for complex queries
- **Execute**: Run individual plan steps using available tools
- **Re-evaluate**: Adapt and replan based on execution results
- **Respond**: Provide final answers when tasks are complete

The system uses LangGraph for workflow orchestration and supports async execution with tool integration.

## Architecture

The system consists of several key components:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Planner   │───▶│   Agent     │───▶│  Replanner  │
│             │    │  Executor   │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────┐
│                Workflow State                       │
│  • Input Query                                      │
│  • Current Plan                                     │
│  • Past Steps                                       │
│  • Response                                         │
└─────────────────────────────────────────────────────┘
```

### Core Components

- **Agent** (`agent.py`): Handles planning, replanning, and tool execution
- **Graph** (`graph.py`): Defines the LangGraph workflow with conditional edges
- **Nodes** (`nodes.py`): Implements the execution logic for each workflow step
- **State** (`state.py`): Manages the shared state across workflow steps
- **Tools** (`tools.py`): Available tools for the agent (currently DuckDuckGo search)

## Installation

### Prerequisites

- Python 3.8+
- Required API keys (see Configuration section)

### Dependencies

Install the required packages using the requirements file:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install langchain langchain-community langchain-core langgraph pydantic python-dotenv pillow typing-extensions
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with your API configuration:

```env
# Required for the language model
GROQ_API_KEY=your_groq_api_key_here

# Optional: Other provider API keys if you change the model
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Model Configuration

The system is currently configured to use the Groq provider with the `qwen-qwq-32b` model. You can modify this in `agent.py`:

```python
self.model = init_chat_model(
    model="qwen-qwq-32b",  # Change model here
    model_provider="groq",  # Change provider here
)
```

## Usage

### Basic Example

```python
from dotenv import load_dotenv
from plan_and_execute.graph import Graph
import asyncio

# Load environment variables
load_dotenv()

# Create and configure the workflow
graph = Graph()
workflow = graph.get_workflow()

# Configure execution parameters
config = {"recursion_limit": 10}
inputs = {"input": "What is the capital of France and its population?"}

# Run the workflow
async def main():
    async for event in workflow.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(v)

asyncio.run(main())
```

**Expected Output:**
```
{'plan': ['Search for the capital of France', 'Search for the population of the capital city', 'Compile the final answer']}
{'past_steps': [('Search for the capital of France', 'The capital of France is Paris.')]}
{'plan': ['Search for the population of Paris', 'Compile the final answer']}
{'past_steps': [('Search for the population of Paris', 'Paris has a population of approximately 2.16 million people.')]}
{'response': 'The capital of France is Paris, and it has a population of approximately 2.16 million people.'}
```

### Advanced Usage

#### Generating Workflow Diagrams

You can visualize the workflow structure:

```python
from plan_and_execute.graph import Graph

graph = Graph()
graph.get_node_diagram("workflow_diagram.png")
```

#### Custom Tool Integration

Extend the tools available to the agent by modifying `tools.py`:

```python
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun

class Tools:
    def __init__(self):
        self.search = DuckDuckGoSearchRun()
        self.wikipedia = WikipediaQueryRun()

    def get_all(self):
        return [
            self.search,
            self.wikipedia
        ]
```

#### State Management

The workflow state includes:

```python
class PlanExecute(TypedDict):
    input: str                    # Original user query
    plan: List[str]              # Current execution plan
    past_steps: List[Tuple]      # Completed steps and results
    response: str                # Final response (when complete)
```

## API Reference

### Graph Class

```python
class Graph:
    def __init__(self):
        """Initialize the workflow graph with nodes and edges."""
    
    def get_workflow(self):
        """Returns the compiled LangGraph workflow."""
        
    def get_node_diagram(self, output_path: str):
        """Generate a visual diagram of the workflow."""
```

### Agent Class

```python
class Agent:
    def __init__(self):
        """Initialize agent with model and tools."""
    
    def run(self, query: str):
        """Execute a single query without planning."""
        
    def run_plan(self):
        """Get the planning chain."""
        
    def run_replan(self):
        """Get the replanning chain."""
        
    def get_agent(self):
        """Get the configured agent executor."""
```

### Nodes Class

```python
class Nodes:
    async def plan_step(self, state: PlanExecute):
        """Generate initial plan for the query."""
        
    async def execute_step(self, state: PlanExecute):
        """Execute the next step in the plan."""
        
    async def replan_step(self, state: PlanExecute):
        """Replan based on execution results."""
        
    def should_end(self, state: PlanExecute):
        """Determine if workflow should continue or end."""
```

## Examples

### Research Query

```python
inputs = {"input": "Research the latest developments in artificial intelligence and summarize the key trends"}
```

### Complex Analysis

```python
inputs = {"input": "Compare the economic growth of Japan and South Korea over the last decade"}
```

### Factual Lookup

```python
inputs = {"input": "Where does Asia's Richest Woman Live?"}
```

## Workflow Process

1. **Planning Phase**: The system analyzes the input and creates a step-by-step plan
2. **Execution Phase**: Each step is executed using available tools
3. **Re-evaluation Phase**: Results are analyzed and the plan is updated if needed
4. **Response Phase**: Final answer is provided when the task is complete

## Error Handling

The system includes built-in error handling and recovery:
- Failed steps trigger replanning
- Recursion limits prevent infinite loops
- Graceful degradation when tools are unavailable

## Performance Considerations

- **Recursion Limit**: Set appropriate limits to prevent infinite planning loops
- **Tool Selection**: Choose efficient tools for your use case
- **Model Selection**: Balance capability with cost and speed
- **Async Execution**: Leverages async patterns for better performance

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/Aryan-401/PlanAndReEval.git
cd PlanAndReEval

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # Create this file with dependencies

# Set up environment variables
cp .env.example .env  # Create this file with required variables
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for workflow orchestration
- Uses [LangChain](https://github.com/langchain-ai/langchain) for AI/ML integrations
- Powered by various language model providers (Groq, OpenAI, Anthropic)

## Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review example usage in `try.py`

---

**Note**: This implementation follows the Plan-and-Execute pattern commonly used in AI agent architectures for breaking down complex tasks into manageable, sequential steps.