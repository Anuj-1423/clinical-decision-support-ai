from backend.database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # ✅ MUST be nullable for Google users
    password = db.Column(db.String(255), nullable=True)

    role = db.Column(db.String(20), nullable=False, default="user")
    # ✅ PROFILE FIELDS
    phone = db.Column(db.String(20))
    alternate_email = db.Column(db.String(120))
    alternate_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    profile_image = db.Column(db.String(255))



