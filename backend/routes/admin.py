from flask import Blueprint, render_template, session, redirect, url_for
from models.prediction_history import PredictionHistory
from models.user import User
from database import db
from sqlalchemy import func



admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ===============================
# ADMIN DASHBOARD
# ===============================
@admin_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login_choice"))

    return render_template("admin/dashboard.html")


# ===============================
# ADMIN PREDICTIONS PAGE
# ===============================
@admin_bp.route("/predictions")
def predictions():

    if session.get("role") != "admin":
        return redirect(url_for("auth.login_choice"))

    # 🔥 JOIN Prediction + User
    records = (
        db.session.query(PredictionHistory, User)
        .join(User, PredictionHistory.user_id == User.id)
        .order_by(PredictionHistory.created_at.desc())
        .all()
    )

    return render_template(
        "admin/predictions.html",
        records=records
    )


# ===============================
# ADMIN USERS ANALYTICS PAGE
# ===============================
@admin_bp.route("/users")
def users():

    if session.get("role") != "admin":
        return redirect(url_for("auth.login_choice"))

    # 🔥 LEFT JOIN + GROUP BY + AGGREGATE
    users_data = (
        db.session.query(
            User.id,
            User.name,
            User.email,
            func.count(PredictionHistory.id).label("total_predictions"),
            func.max(PredictionHistory.created_at).label("last_prediction")
        )
        .outerjoin(
            PredictionHistory,
            PredictionHistory.user_id == User.id
        )
        .group_by(User.id)
        .order_by(func.max(PredictionHistory.created_at).desc())
        .all()
    )

    return render_template(
        "admin/users.html",
        users=users_data
    )




# ===============================
# Models PAGE
# ===============================
@admin_bp.route("/models")
def models():
    if session.get("role") != "admin":
        return redirect(url_for("auth.login_choice"))

    return render_template("admin/models.html")
