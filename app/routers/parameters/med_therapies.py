from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/med_therapies', tags=['Medical Therapies'])


@router.get('/', response_model=List[gen_schemas.MedProcedure])
def get_therapies(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_therapies(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    therapies = db.query(gen_models.MedTherapy).order_by(
        gen_models.MedTherapy.date).all()

    if not therapies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No therapies were found")
    return therapies


@router.get('/{id}', response_model=gen_schemas.MedProcedure)
def get_therapy(id: int, db: Session = Depends(get_db), ):
    # def get_therapy(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    therapy = db.query(gen_models.MedTherapy).filter(
        gen_models.MedTherapy.id == id).first()
    if not therapy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No therapy with id: {id} was found")
    return therapy


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.MedProcedure)
def create_therapy(therapy: gen_schemas.MedProcedure, db: Session = Depends(get_db), ):
    # def create_therapy(therapy: gen_schemas.MedProcedure, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 2 or current_user.role_id != 4:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_therapy = gen_models.MedTherapy(**therapy.dict())
    db.add(new_therapy)
    db.commit()
    db.refresh(new_therapy)
    print(new_therapy)
    return new_therapy


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_therapy(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 4:
        therapy = db.query(gen_models.MedTherapy).filter(
            gen_models.MedTherapy.id == id)
        if not therapy.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No therapy with id: {id} was found!")
        therapy.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_therapy(id: int, updated_therapy: gen_schemas.MedProcedure, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 4:
        therapy = db.query(gen_models.MedTherapy).filter(
            gen_models.MedTherapy.id == id)
        if not therapy.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No therapy with id: {id} was not found")

        therapy.update(updated_therapy.dict(),
                       synchronize_session=False)
        db.commit()
        return therapy

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
