from fastapi import FastAPI

from app.api.v1.orders import router as orders_router
from app.api.v1.risk import router as risk_router
from app.api.v1.signals import router as signals_router
from app.api.v1.strategies import router as strategies_router
from app.core.lifecycle import lifespan

api_v1_prefix = '/api/v1'

app = FastAPI(
    title='Aegis',
    version='0.1.0',
    lifespan=lifespan,
)

app.include_router(signals_router, prefix=api_v1_prefix)
app.include_router(orders_router, prefix=api_v1_prefix)
app.include_router(risk_router, prefix=api_v1_prefix)
app.include_router(strategies_router, prefix=api_v1_prefix)
