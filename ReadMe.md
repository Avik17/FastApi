# AI Engineering Projects

Two live production projects built during AI Engineering learning journey.

## Project 1 — AI Engineering Assistant Chatbot
**Live:** https://huggingface.co/spaces/avik1706/ai-engineering-assistant

An AI chatbot that answers questions about AI Engineering — LLMs, RAG, FastAPI, agents, deployment.

**Features:**
- Multi-turn conversation with sliding window memory
- Claude Haiku integration via Anthropic API
- Gradio UI deployed on HuggingFace Spaces
- FastAPI streaming chat API (`chat.py`)

**Stack:** Python · Anthropic Claude · Gradio · FastAPI · HuggingFace Spaces

**Setup:**
```bash
cd project1-ai-chatbot
pip install -r requirements.txt

# Run Gradio UI
python app.py

# Run FastAPI chat API
uvicorn chat:app --reload
```

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

**Setup:**
```bash
cd project0-patient-api
pip install -r requirements.txt
uvicorn main:app --reload

# Docker
docker build -t patient-api .
docker run -p 8000:8000 patient-api
```

---

## practice/
Learning scripts for Pydantic models, nested models, and LLM API basics.

---

## Repository Structure
```
project0-patient-api/   # Patient CRUD API (FastAPI + Docker + Railway)
project1-ai-chatbot/    # AI chatbot (Gradio + FastAPI + HuggingFace Spaces)
practice/               # Learning scripts (Pydantic, LLM basics)
learning-log/           # Daily learning notes
```

## Add to .env
```
ANTHROPIC_API_KEY=your-key-here
```
