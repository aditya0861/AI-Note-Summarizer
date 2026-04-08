# 🚀 AI Note Summarizer

An AI-powered full-stack web application that summarizes notes, extracts key insights, generates flashcards, and allows users to ask questions — all strictly based on the provided content.

---

## 🌐 Live Demo

* **Frontend (Vercel):** https://your-frontend-link.vercel.app
* **Backend (Render):** https://ai-note-backend-1umg.onrender.com

---

## ✨ Features

* 🧠 Generate summaries (concise, detailed, key points)
* 📌 Extract important keywords with explanations
* 🎴 Create flashcards for revision
* 💬 Ask questions from notes (Chat with notes)
* 📄 Upload text or PDF notes
* 🕘 View history of notes and outputs
* 🔒 AI safety: no hallucination, answers only from input

---

## 🏗️ Architecture

```
User → React (Frontend)
     → Flask API (Backend)
     → Groq LLM
     → Response → UI
```

---

## ⚙️ Tech Stack

* **Frontend:** React (Vite), Axios
* **Backend:** Flask (Python)
* **Database:** SQLite (development), PostgreSQL (production-ready)
* **AI:** Groq (LLaMA 3)
* **Deployment:** Vercel (frontend), Render (backend)

---

## 🔌 API Endpoints

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| POST   | `/api/notes`     | Upload note (text/file) |
| POST   | `/api/summarize` | Generate summary        |
| POST   | `/api/ask`       | Ask question            |
| GET    | `/api/history`   | Get history             |
| GET    | `/api/health`    | Health check            |

---

## 🧠 AI Design

* Uses structured prompts for consistent output
* Model strictly grounded in user input
* If information is missing → returns:
  **"Not specified in the notes"**
* Low temperature (0.2) for accuracy
* Prompts stored separately in `/prompts`

---

## 🔧 Setup Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY
python app.py
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open: http://localhost:3000

---

## 🔐 Environment Variables

```
GROQ_API_KEY=your_api_key
DATABASE_URL=your_database_url (optional)
FLASK_ENV=development or production
```

---

## 📁 Project Structure

```
backend/
  app.py
  routes/
  services/
  models/
  prompts/
  tests/

frontend/
  src/
    api.js
    components/

agents.md
claude.md
```

---

## ⚠️ Limitations

* No user authentication (all notes are shared)
* Free AI tier may have rate limits
* Chat history not persisted

---

## 🚀 Future Improvements

* Add user authentication (JWT)
* Store chat history
* Improve UI/UX
* Support multiple languages

---

## 🏆 Conclusion

This project demonstrates:

* Full-stack development (React + Flask)
* AI integration with prompt engineering
* Secure API handling with environment variables
* Deployment using Vercel and Render

---
