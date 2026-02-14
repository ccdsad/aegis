from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.core.config import Settings, get_settings
from app.core.lifecycle import Runtime, get_runtime
from app.domain.order import Fill
from app.domain.risk import RiskReason
from app.domain.signal import Signal, SignalSide, SignalType

router = APIRouter(prefix='/signals', tags=['signals'])


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

    id: UUID
    order_id: UUID
    quantity: float
    price: float
    fee: float
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProcessSignalResponse(BaseModel):
    """Result of one signal processing request."""

    approved: bool
    reason: RiskReason
    message: str
    intent_id: UUID
    fills: list[FillOut] = Field(default_factory=list[FillOut])


def _to_domain_signal(signal_in: SignalIn) -> Signal:
    return Signal(
        strategy_id=signal_in.strategy_id,
        symbol=signal_in.symbol,
        side=signal_in.side,
        signal_type=signal_in.signal_type,
        quantity=signal_in.quantity,
        price_hint=signal_in.price_hint,
        confidence=signal_in.confidence,
    )


def _to_fill_out(fill: Fill) -> FillOut:
    return FillOut.model_validate(fill)


@router.post('', response_model=ProcessSignalResponse, status_code=status.HTTP_200_OK)
def process_signal(
    payload: ProcessSignalRequest,
    runtime: Runtime = Depends(get_runtime),
    settings: Settings = Depends(get_settings),
) -> ProcessSignalResponse:
    """Run one signal through decision, risk, and selected runner."""
    signal = _to_domain_signal(payload.signal)
    intent = runtime.decision_engine.decide(payload.market_state, signal)
    risk_result = runtime.risk_engine.check(intent, payload.risk_state)

    runtime.uow.orders.upsert_intent_audit(
        signal=signal,
        intent=intent,
        risk_result=risk_result,
    )

    if not risk_result.approved:
        runtime.uow.commit()
        return ProcessSignalResponse(
            approved=False,
            reason=risk_result.reason,
            message=risk_result.message,
            intent_id=risk_result.intent.id,
        )

    runner = runtime.get_runner(settings.mode)
    try:
        fills = runner.run(risk_result.intent)
    except NotImplementedError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Runner is not implemented for current mode.',
        ) from exc

    runtime.uow.orders.add_fills(intent_id=risk_result.intent.id, fills=fills)
    runtime.uow.commit()

    return ProcessSignalResponse(
        approved=True,
        reason=risk_result.reason,
        message=risk_result.message,
        intent_id=risk_result.intent.id,
        fills=[_to_fill_out(fill) for fill in fills],
    )
