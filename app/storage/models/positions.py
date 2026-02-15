from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True, kw_only=True)
class PositionRecord:
    """Persisted position aggregate for strategy/symbol."""

    strategy_id: str
    symbol: str
    quantity: float = 0.0
    average_price: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
