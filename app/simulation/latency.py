from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class LatencyModel:
    """Deterministic latency profile for simulation mode."""

    decision_ms: int = 1
    risk_ms: int = 1
    execution_ms: int = 2

    @property
    def total_ms(self) -> int:
        return self.decision_ms + self.risk_ms + self.execution_ms
