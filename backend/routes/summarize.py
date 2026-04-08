import logging
from flask import Blueprint, request, jsonify
from extensions import limiter
from services.note_service import get_note_by_id, save_summary
from services.ai_service import generate_summary, VALID_MODES

logger = logging.getLogger(__name__)
summarize_bp = Blueprint("summarize", __name__, url_prefix="/api")


@summarize_bp.route("/summarize", methods=["POST"])
@limiter.limit("10 per minute")
def summarize():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    note_id = data.get("note_id")
    mode = data.get("mode", "").strip().lower()

    if not isinstance(note_id, int) or note_id < 1:
        return jsonify({"error": "'note_id' must be a positive integer"}), 400
    if mode not in VALID_MODES:
        return jsonify({"error": f"Invalid mode. Choose from: {sorted(VALID_MODES)}"}), 400

    note = get_note_by_id(note_id)
    if not note:
        return jsonify({"error": f"Note {note_id} not found"}), 404

    try:
        output = generate_summary(note.content, mode)
    except RuntimeError as e:
        logger.error("AI config error: %s", e)
        return jsonify({"error": "AI not configured. Check your API key."}), 503
    except Exception:
        logger.exception("Summary failed note_id=%d", note_id)
        return jsonify({"error": "AI error. Please try again."}), 502

    return jsonify(save_summary(note_id, mode, output).to_dict()), 200
