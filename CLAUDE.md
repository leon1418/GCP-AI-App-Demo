# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GCP AI Dog Breed Detector — users upload dog photos, Gemini AI identifies breeds, results are displayed with query history. Showcases GCP services: GKE, GCS, Firestore, Gemini.

## Architecture

- **Backend**: Python + FastAPI (app/main.py)
- **Frontend**: Static HTML/CSS/JS served by FastAPI (app/static/)
- **AI**: Gemini 2.0 Flash via google-genai (GCS URI method)
- **Storage**: GCS for images, Firestore for query history
- **Infra**: Terraform (terraform/), Docker + K8s (kubernetes/)

## Development Environment

- Python package manager: `uv`
- Run locally: `uv run uvicorn app.main:app --reload`
- Requires `.env` file (see `.env.example`)

## Key Commands

- `uv sync` — install dependencies
- `uv run uvicorn app.main:app --reload` — local dev server
- `docker build -t dog-detector .` — build container
- `cd terraform && terraform plan` — preview infra changes

## Project Structure

- `app/main.py` — FastAPI routes, session middleware
- `app/config.py` — pydantic-settings configuration
- `app/models.py` — Pydantic request/response models
- `app/services/` — GCS, Gemini, Firestore service modules
- `app/static/` — Frontend (index.html, style.css, app.js)
- `terraform/` — GKE, GCS, Firestore, IAM infrastructure
- `kubernetes/` — Deployment, Service, ConfigMap manifests
