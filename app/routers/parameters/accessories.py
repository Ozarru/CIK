from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import pharm_models
from ...utils import oauth2
from ...schemas import pharm_schemas
from ...config.database import get_db

router = APIRouter(prefix='/accessories', tags=['Accessories'])


@router.get('/', response_model=List[pharm_schemas.AccessoryRes])
def get_accessories(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_accessories(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    accessories = db.query(pharm_models.Accessory).order_by(
        pharm_models.Accessory.date_added).all()

    if not accessories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No accessories were found")
    return accessories


@router.get('/{id}', response_model=pharm_schemas.AccessoryRes)
def get_accessory(id: int, db: Session = Depends(get_db),):
    # def get_accessory(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    accessory = db.query(pharm_models.Accessory).filter(
        pharm_models.Accessory.id == id).first()
    if not accessory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No accessory with id: {id} was found")
    return accessory


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=pharm_schemas.AccessoryRes)
def create_accessory(accessory: pharm_schemas.AccessoryReq, db: Session = Depends(get_db),):
    # def create_accessory(accessory: pharm_schemas.AccessoryReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1 or current_user.role_id != 8:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_accessory = pharm_models.Accessory(**accessory.dict())
    db.add(new_accessory)
    db.commit()
    db.refresh(new_accessory)
    print(new_accessory)
    return new_accessory


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_accessory(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id == 1 or current_user.role_id == 8:
        accessory = db.query(pharm_models.Accessory).filter(
            pharm_models.Accessory.id == id)
        if not accessory.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No accessory with id: {id} was found!")
        accessory.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_accessory(id: int, updated_accessory: pharm_schemas.AccessoryReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1 or current_user.role_id == 8:
        accessory = db.query(pharm_models.Accessory).filter(
            pharm_models.Accessory.id == id)
        if not accessory.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No accessory with id: {id} was not found")

        accessory.update(updated_accessory.dict(), synchronize_session=False)
        db.commit()
        return accessory

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
