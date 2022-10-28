from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import fin_models
from ...utils import oauth2
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/wages/payments', tags=['Wages Payments'])


@router.get('/', response_model=List[fin_schemas.PayWageRes])
def get_wage_payments(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if current_user.role_id < 3:
        wages = db.query(fin_models.PayWage).order_by(
            fin_models.PayWage.date).all()

        if not wages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No wages were found")
        return wages

    elif current_user:
        wages = db.query(fin_models.PayWage).filter(fin_models.PayWage.staff_id == current_user.id).order_by(
            fin_models.PayWage.date)
        if not wages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No wage payment was found with you as the recipient")
        return wages

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")


@router.get('/{id}', response_model=fin_schemas.PayWageRes)
def get_wage_payment(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        wage = db.query(fin_models.PayWage).filter(
            fin_models.PayWage.id == id).first()
        if not wage:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No wage payment with id: {id} was found")
        return wage

    elif current_user:
        wage = db.query(fin_models.PayWage).filter(
            fin_models.PayWage.id == id, fin_models.PayWage.staff_id == current_user.id).first()
        if not wage:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No wage payment with id: {id} was found")
        return wage

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.PayWageReq)
def create_wage_payment(paid_wage: fin_schemas.PayWageReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id >= 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_wage_payment = fin_models.PayWage(
        **paid_wage.dict())
    db.add(new_wage_payment)
    db.commit()
    db.refresh(new_wage_payment)
    print(new_wage_payment)
    return new_wage_payment


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wage_payment(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id < 3:
        wage = db.query(fin_models.PayWage).filter(
            fin_models.PayWage.id == id)
        if not wage.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No wage payment with id: {id} was found!")
        wage.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_wage_payment(id: int, paid_wage: fin_schemas.PayWageReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        wage = db.query(fin_models.PayWage).filter(
            fin_models.PayWage.id == id)
        if not wage.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No wage payment with id: {id} was not found")

        wage.update(paid_wage.dict(), synchronize_session=False)
        db.commit()
        return wage

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
