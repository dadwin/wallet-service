from fastapi import FastAPI

from .routers import balance, transfers

app = FastAPI()

app.include_router(transfers.router)
app.include_router(balance.router)
