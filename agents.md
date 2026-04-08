# AI Agent Guidance

## Purpose
This file defines how AI agents should behave when working on this codebase.

## Coding Standards
- Python: follow PEP8, max line length 100
- JavaScript: ES6+, functional React components only
- No inline styles in JSX except ErrorBoundary (one-off component)
- All API responses must be JSON with consistent shape: `{ "key": value }` or `{ "error": "message" }`

## Constraints
- Never expose internal error details to the client — log server-side, return generic message
- Never store user content in logs — only metadata (length, mode, IDs)
- All AI calls must go through `backend/services/ai_service.py` only
- Do not add new routes without input validation and rate limiting
- Do not change the `/api` URL prefix — frontend and vercel.json depend on it

## Prompting Rules
- System prompt lives in `backend/prompts/system_prompt.txt` — edit there, not in code
- Mode prompts live in `backend/prompts/mode_prompts.txt` — one section per mode, format: `[mode_name]`
- Temperature must stay at 0.2 for deterministic outputs
- Model: `llama-3.3-70b-versatile` via Groq API

## AI Safety Rules
- The AI must only use content from the provided notes
- If information is not in the notes, respond: "Not specified in the notes."
- No hallucination — prompts are designed to ground the model strictly in user input

## File Responsibilities
| File | Responsibility |
|---|---|
| `backend/app.py` | App factory, middleware, error handlers |
| `backend/config.py` | All config from environment variables |
| `backend/extensions.py` | Shared Flask extensions (limiter) |
| `backend/routes/` | HTTP layer only — validate input, call service, return response |
| `backend/services/` | Business logic — no HTTP concerns |
| `backend/models/` | SQLAlchemy models only |
| `backend/prompts/` | Prompt text files — no logic |
| `frontend/src/api.js` | All HTTP calls — nowhere else |
| `frontend/src/components/` | UI only — no direct API calls except via api.js |

## What NOT to Do
- Do not put business logic in routes
- Do not put HTTP logic in services
- Do not hardcode API keys, URLs, or model names in code
- Do not use `db.create_all()` in production — use migrations
- Do not add dependencies without updating `requirements.txt`
