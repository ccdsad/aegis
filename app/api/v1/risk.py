from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.lifecycle import Runtime, get_runtime
from app.domain.risk import RiskReason

router = APIRouter(prefix='/risk', tags=['risk'])


class RiskDecisionOut(BaseModel):
    """Serialized risk decision details for one intent."""

    intent_id: UUID
    reason: RiskReason
    message: str
    status: str
    updated_at: datetime


@router.get('/decisions/{intent_id}', response_model=RiskDecisionOut)
def get_risk_decision(
    intent_id: UUID,
    runtime: Runtime = Depends(get_runtime),
) -> RiskDecisionOut:
    """Return last stored risk decision for a processed intent."""
    record = runtime.uow.orders.get_intent(intent_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Risk decision not found.',
        )
    return RiskDecisionOut(
        intent_id=record.id,
        reason=record.reason,
        message=record.message,
        status=record.status.value,
        updated_at=record.updated_at,
    )
