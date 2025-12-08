""" 
The Main Entry Point (Streamlit UI)
"""

import streamlit as st
import docker
import time
import sys
import os

from src.agent import app as agent_app
from src.config import CONTAINER_NAME
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Auto-Ops Sentinel", layout="wide")
st.title("🤖 Auto-Ops Sentinel: Self-Healing Infrastructure")


# Ensure we can find the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
client = docker.from_env()

# --- Sidebar Controls ---
st.sidebar.header("Simulation Controls")

if st.sidebar.button("🟢 Start/Reset Environment"):
    import subprocess
    subprocess.run(["python", "setup_victim.py"])
    st.sidebar.success("Environment Reset!")

if st.sidebar.button("🔴 SABOTAGE: Stop Container"):
    try:
        c = client.containers.get(CONTAINER_NAME)
        c.stop()
        st.sidebar.error("Container Stopped! Alert Triggered!")
    except:
        st.sidebar.write("Container not found.")

# --- Main Dashboard ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Live System Status")
    status_placeholder = st.empty()

with col2:
    st.subheader("Agent Thought Process")
    chat_container = st.container()

# --- Continuous Monitoring Loop ---
if "messages" not in st.session_state:
    st.session_state.messages = []

def run_agent_check(error_msg):
    # Add the alert to history
    st.session_state.messages.append(HumanMessage(content=f"ALERT: System check failed. Error: {error_msg}. Fix it."))
    
    # Run LangGraph
    inputs = {"messages": st.session_state.messages}
    
    # 👇 UPDATED LOOP STARTS HERE
    for output in agent_app.stream(inputs):
        for key, value in output.items():
            # Get all new messages (could be 1, could be 5)
            new_messages = value["messages"]
            
            for msg in new_messages:
                # Append EVERY message to session state
                st.session_state.messages.append(msg)
                
                # Visualize based on who sent it
                if key == "agent":
                    with chat_container:
                        st.info(f"🧠 **Agent Thinking:** {msg.content}")
                elif key == "tools":
                    with chat_container:
                        st.success(f"🛠️ **Tool Output:** {msg.name} -> {msg.content[:100]}...") # Truncate long logs for UI
    # 👆 UPDATED LOOP ENDS HERE

# Simple polling loop simulating a monitoring tool
while True:
    try:
        c = client.containers.get(CONTAINER_NAME)
        status = c.status
        if status != "running":
            status_placeholder.error(f"⚠️ Status: {status}")
            # If not running, trigger the agent!
            run_agent_check(f"Container {CONTAINER_NAME} is in state: {status}")
            time.sleep(5) # Wait for fix
        else:
            status_placeholder.success(f"✅ Status: {status}")
    except Exception as e:
        status_placeholder.error("⚠️ Connection Lost")
        run_agent_check("Container appears to be missing or docker is down.")
    
    time.sleep(2)