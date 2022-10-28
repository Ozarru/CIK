from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .user_schemas import *


# Bills payment---------------------------------
class BillReq(BaseModel):
    date_issued: datetime
    date_due: datetime
    genre: str
    total: int
    paid: int
    balance: int
    is_paid: bool
    patient_id: int


class BillReq(BaseModel):
    date_issued: datetime
    date_due: datetime
    genre: str
    total: int
    paid: int
    balance: int
    is_paid: bool
    patient: PatientResume

    class Config:
        orm_mode = True


# Salary payment---------------------------------
class PaySalary(BaseModel):
    date: datetime
    amount: int
    month: str


class PaySalaryReq(PaySalary):
    pass
    staff_id: str


class PaySalaryRes(PaySalary):
    pass
    staff: UserResume

    class Config:
        orm_mode = True


# Wage payment---------------------------------
class PayWage(BaseModel):
    date: datetime
    amount: float
    hourly_rate: int
    hours_worked: float
    month: str


class PayWageReq(PayWage):
    pass
    staff_id: str


class PayWageRes(PayWage):
    pass
    staff: UserResume

    class Config:
        orm_mode = True

# Insurance------------------------------------


class Insurance(BaseModel):
    name: str

    class Config:
        orm_mode = True


class InsuranceRes(BaseModel):
    name: str
    tiers: "List[InsuranceTierRes]"

    class Config:
        orm_mode = True


class InsuranceTierReq(BaseModel):
    name: str
    percentage: float
    insurance_id: int


class InsuranceTierRes(BaseModel):
    name: str
    percentage: float
    insurance: Insurance

    class Config:
        orm_mode = True

# Payroll---------------------------------------


class SalaryReq(BaseModel):
    amount: int
    qualification: str
    role_id: int


class SalaryRes(BaseModel):
    amount: int
    qualification: str
    role: Role

    class Config:
        orm_mode = True


class WageReq(BaseModel):
    hourly_rate: int
    qualification: str
    role_id: int


class WageRes(BaseModel):
    hourly_rate: int
    qualification: str
    role: Role

    class Config:
        orm_mode = True
# Bills-----------------------------------------


class BillReq(BaseModel):
    date_issued: datetime
    date_due: datetime
    genre: str
    total: int
    paid: int
    balance: int
    patient_id: int


class BillRes(BaseModel):
    date_issued: datetime
    date_due: datetime
    genre: str
    total: int
    paid: int
    balance: int
    patient: PatientResume

    class Config:
        orm_mode = True
