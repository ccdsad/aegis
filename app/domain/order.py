from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from app.domain.signal import SignalSide


class OrderType(StrEnum):
    """Execution order type."""

    MARKET = 'market'
    LIMIT = 'limit'


class TimeInForce(StrEnum):
    """Exchange time-in-force policy."""

    GTC = 'gtc'
    IOC = 'ioc'
    FOK = 'fok'


class OrderStatus(StrEnum):
    """Order lifecycle state."""

    NEW = 'new'
    SUBMITTED = 'submitted'
    PARTIALLY_FILLED = 'partially_filled'
    FILLED = 'filled'
    CANCELED = 'canceled'
    REJECTED = 'rejected'
    FAILED = 'failed'


@dataclass(kw_only=True)
class Order:
    """Executable order created from an approved intent."""

    id: UUID = field(default_factory=uuid4)
    intent_id: UUID
    symbol: str
    side: SignalSide
    quantity: float
    order_type: OrderType = OrderType.MARKET
    tif: TimeInForce = TimeInForce.GTC
    limit_price: float | None = None
    status: OrderStatus = OrderStatus.NEW
    filled_quantity: float = 0.0
    average_fill_price: float | None = None
    external_order_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True, frozen=True, kw_only=True)
class Fill:
    """Execution fill fact produced by simulation or live execution."""

    id: UUID = field(default_factory=uuid4)
    order_id: UUID
    quantity: float
    price: float
    fee: float = 0.0
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
