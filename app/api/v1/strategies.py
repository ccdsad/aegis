from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.api.v1.schemas.strategies import StrategyStatusOut

router = APIRouter(prefix='/strategies', tags=['strategies'])


@router.get(
    '/{strategy_id}/status',
    response_model=StrategyStatusOut,
    response_class=ORJSONResponse,
)
def get_strategy_status(strategy_id: str) -> StrategyStatusOut:
    """Return strategy status snapshot.

    For now this is a lightweight control-plane placeholder.
    """
    return StrategyStatusOut(
        strategy_id=strategy_id,
        status='active',
        enabled=True,
        updated_at=datetime.now(timezone.utc),
    )
