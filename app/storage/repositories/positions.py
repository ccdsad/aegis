from datetime import datetime, timezone

from app.domain.position import Position
from app.storage.models.positions import PositionRecord


class PositionsRepository:
    """In-memory repository for strategy positions."""

    def __init__(self) -> None:
        self._positions: dict[tuple[str, str], PositionRecord] = {}

    def upsert(self, position: Position) -> PositionRecord:
        key = (position.strategy_id, position.symbol)
        record = PositionRecord(
            strategy_id=position.strategy_id,
            symbol=position.symbol,
            quantity=position.quantity,
            average_price=position.average_price,
            realized_pnl=position.realized_pnl,
            unrealized_pnl=position.unrealized_pnl,
            updated_at=datetime.now(timezone.utc),
        )
        self._positions[key] = record
        return record

    def get(self, *, strategy_id: str, symbol: str) -> PositionRecord | None:
        return self._positions.get((strategy_id, symbol))
