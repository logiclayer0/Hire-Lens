# Contributing to HireLens

Thanks for your interest. This project was built for AI Agent Hackathon 2026.

## Setup

1. Fork and clone.
2. Run `scripts/setup.ps1` (Windows) or `scripts/setup.sh` (macOS/Linux).
3. Add `GROQ_API_KEY` to `backend/.env`.
4. Start backend and frontend via `scripts/run_all.ps1` or `scripts/run_all.sh`.

## Branching

- `main` — stable
- `feat/<name>` — new features
- `fix/<name>` — bug fixes

## Commit Style

Follow Conventional Commits:

- `feat: add candidate export`
- `fix: handle empty resume`
- `docs: update api reference`

## Pull Requests

- Keep PRs focused.
- Include screenshots for UI changes.
- Ensure `npm run build` and `pytest` pass locally.

## Code Style

- Backend: Python 3.11, type hints, Pydantic models.
- Frontend: TypeScript strict, functional components, Tailwind only.

## Reporting Issues

Open an issue with reproduction steps, expected vs actual behavior.