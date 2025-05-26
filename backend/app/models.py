from datetime import datetime
from . import db


PLAN_LIMITS = {
    "free": 3,       # 3 транспонирования в день
    "premium": 50,   # 50 в день
    "pro": None      # безлимит
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    plan = db.Column(db.String(20), default='free')  # free, premium, pro
    usage_today = db.Column(db.Integer, default=0)
    last_used = db.Column(db.Date, default=datetime.utcnow().date)


class TransposeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_type = db.Column(db.String(10))  # 'png', 'midi', 'xml'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)