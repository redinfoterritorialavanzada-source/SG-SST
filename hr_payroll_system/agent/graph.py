import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StatefulGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation

# Import the tools
from tools.employee_tools import add_employee, list_employees

# 1. Define the tools for the agent
tools = [add_employee, list_employees]
tool_executor = ToolExecutor(tools)

# 2. Define the model
# Ensure OPENAI_API_KEY is set in your environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # This will be handled more gracefully in the UI, but as a safeguard:
    print("WARNING: OPENAI_API_KEY environment variable not set. Agent will not work.")
    model = None
else:
    model = ChatOpenAI(temperature=0, streaming=True, api_key=api_key)
    model = model.bind_tools(tools)

# 3. Define the State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]

# 4. Define the Nodes
def call_model(state):
    """Calls the LLM with the current state."""
    if not model:
        return {"messages": [HumanMessage(content="Error: API Key no configurada.")]}
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

def call_tool(state):
    """Executes a tool call and returns the result."""
    last_message = state['messages'][-1]
    action = ToolInvocation(
        tool=last_message.tool_calls[0]["name"],
        tool_input=last_message.tool_calls[0]["args"],
    )
    response = tool_executor.invoke(action)
    tool_message = ToolMessage(content=str(response), tool_call_id=last_message.tool_calls[0]['id'])
    return {"messages": [tool_message]}

# 5. Define the Graph Logic (Conditional Edges)
def should_continue(state):
    """Determines whether to continue the loop or end."""
    last_message = state['messages'][-1]
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "end"
    return "continue"

# 6. Build the Graph
workflow = StatefulGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)
workflow.add_edge("action", "agent")

# 7. Compile the graph
app = workflow.compile()

# 8. Wrapper class for easy use
class HRAgent:
    def __init__(self):
        self.graph = app

    def invoke(self, query: str):
        if not model:
            yield {"messages": [HumanMessage(content="Error: OPENAI_API_KEY no está configurada. No puedo procesar tu solicitud.")]}
            return

        inputs = {"messages": [HumanMessage(content=query)]}
        # Using stream to get intermediate steps
        yield from self.graph.stream(inputs, stream_mode="values")
