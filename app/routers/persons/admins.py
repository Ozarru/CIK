from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import user_models
from ...utils import oauth2, hasher
from ...schemas import user_schemas
from ...config.database import get_db

router = APIRouter(prefix='/admins', tags=['Administrators'])


@router.get('/', response_model=List[user_schemas.UserRes])
def get_admins(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    admins = db.query(user_models.User).filter(
        user_models.User.role_id == 1).all()

    if not admins:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No admins were found")
    return admins


@router.get('/{id}', response_model=user_schemas.UserRes)
def get_admin(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    admin = db.query(user_models.User).filter(
        user_models.User.role_id == 1, user_models.User.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No admin with id: {id} was found")
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    return admin


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserRes)
# def create_admins(user: user_schemas.UserReq, db: Session = Depends(get_db)):
def create_admins(user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    hashed_pass = hasher.hash(user.password)
    user.password = hashed_pass
    new_user = user_models.User(role_id=1, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id == 1:
        admin = db.query(user_models.User).filter(
            user_models.User.role_id == 1, user_models.User.id == id)
        if not admin.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No admin with id: {id} was found!")
        admin.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_admin(id: int, updated_user: user_schemas.UserReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1:
        admin = db.query(user_models.User).filter(
            user_models.User.role_id == 1, user_models.User.id == id)
        if not admin.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No admin with id: {id} was not found")

        admin.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        return admin

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
