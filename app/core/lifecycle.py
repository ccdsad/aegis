from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Protocol, cast

from fastapi import FastAPI, Request

from app.core.config import AppMode
from app.decision.engine import DecisionEngine
from app.domain.intent import Intent
from app.domain.order import Fill
from app.execution.engine import ExecutionEngine
from app.risk.engine import RiskEngine
from app.simulation.engine import SimulationEngine
from app.storage.unit_of_work import UnitOfWork


class Runner(Protocol):
    """Runner contract shared by simulation and real execution engines."""

    def run(self, intent: Intent) -> list[Fill]:
        """Execute one approved intent and return resulting fills."""


@dataclass(slots=True)
class Runtime:
    """Runtime service container initialized during application startup."""

    decision_engine: DecisionEngine
    risk_engine: RiskEngine
    simulation_engine: SimulationEngine
    execution_engine: ExecutionEngine
    uow: UnitOfWork

    def get_runner(self, mode: AppMode) -> Runner:
        """Select execution runner according to application mode."""
        if mode == AppMode.PAPER:
            return self.simulation_engine
        return self.execution_engine


def build_runtime() -> Runtime:
    """Construct engine instances used by the request pipeline."""
    return Runtime(
        decision_engine=DecisionEngine(),
        risk_engine=RiskEngine(),
        simulation_engine=SimulationEngine(),
        execution_engine=ExecutionEngine(),
        uow=UnitOfWork(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize and expose runtime dependencies through app state."""
    app.state.runtime = build_runtime()
    yield


def get_runtime(request: Request) -> Runtime:
    """Resolve runtime container from FastAPI app state."""
    runtime = getattr(request.app.state, 'runtime', None)
    if runtime is None:
        raise RuntimeError('Runtime is not initialized.')
    return cast(Runtime, runtime)
