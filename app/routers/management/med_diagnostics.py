from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/med_diagnostics', tags=['Medical Diagnostics'])


@router.get('/', response_model=List[gen_schemas.MedProcedure])
def get_diagnostics(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    diagnostics = db.query(gen_models.MedDiagnostic).order_by(
        gen_models.MedDiagnostic.date).all()

    if not diagnostics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No diagnostics were found")
    return diagnostics


@router.get('/{id}', response_model=gen_schemas.MedProcedure)
def get_diagnostic(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    diagnostic = db.query(gen_models.MedDiagnostic).filter(
        gen_models.MedDiagnostic.id == id).first()
    if not diagnostic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No diagnostic with id: {id} was found")
    return diagnostic


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.MedProcedure)
def create_diagnostic(diagnostic: gen_schemas.MedProcedure, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id > 2 or current_user.role_id != 4:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_diagnostic = gen_models.MedDiagnostic(**diagnostic.dict())
    db.add(new_diagnostic)
    db.commit()
    db.refresh(new_diagnostic)
    print(new_diagnostic)
    return new_diagnostic


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_diagnostic(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 4:
        diagnostic = db.query(gen_models.MedDiagnostic).filter(
            gen_models.MedDiagnostic.id == id)
        if not diagnostic.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No diagnostic with id: {id} was found!")
        diagnostic.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_diagnostic(id: int, updated_diagnostic: gen_schemas.MedProcedure, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 4:
        diagnostic = db.query(gen_models.MedDiagnostic).filter(
            gen_models.MedDiagnostic.id == id)
        if not diagnostic.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No diagnostic with id: {id} was not found")

        diagnostic.update(updated_diagnostic.dict(),
                          synchronize_session=False)
        db.commit()
        return diagnostic

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
