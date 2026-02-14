from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.lifecycle import Runtime, get_runtime
from app.domain.risk import RiskReason

router = APIRouter(prefix='/orders', tags=['orders'])


class IntentAuditOut(BaseModel):
    """Serialized intent audit state."""

    id: UUID
    signal_id: UUID
    strategy_id: str
    symbol: str
    quantity: float
    reason: RiskReason
    message: str
    status: str
    created_at: datetime
    updated_at: datetime


@router.get('/{intent_id}', response_model=IntentAuditOut)
def get_order_audit(
    intent_id: UUID,
    runtime: Runtime = Depends(get_runtime),
) -> IntentAuditOut:
    """Return stored audit information for one processed intent."""
    record = runtime.uow.orders.get_intent(intent_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Intent audit record not found.',
        )
    return IntentAuditOut(
        id=record.id,
        signal_id=record.signal_id,
        strategy_id=record.strategy_id,
        symbol=record.symbol,
        quantity=record.quantity,
        reason=record.reason,
        message=record.message,
        status=record.status.value,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )
