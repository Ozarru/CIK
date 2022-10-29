from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/pending-consultations',
                   tags=['Pending Consultations (waiting room)'])


@router.get('/', response_model=List[gen_schemas.ConsultationResume])
def get_consultation(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    consultations = db.query(gen_models.Consultation).filter(gen_models.Consultation.is_pending == True).order_by(
        gen_models.Consultation.date).all()

    if not consultations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No pending consultations were found")
    return consultations


@router.get('/{id}', response_model=gen_schemas.ConsultationResume)
def get_consultation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    consultation = db.query(gen_models.Consultation).filter(gen_models.Consultation.is_pending == True,
                                                            gen_models.Consultation.id == id).first()
    if not consultation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No pending consultation with id: {id} was found")
    return consultation


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.ConsultationReq)
def create_consultation(consultation: gen_schemas.ConsultationReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 2 and current_user.role_id >= 8:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_consultation = gen_models.Consultation(**consultation.dict())
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    print(new_consultation)
    return new_consultation


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_consultation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        consultation = db.query(gen_models.Consultation).filter(gen_models.Consultation.is_pending == True,
                                                                gen_models.Consultation.id == id)
        if not consultation.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No pending consultation with id: {id} was found!")
        consultation.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_consultation(id: int, updated_user: gen_schemas.ConsultationReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 4 and current_user.role_id >= 8:
        consultation = db.query(gen_models.Consultation).filter(gen_models.Consultation.is_pending == True,
                                                                gen_models.Consultation.id == id)
        if not consultation.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No pending consultation with id: {id} was not found")

        consultation.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        return consultation

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
