import os

from app import create_app


config_name = os.environ.get("APP_ENV", "development")

app = create_app(config_name)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )