from collections.abc import Mapping
from typing import Any

from app.domain.intent import Intent
from app.domain.risk import RiskReason, RiskResult, RiskStatus
from app.risk.limits import RiskLimits
from app.risk.projection import estimate_notional, extract_drawdown


class RiskEngine:
    """Validate intents against portfolio and governance limits."""

    def __init__(self, limits: RiskLimits | None = None) -> None:
        self._limits = limits or RiskLimits()

    def check(self, intent: Intent, state: Mapping[str, Any]) -> RiskResult:
        """Approve or reject an intent according to configured limits."""
        snapshots: dict[str, Any] = {
            'quantity': intent.quantity,
            'notional': estimate_notional(intent),
            'drawdown': extract_drawdown(state),
            'symbol': intent.symbol,
        }

        if self._limits.kill_switch:
            return RiskResult(
                intent=intent,
                status=RiskStatus.REJECTED,
                reason=RiskReason.KILL_SWITCH,
                message='Kill switch is active.',
                snapshots=snapshots,
            )

        if intent.symbol in self._limits.blocked_symbols:
            return RiskResult(
                intent=intent,
                status=RiskStatus.REJECTED,
                reason=RiskReason.INSTRUMENT_BLOCKED,
                message=f'Symbol {intent.symbol} is blocked.',
                snapshots=snapshots,
            )

        if intent.quantity > self._limits.max_quantity:
            return RiskResult(
                intent=intent,
                status=RiskStatus.REJECTED,
                reason=RiskReason.LIMIT_EXCEEDED,
                message='Quantity exceeds max_quantity.',
                snapshots=snapshots,
            )

        if snapshots['notional'] > self._limits.max_notional:
            return RiskResult(
                intent=intent,
                status=RiskStatus.REJECTED,
                reason=RiskReason.LIMIT_EXCEEDED,
                message='Notional exceeds max_notional.',
                snapshots=snapshots,
            )

        if snapshots['drawdown'] > self._limits.max_drawdown:
            return RiskResult(
                intent=intent,
                status=RiskStatus.REJECTED,
                reason=RiskReason.LIMIT_EXCEEDED,
                message='Drawdown exceeds max_drawdown.',
                snapshots=snapshots,
            )

        return RiskResult(
            intent=intent,
            status=RiskStatus.APPROVED,
            reason=RiskReason.OK,
            message='Intent approved by risk engine.',
            snapshots=snapshots,
        )
