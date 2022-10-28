from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import fin_models
from ...utils import oauth2
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/salaries', tags=['Salaries'])


@router.get('/', response_model=List[fin_schemas.SalaryRes])
def get_salaries(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    salaries = db.query(fin_models.Salary).order_by(
        fin_models.Salary.role_id).all()

    if not salaries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No salaries were found")
    return salaries


@router.get('/{id}', response_model=fin_schemas.SalaryRes)
def get_salary(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    salary = db.query(fin_models.Salary).filter(
        fin_models.Salary.id == id).first()
    if not salary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No salary with id: {id} was found")
    return salary


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.SalaryReq)
def create_salary(salary: fin_schemas.SalaryReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id > 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_salary = fin_models.Salary(**salary.dict())
    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)
    print(new_salary)
    return new_salary


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_salary(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        salary = db.query(fin_models.Salary).filter(
            fin_models.Salary.id == id)
        if not salary.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No salary with id: {id} was found!")
        salary.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_salary(id: int, updated_salary: fin_schemas.SalaryReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        salary = db.query(fin_models.Salary).filter(
            fin_models.Salary.id == id)
        if not salary.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No salary with id: {id} was not found")

        salary.update(updated_salary.dict(), synchronize_session=False)
        db.commit()
        return salary

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
