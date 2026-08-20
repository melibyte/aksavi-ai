from flask import Flask, jsonify
from flask_cors import CORS

from config import config_by_name
from app.database import init_db
from app.routes import api_bp, main_bp


def create_app(config_name="development"):
    """Flask uygulamasını oluşturur ve gerekli bileşenleri bağlar."""

    app = Flask(__name__)

    config_class = config_by_name.get(
        config_name,
        config_by_name["default"]
    )
    app.config.from_object(config_class)

    CORS(
        app,
        origins=app.config["CORS_ORIGINS"]
    )

    init_db(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok"
        }), 200

    return app