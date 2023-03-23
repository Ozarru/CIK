from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import user_models
from ...utils import oauth2
from ...schemas import user_schemas
from ...config.database import get_db

router = APIRouter(prefix='/specialties', tags=['Specialties'])


@router.get('/', response_model=List[user_schemas.Specialty])
def get_specialties(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_specialty(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    specialties = db.query(user_models.Specialty).order_by(
        user_models.Specialty.name).all()

    if not specialties:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No specialties were found")
    return specialties


@router.get('/{id}', response_model=user_schemas.Specialty)
def get_specialty(id: int, db: Session = Depends(get_db),):
    # def get_specialty(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    specialty = db.query(user_models.Specialty).filter(
        user_models.Specialty.id == id).first()
    if not specialty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No specialty with id: {id} was found")
    return specialty


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.Specialty)
def create_specialty(specialty: user_schemas.Specialty, db: Session = Depends(get_db), ):
    # def create_specialty(specialty: user_schemas.Specialty, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1 or current_user.role_id != 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_specialty = user_models.Specialty(**specialty.dict())
    db.add(new_specialty)
    db.commit()
    db.refresh(new_specialty)
    print(new_specialty)
    return new_specialty


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_specialty(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 2:
        specialty = db.query(user_models.Specialty).filter(
            user_models.Specialty.id == id)
        if not specialty.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No specialty with id: {id} was found!")
        specialty.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_booked_specialty(id: int, update_bookedd_consultion: user_schemas.Specialty, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 2 or current_user.role_id == 4:
        specialty = db.query(user_models.Specialty).filter(
            user_models.Specialty.id == id)
        if not specialty.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No specialty with id: {id} was not found")

        specialty.update_booked(update_bookedd_consultion.dict(),
                                synchronize_session=False)
        db.commit()
        return specialty

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
