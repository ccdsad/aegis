from types import TracebackType
from typing import Literal

from app.storage.repositories.orders import OrdersRepository
from app.storage.repositories.positions import PositionsRepository


class UnitOfWork:
    """Minimal unit-of-work abstraction for storage access boundaries."""

    def __init__(self) -> None:
        self.orders = OrdersRepository()
        self.positions = PositionsRepository()

    def __enter__(self) -> 'UnitOfWork':
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> Literal[False]:
        if exc is not None:
            self.rollback()
        return False

    def commit(self) -> None:
        """Commit transaction boundary (no-op for in-memory storage)."""

    def rollback(self) -> None:
        """Rollback transaction boundary (no-op for in-memory storage)."""
