from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID

from app.domain.intent import IntentType
from app.domain.risk import RiskReason
from app.domain.signal import SignalSide, SignalType


class ProcessingStatus(StrEnum):
    """Signal processing status persisted for audit and replay."""

    APPROVED = 'approved'
    REJECTED = 'rejected'


@dataclass(slots=True, kw_only=True)
class IntentRecord:
    """Persisted audit record for one processed signal intent."""

    uid: UUID
    signal_uid: UUID
    strategy_id: str
    symbol: str
    side: SignalSide
    signal_type: SignalType
    intent_type: IntentType
    quantity: float
    status: ProcessingStatus
    reason: RiskReason
    message: str | None
    limit_price: float | None
    created_at: datetime
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True, kw_only=True)
class FillRecord:
    """Persisted execution/simulation fill linked to an intent record."""

    uid: UUID
    intent_uid: UUID
    order_uid: UUID
    quantity: float
    price: float
    fee: float
    occurred_at: datetime
