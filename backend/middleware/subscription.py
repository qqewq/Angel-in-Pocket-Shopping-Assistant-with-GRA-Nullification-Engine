# subscription.py (обновлённый фрагмент)
from fastapi import HTTPException, Depends
from .auth import get_current_user
from ..config.plans import plans

def require_feature(feature: str):
    def dependency(user = Depends(get_current_user)):
        plan = get_user_plan(user.id)
        if feature not in plans[plan]["features"]:
            raise HTTPException(status_code=403, detail="Upgrade required")
        return user
    return dependency

def get_user_plan(user_id: str) -> str:
    # логика из БД
    ...
