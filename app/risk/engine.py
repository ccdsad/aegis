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
        risk_result = RiskResult(
            intent=intent,
            status=RiskStatus.REJECTED,
            reason=RiskReason.OK,
            message=None,
            snapshots=snapshots,
        )

        if self._limits.kill_switch:
            risk_result.reason = RiskReason.KILL_SWITCH
            risk_result.message = 'Kill switch is active.'
            return risk_result

        if intent.symbol in self._limits.blocked_symbols:
            risk_result.reason = RiskReason.INSTRUMENT_BLOCKED
            risk_result.message = f'Symbol {intent.symbol} is blocked.'
            return risk_result

        if intent.quantity > self._limits.max_quantity:
            risk_result.reason = RiskReason.LIMIT_EXCEEDED
            risk_result.message = 'Quantity exceeds max_quantity.'
            return risk_result

        if snapshots['notional'] > self._limits.max_notional:
            risk_result.reason = RiskReason.LIMIT_EXCEEDED
            risk_result.message = 'Notional exceeds max_notional.'
            return risk_result

        if snapshots['drawdown'] > self._limits.max_drawdown:
            risk_result.reason = RiskReason.LIMIT_EXCEEDED
            risk_result.message = 'Drawdown exceeds max_drawdown.'
            return risk_result

        risk_result.status = RiskStatus.APPROVED
        risk_result.reason = RiskReason.OK
        risk_result.message = 'Intent approved by risk engine.'
        return risk_result
