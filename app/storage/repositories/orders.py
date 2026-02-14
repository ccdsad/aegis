from datetime import datetime, timezone
from uuid import UUID

from app.domain.intent import Intent
from app.domain.order import Fill
from app.domain.risk import RiskReason, RiskResult
from app.domain.signal import Signal
from app.storage.models.orders import FillRecord, IntentRecord, ProcessingStatus


class OrdersRepository:
    """In-memory repository for intent and fill audit records."""

    def __init__(self) -> None:
        self._intents: dict[UUID, IntentRecord] = {}
        self._fills: dict[UUID, FillRecord] = {}

    def upsert_intent_audit(
        self,
        *,
        signal: Signal,
        intent: Intent,
        risk_result: RiskResult,
    ) -> IntentRecord:
        now = datetime.now(timezone.utc)
        status = (
            ProcessingStatus.APPROVED
            if risk_result.approved
            else ProcessingStatus.REJECTED
        )
        existing = self._intents.get(intent.uid)

        record = IntentRecord(
            uid=intent.uid,
            signal_uid=signal.uid,
            strategy_id=intent.strategy_id,
            symbol=intent.symbol,
            side=intent.side,
            signal_type=signal.signal_type,
            intent_type=intent.intent_type,
            quantity=intent.quantity,
            status=status,
            reason=risk_result.reason,
            message=risk_result.message,
            limit_price=intent.limit_price,
            created_at=existing.created_at if existing else now,
            updated_at=now,
        )
        self._intents[intent.uid] = record
        return record

    def add_fills(self, *, intent_uid: UUID, fills: list[Fill]) -> list[FillRecord]:
        records: list[FillRecord] = []
        for fill in fills:
            record = FillRecord(
                uid=fill.uid,
                intent_uid=intent_uid,
                order_uid=fill.order_uid,
                quantity=fill.quantity,
                price=fill.price,
                fee=fill.fee,
                occurred_at=fill.occurred_at,
            )
            self._fills[fill.uid] = record
            records.append(record)
        return records

    def get_intent(self, intent_uid: UUID) -> IntentRecord | None:
        return self._intents.get(intent_uid)

    def list_fills_for_intent(self, intent_uid: UUID) -> list[FillRecord]:
        return [fill for fill in self._fills.values() if fill.intent_uid == intent_uid]

    def get_intent_risk_reason(self, intent_uid: UUID) -> RiskReason | None:
        record = self._intents.get(intent_uid)
        if record is None:
            return None
        return record.reason
