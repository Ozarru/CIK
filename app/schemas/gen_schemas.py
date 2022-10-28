from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from .user_schemas import *
from .pharm_schemas import *


# ---------------Authentication-----------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str]

    class Config:
        orm_mode = True


# Consultation----------------------------------------
class ConsultationReq(BaseModel):
    chem_tests: Optional[str]
    para_chem_tests: Optional[str]
    observations: Optional[str]
    diagnosis:  Optional[str]
    prognosis: Optional[str]
    treatment: Optional[str]
    requested_tests: Optional[str]
    weight: Optional[float]
    height: Optional[float]
    temperatur: Optional[float]
    systole: Optional[float]
    diastole: Optional[float]
    oxymetry: Optional[float]
    bmi: Optional[float]
    is_pending: bool
    doctor_id: int
    patient_id: int


class ConsultationRes(BaseModel):
    id: int
    date: datetime
    chem_tests: Optional[str]
    para_chem_tests: Optional[str]
    observations: Optional[str]
    diagnosis: Optional[str]
    prognosis: Optional[str]
    treatment: Optional[str]
    requested_tests: Optional[str]
    weight: Optional[float]
    height: Optional[float]
    temperature: Optional[float]
    systole: Optional[float]
    diastole: Optional[float]
    oxymetry: Optional[float]
    bmi: Optional[float]
    is_pending: bool
    doctor: UserResume
    patient: PatientResume

    class Config:
        orm_mode = True


class ConsultationResume(BaseModel):
    id: int
    date: datetime
    weight: Optional[float]
    height: Optional[float]
    temperature: Optional[float]
    systole: Optional[float]
    diastole: Optional[float]
    is_pending: bool
    doctor: UserResume
    patient: PatientResume

    class Config:
        orm_mode = True


class AdmissionReq(BaseModel):
    date: datetime
    genre: str
    note: str
    motif: str
    duration: str
    doctor_id: str
    patient_id: str


class AdmissionRes(BaseModel):
    id: int
    date: datetime
    genre: str
    note: str
    motif: str
    duration: str
    doctor: UserResume
    patient: PatientResume

    class Config:
        orm_mode = True


class OrdinanceReq(BaseModel):
    date: datetime
    reference: str
    antecedents: str
    doctor_id: int
    patient_id: int


class OrdinanceRes(BaseModel):
    id: int
    date: datetime
    reference: str
    antecedents: str
    doctor: UserResume
    patient: PatientResume

    class Config:
        orm_mode = True


class PrescriptionReq(BaseModel):
    qsp: str
    boxes: int
    dosage: str
    ailments: str
    medication_id: int


class PrescriptionRes(BaseModel):
    id: int
    qsp: str
    boxes: int
    dosage: str
    ailments: str
    medication: MedicationRes

    class Config:
        orm_mode = True


class CertificationReq(BaseModel):
    date: datetime
    observations: str
    ailments: Optional[str]
    doctor_id: int
    patient_id: int


class CertificationRes(BaseModel):
    id: int
    date: datetime
    observations: Optional[str]
    ailments: str
    doctor: UserResume
    patient: PatientResume

    class Config:
        orm_mode = True


class Room(BaseModel):
    genre: str
    name: str
    cost: int

    class Config:
        orm_mode = True
