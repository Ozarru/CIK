from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/consultations', tags=['Consultations'])


@router.get('/', response_model=List[gen_schemas.ConsultationRes])
def get_consultation(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_consultation(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    consultations = db.query(gen_models.Ordinance).order_by(
        gen_models.Ordinance.date).all()

    if not consultations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No consultations were found")
    return consultations


@router.get('/{id}', response_model=gen_schemas.ConsultationRes)
def get_consultation(id: int, db: Session = Depends(get_db),):
    # def get_consultation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    consultation = db.query(gen_models.Ordinance).filter(
        gen_models.Ordinance.id == id).first()
    if not consultation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No consultation with id: {id} was found")
    return consultation


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.ConsultationRes)
def create_consultation(consultation: gen_schemas.ConsultationReq, db: Session = Depends(get_db),):
    # def create_consultation(consultation: gen_schemas.ConsultationReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1 or current_user.role_id != 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_consultation = gen_models.Ordinance(**consultation.dict())
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    print(new_consultation)
    return new_consultation


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_consultation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 2:
        consultation = db.query(gen_models.Ordinance).filter(
            gen_models.Ordinance.id == id)
        if not consultation.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No consultation with id: {id} was found!")
        consultation.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_consultation(id: int, updated_consultion: gen_schemas.ConsultationReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 2 or current_user.role_id == 4:
        consultation = db.query(gen_models.Ordinance).filter(
            gen_models.Ordinance.id == id)
        if not consultation.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No consultation with id: {id} was not found")

        consultation.update(updated_consultion.dict(),
                            synchronize_session=False)
        db.commit()
        return consultation

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
