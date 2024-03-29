from os import access, remove
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..models import user_models
from ..config.database import get_db
from ..schemas import gen_schemas
from ..utils import hasher, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=gen_schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(
        user_models.User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    if not hasher.verify_pass(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {'access_token': access_token, "token_type": "bearer"}


@router.get('/logout')
def logout(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    return remove(current_user)
