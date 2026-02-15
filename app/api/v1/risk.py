from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.api.v1.schemas.risk import RiskDecisionOut
from app.core.lifecycle import Runtime, get_runtime

router = APIRouter(prefix='/risk', tags=['risk'])


@router.get(
    '/decisions/{intent_uid}',
    response_model=RiskDecisionOut,
    response_class=ORJSONResponse,
)
def get_risk_decision(
    intent_uid: UUID,
    runtime: Runtime = Depends(get_runtime),
) -> RiskDecisionOut:
    """Return last stored risk decision for a processed intent."""
    record = runtime.uow.orders.get_intent(intent_uid)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Risk decision not found.',
        )
    return RiskDecisionOut(
        intent_uid=record.uid,
        reason=record.reason,
        message=record.message,
        status=record.status.value,
        updated_at=record.updated_at,
    )
