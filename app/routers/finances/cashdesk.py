from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...utils import oauth2
from ...models import fin_models
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/cashdesks', tags=['Cashdesks'])


@router.get('/', response_model=List[fin_schemas.Cashdesk])
def get_cashdesks(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_cashdesk(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    cashdesks = db.query(fin_models.Cashdesk).order_by(
        fin_models.Cashdesk.name).all()

    if not cashdesks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No cashdesks were found")
    return cashdesks


@router.get('/{id}', response_model=fin_schemas.Cashdesk)
def get_cashdesk(id: int, db: Session = Depends(get_db),):
    # def get_cashdesk(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    cashdesk = db.query(fin_models.Cashdesk).filter(
        fin_models.Cashdesk.id == id).first()
    if not cashdesk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No cashdesk with id: {id} was found")
    return cashdesk


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.Cashdesk)
def create_cashdesk(cashdesk: fin_schemas.Cashdesk, db: Session = Depends(get_db), ):
    # def create_cashdesk(cashdesk: fin_schemas.Cashdesk, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1 or current_user.role_id != 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_cashdesk = fin_models.Cashdesk(**cashdesk.dict())
    db.add(new_cashdesk)
    db.commit()
    db.refresh(new_cashdesk)
    print(new_cashdesk)
    return new_cashdesk


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_cashdesk(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 2:
        cashdesk = db.query(fin_models.Cashdesk).filter(
            fin_models.Cashdesk.id == id)
        if not cashdesk.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No cashdesk with id: {id} was found!")
        cashdesk.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_cashdesk(id: int, updated_consultion: fin_schemas.Cashdesk, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 2 or current_user.role_id == 4:
        cashdesk = db.query(fin_models.Cashdesk).filter(
            fin_models.Cashdesk.id == id)
        if not cashdesk.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No cashdesk with id: {id} was not found")

        cashdesk.update(updated_consultion.dict(),
                        synchronize_session=False)
        db.commit()
        return cashdesk

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
