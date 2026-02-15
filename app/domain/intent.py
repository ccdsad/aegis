from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from app.domain.signal import Signal, SignalSide


class IntentType(StrEnum):
    """Action class produced by decision engine."""

    OPEN = 'open'
    CLOSE = 'close'
    ADJUST = 'adjust'


@dataclass(slots=True, frozen=True, kw_only=True)
class Intent:
    """Normalized execution request created from one strategy signal."""

    uid: UUID = field(default_factory=uuid4)
    strategy_id: str
    signal_uid: UUID
    symbol: str
    side: SignalSide
    quantity: float
    intent_type: IntentType
    limit_price: float | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def from_signal(
        cls,
        signal: Signal,
        *,
        intent_type: IntentType,
        quantity: float | None = None,
        limit_price: float | None = None,
    ) -> Self:
        return cls(
            strategy_id=signal.strategy_id,
            signal_uid=signal.uid,
            symbol=signal.symbol,
            side=signal.side,
            quantity=signal.quantity if quantity is None else quantity,
            intent_type=intent_type,
            limit_price=limit_price,
        )
