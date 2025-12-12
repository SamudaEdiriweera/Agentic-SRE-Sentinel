# 🛡️ Agentic SRE Sentinel

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)
![Docker](https://img.shields.io/badge/Infrastructure-Docker-2496ED)
![OpenAI](https://img.shields.io/badge/AI-GPT--4o-green)

> **An autonomous DevOps engineer that monitors infrastructure, performs Root Cause Analysis (RCA), and self-heals services without human intervention.**

---

## 📖 Overview

**Agentic SRE Sentinel** is a Multi-Agent System (MAS) designed to automate Level 1 (L1) Site Reliability Engineering tasks. 

In traditional DevOps, when a service crashes, an engineer must:
1.  Receive an alert.
2.  SSH into the server.
3.  Read logs to diagnose the issue.
4.  Execute a fix (e.g., restart).

This project replaces that manual workflow with an **Agentic Workflow** using **LangGraph**. The system autonomously detects container failures, inspects Docker logs to understand *why* the failure happened, and executes the appropriate Docker commands to restore service health.

---

## 📸 Demo

*(Place a screenshot here named `demo_screenshot.png` showing the interface)*
[Screencast from 2025-12-12 10-09-16.webm](https://github.com/user-attachments/assets/54cb728d-2906-46e6-859d-c20915d42c16)


---

## 🏗️ Architecture

The system follows a **Graph-based State Machine** approach rather than a simple linear chain. This allows the agent to loop, retry, or ask for more information before acting.

```mermaid
graph TD
    Start[⚠️ Monitoring Loop Detects Failure] --> Agent
    
    subgraph "LangGraph Agent Workflow"
        Agent{Agent Brain}
        Agent -->|Decide Tool| Tools[Tool Executor Node]
        Tools -->|Docker API| Logs[Check Logs]
        Tools -->|Docker API| Status[Check Status]
        Tools -->|Docker API| Restart[Restart Container]
        Tools -->|Tool Output| Agent
    end
    
    Agent -->|Issue Resolved| End[✅ System Restored]
