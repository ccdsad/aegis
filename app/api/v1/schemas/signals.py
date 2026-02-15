from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.risk import RiskReason
from app.domain.signal import SignalSide, SignalType


class SignalIn(BaseModel):
    """Control-plane payload used to submit one strategy signal."""

    strategy_id: str
    symbol: str
    side: SignalSide
    signal_type: SignalType
    quantity: float = Field(gt=0)
    price_hint: float | None = Field(default=None, gt=0)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class ProcessSignalRequest(BaseModel):
    """Request envelope for decision-risk-runner orchestration."""

    signal: SignalIn
    market_state: dict[str, Any] = Field(default_factory=dict[str, Any])
    risk_state: dict[str, Any] = Field(default_factory=dict[str, Any])


class FillOut(BaseModel):
    """Serialized fill payload for API responses."""

    uid: UUID
    order_uid: UUID
    quantity: float
    price: float
    fee: float
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProcessSignalResponse(BaseModel):
    """Result of one signal processing request."""

    approved: bool
    reason: RiskReason
    message: str | None
    intent_uid: UUID
    fills: list[FillOut] = Field(default_factory=list[FillOut])
