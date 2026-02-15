from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.domain.risk import RiskReason


class RiskDecisionOut(BaseModel):
    """Serialized risk decision details for one intent."""

    intent_uid: UUID
    reason: RiskReason
    message: str | None
    status: str
    updated_at: datetime
