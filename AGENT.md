# AI Agent Guidelines

This repository is designed to be maintained and evolved with the assistance of AI agents.

## Architecture
- **Pattern**: Clean Architecture.
- **Framework**: FastAPI.
- **Logging**: JSONL format strictly.
- **Configuration**: AWS SSM -> K8s Env -> .env.

## Conventions
- **Language**: Python 3.11+.
- **Docstrings**: Google Style.
- **Typing**: Strict type hints required.
- **Tests**: Pytest with high coverage.

## Task Execution
When asking an agent to modify this codebase:
1. Always check `src/core/config.py` for configuration logic.
2. Ensure new endpoints follow the HATEOAS pattern.
3. Update `docs/` when changing API contracts.
