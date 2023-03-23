from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/med_operations', tags=['Medical operations'])


@router.get('/', response_model=List[gen_schemas.MedOperation])
def get_operations(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_operations(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    operations = db.query(gen_models.MedOperation).order_by(
        gen_models.MedOperation.date).all()

    if not operations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No operations were found")
    return operations


@router.get('/{id}', response_model=gen_schemas.MedOperation)
def get_operation(id: int, db: Session = Depends(get_db)):
    # def get_operation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    operation = db.query(gen_models.MedOperation).filter(
        gen_models.MedOperation.id == id).first()
    if not operation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No operation with id: {id} was found")
    return operation


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.MedOperation)
def create_operation(operation: gen_schemas.MedOperation, db: Session = Depends(get_db),):
    # def create_operation(operation: gen_schemas.MedOperation, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 2 or current_user.role_id != 4:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_operation = gen_models.MedOperation(**operation.dict())
    db.add(new_operation)
    db.commit()
    db.refresh(new_operation)
    print(new_operation)
    return new_operation


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_operation(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 4:
        operation = db.query(gen_models.MedOperation).filter(
            gen_models.MedOperation.id == id)
        if not operation.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No operation with id: {id} was found!")
        operation.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_operation(id: int, updated_operation: gen_schemas.MedOperation, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 4:
        operation = db.query(gen_models.MedOperation).filter(
            gen_models.MedOperation.id == id)
        if not operation.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No operation with id: {id} was not found")

        operation.update(updated_operation.dict(),
                         synchronize_session=False)
        db.commit()
        return operation

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
