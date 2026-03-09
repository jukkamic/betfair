# AI-Driven Refactoring: The Betfair UI Migration
## Testing the Limits of Agentic IDE Integration

**As AI coding assistants evolve from simple autocomplete tools into autonomous agents, the development environment itself must change. The purpose of this project was pedagogical: to create a controlled laboratory to test various AI models (like Z.ai) and agentic extensions (like VS Code Cline/Continue) operating entirely inside an isolated Docker Dev Container.**

The goal was to evaluate how well an AI can act as a migration engine—specifically, navigating the complexities of porting a live UI across language paradigms while adhering to strict environmental boundaries.

### The Architecture & Environment
Rather than fighting dependency hell on a host machine, this project relies on Docker Dev Containers as the fundamental unit of isolation.

The Stack: Python, Flask, HTML, integrating with the live Betfair Exchange API using Non-Interactive (Bot) SSL authentication.

The Agentic Layer: Configured to run with the Continue/Cline extension, pointing to specific LLM endpoints (like glm-4.7 via Z.ai) to drive code generation.

The "Mock" Safety Net: Implemented a --test CLI flag. This allows agents to iteratively build and test logic against mock services without burning through live API limits or requiring complex credentials during development.

### Technical Lessons 
Managing AI inside an IDE requires strict governance, not just a good prompt. The core lessons derived from this setup include:

Prompting the Environment, Not Just the Code: AI agents will natively try to create virtual environments (venv) or suggest Windows commands. The system prompt had to explicitly govern the agent: "The user is working inside a Docker Dev Container on Windows. 1. Do not suggest using a Python virtual environment (venv), as the Docker container handles isolation."

Role-Based Agent Orchestration: By configuring separate system messages for a "Coding Agent" (focused on files and syntax) and a "Planning Agent" (restricted only to architectural blueprints), I prevented the AI from rushing into implementation before the structure was sound.

Security & Complex Authentication: Guiding an AI through the generation of OpenSSL certificates and integrating them into a Python requests workflow proved that agents can handle more than just boilerplate—if directed correctly.

### The Laboratory
This project demonstrates the transition from manual coding to Pragmatic Agentic Orchestration.

It proves to stakeholders that my approach to AI is highly structured. I do not just install a plugin and hope for the best; I architect the exact boundaries, system prompts, and containerized environments the AI needs to succeed safely. It is a live demonstration of managing an AI as a high-speed execution engine while retaining absolute authority over the system.