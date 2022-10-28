from ..config.database import Base
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .user_models import *
from .pharm_models import *
from .fin_models import *


class Consultation(Base):
    __tablename__ = 'consultations'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
    chemical_tests = Column(String, nullable=True)
    parachemical_tests = Column(String, nullable=True)
    observations = Column(String, nullable=True)
    diagnosis = Column(String, nullable=True)
    prognosis = Column(String, nullable=True)
    treatment = Column(String, nullable=True)
    requested_tests = Column(String, nullable=True)
    patient_history = Column(String, nullable=True)
    # parameters
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    systole = Column(Float, nullable=True)
    diastole = Column(Float, nullable=True)
    oxymetry = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)
    #
    is_pending = Column(Boolean, nullable=False, server_default='True')
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    doctor = relationship('User', backref="consultations")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=False)
    patient = relationship('Patient', backref="consultations")


class Certification(Base):
    __tablename__ = 'certificaions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
    observations = Column(String, nullable=True)
    ailments = Column(String, nullable=False)
    #
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="certificaions")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="certificaions")


# RX management-----------------------
class Prescription(Base):
    __tablename__ = 'prescriptions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
    reference = Column(String, nullable=True)
    history = Column(String, nullable=True)
    drugs = relationship("RxLine", backref="prescriptions")
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="prescriptions")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="prescriptions")


class RxLine(Base):
    __tablename__ = 'rx_line'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    qsp = Column(String, nullable=True)
    boxes = Column(Integer, nullable=True)
    dosage = Column(String, nullable=True)
    ailments = Column(String, nullable=True)
    medication_id = Column(Integer, ForeignKey(
        'medications.id', ondelete="CASCADE"), nullable=True)
    medication = relationship('Medication', backref="rx_line")
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"))


# Medical procedures------------------
class MedDiagnostic(Base):
    __tablename__ = 'med_diagnostics'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)


class MedLabTest(Base):
    __tablename__ = 'med_labtests'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)


class MedTherapy(Base):
    __tablename__ = 'med_therapies'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)


class MedImagery(Base):
    __tablename__ = 'med_imageries'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)


class MedSurgery(Base):
    __tablename__ = 'med_surgeries'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    survival_rate = Column(Float, nullable=True)
    duration = Column(String, nullable=True)


# class MedExam(Base):
#     __tablename__ = 'med_exams'
#     id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
#     # test_id = Column(Integer, ForeignKey(
#     #     'medtests.id', ondelete="CASCADE"), nullable=True)
#     # test = relationship('MedTest', backref="medexams")
#     # patient_id = Column(Integer, ForeignKey(
#     #     'patients.id', ondelete="CASCADE"), nullable=True)
#     # patient = relationship('Patient', backref="medexams")
#     # doctor_id = Column(Integer, ForeignKey(
#     #     'users.id', ondelete="CASCADE"), nullable=True)
#     # doctor = relationship('User', backref="medexams")
#     date_asked = Column(TIMESTAMP(timezone=True),
#                         server_default=text('now()'))
#     date_run = Column(TIMESTAMP(timezone=True),
#                       server_default=text('now()'))
#     date_received = Column(TIMESTAMP(timezone=True),
#                            server_default=text('now()'))
#     result = Column(String, nullable=True)
#     units = Column(String, nullable=True)
#     interval = Column(String, nullable=True)


# Admission-----------------------------
class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    genre = Column(String, nullable=True)
    name = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)


class Admission(Base):
    __tablename__ = 'admissions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
    room_id = Column(Integer, ForeignKey(
        'rooms.id', ondelete="CASCADE"), nullable=True)
    room = relationship('Room', backref="admissions")
    genre = Column(String, nullable=True)
    note = Column(String, nullable=True)
    cause = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    is_pending = Column(Boolean, nullable=False, server_default='True')
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="admissions")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="admissions")


class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    updated_on = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    allergies = Column(String, nullable=True)
    ailments = Column(String, nullable=True)
    treatments = Column(String, nullable=True)
    tests = Column(String, nullable=True)
    current_state = Column(String, nullable=True)
    #
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="medical_records")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="medical_records")
