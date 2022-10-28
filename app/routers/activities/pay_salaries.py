from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import fin_models
from ...utils import oauth2
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/salaries/payments', tags=['Salary Payments'])


@router.get('/', response_model=List[fin_schemas.PaySalaryRes])
def get_salary_payments(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if current_user.role_id < 3:
        salaries = db.query(fin_models.PaySalary).order_by(
            fin_models.PaySalary.date).all()

        if not salaries:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No salary payments were found")
        return salaries

    elif current_user:
        salaries = db.query(fin_models.PaySalary).filter(fin_models.PaySalary.staff_id == current_user.id).order_by(
            fin_models.PaySalary.date)
        if not salaries:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No salary payment was found with you as the recipient")
        return salaries

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")


@router.get('/{id}', response_model=fin_schemas.PaySalaryRes)
def get_salary_payment(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        salary = db.query(fin_models.PaySalary).filter(
            fin_models.PaySalary.id == id).first()
        if not salary:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No salary payment with id: {id} was found")
        return salary

    elif current_user:
        salary = db.query(fin_models.PaySalary).filter(
            fin_models.PaySalary.id == id, fin_models.PaySalary.staff_id == current_user.id).first()
        if not salary:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No salary payment with id: {id} was found")
        return salary

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.PaySalaryReq)
def create_salary_payment(paid_salary: fin_schemas.PaySalaryReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id >= 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_salary_payment = fin_models.PaySalary(
        **paid_salary.dict())
    db.add(new_salary_payment)
    db.commit()
    db.refresh(new_salary_payment)
    print(new_salary_payment)
    return new_salary_payment


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_salary_payment(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id < 3:
        salary = db.query(fin_models.PaySalary).filter(
            fin_models.PaySalary.id == id)
        if not salary.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No salary payment with id: {id} was found!")
        salary.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_salary_payment(id: int, paid_salary: fin_schemas.PaySalaryReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        salary = db.query(fin_models.PaySalary).filter(
            fin_models.PaySalary.id == id)
        if not salary.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No salary payment with id: {id} was not found")

        salary.update(paid_salary.dict(), synchronize_session=False)
        db.commit()
        return salary

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
