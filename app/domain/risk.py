from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from app.domain.intent import Intent


class RiskStatus(StrEnum):
    """Final decision from risk evaluation."""

    APPROVED = 'approved'
    REJECTED = 'rejected'


class RiskReason(StrEnum):
    """Reason code attached to risk evaluation outcome."""

    OK = 'ok'
    LIMIT_EXCEEDED = 'limit_exceeded'
    KILL_SWITCH = 'kill_switch'
    INSTRUMENT_BLOCKED = 'instrument_blocked'
    INVALID_INTENT = 'invalid_intent'


@dataclass(slots=True, frozen=True, kw_only=True)
class RiskResult:
    """Risk-check output consumed by execution or simulation runner."""

    intent: Intent
    status: RiskStatus
    reason: RiskReason = RiskReason.OK
    message: str = ''
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    snapshots: dict[str, Any] = field(default_factory=dict[str, Any])

    @property
    def approved(self) -> bool:
        return self.status == RiskStatus.APPROVED
