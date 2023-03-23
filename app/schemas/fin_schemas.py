from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .user_schemas import *


# Insurance------------------------------------


class Comodity(BaseModel):
    id: Optional[int]
    name: str
    genre: str
    price: int
    description: Optional[str]
    date_added: Optional[datetime]

    class Config:
        orm_mode = True


class Insurance(BaseModel):
    id: Optional[int]
    name: str
    overview: Optional[str]

    class Config:
        orm_mode = True


class InsuranceTier(BaseModel):
    id: Optional[int]
    name: str
    percentage: Optional[float]
    ceiling: Optional[int]
    custom_price: Optional[int]
    overview: Optional[str]
    insurance_id: int

    class Config:
        orm_mode = True


class Company(BaseModel):
    id: Optional[int]
    name: str
    overview: Optional[str]
    insurance_id: int


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
    id: Optional[int]
    name: str
    overview: Optional[str]

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

# Bills-----------------------------------------


class Cashdesk(BaseModel):
    id: Optional[int]
    name: str
    credit: Optional[int]
    debit: Optional[int]
    balance: Optional[int]
    overview: Optional[str]

    class Config:
        orm_mode = True


class MomoAccount(BaseModel):
    id: Optional[int]
    name: str
    number: str
    carrier: str
    credit: int
    debit: int
    balance: int

    class Config:
        orm_mode = True


class Bank(BaseModel):
    id: Optional[int]
    name: str
    acc_number: str
    overview: str
    credit: int
    debit: int
    balance: int

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    id: Optional[int]
    overview: Optional[str]
    amount: Optional[int]
    paid: Optional[int]
    due: Optional[int]
    genre: str
    date: datetime

    class Config:
        orm_mode = True


class BankTransaction(Transaction):
    pass
    bank_id: int
    bank: Optional[Bank]

    class Config:
        orm_mode = True


class MomoTransaction(Transaction):
    pass
    bank_id: int
    momo_account: Optional[MomoAccount]

    class Config:
        orm_mode = True


class CashTransaction(Transaction):
    pass
    cashdesk_id: int
    cashdesk: Optional[Cashdesk]

    class Config:
        orm_mode = True


class PatientTransaction(BaseModel):
    patient_id: Optional[int]
    patient: Optional[PatientResume]
    comodity_id: Optional[int]
    comodity: Optional[Comodity]
    insurance_tier_id: Optional[int]
    insurance_tier: Optional[InsuranceTier]


class PatientCashTransaction(CashTransaction, PatientTransaction):
    pass
    # comodity_id: int
    # comodity: Optional[Comodity]
    # insurance_tier_id: Optional[int]
    # insurance_tier: Optional[InsuranceTier]
    # patient_id: int
    # patient: Optional[PatientResume]

    class Config:
        orm_mode = True


class PatientMobileTransaction(MomoTransaction):
    pass
    comodity_id: int
    comodity: Optional[Comodity]
    insurance_tier_id: Optional[int]
    insurance_tier: Optional[InsuranceTier]
    patient_id: int
    patient: Optional[PatientResume]

    class Config:
        orm_mode = True


class PatientBankTransaction(BankTransaction):
    pass
    comodity_id: int
    comodity: Optional[Comodity]
    insurance_tier_id: Optional[int]
    insurance_tier: Optional[InsuranceTier]
    patient_id: int
    patient: Optional[PatientResume]

    class Config:
        orm_mode = True
