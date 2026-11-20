# Google ADK – AI Agent Development

A hands-on repository dedicated to learning and building AI agents using **Google Agent Development Kit (ADK)** and Python.

This repository contains practical implementations of different agent architectures and workflows, starting from basic tool-using agents to advanced multi-agent workflows.

## 🚀 What I'm Learning

- Google Agent Development Kit (ADK)
- LLM Agents and Agent Architecture
- Tool Integration and Function Calling
- Human-in-the-Loop (HITL) Workflows
- Sequential and Multi-Agent Workflows
- Parallel Workflow Agents
- Loop Workflow Agents
- Agent Communication and Orchestration
- Practical AI Agent Development using Python
- Model Context Protocol(MCP)

## 📂 Project Structure

```text
Google-Adk/
│
├── .adk/
│
├── human_in_the_loop_workflow/
│   └── Human approval and interaction workflows
│
├── loop_workflow_agent/
│   └── Loop-based agent execution
│
├── parallel_workflow_agent/
│   └── Parallel agent execution
│
├── tool_agent/
│   └── Tool integration with LLM agents
│
├── requirements.txt
└── README.md
```

## 🧠 Implementations

### 1. Tool Agent

An AI agent that uses external tools to perform specific tasks based on user instructions.

### 2. Human-in-the-Loop Workflow

A workflow where human approval or feedback is required before an agent proceeds with specific actions.

### 3. Parallel Workflow Agent

Executes multiple independent agents or tasks simultaneously to improve workflow efficiency.

### 4. Loop Workflow Agent

Uses iterative execution to repeat tasks until a defined condition or stopping criterion is reached.

## 🛠️ Tech Stack

- Python
- Google Agent Development Kit (ADK)
- Gemini Models
- LLM-based Agents
- Function Calling
- Multi-Agent Workflows

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/vedchaudhary2005/Google-Adk.git

cd Google-Adk
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and add your Gemini API key:

```env
GOOGLE_API_KEY=your_google_api_key
```

### 5. Run an Agent

For example, to run the tool agent:

```bash
adk run tool_agent
```

To launch the ADK web interface:

```bash
adk web
```

Run commands from the project directory containing your agent folders.

## 🎯 Repository Goal

The goal of this repository is to understand how AI agents work internally and gain practical experience building agent-based applications using Google's ADK framework.

This repository will continue to evolve as I explore more advanced concepts and implement new AI agent workflows.

---

**Author:** [Ved Chaudhary](https://github.com/vedchaudhary2005)

**GitHub:** [Google-Adk](https://github.com/vedchaudhary2005/Google-Adk)
