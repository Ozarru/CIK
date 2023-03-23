from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import pharm_models
from ...utils import oauth2
from ...schemas import pharm_schemas
from ...config.database import get_db

router = APIRouter(prefix='/medications', tags=['Medications'])


@router.get('/', response_model=List[pharm_schemas.MedicationRes])
def get_medications(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_medications(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    medications = db.query(pharm_models.Medication).order_by(
        pharm_models.Medication.date_added).all()

    if not medications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No medications were found")
    return medications


@router.get('/{id}', response_model=pharm_schemas.MedicationRes)
def get_medication(id: int, db: Session = Depends(get_db),):
    # def get_medication(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    medication = db.query(pharm_models.Medication).filter(
        pharm_models.Medication.id == id).first()
    if not medication:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No medication with id: {id} was found")
    return medication


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=pharm_schemas.MedicationRes)
def create_medication(medication: pharm_schemas.MedicationReq, db: Session = Depends(get_db),):
    # def create_medication(medication: pharm_schemas.MedicationReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1 and current_user.role_id != 8:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_medication = pharm_models.Medication(**medication.dict())
    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)
    print(new_medication)
    return new_medication


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_medication(id: int, db: Session = Depends(get_db),):
    # def delete_medication(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    # if current_user.role_id == 1 or current_user.role_id == 8:
    medication = db.query(pharm_models.Medication).filter(
        pharm_models.Medication.id == id)
    if not medication.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No medication with id: {id} was found!")
    medication.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # else:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_medication(id: int, updated_med: pharm_schemas.MedicationReq, db: Session = Depends(get_db),):
    # def update_medication(id: int, updated_med: pharm_schemas.MedicationReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    # if current_user.role_id == 1 or current_user.role_id == 8:
    medication = db.query(pharm_models.Medication).filter(
        pharm_models.Medication.id == id)
    if not medication.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No medication with id: {id} was not found")

    medication.update(updated_med.dict(), synchronize_session=False)
    db.commit()
    return medication

    # else:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Forbidden!!! Insufficient authentication credentials!")
