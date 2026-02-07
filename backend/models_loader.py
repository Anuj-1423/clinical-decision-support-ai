import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

phase1_model = joblib.load(os.path.join(MODEL_DIR, "clinical_risk_model.pkl"))
phase2_model = joblib.load(os.path.join(MODEL_DIR, "phase2_treatment_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "phase1_scaler.pkl"))
phase1_features = joblib.load(os.path.join(MODEL_DIR, "phase1_features.pkl"))
