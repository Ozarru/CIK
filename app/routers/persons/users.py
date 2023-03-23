from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import user_models
from ...utils import oauth2, hasher
from ...schemas import user_schemas
from ...config.database import get_db

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=List[user_schemas.UserRes])
def get_users(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_users(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    users = db.query(user_models.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No users were found")
    return users


@router.get('/{id}', response_model=user_schemas.UserRes)
def get_user(id: int, db: Session = Depends(get_db),):
    # def get_user(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    user = db.query(user_models.User).filter(user_models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with id: {id} was found")
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserRes)
def create_users(user: user_schemas.UserReq, db: Session = Depends(get_db)):
    # def create_users(user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    hashed_pass = hasher.hash_pass(user.password)
    user.password = hashed_pass
    new_user = user_models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id == 1:
        user = db.query(user_models.User).filter(
            user_models.User.role_id == 1, user_models.User.id == id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No user with id: {id} was found!")
        user.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=user_schemas.UserRes)
def update_user(id: int, updated_user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1:
        user = db.query(user_models.User).filter(
            user_models.User.role_id == 1, user_models.User.id == id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No user with id: {id} was not found")

        user.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        return user

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


# --------------------------------------------Profile---------------------------------------------------------

@router.get('/me', response_model=user_schemas.UserRes)
def get_current_user(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    user = db.query(user_models.User).filter(
        user_models.User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with id: {id} was found")
    return user


@router.put('/me/update', status_code=status.HTTP_202_ACCEPTED, response_model=user_schemas.UserRes)
def update_current_user(updated_user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    user = db.query(user_models.User).filter(
        user_models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with id: {current_user.id} was found")
    user.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user
