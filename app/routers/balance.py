from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, services
from app.dependencies import get_db, get_user_by_token

router = APIRouter()


@router.get("/balance", response_model=schemas.AccountBalance)
def get_account_balance(db: Session = Depends(get_db),
                        user: str = Depends(get_user_by_token)):
    try:
        return services.get_account_balance_by_user(db, user)
    except services.NoUserAccountError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
