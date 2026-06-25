from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from ..services.evolution_predictor import EvolutionPredictor
from ..services.ethical_filter import EthicalFilter
from ..middleware.subscription import require_feature, get_current_user

router = APIRouter(prefix="/api/roadmap", tags=["roadmap"])
predictor = EvolutionPredictor()

@router.get("/{user_id}")
async def get_roadmap(
    user_id: str,
    horizon: int = Query(5, le=10),
    scenario: Optional[str] = None,
    current_user = Depends(require_feature("personal_roadmap_3y"))
):
    # Дополнительная проверка: horizon >3 только для Visionary
    if horizon > 3 and "personal_roadmap_10y" not in current_user.features:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Upgrade to Visionary for 10y roadmap")

    user_profile = await get_user_profile(user_id)  # функция получения из БД
    if scenario:
        user_profile["life_scenario"] = scenario
    raw_predictions = predictor.predict(user_profile, horizon)
    # Применяем этический фильтр
    filtered = [EthicalFilter.filter(item) for item in raw_predictions]
    return {"roadmap": filtered}

@router.post("/feedback")
async def feedback(
    user_id: str,
    prediction_id: str,
    accepted: bool,
    corrected_category: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    # Логика сохранения обратной связи для обучения GRA-роя
    # ...
    return {"status": "feedback_recorded"}
