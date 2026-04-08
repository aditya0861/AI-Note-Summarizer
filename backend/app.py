import os
import time
import logging
import logging.handlers

from dotenv import load_dotenv
from flask import Flask, jsonify, g, request
from flask_cors import CORS

from config import get_config
from models.database import db
from extensions import limiter
from routes.notes import notes_bp
from routes.summarize import summarize_bp
from routes.ask import ask_bp
from routes.history import history_bp


# =========================
# Load environment variables
# =========================
load_dotenv()


# =========================
# Logging setup
# =========================
def setup_logging():
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handlers = [logging.StreamHandler()]

    log_file = os.environ.get("LOG_FILE")
    if log_file:
        handlers.append(
            logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=5
            )
        )

    logging.basicConfig(level=logging.INFO, format=fmt, handlers=handlers)


setup_logging()
logger = logging.getLogger(__name__)


# =========================
# App Factory
# =========================
def create_app():
    app = Flask(__name__)

    # Load config
    cfg = get_config()
    app.config.from_object(cfg)

    # Enable CORS
    CORS(app, origins=cfg.CORS_ORIGINS, supports_credentials=False)

    # Init extensions
    db.init_app(app)
    limiter.init_app(app)

    # =========================
    # Security Headers
    # =========================
    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        if os.environ.get("FLASK_ENV") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response

    # =========================
    # Request Timing
    # =========================
    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        duration = (time.time() - g.get("start_time", time.time())) * 1000
        logger.info(
            "%s %s %s %d %.2fms",
            request.remote_addr,
            request.method,
            request.path,
            response.status_code,
            duration
        )
        return response

    # =========================
    # Error Handlers
    # =========================
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(413)
    def file_too_large(e):
        return jsonify({"error": "File too large. Max 10MB."}), 413

    @app.errorhandler(429)
    def rate_limited(e):
        return jsonify({"error": "Too many requests. Please slow down."}), 429

    @app.errorhandler(500)
    def server_error(e):
        logger.exception("Internal Server Error")
        return jsonify({"error": "Something went wrong. Try again later."}), 500

    # =========================
    # Register Blueprints
    # =========================
    app.register_blueprint(notes_bp)
    app.register_blueprint(summarize_bp)
    app.register_blueprint(ask_bp)
    app.register_blueprint(history_bp)

    # =========================
    # Health Check
    # =========================
    @app.route("/api/health")
    def health():
        try:
            db.session.execute(db.text("SELECT 1"))
            return jsonify({"status": "ok"}), 200
        except Exception:
            return jsonify({"status": "error"}), 503

    # =========================
    # Create DB Tables
    # =========================
    with app.app_context():
        db.create_all()

    return app


# =========================
# IMPORTANT FOR RENDER
# =========================
app = create_app()


# =========================
# Local Run
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=app.config.get("DEBUG", False)
    )