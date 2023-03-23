from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from .user_schemas import *

# Consultation----------------------------------------


class Lot(BaseModel):
    id: Optional[int]
    number: int
    name: str
    date: Optional[datetime]

    class Config:
        orm_mode = True


class Product(BaseModel):
    maker: str
    name: str
    quantity: int
    unit_cost: int
    lot_id: Optional[int]
    date_added: Optional[datetime]
    produced_on: Optional[datetime]
    expires_on: Optional[datetime]


# -------------------------------
class MedicationReq(Product):
    pass
    notice: Optional[str]
    dosage: Optional[str]


class MedicationRes(Product):
    id: int
    lot: Optional[Lot]
    pass

    class Config:
        orm_mode = True


# -------------------------------
class AccessoryReq(Product):
    pass
    # usage: Optional[str]


class AccessoryRes(Product):
    id: int
    lot: Lot
    pass

    class Config:
        orm_mode = True

# -------------------------------


class ExternalRxReq(BaseModel):
    prescriptions: str
    patient_id: str
    doctor_id: str


class ExternalRxRes(Product):
    id: int
    prescriptions: str
    doctor: UserResume
    patient: PatientResume

    class Config:
        orm_mode = True
