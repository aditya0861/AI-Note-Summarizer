# Claude AI Guidance

## Role
You are assisting with a Flask + React note summarizer app. Follow these rules strictly.

## Architecture Rules
- Routes are HTTP-only: validate input → call service → return JSON
- Services contain all logic: no `request`, no `jsonify` in services
- Models are data-only: no business logic
- All AI calls go through `backend/services/ai_service.py` — nowhere else

## When Adding a New Feature
1. Add the route in `backend/routes/`
2. Add the logic in `backend/services/`
3. Add rate limiting with `@limiter.limit()`
4. Validate all inputs — type check, length check, required fields
5. Return `{"error": "..."}` for failures, never raw exceptions
6. Update `requirements.txt` if adding a dependency

## When Editing AI Behavior
- Edit `backend/prompts/system_prompt.txt` for global behavior
- Edit `backend/prompts/mode_prompts.txt` for per-mode output format
- Never change temperature above 0.2
- Never instruct the model to use external knowledge
- Always test that "Not specified in the notes." is returned for missing info

## When Editing the Frontend
- All API calls go in `frontend/src/api.js` only
- Components receive data as props or from local state — no fetch/axios in components
- Always handle loading, error, and empty states
- Use `e.displayMessage` for error messages (set by axios interceptor in api.js)

## Code Style
- Python: PEP8, 100 char line limit, f-strings, type hints on function signatures
- JS: ES6+, arrow functions, destructuring, no var
- No commented-out code
- No TODO comments in committed code

## Security Rules
- Never log note content — only IDs, lengths, modes
- Never return stack traces to the client
- Never hardcode secrets — use environment variables
- Input length limits must be enforced in routes before calling services

## What to Avoid
- Do not use `Query.get()` — use `db.session.get(Model, id)` (SQLAlchemy 2.x)
- Do not use `db.create_all()` in production
- Do not import from `app.py` in routes — use `extensions.py` for shared objects
- Do not add inline styles to JSX components
