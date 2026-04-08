import logging
import logging.handlers
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, g, request
from flask_cors import CORS

from config import get_config
from models.database import db
from extensions import limiter
from routes.notes import notes_bp
from routes.summarize import summarize_bp
from routes.ask import ask_bp
from routes.history import history_bp


def setup_logging():
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handlers = [logging.StreamHandler()]
    log_file = os.environ.get("LOG_FILE")
    if log_file:
        handlers.append(
            logging.handlers.RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        )
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=handlers)


setup_logging()
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    cfg = get_config()
    app.config.from_object(cfg)

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if os.environ.get("FLASK_ENV") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    @app.before_request
    def start_timer():
        g.start = __import__("time").time()

    @app.after_request
    def log_request(response):
        ms = (__import__("time").time() - g.get("start", 0)) * 1000
        logger.info("%s %s %d %.0fms", request.method, request.path, response.status_code, ms)
        return response

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"error": "File too large. Max 10MB."}), 413

    @app.errorhandler(429)
    def rate_limited(e):
        return jsonify({"error": "Too many requests. Slow down."}), 429

    @app.errorhandler(500)
    def server_error(e):
        logger.exception("Internal error")
        return jsonify({"error": "Something went wrong. Try again."}), 500

    CORS(app, origins=cfg.CORS_ORIGINS, supports_credentials=False)
    db.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(notes_bp)
    app.register_blueprint(summarize_bp)
    app.register_blueprint(ask_bp)
    app.register_blueprint(history_bp)

    @app.route("/api/health")
    def health():
        try:
            db.session.execute(db.text("SELECT 1"))
            return jsonify({"status": "ok"}), 200
        except Exception:
            return jsonify({"status": "error"}), 503

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False), port=int(os.environ.get("PORT", 5000)))
