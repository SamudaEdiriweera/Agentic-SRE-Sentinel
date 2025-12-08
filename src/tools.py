""" 
Defines the specific capabilities og the agent
"""
import docker
from langchain_core.tools import tool
from src.config import CONTAINER_NAME

client = docker.from_env()

@tool
def check_container_logs():
    """ Fetches the last 50 lines of logs from the victim container to diagnose issues."""
    try:
        container = client.containers.get(CONTAINER_NAME)
        return container.logs(tail=50).decode("utf-8")
    except Exception as e:
        return f"Error fetching logs: {str(e)}"
    
@tool
def check_container_status():
    """ Chgecks if the container is running, paused, or exited"""
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.reload()
        return f"Status: {container.status}"
    except Exception as e:
        return f"Error checking status: {str(e)}"
    
@tool
def restart_container():
    """ Restarts the container. use this if the service is down or unresponsive"""
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.restart()
        return "Successfully restarted the container"
    except Exception as e:
        return f"Failed to restart: {str(e)}"