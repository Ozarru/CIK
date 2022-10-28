from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import fin_models
from ...utils import oauth2
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/insurances', tags=['Insurances'])


@router.get('/', response_model=List[fin_schemas.InsuranceRes])
def get_insurances(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    insurances = db.query(fin_models.Insurance).order_by(
        fin_models.Insurance.name).all()

    if not insurances:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No insurances were found")
    return insurances


@router.get('/{id}', response_model=fin_schemas.InsuranceRes.update_forward_refs())
def get_insurance(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    insurance = db.query(fin_models.Insurance).filter(
        fin_models.Insurance.id == id).first()
    if not insurance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No insurance with id: {id} was found")
    return insurance


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.Insurance)
def create_insurance(insurance: fin_schemas.Insurance, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id > 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_insurance = fin_models.Insurance(**insurance.dict())
    db.add(new_insurance)
    db.commit()
    db.refresh(new_insurance)
    print(new_insurance)
    return new_insurance


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_insurance(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        insurance = db.query(fin_models.Insurance).filter(
            fin_models.Insurance.id == id)
        if not insurance.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No insurance with id: {id} was found!")
        insurance.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_insurance(id: int, updated_insurance: fin_schemas.Insurance, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        insurance = db.query(fin_models.Insurance).filter(
            fin_models.Insurance.id == id)
        if not insurance.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No insurance with id: {id} was not found")

        insurance.update(updated_insurance.dict(), synchronize_session=False)
        db.commit()
        return insurance

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
