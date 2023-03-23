from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import user_models
from ...utils import oauth2, hasher
from ...schemas import user_schemas
from ...config.database import get_db

router = APIRouter(prefix='/doctors', tags=['Doctors'])


@router.get('/', response_model=List[user_schemas.UserRes])
def get_doctors(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_doctors(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if current_user.role_id != 1:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    doctors = db.query(user_models.User).filter(
        user_models.User.role_id == 4).all()

    if not doctors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No doctors were found")
    return doctors


@router.get('/{id}', response_model=user_schemas.UserRes)
def get_doctor(id: int, db: Session = Depends(get_db),):
    # def get_doctor(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    doctor = db.query(user_models.User).filter(
        user_models.User.role_id == 4, user_models.User.id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No doctor with id: {id} was found")
    return doctor


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserRes)
def create_doctors(user: user_schemas.UserReq, db: Session = Depends(get_db)):
    # def create_doctors(user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    hashed_pass = hasher.hash(user.password)
    user.password = hashed_pass
    new_user = user_models.User(role_id=4, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(id: int, db: Session = Depends(get_db),):
    # def delete_doctor(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    # if current_user.role_id == 1:
    #     doctor = db.query(user_models.User).filter(
    #         user_models.User.role_id == 4, user_models.User.id == id)
    #     if not doctor.first():
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail=f"No doctor with id: {id} was found!")
    #     doctor.delete(synchronize_session=False)
    #     db.commit()
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)

    # else:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Forbidden!!! Insufficient authentication credentials!")

    doctor = db.query(user_models.User).filter(
        user_models.User.role_id == 4, user_models.User.id == id)
    if not doctor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No doctor with id: {id} was found!")
    doctor.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}')
def update_doctor(id: int, updated_user: user_schemas.UserReq, db: Session = Depends(get_db)):
    # def update_doctor(id: int, updated_user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id == 1:
    #         doctor = db.query(user_models.User).filter(
    #             user_models.User.role_id == 4, user_models.User.id == id)
    #         if not doctor.first():
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                                 detail=f"No doctor with id: {id} was not found")

    #         doctor.update(updated_user.dict(), synchronize_session=False)
    #         db.commit()
    #         return doctor

    #     else:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials!")

    doctor = db.query(user_models.User).filter(
        user_models.User.role_id == 4, user_models.User.id == id)
    if not doctor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No doctor with id: {id} was not found")

    doctor.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return doctor
