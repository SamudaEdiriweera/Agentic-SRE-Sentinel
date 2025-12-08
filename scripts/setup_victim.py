""" 
This creates the "problem" (the Nginx container). 
It is separated because in a real production environment, wouldn't deploy the "virus" along with the "cure."
"""
import sys
import os
# Add the parent directory (project root) to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import docker
from src.config import CONTAINER_NAME

client = docker.from_env()

def setup_victim():
    container_name = CONTAINER_NAME
    try:
        # Chaeck if exists and remove
        old = client.containers.get(CONTAINER_NAME)
        old.stop()
        old.remove()
    except Exception as e:
        pass
    
    print(f" Starting {container_name}...")
    container = client.containers.run(
        "nginx:latest",
        name=container_name,
        ports={'80/tcp': 8081},
        detach=True
    )
    print(f"Victim service running at http://localhost:8081")
    
if __name__ == "__main__":
    setup_victim()