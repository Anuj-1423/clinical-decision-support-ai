from database import db
from datetime import datetime

class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Phase-1 results
    risk_score = db.Column(db.Float, nullable=False)
    risk_tier = db.Column(db.String(20), nullable=False)

    # Phase-2 results
    risk_no_antibiotic = db.Column(db.Float, nullable=False)
    risk_with_antibiotic = db.Column(db.Float, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
