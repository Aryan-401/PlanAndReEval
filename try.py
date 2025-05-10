from dotenv import load_dotenv
from plan_and_execute.graph import Graph
import asyncio

load_dotenv()

graph = Graph()
workflow = graph.get_workflow()

# Uncomment the following lines to generate a diagram of the workflow
# graph.get_node_diagram("workflow_diagram.png")

config = {"recursion_limit": 10}
inputs = {"input": "Where does Asia's Richest Woman Live?"}

async def main():
    async for event in workflow.astream(inputs, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(v)

asyncio.run(main())
