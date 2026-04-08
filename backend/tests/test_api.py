import pytest
from app import create_app
from models.database import db as _db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# --- /api/notes ---

def test_create_note_success(client):
    res = client.post("/api/notes", json={"content": "Photosynthesis converts sunlight to energy."})
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data
    assert "Photosynthesis" in data["content"]
    assert "created_at" in data


def test_create_note_missing_content(client):
    res = client.post("/api/notes", json={})
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_create_note_empty_string(client):
    res = client.post("/api/notes", json={"content": "   "})
    assert res.status_code == 400


def test_create_note_too_long(client):
    res = client.post("/api/notes", json={"content": "x" * 200_001})
    assert res.status_code == 400


def test_create_note_wrong_type(client):
    res = client.post("/api/notes", json={"content": 12345})
    assert res.status_code == 400


# --- /api/summarize ---

def test_summarize_invalid_mode(client):
    client.post("/api/notes", json={"content": "Some note content."})
    res = client.post("/api/summarize", json={"note_id": 1, "mode": "invalid"})
    assert res.status_code == 400


def test_summarize_note_not_found(client):
    res = client.post("/api/summarize", json={"note_id": 999, "mode": "concise"})
    assert res.status_code == 404


def test_summarize_missing_note_id(client):
    res = client.post("/api/summarize", json={"mode": "concise"})
    assert res.status_code == 400


def test_summarize_invalid_note_id_type(client):
    res = client.post("/api/summarize", json={"note_id": "abc", "mode": "concise"})
    assert res.status_code == 400


# --- /api/ask ---

def test_ask_missing_question(client):
    client.post("/api/notes", json={"content": "Some note content."})
    res = client.post("/api/ask", json={"note_id": 1, "question": ""})
    assert res.status_code == 400


def test_ask_note_not_found(client):
    res = client.post("/api/ask", json={"note_id": 999, "question": "What is this?"})
    assert res.status_code == 404


def test_ask_question_too_long(client):
    client.post("/api/notes", json={"content": "Some note content."})
    res = client.post("/api/ask", json={"note_id": 1, "question": "q" * 2000})
    assert res.status_code == 400


def test_ask_missing_note_id(client):
    res = client.post("/api/ask", json={"question": "What is this?"})
    assert res.status_code == 400


# --- /api/history ---

def test_history_empty(client):
    res = client.get("/api/history")
    assert res.status_code == 200
    assert res.get_json() == []


def test_history_returns_notes(client):
    client.post("/api/notes", json={"content": "Test note."})
    res = client.get("/api/history")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["content"] == "Test note."
    assert "summaries" in data[0]


def test_history_invalid_limit(client):
    res = client.get("/api/history?limit=abc")
    assert res.status_code == 400


# --- /api/health ---

def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"
