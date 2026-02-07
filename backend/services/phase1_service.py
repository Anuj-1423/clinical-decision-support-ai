import os
import joblib
import pandas as pd

# ===============================
# PATH SETUP
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

# ===============================
# LOAD MODEL ARTIFACTS
# ===============================
log_model = joblib.load(
    os.path.join(MODEL_DIR, "clinical_risk_model.pkl")
)

scaler = joblib.load(
    os.path.join(MODEL_DIR, "phase1_scaler.pkl")
)

# This contains ALL features used during training
features = joblib.load(
    os.path.join(MODEL_DIR, "phase1_features.pkl")
)

# ===============================
# RISK TIER LOGIC
# ===============================
def assign_risk_tier(prob):
    if prob >= 0.30:
        return "HIGH"
    elif prob >= 0.15:
        return "MODERATE"
    return "LOW"

# ===============================
# MAIN PREDICTION FUNCTION
# ===============================
def predict_risk(data: dict, return_scaled=False):
    """
    Phase-1 mortality risk prediction.

    Parameters
    ----------
    data : dict
        Raw clinical inputs from frontend
    return_scaled : bool
        If True, also return scaled feature vector
        (needed for Phase-2 model)

    Returns
    -------
    dict OR (dict, np.ndarray)
    """

    # Convert input to DataFrame
    df = pd.DataFrame([data])

    # ===============================
    # AUTO-FILL MISSING FEATURES
    # ===============================
    for col in features:
        if col not in df.columns:
            if col.startswith("max_"):
                mean_col = col.replace("max_", "mean_")
                df[col] = df.get(mean_col, 0)
            elif col.startswith("min_"):
                mean_col = col.replace("min_", "mean_")
                df[col] = df.get(mean_col, 0)
            else:
                df[col] = 0

    # Ensure correct column order
    df = df[features]

    # Scale features
    df_scaled = scaler.transform(df)

    # Predict probability
    risk_prob = log_model.predict_proba(df_scaled)[0][1]
    tier = assign_risk_tier(risk_prob)

    result = {
        "risk": round(float(risk_prob), 4),
        "tier": tier
    }

    if return_scaled:
        return result, df_scaled

    return result
