from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import user_models
from ...utils import oauth2
from ...schemas import user_schemas
from ...config.database import get_db

router = APIRouter(prefix='/roles', tags=['Roles'])


@router.get('/', response_model=List[user_schemas.Role])
def get_roles(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_roles(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    roles = db.query(user_models.Role).all()

    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No roles were found")
    return roles


@router.get('/{id}', response_model=user_schemas.Role)
def get_role(id: int, db: Session = Depends(get_db),):
    # def get_role(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    role = db.query(user_models.Role).filter(
        user_models.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No role with id: {id} was found")
    return role


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.Role)
def create_role(role: user_schemas.Role, db: Session = Depends(get_db)):
    # def create_role(role: user_schemas.Role, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_role = user_models.Role(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    print(new_role)
    return new_role


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_role(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        role = db.query(user_models.Role).filter(
            user_models.Role.id == id)
        if not role.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No role with id: {id} was found!")
        role.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_role(id: int, updated_role: user_schemas.Role, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        role = db.query(user_models.Role).filter(
            user_models.Role.id == id)
        if not role.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No role with id: {id} was not found")

        role.update(updated_role.dict(), synchronize_session=False)
        db.commit()
        return role

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
