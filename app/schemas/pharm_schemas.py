from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Consultation----------------------------------------


class Product(BaseModel):
    maker: str
    name: str
    quantity: int
    unit_cost: int
    date_added: datetime
    produced_on: datetime
    expires_on: datetime


# -------------------------------
class MedicationReq(Product):
    pass
    notice: str
    dosage: str


class MedicationRes(Product):
    id: int
    pass

    class Config:
        orm_mode = True


# -------------------------------
class AccessoryReq(Product):
    pass
    notice: str
    dosage: str


class AccessoryRes(Product):
    id: int
    pass

    class Config:
        orm_mode = True
