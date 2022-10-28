from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/certifications', tags=['Certifications'])


@router.get('/', response_model=List[gen_schemas.CertificationRes])
def get_certification(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")
    certifications = db.query(gen_models.Certification).order_by(
        gen_models.Certification.date).all()

    if not certifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No certifications were found")
    return certifications


@router.get('/{id}', response_model=gen_schemas.CertificationRes)
def get_certification(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials.")
    certification = db.query(gen_models.Certification).filter(
        gen_models.Certification.id == id).first()
    if not certification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No certification with id: {id} was found")
    return certification


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.CertificationReq)
def create_certification(certification: gen_schemas.CertificationReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id != 1 or current_user.role_id != 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials")

    new_certification = gen_models.Certification(**certification.dict())
    db.add(new_certification)
    db.commit()
    db.refresh(new_certification)
    print(new_certification)
    return new_certification


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id == 1 or current_user.role_id == 3:
        certification = db.query(gen_models.Certification).filter(
            gen_models.Certification.id == id)
        if not certification.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No certification with id: {id} was found!")
        certification.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_certification(id: int, updated_certification: gen_schemas.CertificationReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id == 1 or current_user.role_id == 3:
        certification = db.query(gen_models.Certification).filter(
            gen_models.Certification.id == id)
        if not certification.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No certification with id: {id} was not found")

        certification.update(updated_certification.dict(),
                             synchronize_session=False)
        db.commit()
        return certification

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
