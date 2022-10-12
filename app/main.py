from fastapi import FastAPI

from .routers import balance, transfers

app = FastAPI(title="WalletService", openapi_url=f"/api/v1/openapi.json")

app.include_router(transfers.router, prefix="/api/v1")
app.include_router(balance.router, prefix="/api/v1")
