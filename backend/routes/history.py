import logging
from flask import Blueprint, jsonify, request
from extensions import limiter
from services.note_service import get_history

logger = logging.getLogger(__name__)
history_bp = Blueprint("history", __name__, url_prefix="/api")


@history_bp.route("/history", methods=["GET"])
@limiter.limit("60 per minute")
def history():
    try:
        limit = min(int(request.args.get("limit", 50)), 100)
        offset = max(int(request.args.get("offset", 0)), 0)
    except ValueError:
        return jsonify({"error": "limit and offset must be integers"}), 400
    return jsonify(get_history(limit=limit, offset=offset)), 200
