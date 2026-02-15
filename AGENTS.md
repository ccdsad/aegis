# Aegis

## Project Description

Aegis is a real-life trading automation platform for:

- Receiving trading signals
- Risk calculation
- Trade simulation
- Execution (paper/real)
- Monitoring and alerts

## High-Level Architecture

```text
                    ┌────────────┐
market data ───────▶│ ingest svc │
                    └─────┬──────┘
                          │
signals ─────▶ FastAPI API│
                          ▼
                ┌─────────────────┐
                │ decision engine │
                └─────┬───────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   risk engine   execution svc   simulator
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                storage / metrics
```

## Local Development

- Install deps: `uv sync`
- Run API (dev): `uv run fastapi dev app/main.py`
- Run tests: `uv run pytest`
- Run lint + type checks + format check: `./scripts/lints.sh`

## Engineering Principles

- Keep domain logic in services/engines, not in API handlers.
- Treat risk checks as mandatory gates before execution.
- Support deterministic simulation paths for strategy validation.
- Keep paper and real execution paths explicit and auditable.
- Emit metrics and alerts for every critical state transition.

## Frequently Used Skills (Recommended)

You can list preferred skills in this file to help contributors work faster. For this project, commonly useful skills are:

- `fastapi-helper` for API/service architecture and patterns
- `python-patterns` for Python code quality and typing
- `python-testing` for pytest structure and coverage improvements
- `python-observability` for logging/metrics/tracing patterns
- `docker-expert` for containerization and runtime hardening

These are recommendations only; they do not replace explicit task requirements.
