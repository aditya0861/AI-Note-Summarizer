# Note Summarizer

Paste or upload your notes and get summaries, key points, flashcards, keywords, or chat with your content.

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
# create .env with your GROQ_API_KEY (free at console.groq.com)
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## Environment Variables

Create `backend/.env`:
```
GROQ_API_KEY=your_key_here
```

## Stack
- React + Vite
- Python + Flask
- SQLite (local) / PostgreSQL (production)
- Groq API (llama-3.3-70b)
