from datetime import datetime, timedelta
from .models import PLAN_LIMITS, TransposeHistory, User
from . import db

def get_daily_limit(plan):
    return {
        'free': 5,
        'pro': 50,
        'unlimited': float('inf')
    }.get(plan, 5)

def check_usage_limit(user):
    today = datetime.utcnow().date()
    
    if user.last_used != today:
        user.usage_today = 0
        user.last_used = today
    
    limit = PLAN_LIMITS.get(user.plan, 3)
    
    if limit is not None and user.usage_today >= limit:
        return False  # превышен лимит
    return True