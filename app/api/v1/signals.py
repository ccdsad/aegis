from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.api.v1.schemas.signals import (
    FillOut,
    ProcessSignalRequest,
    ProcessSignalResponse,
)
from app.core.config import Settings, get_settings
from app.core.lifecycle import Runtime, get_runtime
from app.domain.signal import Signal

router = APIRouter(prefix='/signals', tags=['signals'])


@router.post(
    '',
    response_model=ProcessSignalResponse,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
def process_signal(
    payload: ProcessSignalRequest,
    runtime: Runtime = Depends(get_runtime),
    settings: Settings = Depends(get_settings),
) -> ProcessSignalResponse:
    """Run one signal through decision, risk, and selected runner."""
    signal = Signal(
        strategy_id=payload.signal.strategy_id,
        symbol=payload.signal.symbol,
        side=payload.signal.side,
        signal_type=payload.signal.signal_type,
        quantity=payload.signal.quantity,
        price_hint=payload.signal.price_hint,
        confidence=payload.signal.confidence,
    )
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
            intent_uid=risk_result.intent.uid,
        )

    runner = runtime.get_runner(settings.mode)
    try:
        fills = runner.run(risk_result.intent)
    except NotImplementedError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Runner is not implemented for current mode.',
        ) from exc

    runtime.uow.orders.add_fills(intent_uid=risk_result.intent.uid, fills=fills)
    runtime.uow.commit()

    return ProcessSignalResponse(
        approved=True,
        reason=risk_result.reason,
        message=risk_result.message,
        intent_uid=risk_result.intent.uid,
        fills=[FillOut.model_validate(fill) for fill in fills],
    )
