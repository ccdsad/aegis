from app.domain.intent import IntentType
from app.domain.signal import Signal, SignalType


def signal_to_intent_type(signal: Signal) -> IntentType:
    """Map incoming signal type to the canonical intent type."""
    if signal.signal_type == SignalType.ENTRY:
        return IntentType.OPEN
    if signal.signal_type == SignalType.EXIT:
        return IntentType.CLOSE
    return IntentType.ADJUST


def validate_signal(signal: Signal) -> None:
    """Validate signal invariants required by the decision pipeline."""
    if signal.quantity <= 0:
        raise ValueError('Signal quantity must be greater than zero.')
