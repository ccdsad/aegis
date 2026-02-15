from collections.abc import Mapping
from typing import Any

from app.domain.intent import Intent


def estimate_notional(intent: Intent) -> float:
    """Estimate notional from intent quantity and available limit price."""
    if intent.limit_price is None:
        return 0.0
    return intent.quantity * intent.limit_price


def extract_drawdown(state: Mapping[str, Any]) -> float:
    """Read current drawdown from risk state with a safe default."""
    raw_drawdown = state.get('drawdown', 0.0)
    if isinstance(raw_drawdown, (float, int)):
        return float(raw_drawdown)
    return 0.0
