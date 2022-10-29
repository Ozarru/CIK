from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/med_tests', tags=['Medical Tests'])


@router.get('/', response_model=List[gen_schemas.MedExamination])
def get_tests(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    tests = db.query(gen_models.MedTest).order_by(
        gen_models.MedTest.date).all()

    if not tests:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No tests were found")
    return tests


@router.get('/{id}', response_model=gen_schemas.MedExamination)
def get_test(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    test = db.query(gen_models.MedTest).filter(
        gen_models.MedTest.id == id).first()
    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No test with id: {id} was found")
    return test


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.MedExamination)
def create_test(test: gen_schemas.MedExamination, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id > 2 or current_user.role_id != 7:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_test = gen_models.MedTest(**test.dict())
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    print(new_test)
    return new_test


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_test(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 2 or current_user.role_id == 7:
        test = db.query(gen_models.MedTest).filter(
            gen_models.MedTest.id == id)
        if not test.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No test with id: {id} was found!")
        test.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_test(id: int, updated_test: gen_schemas.MedExamination, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 2 or current_user.role_id == 7:
        test = db.query(gen_models.MedTest).filter(
            gen_models.MedTest.id == id)
        if not test.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No test with id: {id} was not found")

        test.update(updated_test.dict(),
                    synchronize_session=False)
        db.commit()
        return test

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
