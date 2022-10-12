from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, services
from app.dependencies import get_db, get_user_by_token

router = APIRouter()


@router.get("/transfers/", response_model=List[schemas.TransferInfo])
def get_transfers(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db),
                  user: str = Depends(get_user_by_token)):
    try:
        return services.get_transfers(db, user, skip, limit)
    except services.NoUserAccountError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.post("/transfers/", response_model=schemas.TransferInfo)
def create_transfer(cmd: schemas.TransferCommand,
                    db: Session = Depends(get_db),
                    user: str = Depends(get_user_by_token)
                    ):
    try:
        return services.create_transfer(db, user, cmd)
    except services.ErrorBase as ex:
        raise HTTPException(status_code=400, detail=str(ex))
