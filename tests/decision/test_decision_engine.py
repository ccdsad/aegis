from app.decision.engine import DecisionEngine
from app.domain.signal import Signal, SignalSide, SignalType


class TestDecisionEngine:
    def test_decide_returns_deterministic_intent(self) -> None:
        engine = DecisionEngine()
        signal = Signal(
            strategy_id='s1',
            symbol='BTCUSDT',
            side=SignalSide.BUY,
            signal_type=SignalType.ENTRY,
            quantity=2.0,
            price_hint=10.0,
        )
        market_state = {'prices': {'BTCUSDT': 11.5}}

        intent = engine.decide(market_state, signal)

        assert intent.strategy_id == signal.strategy_id
        assert intent.signal_id == signal.id
        assert intent.quantity == signal.quantity
        assert intent.limit_price == 11.5
