from uuid import uuid4

from app.domain.intent import Intent, IntentType
from app.domain.signal import SignalSide
from app.domain.risk import RiskReason, RiskStatus
from app.risk.engine import RiskEngine
from app.risk.limits import RiskLimits


class TestRiskEngine:
    def test_check_rejects_when_quantity_limit_exceeded(self) -> None:
        engine = RiskEngine(limits=RiskLimits(max_quantity=1.0))
        intent = Intent(
            strategy_id='s1',
            signal_uid=uuid4(),
            symbol='BTCUSDT',
            side=SignalSide.BUY,
            quantity=2.0,
            intent_type=IntentType.OPEN,
            limit_price=100.0,
        )

        result = engine.check(intent, state={})

        assert result.status == RiskStatus.REJECTED
        assert result.reason == RiskReason.LIMIT_EXCEEDED

    def test_check_approves_valid_intent(self) -> None:
        engine = RiskEngine(limits=RiskLimits(max_quantity=10.0, max_notional=1_000.0))
        intent = Intent(
            strategy_id='s1',
            signal_uid=uuid4(),
            symbol='BTCUSDT',
            side=SignalSide.BUY,
            quantity=2.0,
            intent_type=IntentType.OPEN,
            limit_price=100.0,
        )

        result = engine.check(intent, state={'drawdown': 0.05})

        assert result.status == RiskStatus.APPROVED
        assert result.reason == RiskReason.OK
