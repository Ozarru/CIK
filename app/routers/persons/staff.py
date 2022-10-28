from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import user_models
from ...utils import oauth2, hasher
from ...schemas import user_schemas
from ...config.database import get_db

router = APIRouter(prefix='/staff', tags=['Staff'])


@router.get('/', response_model=List[user_schemas.UserRes])
def get_staff(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    staff = db.query(user_models.User).order_by(user_models.User.role_id).all()

    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No staff were found")
    return staff


@router.get('/{id}', response_model=user_schemas.UserRes)
def get_staff(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    staff = db.query(user_models.User).filter(
        user_models.User.id == id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No staff with id: {id} was found")
    return staff


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserRes)
# def create_staff(user: user_schemas.UserReq, db: Session = Depends(get_db)):
def create_staff(user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    hashed_pass = hasher.hash(user.password)
    user.password = hashed_pass
    new_user = user_models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id == 1:
        staff = db.query(user_models.User).filter(user_models.User.id == id)
        if not staff.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No staff with id: {id} was found!")
        staff.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_staff(id: int, updated_user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1:
        staff = db.query(user_models.User).filter(
            user_models.User.role_id == 1, user_models.User.id == id)
        if not staff.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No staff with id: {id} was not found")

        staff.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        return staff

    elif current_user:
        staff = db.query(user_models.User).filter(
            user_models.User.id == current_user == id)
        if not staff.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No staff with id: {id} was not found")

        staff.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        return staff

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
