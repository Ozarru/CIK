from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import pharm_models
from ...utils import oauth2
from ...schemas import pharm_schemas
from ...config.database import get_db

router = APIRouter(prefix='/prescriptions', tags=['Prescriptions'])


@router.get('/', response_model=List[pharm_schemas.PrescriptionRes])
def get_prescriptions(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    prescriptions = db.query(pharm_models.Prescription).order_by(
        pharm_models.Prescription.date).all()

    if not prescriptions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No prescriptions were found")
    return prescriptions


@router.get('/{id}', response_model=pharm_schemas.PrescriptionRes)
def get_prescription(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    prescription = db.query(pharm_models.Prescription).filter(
        pharm_models.Prescription.id == id).first()
    if not prescription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No prescription with id: {id} was found")
    return prescription


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=pharm_schemas.PrescriptionRes)
def create_prescription(prescription: pharm_schemas.PrescriptionReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 1 or current_user.role_id != 8:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_prescription = pharm_models.Prescription(**prescription.dict())
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    print(new_prescription)
    return new_prescription


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_prescription(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id == 1 or current_user.role_id == 8:
        prescription = db.query(pharm_models.Prescription).filter(
            pharm_models.Prescription.id == id)
        if not prescription.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No prescription with id: {id} was found!")
        prescription.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_prescription(id: int, updated_prescription: pharm_schemas.PrescriptionReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1 or current_user.role_id == 8:
        prescription = db.query(pharm_models.Prescription).filter(
            pharm_models.Prescription.id == id)
        if not prescription.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No prescription with id: {id} was not found")

        prescription.update(updated_prescription.dict(),
                            synchronize_session=False)
        db.commit()
        return prescription

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
