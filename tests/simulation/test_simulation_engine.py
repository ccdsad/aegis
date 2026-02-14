from uuid import uuid4

from app.domain.intent import Intent, IntentType
from app.domain.signal import SignalSide
from app.simulation.engine import SimulationEngine


class TestSimulationEngine:
    def test_run_returns_one_deterministic_fill(self) -> None:
        engine = SimulationEngine()
        intent = Intent(
            strategy_id='s1',
            signal_id=uuid4(),
            symbol='BTCUSDT',
            side=SignalSide.BUY,
            quantity=2.0,
            intent_type=IntentType.OPEN,
            limit_price=123.45,
        )

        fills = engine.run(intent)

        assert len(fills) == 1
        assert fills[0].order_id == intent.id
        assert fills[0].quantity == 2.0
        assert fills[0].price == 123.45
