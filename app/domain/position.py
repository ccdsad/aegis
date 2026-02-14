from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(kw_only=True)
class Position:
    """Current strategy position snapshot for one symbol."""

    strategy_id: str
    symbol: str
    quantity: float = 0.0
    average_price: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_flat(self) -> bool:
        return self.quantity == 0.0
