from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/med_imageries', tags=['Medical Imageries'])


@router.get('/', response_model=List[gen_schemas.MedExamination])
def get_imageries(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_imageries(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    imageries = db.query(gen_models.MedImagery).order_by(
        gen_models.MedImagery.date).all()

    if not imageries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No imageries were found")
    return imageries


@router.get('/{id}', response_model=gen_schemas.MedExamination)
def get_imagery(id: int, db: Session = Depends(get_db),):
    # def get_imagery(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    imagery = db.query(gen_models.MedImagery).filter(
        gen_models.MedImagery.id == id).first()
    if not imagery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No imagery with id: {id} was found")
    return imagery


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.MedExamination)
def create_imagery(imagery: gen_schemas.MedExamination, db: Session = Depends(get_db),):
    # def create_imagery(imagery: gen_schemas.MedExamination, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 2 or current_user.role_id != 4:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_imagery = gen_models.MedImagery(**imagery.dict())
    db.add(new_imagery)
    db.commit()
    db.refresh(new_imagery)
    print(new_imagery)
    return new_imagery


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_imagery(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 4:
        imagery = db.query(gen_models.MedImagery).filter(
            gen_models.MedImagery.id == id)
        if not imagery.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No imagery with id: {id} was found!")
        imagery.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_imagery(id: int, updated_imagery: gen_schemas.MedExamination, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 4:
        imagery = db.query(gen_models.MedImagery).filter(
            gen_models.MedImagery.id == id)
        if not imagery.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No imagery with id: {id} was not found")

        imagery.update(updated_imagery.dict(),
                       synchronize_session=False)
        db.commit()
        return imagery

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
