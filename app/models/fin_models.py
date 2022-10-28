from ..config.database import Base
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .user_models import *


class Bill(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date_issued = Column(TIMESTAMP(timezone=True),
                         server_default=text('now()'))
    date_due = Column(TIMESTAMP(timezone=True),
                      server_default=text('now()'))
    genre = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    paid = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    is_paid = Column(Boolean, nullable=False, server_default='False')
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="bills")


class Salary(Base):
    __tablename__ = 'salaries'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    amount = Column(Integer, nullable=False)
    qualification = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(
        'roles.id', ondelete="CASCADE"), nullable=True)
    role = relationship('Role', backref="salaries")


class Wage(Base):
    __tablename__ = 'wages'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    hourly_rate = Column(Integer, nullable=False)
    qualification = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(
        'roles.id', ondelete="CASCADE"), nullable=True)
    role = relationship('Role', backref="wages")


# ----------------------
class PaySalary(Base):
    __tablename__ = 'pay_salaries'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
    amount = Column(Integer, nullable=False)
    month = Column(String, nullable=False)
    staff_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    staff = relationship('User', backref="pay_salaries")


class PayWage(Base):
    __tablename__ = 'pay_wages'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
    amount = Column(Integer, nullable=False)
    hourly_rate = Column(Integer, nullable=False)
    hours_worked = Column(Float, nullable=False)
    month = Column(String, nullable=False)
    staff_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    staff = relationship('User', backref="pay_wages")


# ----------------------
class Insurance(Base):
    __tablename__ = 'insurances'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    tiers = relationship("InsuranceTier", backref="insurances")


class InsuranceTier(Base):
    __tablename__ = 'insurance_tiers'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)
    inssurance_id = Column(Integer, ForeignKey("insurances.id"))
