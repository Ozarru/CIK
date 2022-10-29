from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import fin_models
from ...utils import oauth2
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/bills', tags=['Bills'])


@router.get('/', response_model=List[fin_schemas.BillRes])
def get_bills(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    bills = db.query(fin_models.Bill).order_by(
        fin_models.Bill.date_issued).all()

    if not bills:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No bills were found")
    return bills


@router.get('/{id}', response_model=fin_schemas.BillRes)
def get_bill(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    bill = db.query(fin_models.Bill).filter(
        fin_models.Bill.id == id).first()
    if not bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No bill with id: {id} was found")
    return bill


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.BillRes)
def create_bill(bill: fin_schemas.BillReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id > 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_bill = fin_models.Bill(**bill.dict())
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    print(new_bill)
    return new_bill


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        bill = db.query(fin_models.Bill).filter(
            fin_models.Bill.id == id)
        if not bill.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No bill with id: {id} was found!")
        bill.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_bill(id: int, updated_bill: fin_schemas.BillReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        bill = db.query(fin_models.Bill).filter(
            fin_models.Bill.id == id)
        if not bill.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No bill with id: {id} was not found")

        bill.update(updated_bill.dict(), synchronize_session=False)
        db.commit()
        return bill

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
