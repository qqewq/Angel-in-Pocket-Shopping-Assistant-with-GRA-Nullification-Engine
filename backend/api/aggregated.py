from fastapi import APIRouter, Depends, Query
from typing import Optional
from ..services.swarm_aggregator import SwarmAggregator
from ..middleware.subscription import require_feature
from ..db import get_db_session

router = APIRouter(prefix="/api/aggregated", tags=["aggregated"])
# Инициализация агрегатора с фабрикой сессий БД
aggregator = SwarmAggregator(get_db_session)

@router.get("/demand")
async def get_aggregated_demand(
    region: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    horizon: int = Query(5, le=10),
    _ = Depends(require_feature("aggregated_demand_access"))
):
    data = aggregator.aggregate(region, sector, horizon)
    return {"demand_forecast": data}
