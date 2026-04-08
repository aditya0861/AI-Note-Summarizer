# Note Summarizer

A full-stack AI-powered app to summarize notes, extract key points, generate flashcards, and chat with your content — all grounded strictly in what you provide.

## Architecture

```
┌─────────────────────────────────────┐
│         React Frontend (Vite)        │
│  NoteInput │ ModeSelector │ Chat     │
│  OutputDisplay │ HistoryPanel        │
└────────────────┬────────────────────┘
                 │ HTTP /api/*
┌────────────────▼────────────────────┐
│         Flask REST API               │
│  routes/ → services/ → models/       │
│  rate limiting │ security headers    │
│  input validation │ error handling   │
└──────────┬──────────────┬───────────┘
           │              │
     ┌─────▼─────┐  ┌─────▼──────┐
     │  SQLite DB │  │  Groq API  │
     │  (local)   │  │  llama-3.3 │
     │  Postgres  │  └────────────┘
     │  (prod)    │
     └────────────┘
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/notes | Save note (text or file upload) |
| POST | /api/summarize | Generate AI summary |
| POST | /api/ask | Ask a question about a note |
| GET | /api/history | Retrieve all notes and summaries |
| GET | /api/health | Health check |

## Key Technical Decisions

**Flask blueprints** — each route group is isolated. Routes only handle HTTP (validate, call service, respond). Business logic lives in services only.

**Groq API (llama-3.3-70b-versatile)** — free tier, fast, OpenAI-compatible SDK. Swappable via `AI_MODEL` env var without code changes.

**SQLite locally, PostgreSQL in production** — zero config for development. `DATABASE_URL` env var switches automatically. `postgres://` is rewritten to `postgresql://` for SQLAlchemy compatibility (Neon quirk).

**Temperature 0.2** — keeps AI outputs consistent and factual across repeated calls.

**Lazy AI client** — `_get_client()` in `ai_service.py` initializes on first use. App starts without a key; only fails when AI is actually called.

**Rate limiting via Flask-Limiter** — 10/min on summarize, 20/min on ask/notes, 60/min on history. In-memory in dev, Redis-backed in production via `RATELIMIT_STORAGE_URL`.

**Vercel deployment** — `api/index.py` is the serverless entry point. `vercel.json` routes `/api/*` to Flask and everything else to the React static build.

## AI Usage

All AI calls go through `backend/services/ai_service.py`. Prompts are stored as plain text files in `backend/prompts/` — not hardcoded.

The system prompt strictly grounds the model in user-provided content. The model is instructed to say "Not specified in the notes." when information is absent. This prevents hallucination by design.

See `agents.md` and `claude.md` for full AI guidance and constraints.

## Risks and Weaknesses

| Risk | Impact | Mitigation |
|------|--------|------------|
| SQLite in production | Data loss under concurrent writes | Use `DATABASE_URL` to switch to PostgreSQL |
| No user authentication | All notes are shared/public | Add JWT auth before public deployment |
| In-memory rate limiting | Resets on restart, not shared across workers | Set `RATELIMIT_STORAGE_URL=redis://...` |
| Chat history not persisted | Lost on page reload | Store chat in DB or localStorage |
| Groq free tier limits | API throttling under heavy use | Add retry logic or switch to paid tier |

## Extension Approach

- **Auth**: Add Flask-JWT-Extended, scope notes per user with a `user_id` FK on the notes table
- **Persistent chat**: Add a `chat_messages` table with `note_id`, `role`, `content`
- **Better DB**: Set `DATABASE_URL` to a PostgreSQL connection string — no code changes needed
- **Different AI model**: Set `AI_MODEL` env var — the client is model-agnostic
- **Redis rate limiting**: Set `RATELIMIT_STORAGE_URL=redis://...`

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # add GROQ_API_KEY
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

### Run Tests
```bash
cd backend
pip install pytest
pytest tests/
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | — | Groq API key (free at console.groq.com) |
| `DATABASE_URL` | No | sqlite:///notes.db | Database connection string |
| `FLASK_ENV` | No | development | Set to `production` for prod |
| `SECRET_KEY` | No | random | Flask secret key |
| `CORS_ORIGINS` | No | * | Comma-separated allowed origins |

## Project Structure

```
api/index.py          # Vercel serverless entry point
backend/
  app.py              # App factory, middleware, error handlers
  config.py           # All config from env vars
  extensions.py       # Shared Flask extensions
  routes/             # HTTP layer — validate, call service, respond
  services/           # Business logic
  models/             # SQLAlchemy models
  prompts/            # AI prompt text files
  tests/              # Pytest tests
frontend/
  src/
    api.js            # All HTTP calls
    components/       # React components
agents.md             # AI agent coding rules and constraints
claude.md             # Claude-specific AI guidance
```
