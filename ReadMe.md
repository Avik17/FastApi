# AI Engineering Projects

Two live production projects built during AI Engineering learning journey.

## Project 1 — AI Engineering Assistant Chatbot
**Live:** https://huggingface.co/spaces/avik1706/ai-engineering-assistant

An AI chatbot that answers questions about AI Engineering — LLMs, RAG, FastAPI, agents, deployment.

**Features:**
- Multi-turn conversation with sliding window memory
- Claude Haiku integration via Anthropic API
- Gradio UI deployed on HuggingFace Spaces

**Stack:** Python · Anthropic Claude · Gradio · HuggingFace Spaces

---

## Project 0 — Patient CRUD API
**Live:** https://fastapi-production-1509.up.railway.app/docs

A production REST API for managing patient records.

**Features:**
- Full CRUD: GET, POST, PUT, DELETE
- Pydantic validation on all inputs and outputs
- HTTPException error handling
- Dockerized and deployed on Railway

**Stack:** FastAPI · Pydantic · Docker · Railway

---

## Setup
```bash
pip install -r requirements.txt

# Add to .env
ANTHROPIC_API_KEY=your-key-here

# Run chatbot
python app.py

# Run patient API
uvicorn main:app --reload
```

## Tech Stack
FastAPI · Pydantic · Anthropic Claude · Gradio · Docker · Railway · HuggingFace Spaces