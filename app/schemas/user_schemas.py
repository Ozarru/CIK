from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
# from .gen_schemas import *


# ----------------------Role---------------------------
class Role(BaseModel):
    name: str
    sec_level: int

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
    matrimony: Optional[str]
    email: Optional[EmailStr]
    tel: Optional[str]
    cel: Optional[str]
    address: Optional[str]


class PatientRes(BaseModel):
    id: int
    title: str
    firstname: str
    lastname: str
    age: int
    gender: str
    matrimony: Optional[str]
    email: Optional[EmailStr]
    tel: Optional[str]
    cel: Optional[str]
    address: Optional[str]

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

    class Config:
        orm_mode = True
