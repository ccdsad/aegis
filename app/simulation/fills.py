from app.domain.intent import Intent
from app.domain.order import Fill


def build_full_fill(intent: Intent) -> Fill:
    """Build a deterministic one-shot fill for paper mode."""
    fill_price = intent.limit_price if intent.limit_price is not None else 0.0
    return Fill(
        order_id=intent.id,
        quantity=intent.quantity,
        price=fill_price,
    )
