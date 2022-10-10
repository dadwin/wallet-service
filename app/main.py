from fastapi import Depends, FastAPI

from .dependencies import get_query_token
from .routers import balance, transfers

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(transfers.router)
app.include_router(balance.router)
