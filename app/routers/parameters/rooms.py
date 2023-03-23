from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.get('/', response_model=List[gen_schemas.Room])
def get_rooms(db: Session = Depends(get_db),  limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_rooms(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    rooms = db.query(gen_models.Room).order_by(
        gen_models.Room.price).all()

    if not rooms:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No rooms were found")
    return rooms


@router.get('/{id}', response_model=gen_schemas.Room)
def get_room(id: int, db: Session = Depends(get_db), ):
    # def get_room(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    room = db.query(gen_models.Room).filter(
        gen_models.Room.id == id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No room with id: {id} was found")
    return room


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.Room)
def create_room(room: gen_schemas.Room, db: Session = Depends(get_db), ):
    # def create_room(room: gen_schemas.Room, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id > 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_room = gen_models.Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    print(new_room)
    return new_room


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_room(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 3:
        room = db.query(gen_models.Room).filter(
            gen_models.Room.id == id)
        if not room.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No room with id: {id} was found!")
        room.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_room(id: int, updated_room: gen_schemas.Room, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 3:
        room = db.query(gen_models.Room).filter(
            gen_models.Room.id == id)
        if not room.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No room with id: {id} was not found")

        room.update(updated_room.dict(), synchronize_session=False)
        db.commit()
        return room

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
