from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domain.risk import RiskReason


class IntentAuditOut(BaseModel):
    """Serialized intent audit state."""

    uid: UUID
    signal_uid: UUID
    strategy_id: str
    symbol: str
    quantity: float
    reason: RiskReason
    message: str | None
    status: str
    created_at: datetime
    updated_at: datetime
