from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...utils import oauth2
from ...models import fin_models
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/patients_cash_transactions',
                   tags=['Patient Cash Transactions'])


@router.get('/', response_model=List[fin_schemas.PatientCashTransaction])
def get_transactions(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_transactions(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    transactions = db.query(fin_models.PatientCashTransaction).order_by(
        fin_models.PatientCashTransaction.date).all()

    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No transactions were found")
    return transactions


@router.get('/{id}', response_model=fin_schemas.PatientCashTransaction.update_forward_refs())
def get_transaction(id: int, db: Session = Depends(get_db),):
    # def get_transaction(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    transaction = db.query(fin_models.PatientCashTransaction).filter(
        fin_models.PatientCashTransaction.id == id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No transaction with id: {id} was found")
    return transaction


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.PatientCashTransaction)
def create_transaction(transaction: fin_schemas.PatientCashTransaction, db: Session = Depends(get_db), ):
    # def create_transaction(transaction: fin_schemas.PatientCashTransaction, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_transaction = fin_models.PatientCashTransaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    print(new_transaction)
    return new_transaction


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        transaction = db.query(fin_models.PatientCashTransaction).filter(
            fin_models.PatientCashTransaction.id == id)
        if not transaction.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No transaction with id: {id} was found!")
        transaction.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_transaction(id: int, updated_transaction: fin_schemas.PatientCashTransaction, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        transaction = db.query(fin_models.PatientCashTransaction).filter(
            fin_models.PatientCashTransaction.id == id)
        if not transaction.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No transaction with id: {id} was not found")

        transaction.update(updated_transaction.dict(),
                           synchronize_session=False)
        db.commit()
        return transaction

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
