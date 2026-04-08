import logging
from flask import Blueprint, request, jsonify, current_app
from extensions import limiter
from services.note_service import get_note_by_id
from services.ai_service import answer_question

logger = logging.getLogger(__name__)
ask_bp = Blueprint("ask", __name__, url_prefix="/api")


@ask_bp.route("/ask", methods=["POST"])
@limiter.limit("20 per minute")
def ask():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    note_id = data.get("note_id")
    question = data.get("question", "")

    if not isinstance(note_id, int) or note_id < 1:
        return jsonify({"error": "'note_id' must be a positive integer"}), 400
    if not isinstance(question, str) or not question.strip():
        return jsonify({"error": "'question' is required"}), 400

    max_q = current_app.config.get("MAX_QUESTION_LENGTH", 1_000)
    if len(question) > max_q:
        return jsonify({"error": f"Question too long. Max {max_q} characters."}), 400

    note = get_note_by_id(note_id)
    if not note:
        return jsonify({"error": f"Note {note_id} not found"}), 404

    try:
        answer = answer_question(note.content, question.strip())
    except RuntimeError as e:
        logger.error("AI config error: %s", e)
        return jsonify({"error": "AI not configured. Check your API key."}), 503
    except Exception:
        logger.exception("Q&A failed note_id=%d", note_id)
        return jsonify({"error": "AI error. Please try again."}), 502

    return jsonify({"note_id": note_id, "question": question.strip(), "answer": answer}), 200
