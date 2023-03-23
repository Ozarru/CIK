from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# from app.schemas.fin_schemas import Insurance
# from .gen_schemas import *


# ----------------------Role---------------------------
class Role(BaseModel):
    id: Optional[int]
    name: str
    sec_level: int

    class Config:
        orm_mode = True


class Specialty(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


# Users (Personnel)--------------------------------------
class UserReq(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    address: Optional[str]
    phone: Optional[str]
    role_id: Optional[int]
    specialty_id: Optional[int]

    class Config:
        orm_mode = True


class UserRes(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    address: Optional[str]
    phone: Optional[str]
    role: Optional[Role]
    specialty: Optional[Specialty]

    class Config:
        orm_mode = True


class UserResume(BaseModel):
    id: int
    firstname: str
    lastname: str
    phone: Optional[str]

    class Config:
        orm_mode = True


# Patients----------------------------------------------
class PatientReq(BaseModel):
    title: str
    firstname: str
    lastname: str
    age: int
    gender: str
    civil_status: Optional[str]
    email: Optional[EmailStr]
    tel: Optional[str]
    cel: Optional[str]
    address: Optional[str]
    is_insurred: Optional[bool]


class PatientRes(BaseModel):
    id: int
    title: str
    firstname: str
    lastname: str
    age: int
    gender: str
    civil_status: Optional[str]
    email: Optional[EmailStr]
    tel: Optional[str]
    cel: Optional[str]
    address: Optional[str]
    allergies: Optional[str]
    weight: Optional[float]
    height: Optional[float]
    is_insurred: Optional[bool]
    # insurrance: Optional[Insurance]

    class Config:
        orm_mode = True


class PatientResume(BaseModel):
    id: int
    title: str
    firstname: str
    lastname: str
    age: int
    gender: str
    tel: Optional[str]
    is_insurred: Optional[bool]

    class Config:
        orm_mode = True
