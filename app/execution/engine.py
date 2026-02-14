from app.domain.intent import Intent
from app.domain.order import Fill


class ExecutionEngine:
    """Real-execution runner interface placeholder."""

    def run(self, intent: Intent) -> list[Fill]:
        """Execute an approved intent in real mode."""
        raise NotImplementedError('Real execution is not implemented yet.')
