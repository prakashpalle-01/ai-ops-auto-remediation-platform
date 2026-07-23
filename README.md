# AI Ops & Auto-Remediation Platform

A practical FastAPI service for monitoring AI systems, evaluating alerts, and suggesting remediation actions for common operational issues.

## What it does

- Accepts operational alerts with severity and category
- Stores a lightweight remediation knowledge base
- Produces ranked remediation suggestions
- Exposes a WebSocket stream for alert events
- Ships with smoke tests and packaging metadata

## API

- `GET /health` - service readiness
- `POST /alerts` - ingest an alert
- `GET /alerts/{alert_id}` - inspect an alert
- `POST /remediate` - generate remediation guidance for an alert
- `WS /ws/alerts` - stream alert events

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[test]
uvicorn src.main:app --reload
```
