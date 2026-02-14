from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, kw_only=True)
class RiskLimits:
    """Static limits applied by the risk engine."""

    max_quantity: float = 1_000.0
    max_notional: float = 1_000_000.0
    max_drawdown: float = 0.20
    kill_switch: bool = False
    blocked_symbols: set[str] = field(default_factory=set[str])
