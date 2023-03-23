from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...utils import oauth2
from ...models import fin_models
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/comodities', tags=['Comodities'])


@router.get('/', response_model=List[fin_schemas.Comodity])
def get_comodities(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_comodities(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    comodities = db.query(fin_models.Comodity).order_by(
        fin_models.Comodity.name).all()

    if not comodities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No comodities were found")
    return comodities


@router.get('/{id}', response_model=fin_schemas.Comodity.update_forward_refs())
def get_comodity(id: int, db: Session = Depends(get_db),):
    # def get_comodity(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    comodity = db.query(fin_models.Comodity).filter(
        fin_models.Comodity.id == id).first()
    if not comodity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No comodity with id: {id} was found")
    return comodity


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.Comodity)
def create_comodity(comodity: fin_schemas.Comodity, db: Session = Depends(get_db), ):
    # def create_comodity(comodity: fin_schemas.Comodity, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_comodity = fin_models.Comodity(**comodity.dict())
    db.add(new_comodity)
    db.commit()
    db.refresh(new_comodity)
    print(new_comodity)
    return new_comodity


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comodity(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        comodity = db.query(fin_models.Comodity).filter(
            fin_models.Comodity.id == id)
        if not comodity.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No comodity with id: {id} was found!")
        comodity.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_comodity(id: int, updated_comodity: fin_schemas.Comodity, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        comodity = db.query(fin_models.Comodity).filter(
            fin_models.Comodity.id == id)
        if not comodity.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No comodity with id: {id} was not found")

        comodity.update(updated_comodity.dict(), synchronize_session=False)
        db.commit()
        return comodity

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
