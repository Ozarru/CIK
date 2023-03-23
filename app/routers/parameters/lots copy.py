from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...utils import oauth2
from ...models import pharm_models
from ...schemas import pharm_schemas
from ...config.database import get_db

router = APIRouter(prefix='/lots', tags=['Lots'])


@router.get('/', response_model=List[pharm_schemas.Lot])
def get_lots(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_lot(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    lots = db.query(pharm_models.Lot).order_by(
        pharm_models.Lot.name).all()

    if not lots:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No lots were found")
    return lots


@router.get('/{id}', response_model=pharm_schemas.Lot)
def get_lot(id: int, db: Session = Depends(get_db),):
    # def get_lot(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    lot = db.query(pharm_models.Lot).filter(
        pharm_models.Lot.id == id).first()
    if not lot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No lot with id: {id} was found")
    return lot


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=pharm_schemas.Lot)
def create_lot(lot: pharm_schemas.Lot, db: Session = Depends(get_db), ):
    # def create_lot(lot: pharm_schemas.Lot, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1 or current_user.role_id != 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_lot = pharm_models.Lot(**lot.dict())
    db.add(new_lot)
    db.commit()
    db.refresh(new_lot)
    print(new_lot)
    return new_lot


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_lot(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 2:
        lot = db.query(pharm_models.Lot).filter(
            pharm_models.Lot.id == id)
        if not lot.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No lot with id: {id} was found!")
        lot.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_lot(id: int, updated_consultion: pharm_schemas.Lot, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 2 or current_user.role_id == 4:
        lot = db.query(pharm_models.Lot).filter(
            pharm_models.Lot.id == id)
        if not lot.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No lot with id: {id} was not found")

        lot.update(updated_consultion.dict(),
                   synchronize_session=False)
        db.commit()
        return lot

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
