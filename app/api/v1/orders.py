from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse

from app.api.v1.schemas.orders import IntentAuditOut
from app.core.lifecycle import Runtime, get_runtime

router = APIRouter(prefix='/orders', tags=['orders'])


@router.get(
    '/{intent_uid}',
    response_model=IntentAuditOut,
    response_class=ORJSONResponse,
)
def get_order_audit(
    intent_uid: UUID,
    runtime: Runtime = Depends(get_runtime),
) -> IntentAuditOut:
    """Return stored audit information for one processed intent."""
    record = runtime.uow.orders.get_intent(intent_uid)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Intent audit record not found.',
        )
    return IntentAuditOut(
        uid=record.uid,
        signal_uid=record.signal_uid,
        strategy_id=record.strategy_id,
        symbol=record.symbol,
        quantity=record.quantity,
        reason=record.reason,
        message=record.message,
        status=record.status.value,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )
