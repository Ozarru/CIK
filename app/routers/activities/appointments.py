from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ...models import gen_models
from ...utils import oauth2
from ...schemas import gen_schemas
from ...config.database import get_db

router = APIRouter(prefix='/appointments', tags=['Appointments'])


@router.get('/', response_model=List[gen_schemas.AppointmentRes])
def get_appointment(db: Session = Depends(get_db), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    # def get_appointment(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 0, offset: int = 0, search: Optional[str] = ""):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")
    appointments = db.query(gen_models.Appointment).order_by(
        gen_models.Appointment.date_booked).all()

    if not appointments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No appointments were found")
    return appointments


@router.get('/{id}', response_model=gen_schemas.AppointmentRes)
def get_appointment(id: int, db: Session = Depends(get_db),):
    # def get_appointment(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if not current_user:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials.")
    appointment = db.query(gen_models.Appointment).filter(
        gen_models.Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No appointment with id: {id} was found")
    return appointment


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=gen_schemas.AppointmentRes)
def create_appointment(appointment: gen_schemas.AppointmentReq, db: Session = Depends(get_db), ):
    # def create_appointment(appointment: gen_schemas.AppointmentReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    #     if current_user.role_id != 1 or current_user.role_id != 3:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                             detail=f"Forbidden!!! Insufficient authentication credentials")

    new_appointment = gen_models.Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    print(new_appointment)
    return new_appointment


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.role_id <= 2:
        appointment = db.query(gen_models.Appointment).filter(
            gen_models.Appointment.id == id)
        if not appointment.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No appointment with id: {id} was found!")
        appointment.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")


@router.put('/{id}')
def update_booked_appointment(id: int, update_bookedd_consultion: gen_schemas.AppointmentReq, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    if current_user.role_id <= 2 or current_user.role_id == 4:
        appointment = db.query(gen_models.Appointment).filter(
            gen_models.Appointment.id == id)
        if not appointment.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No appointment with id: {id} was not found")

        appointment.update_booked(update_bookedd_consultion.dict(),
                                  synchronize_session=False)
        db.commit()
        return appointment

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Forbidden!!! Insufficient authentication credentials!")
