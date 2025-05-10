from langgraph.graph import StateGraph, START, END
from plan_and_execute.state import PlanExecute
from plan_and_execute.nodes import Nodes
class Graph:
    def __init__(self):
        self.nodes = Nodes()

        workflow = StateGraph(PlanExecute)

        # Add the plan node
        workflow.add_node("planner", self.nodes.plan_step)
        workflow.add_node("agent", self.nodes.execute_step)
        workflow.add_node("replan", self.nodes.replan_step)
        workflow.add_edge(START, "planner")
        workflow.add_edge("planner", "agent")
        workflow.add_edge("agent", "replan")

        workflow.add_conditional_edges(
            "replan",
            # Next, we pass in the function that will determine which node is called next.
            self.nodes.should_end,
            ["agent", END],
        )
        self.app = workflow.compile()


    def get_workflow(self):
        return self.app


    def get_node_diagram(self, output_path: str):
        from PIL import Image
        import io
        try:
            image = Image.open(io.BytesIO(self.app.get_graph(xray=True).draw_mermaid_png()))
            image.save(output_path, format="PNG")
            print(f"Image saved successfully to {output_path}")
        except Exception as e:
            print(f"Error: {e}")