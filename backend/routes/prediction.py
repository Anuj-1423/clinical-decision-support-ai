from flask import Blueprint, request, jsonify, session
from services.phase1_service import predict_risk
from services.phase2_service import compare_treatment
from database import db
from models.prediction_history import PredictionHistory

prediction_bp = Blueprint("prediction", __name__, url_prefix="/predict")


@prediction_bp.route("/", methods=["POST"])
def predict():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    # Phase 1
    phase1_result, scaled_features = predict_risk(
        data,
        return_scaled=True
    )

    # Phase 2
    treatment = compare_treatment(scaled_features)

    # SAVE HISTORY
    record = PredictionHistory(
        user_id=session["user_id"],
        risk_score=phase1_result["risk"],
        risk_tier=phase1_result["tier"],
        risk_no_antibiotic=treatment["no_antibiotic"],
        risk_with_antibiotic=treatment["with_antibiotic"]
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({
        "risk": phase1_result["risk"],
        "tier": phase1_result["tier"],
        "treatment": treatment
    })
