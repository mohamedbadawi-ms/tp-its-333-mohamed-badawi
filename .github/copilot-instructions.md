# Copilot Instructions — upec-its-333

Purpose: short, actionable notes for an AI coding assistant to be immediately productive in this teaching repository.

## Big picture
- This repo contains small, independent Flask-based teaching examples (APIs, DB exercises) grouped under `srcCodeAPIs/` and `srcCodeFichiersSemiStruct/`.
- Each example is self-contained; common pattern: an `app` package or single-file `app.py` exposing a Flask `app` and a `run` script (either `run.py` or `if __name__ == '__main__'` in `app.py`/`views.py`).

## Entry points & how to run (examples)
- myFirstAPI_with_webAPI: cd `srcCodeAPIs/myFirstAPI_with_webAPI` → `python app.py` (exposes `/api/salutation` and `/api/utilisateurs`).
- mySecondAPI_with_MVC: cd `srcCodeAPIs/mySecondAPI_with_MVC` → `python run.py` (package `app/` with `views.py` and templates).
- sqlite_demo: cd `srcCodeFichiersSemiStruct/sqlite_demo` → `python -m app.views` or `python app/views.py` (creates `database.db` in working dir; `models.init_db()` runs on import).
- sqlalchemy: cd `srcCodeFichiersSemiStruct/sqlalchemy` → `python run.py` (uses `flask_sqlalchemy` models in `app/models.py`).
- BDD102 API: cd `srcCodeFichiersSemiStruct/BDD102` → `python api.py` (exposes `/patient/recherche` on port 5000).

Note: Many modules rely on relative file paths (e.g. `BDD102/data.json`) — run scripts from the project root (or the repo root) to avoid path issues.

## Dependencies & setup
- Global / per-example: install dependencies via `pip install -r requirements.txt` where provided (e.g. `srcCodeAPIs/myFirstAPI_with_webAPI/requirements.txt` contains `Flask==3.1.0`).
- Projects using SQL: `flask_sqlalchemy` is used in `srcCodeFichiersSemiStruct/sqlalchemy` (not declared in a requirements file); install with `pip install Flask-SQLAlchemy` when working with that example.
- Swagger UI: The `sqlalchemy` example uses `flasgger` for a Swagger UI. If `flasgger` is not installed the app will still run but the Swagger UI will be disabled; install with `pip install flasgger` or `pip install -r srcCodeFichiersSemiStruct/sqlalchemy/requirements.txt`.

## Project-specific conventions and patterns
- Many examples use the package name `app` and rely on the import order: `app/__init__.py` defines `app=Flask(__name__)` then imports `views` which may import `models` — avoid circular import regressions by keeping `app` factory at top of `app/__init__.py`.
- Data files are read with relative paths (e.g., `chemin = "BDD102/data.json"` in `recherche.py`). Keep current working directory consistent when running scripts.
- Templates live under `*/templates/` and are used by `render_template` in MVC examples.

## Important discoveries / gotchas
- MISMATCH: `srcCodeFichiersSemiStruct/BDD102/recherche.py` uses `chemin = "BDD102/data.json"` but the repo contains `srcCodeFichiersSemiStruct/BDD102/patient.json`. This will cause the API in `api.py` to return a file-not-found error. Quick fixes:
  - Rename `patient.json` → `data.json`, or
  - Update `recherche.py` to point to `"BDD102/patient.json"`.

- Several examples do not have pinned requirements; install `Flask` and `Flask-SQLAlchemy` in a virtualenv as needed.

## Guidance for code edits an AI assistant should follow
- Make minimal, well-scoped changes with tests or manual run instructions (examples above) to verify behavior.
- When changing data file paths, update all callers (e.g., `recherche.py` and any tests or example scripts).
- Prefer edits that preserve the educational intent: keep short, explicit APIs and small model examples intact.

## Useful files to inspect when making changes
- Entry points: `app.py`, `run.py`, `api.py`, `app/views.py`
- Models & DB: `srcCodeFichiersSemiStruct/sqlalchemy/app/models.py`, `sqlite_demo/app/models.py`
- Data helper code: `srcCodeFichiersSemiStruct/BDD101/read.py`, `srcCodeFichiersSemiStruct/BDD102/recherche.py`
- Templates: any `templates/` folders under example apps for UI examples.

---
If any of the sections are unclear or you'd like me to add automated checks (e.g., CI step verifying `BDD102/data.json` exists), tell me which check to add and I can propose a PR with a unit test or CI job. Please indicate which examples you expect to prioritize. ✅