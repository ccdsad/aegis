from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class SignalSide(StrEnum):
    """Trade direction attached to a signal."""

    BUY = 'buy'
    SELL = 'sell'


class SignalType(StrEnum):
    """Signal semantic used by downstream decision rules."""

    ENTRY = 'entry'
    EXIT = 'exit'
    REBALANCE = 'rebalance'


@dataclass(slots=True, frozen=True, kw_only=True)
class Signal:
    """Immutable market/strategy signal entering the decision pipeline."""

    id: UUID = field(default_factory=uuid4)
    strategy_id: str
    symbol: str
    side: SignalSide
    signal_type: SignalType
    quantity: float
    price_hint: float | None = None
    confidence: float = 1.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict[str, Any])
