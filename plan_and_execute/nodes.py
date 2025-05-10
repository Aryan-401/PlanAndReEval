from plan_and_execute.state import PlanExecute
from plan_and_execute.agent import Agent
from plan_and_execute.standard_output import Response
from langgraph.graph import END


class Nodes:
    def __init__(self):
        self.agent = Agent()
        self.agent_executor = self.agent.get_agent()
        self.planner = self.agent.run_plan()
        self.replanner = self.agent.run_replan()

    async def execute_step(self, state: PlanExecute):
        plan = state["plan"]
        plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))
        task = plan[0]
        task_formatted = f"""For the following plan:
    {plan_str}\n\nYou are tasked with executing step {1}, {task}."""
        agent_response = await self.agent_executor.ainvoke(
            {"messages": [("user", task_formatted)]}
        )
        return {
            "past_steps": [(task, agent_response["messages"][-1].content)],
        }


    async def plan_step(self, state: PlanExecute):
        plan = await self.planner.ainvoke({"messages": [("user", state["input"])]})
        return {"plan": plan.steps}


    async def replan_step(self, state: PlanExecute):
        output = await self.replanner.ainvoke(state)
        if isinstance(output.action, Response):
            return {"response": output.action.response}
        else:
            return {"plan": output.action.steps}


    def should_end(self, state: PlanExecute):
        if "response" in state and state["response"]:
            return END
        else:
            return "agent"