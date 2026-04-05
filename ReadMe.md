# Patient API

A REST API for managing patient records built with FastAPI.

## Live URL
https://fastapi-production-1509.up.railway.app/docs

## Endpoints
- GET /patients — filter by city and status
- GET /info/{patient_id} — get patient by ID
- POST /patients — create new patient
- PUT /patients/{patient_id} — update patient
- DELETE /patients/{patient_id} — delete patient

## Tech Stack
FastAPI · Pydantic · Docker · Railway