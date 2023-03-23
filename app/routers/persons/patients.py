from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import user_models
from ...utils import oauth2, hasher
from ...schemas import user_schemas
from ...config.database import get_db

router = APIRouter(prefix='/patients', tags=['Patients'])


@router.get('/', response_model=List[user_schemas.PatientRes])
def get_patients(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_patient(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    patients = db.query(user_models.Patient).order_by(
        user_models.Patient.reg_date).all()

    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No patients were found")
    return patients


@router.get('/{id}', response_model=user_schemas.PatientRes)
def get_patient(id: int, db: Session = Depends(get_db),):
    # def get_patient(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    patient = db.query(user_models.Patient).filter(
        user_models.Patient.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No patient with id: {id} was found")
    return patient


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.PatientRes)
def create_patient(patient: user_schemas.PatientReq, db: Session = Depends(get_db),):
    # def create_patient(patient: user_schemas.PatientReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 3 and current_user.role_id < 8:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_patient = user_models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    print(new_patient)
    return new_patient


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id == 1 or current_user.role_id == 7:
        patient = db.query(user_models.Patient).filter(
            user_models.Patient.id == id)
        if not patient.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No patient with id: {id} was found!")
        patient.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_patient(id: int, updated_user: user_schemas.PatientReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1 or current_user.role_id == 7:
        patient = db.query(user_models.Patient).filter(
            user_models.Patient.id == id)
        if not patient.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No patient with id: {id} was not found")

        patient.update(updated_user.dict(), synchronize_session=False)
        db.commit()
        return patient

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
