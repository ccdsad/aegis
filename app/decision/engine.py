from collections.abc import Mapping
from typing import Any

from app.decision.evaluators import evaluate_limit_price
from app.decision.rules import signal_to_intent_type, validate_signal
from app.domain.intent import Intent
from app.domain.signal import Signal


class DecisionEngine:
    """Build execution intents from validated strategy signals."""

    def decide(self, market_state: Mapping[str, Any], signal: Signal) -> Intent:
        """Create a deterministic intent from a signal and current market state."""
        validate_signal(signal)
        intent_type = signal_to_intent_type(signal)
        limit_price = evaluate_limit_price(signal, market_state)
        return Intent.from_signal(
            signal,
            intent_type=intent_type,
            limit_price=limit_price,
        )
