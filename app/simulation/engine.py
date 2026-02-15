from app.domain.intent import Intent
from app.domain.order import Fill
from app.simulation.fills import build_full_fill
from app.simulation.latency import LatencyModel


class SimulationEngine:
    """Paper-trading runner that produces deterministic simulated fills."""

    def __init__(self, latency: LatencyModel | None = None) -> None:
        self._latency = latency or LatencyModel()

    @property
    def latency(self) -> LatencyModel:
        """Expose simulation latency profile for observability."""
        return self._latency

    def run(self, intent: Intent) -> list[Fill]:
        """Execute an approved intent in simulation mode."""
        return [build_full_fill(intent)]
