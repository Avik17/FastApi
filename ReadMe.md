# AI Chat API

A production-ready AI chat API built with FastAPI and Claude (Anthropic).

## Live URLs
- Patient API: https://fastapi-production-1509.up.railway.app/docs
- Chat API: Run locally on port 8001

## Endpoints

### Patient API
- `GET /patients` — filter patients by city and status
- `GET /info/{patient_id}` — get patient by ID
- `POST /patients` — create new patient
- `PUT /patients/{patient_id}` — update patient fields
- `DELETE /patients/{patient_id}` — delete patient

### Chat API
- `POST /chat` — multi-turn conversation with memory
- `POST /chat/stream` — streaming responses word by word

## Features
- Multi-turn memory with sliding window (last 10 messages)
- Streaming responses via StreamingResponse
- Token usage and cost tracking
- Pydantic validation on all inputs and outputs
- Anthropic Claude Haiku integration

## Tech Stack
FastAPI · Pydantic · Anthropic Claude · Docker · Railway

## Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Add your API key to .env
ANTHROPIC_API_KEY=your-key-here

# Run Patient API
uvicorn main:app --reload

# Run Chat API
uvicorn chat:app --reload --port 8001
```

## Models Used
- `claude-haiku-4-5-20251001` — fast and cheap for learning
- `claude-sonnet-4-6` — balanced for production
- `claude-opus-4-6` — most capable for complex tasks