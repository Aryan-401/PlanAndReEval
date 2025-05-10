from langchain import hub
from langchain.chat_models.base import init_chat_model
from langgraph.prebuilt import create_react_agent
from plan_and_execute.tools import Tools
from plan_and_execute.standard_output import Plan, Act, Response
from langchain_core.prompts import ChatPromptTemplate

class Agent():
    def __init__(self):
        self.model = init_chat_model(
            model="qwen-qwq-32b",
            model_provider="groq",
            )
        self.tools = Tools()
        self.agent = create_react_agent(
                model=self.model,
                prompt="You are a helpful assistant that can answer questions and help with tasks.",
                tools=self.tools.get_all(),
            )
    
    def run(self, query: str):
        return self.agent.invoke({"messages": [("user", query)]})


    def run_plan(self):
        planner_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """For the given objective, come up with a simple step by step plan. \
        This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
        The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.""",
                ),
                ("placeholder", "{messages}"),
            ]
        )
        planner = planner_prompt | self.model.with_structured_output(Plan)
        return planner


    def run_replan(self):
        replanner_prompt = ChatPromptTemplate.from_template(
            """For the given objective, come up with a simple step by step plan. \
        This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
        The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

        Your objective was this:
        {input}

        Your original plan was this:
        {plan}

        You have currently done the follow steps:
        {past_steps}

        Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan."""
        )

        replanner = replanner_prompt | self.model.with_structured_output(Act)
        return replanner

    def get_agent(self):
        return self.agent

