import os
from flask import Flask
from backend.database import db
from backend.extensions import oauth

from backend.routes.public import public_bp
from backend.routes.auth import auth_bp
from backend.routes.user import user_bp
from backend.routes.admin import admin_bp
from backend.routes.prediction import prediction_bp

from backend.config import (
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET
)


def create_app():

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
        static_folder=os.path.join(BASE_DIR, "frontend", "static")
    )

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SESSION_COOKIE_SECURE"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    oauth.init_app(app)

    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        access_token_url="https://oauth2.googleapis.com/token",
        api_base_url="https://openidconnect.googleapis.com/v1/",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        client_kwargs={
            "scope": "openid email profile",
            "prompt": "select_account"
        }
    )

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(prediction_bp)

    return app

app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Print all registered routes for debugging
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule}")
    print()
    app.run(host="0.0.0.0", port=port, debug=True)