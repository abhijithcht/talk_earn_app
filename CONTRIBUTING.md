# Contributing to Talk & Earn

Thank you for your interest in contributing! Here's how to get started.

---

## Setup

1. Follow the full setup guide in [`docs/setup.md`](docs/setup.md)
2. Make sure all tests pass before making changes:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   pytest tests/ -v
   ```

## Workflow

1. **Create a branch** from `master` with a descriptive name:
   ```
   git checkout -b feat/wallet-history
   ```
2. **Make your changes** — keep commits focused and small.
3. **Run tests** and ensure they pass.
4. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` — new features
   - `fix:` — bug fixes
   - `docs:` — documentation changes
   - `refactor:` — code refactoring
   - `test:` — adding or fixing tests
   - `chore:` — maintenance / config changes

## Project Structure

| Directory      | Purpose                                     |
| -------------- | ------------------------------------------- |
| `app/`         | FastAPI backend (routers, services, models) |
| `www/`         | Web frontend (vanilla JS + HTML)            |
| `flutter_app/` | Flutter mobile WebView wrapper              |
| `tests/`       | Integration tests (pytest)                  |
| `scripts/`     | One-off utility scripts                     |
| `docs/`        | Documentation                               |

## Code Style

- **Python**: Follow PEP 8. Use async/await for all DB operations.
- **JavaScript**: Vanilla JS — no build tools required.
- **Commits**: Conventional Commits format.

## Adding a New API Endpoint

1. Create or update the router in `app/routers/`
2. Add schema classes to `app/schemas.py` if needed
3. Add models to `app/models.py` if needed
4. Write a test in `tests/`
5. Update `docs/api.md` with the new endpoint
