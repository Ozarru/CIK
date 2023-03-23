from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...utils import oauth2
from ...models import fin_models
from ...schemas import fin_schemas
from ...config.database import get_db

router = APIRouter(prefix='/insurance_tiers', tags=['Insurance Tiers'])


@router.get('/', response_model=List[fin_schemas.InsuranceTier])
def get_tiers(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_tiers(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    tiers = db.query(fin_models.InsuranceTier).order_by(
        fin_models.InsuranceTier.name).all()

    if not tiers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No tiers were found")
    return tiers


@router.get('/{id}', response_model=fin_schemas.InsuranceTier.update_forward_refs())
def get_tier(id: int, db: Session = Depends(get_db),):
    # def get_tier(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    tier = db.query(fin_models.InsuranceTier).filter(
        fin_models.InsuranceTier.id == id).first()
    if not tier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No tier with id: {id} was found")
    return tier


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=fin_schemas.InsuranceTier)
def create_tier(tier: fin_schemas.InsuranceTier, db: Session = Depends(get_db), ):
    # def create_tier(tier: fin_schemas.InsuranceTier, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_tier = fin_models.InsuranceTier(**tier.dict())
    db.add(new_tier)
    db.commit()
    db.refresh(new_tier)
    print(new_tier)
    return new_tier


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_tier(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        tier = db.query(fin_models.InsuranceTier).filter(
            fin_models.InsuranceTier.id == id)
        if not tier.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No tier with id: {id} was found!")
        tier.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_tier(id: int, updated_tier: fin_schemas.InsuranceTier, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        tier = db.query(fin_models.InsuranceTier).filter(
            fin_models.InsuranceTier.id == id)
        if not tier.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No tier with id: {id} was not found")

        tier.update(updated_tier.dict(), synchronize_session=False)
        db.commit()
        return tier

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
