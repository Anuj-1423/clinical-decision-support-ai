import os
import joblib
import numpy as np

# ===============================
# PATH SETUP
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

# ===============================
# LOAD PHASE-2 MODEL
# ===============================
treatment_model = joblib.load(
    os.path.join(MODEL_DIR, "phase2_treatment_model.pkl")
)

# ===============================
# TREATMENT COMPARISON FUNCTION
# ===============================
def compare_treatment(scaled_features: np.ndarray):
    """
    Compare predicted risk with and without antibiotic treatment.

    Parameters
    ----------
    scaled_features : np.ndarray
        Output from Phase-1 scaler.
        Shape: (1, n_features)

    Returns
    -------
    dict
        {
            "no_antibiotic": float,
            "with_antibiotic": float
        }
    """

    # ---------- No Antibiotic ----------
    no_antibiotic_input = np.hstack([
        scaled_features,
        np.array([[0]])
    ])
    risk_no_antibiotic = treatment_model.predict_proba(
        no_antibiotic_input
    )[0][1]

    # ---------- With Antibiotic ----------
    with_antibiotic_input = np.hstack([
        scaled_features,
        np.array([[1]])
    ])
    risk_with_antibiotic = treatment_model.predict_proba(
        with_antibiotic_input
    )[0][1]

    return {
        "no_antibiotic": round(float(risk_no_antibiotic), 4),
        "with_antibiotic": round(float(risk_with_antibiotic), 4)
    }
