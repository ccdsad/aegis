from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/strategies', tags=['strategies'])


class StrategyStatusOut(BaseModel):
    """Control-plane strategy status view."""

    strategy_id: str
    status: str
    enabled: bool
    updated_at: datetime


@router.get('/{strategy_id}/status', response_model=StrategyStatusOut)
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
