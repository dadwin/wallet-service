from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.dependencies import get_db

router = APIRouter()


@router.get("/balance", response_model=schemas.AccountBalance)
def get_account_balance(db: Session = Depends(get_db)):
    pass
