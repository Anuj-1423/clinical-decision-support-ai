from flask import Blueprint, render_template, request, redirect, url_for, session
from database import db
from services.auth import hash_password, verify_password
from models.user import User
from extensions import oauth
import secrets
from flask import session, redirect, url_for




auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ===============================
# FORCE LOGIN → CHOICE
# ===============================
@auth_bp.route("/login")
def login():
    return redirect(url_for("auth.login_choice"))


# ===============================
# LOGIN CHOICE
# ===============================
@auth_bp.route("/login-choice")
def login_choice():
    return render_template("auth/choose_login.html")


# ===============================
# ADMIN LOGIN (UNCHANGED)
# ===============================
@auth_bp.route("/login/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        session["role"] = "admin"
        return redirect(url_for("admin.dashboard"))

    return render_template("auth/login.html")


# ===============================
# USER LOGIN (FIXED)
# ===============================


@auth_bp.route("/login/user", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # ❌ user not found
        if not user:
            return render_template(
                "auth/user_login.html",
                error="Invalid email or password"
            )

        # ❌ user registered via Google
        if not user.password:
            return render_template(
                "auth/user_login.html",
                error="Please login using Google"
            )

        # ❌ password mismatch
        if not verify_password(user.password, password):
            return render_template(
                "auth/user_login.html",
                error="Invalid email or password"
            )

        # ❌ wrong role
        if user.role != "user":
            return render_template(
                "auth/user_login.html",
                error="Not a user account"
            )

        # ✅ SUCCESS
        session["user_id"] = user.id
        session["user_email"] = user.email
        session["role"] = "user"

        return redirect(url_for("user.dashboard"))

    return render_template("auth/user_login.html")



import secrets
from flask import Blueprint, render_template, request, redirect, url_for, session
from database import db
from models.user import User
from extensions import oauth


# ===============================
# GOOGLE LOGIN
# ===============================
@auth_bp.route("/login/google")
def google_login():
    nonce = secrets.token_urlsafe(16)
    session["google_nonce"] = nonce

    redirect_uri = url_for(
        "auth.google_callback",
        _external=True
    )

    return oauth.google.authorize_redirect(
        redirect_uri,
        nonce=nonce
    )


# ===============================
# GOOGLE CALLBACK
# ===============================
@auth_bp.route("/login/google/callback")
def google_callback():

    nonce = session.pop("google_nonce", None)
    if not nonce:
        return redirect(url_for("auth.login_choice"))

    token = oauth.google.authorize_access_token()

    user_info = oauth.google.parse_id_token(
        token,
        nonce=nonce
    )

    email = user_info["email"]
    name = user_info.get("name", email.split("@")[0])

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            name=name,
            email=email,
            role="user"
        )
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session["user_email"] = user.email
    session["role"] = "user"

    return redirect(url_for("user.dashboard"))



@auth_bp.route("/register/user", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            return redirect(url_for("auth.user_login"))

        user = User(
            name=email.split("@")[0],
            email=email,
            password=hash_password(password),
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.user_login"))

    return render_template("auth/user_register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("public.home"))




