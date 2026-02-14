from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class StrategyStatus(StrEnum):
    """Lifecycle status of a strategy configuration."""

    ACTIVE = 'active'
    PAUSED = 'paused'
    DISABLED = 'disabled'


@dataclass(kw_only=True)
class StrategyConfig:
    """Declarative strategy configuration used by decision and risk modules."""

    id: str
    name: str
    status: StrategyStatus = StrategyStatus.ACTIVE
    version: int = 1
    params: dict[str, Any] = field(default_factory=dict[str, Any])


@dataclass(slots=True, frozen=True, kw_only=True)
class StrategySnapshot:
    """Runtime strategy state snapshot for control-plane and auditing flows."""

    id: str
    enabled: bool
    status: StrategyStatus
    version: int
