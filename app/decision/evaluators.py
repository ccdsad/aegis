from collections.abc import Mapping
from typing import Any

from app.domain.signal import Signal


def evaluate_limit_price(
    signal: Signal,
    market_state: Mapping[str, Any],
) -> float | None:
    """Select deterministic limit price from market state for the signal symbol."""
    prices = market_state.get('prices')
    if not isinstance(prices, Mapping):
        return signal.price_hint

    symbol_price = prices.get(signal.symbol)
    if not isinstance(symbol_price, (float, int)):
        return signal.price_hint
    return float(symbol_price)
