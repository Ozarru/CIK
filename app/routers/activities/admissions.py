from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/admissions', tags=['Admissions'])


@router.get('/', response_model=List[gen_schemas.AdmissionRes])
def get_admission(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    admissions = db.query(gen_models.Admission).order_by(
        gen_models.Admission.date).all()

    if not admissions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No admissions were found")
    return admissions


@router.get('/{id}', response_model=gen_schemas.AdmissionRes)
def get_admission(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    admission = db.query(gen_models.Admission).filter(
        gen_models.Admission.id == id).first()
    if not admission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No admission with id: {id} was found")
    return admission


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.AdmissionRes)
def create_admission(admission: gen_schemas.AdmissionReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id > 3 and current_user.role_id != 4:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_admission = gen_models.Admission(
        doctor_id=current_user.id, **admission.dict())
    db.add(new_admission)
    db.commit()
    db.refresh(new_admission)
    print(new_admission)
    return new_admission


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_admission(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id == 1 or current_user.role_id == 3:
        admission = db.query(gen_models.Admission).filter(
            gen_models.Admission.id == id)
        if not admission.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No admission with id: {id} was found!")
        admission.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_admission(id: int, updated_admission: gen_schemas.AdmissionReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1 or current_user.role_id == 3:
        admission = db.query(gen_models.Admission).filter(
            gen_models.Admission.id == id)
        if not admission.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No admission with id: {id} was not found")

        admission.update(updated_admission.dict(), synchronize_session=False)
        db.commit()
        return admission

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
