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

# Appointment----------------------------------------


class AppointmentReq(BaseModel):
    patient_name: str
    patient_tel: str
    day: str
    time: str
    is_pending: bool = True
    doctor_id: int


class AppointmentRes(BaseModel):
    id: int
    date_booked: datetime
    patient_name: str
    patient_name: str
    day: str
    time: str
    is_pending: bool
    doctor: UserRes

    class Config:
        orm_mode = True


# Consultation----------------------------------------


class ConsultationGenre(BaseModel):
    id: Optional[int]
    name: str
    price: int
    parameters: Optional[str]

    class Config:
        orm_mode = True


class ConsultationReq(BaseModel):
    chemical_tests: Optional[str]
    parachemical_tests: Optional[str]
    observations: Optional[str]
    diagnosis:  Optional[str]
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
    is_pending: bool = True
    doctor_id: int
    patient_id: int
    genre_id: Optional[int]


class ConsultationRes(BaseModel):
    id: int
    date: datetime
    chemical_tests: Optional[str]
    parachemical_tests: Optional[str]
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
    doctor: UserRes
    patient: PatientRes
    genre: Optional[ConsultationGenre]

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
    genre: Optional[ConsultationGenre]

    class Config:
        orm_mode = True


class AdmissionReq(BaseModel):
    date: datetime
    genre: str
    cause: str
    note: Optional[str]
    duration: Optional[str]
    patient_id: int


class AdmissionRes(BaseModel):
    id: int
    date: datetime
    genre: str
    cause: str
    note: Optional[str]
    duration: Optional[str]
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
    name: str
    genre: Optional[str]
    price: Optional[int]
    beds: Optional[int]

    class Config:
        orm_mode = True


class MedExamination(BaseModel):
    name: str
    cost: Optional[int]
    description: Optional[str]

    class Config:
        orm_mode = True


class MedProcedure(BaseModel):
    name: str
    cost: Optional[int]
    description: Optional[str]
    duration: Optional[str]
    sessions: Optional[int]

    class Config:
        orm_mode = True


class MedOperation(BaseModel):
    name: str
    cost: Optional[int]
    description: Optional[str]
    duration: Optional[str]
    sessions: Optional[int]

    class Config:
        orm_mode = True
