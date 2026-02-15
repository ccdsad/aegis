# USECASES

This document defines key product and architecture scenarios for the algorithmic trading system.
Goal: specify how `decision`, `risk`, `execution`, `simulation`, `ingest`, and `storage` should behave under real operating conditions.

Base pipeline:

1. `intent = decision_engine.decide(market_state)`
2. `risk_result = risk_engine.check(intent, state)`
3. If `risk_result.approved == false` -> stop execution
4. `runner = simulator if mode == PAPER else executor`
5. `runner.run(risk_result.intent)`

## 1) Live Trading with Risk Gating

**Scenario**
- Strategy produces a signal.
- `decision engine` builds an `intent`.
- `risk engine` validates limits and portfolio state.
- `execution` sends orders to the market.

**Why it is hard**
- Race conditions between market-state updates and intent processing.
- Partial fills causing `position/order` state drift.
- Limits must be evaluated in real time before order submission.

**Definition of done**
- No order is submitted without explicit `risk approval`.
- All execution events are persisted in `storage` and emitted to metrics.
- Behavior is deterministic for identical input streams.

## 2) Paper Trading with No Logic Changes

**Scenario**
- Same strategy.
- Same `decision/risk` pipeline.
- Only routing changes: `execution` -> `simulation`.

**Why it matters**
- Zero domain-logic changes between PAPER and REAL modes.
- Fair strategy validation on identical rules.
- Fast regression detection.

**Definition of done**
- Mode switch changes only the `runner` selection.
- Input `intent` values are identical for PAPER and REAL under the same `market_state`.
- PAPER vs REAL comparison metrics are available.

## 3) Real-Time Risk Kill Switch

**Scenario**
- PnL drops.
- Drawdown threshold is exceeded.
- `risk engine` activates kill switch and blocks all new intents.
- `execution` is no longer called.

**Why it is hard**
- Asynchrony: drawdown events and new signals can arrive at the same time.
- State consistency under concurrent processing.
- Protection against "one bad tick" false triggers.

**Definition of done**
- Kill switch activation is atomic.
- After activation, all new intents are consistently rejected.
- Deactivation requires explicit operational action.

## 4) Market Replay (Time Travel)

**Scenario**
- Replay historical market data for a past session.
- `decision engine` behaves as if data were live.
- `simulation` computes fills and PnL.

**Why it matters**
- Determinism and reproducibility.
- Faster bug isolation.
- Objective strategy change validation.

**Definition of done**
- Re-running the same dataset produces identical outcomes.
- Pause/seek/restart works without losing consistency.
- PnL, fill-rate, and drawdown reports are generated automatically.

## 5) Partial Execution and Retries

**Scenario**
- `intent` is approved.
- `execution` submits multiple orders.
- One order fills, one is partial, one fails.
- State is updated correctly without duplicates.

**Why it is hard**
- Idempotency under retries.
- Exactly-once semantics at the boundary: signal -> order -> execution facts.
- Crash recovery mid-flow.

**Definition of done**
- Reprocessing the same event does not duplicate position changes.
- Retry is safe and bounded by policy.
- `orders/positions` state converges to exchange reality.

## 6) Multiple Strategies with Shared Risk Budget

**Scenario**
- Multiple strategies run in parallel.
- They share one risk budget.
- An aggressive strategy can consume budget and block others.

**Why it is hard**
- Fair scheduling across strategies.
- Starvation of lower-priority strategies.
- Priority and quota policy design.

**Definition of done**
- Transparent risk allocation policy (quota/priority).
- Observability shows who consumed budget and why.
- Guaranteed minimum throughput for critical strategies.

## 7) Hot Config Update (No Restart)

**Scenario**
- Risk limits and related parameters are updated.
- Changes are applied at runtime.
- New config affects `decision -> risk` flow immediately.

**Why it matters**
- Governance and production risk control.
- Operational maturity without downtime.

**Definition of done**
- Configuration is versioned and auditable.
- Update is atomically applied after validation.
- Rollback to a previous config version is supported.

## 8) Incident Recovery

**Scenario**
- A service crashes.
- On restart:
- state is restored from `storage`,
- duplicate orders are prevented,
- `decision` does not replay already-processed actions.

**Why this is a mature scenario**
- Covers real incidents, not only happy paths.
- Validates reliability of recovery protocols.

**Definition of done**
- Recovery runbook is documented.
- Event-log replay is safe and idempotent.
- Health/readiness checks and degradation alerts are in place.

## Non-Functional Requirements (for all scenarios)

- Observability: structured logs, metrics, tracing.
- Auditability: explicit reason for every `risk approve/reject` decision.
- Idempotency: operation keys and deduplication controls.
- Time discipline: consistent timestamp model and timezone policy.
- Testability: scenarios are reproducible in integration/E2E environments.
