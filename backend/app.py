from flask import Flask
from database import db
from extensions import oauth   # ✅ SAME INSTANCE

# ===============================
# Config
# ===============================
from config import (
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET
)

# ===============================
# Blueprints
# ===============================
from routes.public import public_bp
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp
from routes.prediction import prediction_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # ===============================
    # App Config
    # ===============================
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SESSION_COOKIE_SECURE"] = False

    # ===============================
    # Init DB
    # ===============================
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # ===============================
    # ✅ INIT OAUTH (THIS WAS MISSING / MISWIRED)
    # ===============================
    oauth.init_app(app)

    oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,

    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    api_base_url="https://openidconnect.googleapis.com/v1/",

    # ✅ THIS FIXES THE ERROR
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",

    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account"
       }
      )


    # ===============================
    # Register Blueprints
    # ===============================
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(prediction_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
