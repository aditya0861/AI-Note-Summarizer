import io
import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import PyPDF2
from extensions import limiter
from services.note_service import create_note

logger = logging.getLogger(__name__)
notes_bp = Blueprint("notes", __name__, url_prefix="/api")


def extract_text(file):
    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in {"txt", "pdf"}:
        raise ValueError(f"Unsupported file type. Use txt or pdf.")
    raw = file.read()
    if ext == "txt":
        return raw.decode("utf-8", errors="ignore"), filename
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(raw))
        return "\n".join(p.extract_text() or "" for p in reader.pages), filename
    except Exception as e:
        raise ValueError(f"Could not read PDF: {e}")


@notes_bp.route("/notes", methods=["POST"])
@limiter.limit("20 per minute")
def upload_note():
    max_len = current_app.config.get("MAX_NOTE_LENGTH", 100_000)
    content = filename = None

    if request.content_type and "multipart/form-data" in request.content_type:
        file = request.files.get("file")
        if not file or not file.filename:
            return jsonify({"error": "No file provided"}), 400
        try:
            content, filename = extract_text(file)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    else:
        data = request.get_json(silent=True)
        if not data or not isinstance(data.get("content"), str):
            return jsonify({"error": "Field 'content' is required"}), 400
        content = data["content"].strip()

    if not content or not content.strip():
        return jsonify({"error": "Note is empty"}), 400
    if len(content) > max_len:
        return jsonify({"error": f"Note too long. Max {max_len} characters."}), 400

    note = create_note(content.strip(), filename)
    return jsonify(note.to_dict()), 201
