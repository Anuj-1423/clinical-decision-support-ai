from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from database import db
from models.user import User
import os
import uuid
from werkzeug.utils import secure_filename


# === IMPORT ML SERVICES ===
from services.phase1_service import predict_risk
from services.phase2_service import compare_treatment
from models.prediction_history import PredictionHistory


user_bp = Blueprint("user", __name__, url_prefix="/user")


# ===============================
# USER DASHBOARD
# ===============================
@user_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "user":
        return redirect(url_for("auth.login_choice"))

    return render_template("user/dashboard.html")


# ===============================
# USER PREDICTION PAGE (GET)
# ===============================
@user_bp.route("/predict", methods=["GET"])
def predict_page():
    if session.get("role") != "user":
        return redirect(url_for("auth.login_choice"))

    return render_template("user/predict.html")


# ===============================
# USER PREDICTION API (POST)
# ===============================
@user_bp.route("/predict", methods=["POST"])
def predict_api():
    if session.get("role") != "user":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    try:
        # -------------------------
        # PHASE 1: RISK PREDICTION
        # -------------------------
        risk_prob, risk_tier = predict_risk(data)

        # -------------------------
        # PHASE 2: TREATMENT COMPARE
        # -------------------------
        treatment = compare_treatment(data)

        return jsonify({
            "risk": round(risk_prob, 4),
            "tier": risk_tier,
            "treatment": {
                "no_antibiotic": round(treatment["no_antibiotic"], 4),
                "with_antibiotic": round(treatment["with_antibiotic"], 4)
            }
        })

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({"error": "Prediction failed"}), 500




# ===============================
# USER HISTORY PAGE
# ===============================
@user_bp.route("/history")
def history():
    if session.get("role") != "user":
        return redirect(url_for("auth.login_choice"))

    records = PredictionHistory.query.filter_by(
        user_id=session["user_id"]
    ).order_by(PredictionHistory.created_at.desc()).all()

    total_predictions = len(records)

    return render_template(
        "user/history.html",
        records=records,
        total_predictions=total_predictions
    )

# ===============================
# USER PROFILE PAGE
# ===============================
@user_bp.route("/profile", methods=["GET", "POST"])
def profile():

    if session.get("role") != "user":
        return redirect(url_for("auth.login_choice"))

    user = User.query.get(session.get("user_id"))

    if not user:
        return redirect(url_for("auth.login_choice"))

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "frontend", "static", "uploads")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    ALLOWED = {"png","jpg","jpeg","webp"}

    def allowed_file(name):
        return "." in name and name.rsplit(".",1)[1].lower() in ALLOWED

    if request.method == "POST":

        print("FILES:", request.files)  # DEBUG

        user.name = request.form.get("name") or user.name
        user.email = request.form.get("email") or user.email
        user.phone = request.form.get("phone") or user.phone
        user.address = request.form.get("address") or user.address

        file = request.files.get("profile_image")

        if file and file.filename != "" and allowed_file(file.filename):

            import uuid
            ext = file.filename.rsplit(".",1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"

            file.save(os.path.join(UPLOAD_FOLDER, filename))

            user.profile_image = f"/static/uploads/{filename}"

        db.session.commit()

        return render_template("user/profile.html", user=user, saved=True)

    return render_template("user/profile.html", user=user)
