from datetime import datetime

from pydantic import BaseModel


class StrategyStatusOut(BaseModel):
    """Control-plane strategy status view."""

    strategy_id: str
    status: str
    enabled: bool
    updated_at: datetime
