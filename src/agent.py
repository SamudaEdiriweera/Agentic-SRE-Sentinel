""" 
Defines the State Graph and decision logic
"""

from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages # <-- Add this!
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from src.tools import check_container_logs, check_container_status, restart_container
from dotenv import load_dotenv
from src.config import MODEL_NAME
import os
load_dotenv()

class AgentState(TypedDict):
    # This tells LangGraph: "When you get a new message, ADD it to the list, don't replace the list."
    messages: Annotated[List[BaseMessage], add_messages] 
    status: str
    
# 2. Setup the LLM and bind tools
llm = ChatOpenAI(model=MODEL_NAME,
                 api_key=os.getenv("OPENAI_API_KEY"))
tools = [check_container_logs, check_container_status, restart_container]
llm_with_tools = llm.bind_tools(tools)

# 3. Define the Node: The Reasoner
def reasoner(state: AgentState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 4. Define the Node: The Tool Executor
# In LangGraph, we typically use a pre-buit ToolNode, but let's keep it custom for learning
from langgraph.prebuilt import ToolNode
tool_node = ToolNode(tools)

# 5. Define Conditional Logic (Should I stop or use a tool?)
def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 6. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", reasoner)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", END: END}
)

workflow.add_edge("tools", "agent") # Loop back to agent after using tool

app = workflow.compile()