from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import fin_models
from ...utils import oauth2
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/wages', tags=['Wages'])


@router.get('/', response_model=List[fin_schemas.WageRes])
def get_wages(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    wages = db.query(fin_models.Wage).order_by(
        fin_models.Wage.role_id).all()

    if not wages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No wages were found")
    return wages


@router.get('/{id}', response_model=fin_schemas.WageRes)
def get_wage(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    wage = db.query(fin_models.Wage).filter(
        fin_models.Wage.id == id).first()
    if not wage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No wage with id: {id} was found")
    return wage


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.WageRes)
def create_wage(wage: fin_schemas.WageReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id > 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_wage = fin_models.Wage(**wage.dict())
    db.add(new_wage)
    db.commit()
    db.refresh(new_wage)
    print(new_wage)
    return new_wage


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wage(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        wage = db.query(fin_models.Wage).filter(
            fin_models.Wage.id == id)
        if not wage.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No wage with id: {id} was found!")
        wage.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_wage(id: int, updated_wage: fin_schemas.WageReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        wage = db.query(fin_models.Wage).filter(
            fin_models.Wage.id == id)
        if not wage.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No wage with id: {id} was not found")

        wage.update(updated_wage.dict(), synchronize_session=False)
        db.commit()
        return wage

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
