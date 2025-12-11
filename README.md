# ai-agents-assignment
AI Engineering Intern — Case Study.
# AI Engineering Internship — Case Study

This repository contains my solution for the AI Engineering Internship assignment.

It includes:
- A minimal workflow engine built using FastAPI
- Nodes, edges, branching, loops
- In-memory graph execution
- A sample workflow: Code Review Mini-Agent

## How to run
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

## Endpoints
POST /graph/create  
POST /graph/run  
GET /graph/state/{run_id}

The sample graph is available at:
POST /graph/create/sample/code_review
