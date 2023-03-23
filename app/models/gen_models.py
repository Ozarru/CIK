from sqlite3 import Date, Time
from ..config.database import Base
from datetime import date, datetime, time, timezone
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .user_models import *
from .pharm_models import *
from .fin_models import *
# from .ops_models import *


class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    # date = Column(Date(), nullable=True)
    # time = Column(Time(), nullable=True)
    day = Column(String, nullable=False)
    time = Column(String, nullable=False)
    patient_name = Column(String, nullable=False)
    patient_tel = Column(String, nullable=False)
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    doctor = relationship('User', backref="appointments")
    is_pending = Column(Boolean, nullable=False, server_default='True')
    date_booked = Column(TIMESTAMP(timezone=True),
                         server_default=text('now()'))


class ConsultationGenre(Base):
    __tablename__ = 'consultation_genres'
    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    parameters = Column(String, nullable=True)


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
    genre_id = Column(Integer, ForeignKey(
        'consultation_genres.id', ondelete="CASCADE"), nullable=True)
    genre = relationship('ConsultationGenre', backref="consultations")


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
class Ordinance(Base):
    __tablename__ = 'ordinances'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
    note = Column(String, nullable=True)
    medicaments = relationship("Medicament", backref="ordinances")
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="ordinances")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="ordinances")


class Medicament(Base):
    __tablename__ = 'medicaments'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    qsp = Column(String, nullable=True)
    boxes = Column(Integer, nullable=True)
    dosage = Column(String, nullable=True)
    ailments = Column(String, nullable=True)
    medication = Column(String, nullable=True)
    ordinance_id = Column(Integer, ForeignKey("ordinances.id"))


# Medical procedures------------------
class MedDiagnostic(Base):
    __tablename__ = 'med_diagnostics'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    sessions = Column(String, nullable=True)


class MedTherapy(Base):
    __tablename__ = 'med_therapies'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    sessions = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)


class MedTest(Base):
    __tablename__ = 'med_tests'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=True)
    description = Column(String, nullable=True)


class MedImagery(Base):
    __tablename__ = 'med_imageries'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=True)
    description = Column(String, nullable=True)


class MedOperation(Base):
    __tablename__ = 'med_operations'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    anaestesia_genre = Column(String, nullable=True)
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
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    beds = Column(Integer, nullable=True, server_default='0')


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
    cause = Column(String, nullable=False)
    duration = Column(Integer, nullable=True)
    is_pending = Column(Boolean, nullable=False, server_default='True')
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="admissions")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="admissions")
    is_pending = Column(Boolean, nullable=False, server_default='True')


class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    updated_on = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    allergies = Column(String, nullable=True)
    ailments = Column(String, nullable=True)
    treatments = Column(String, nullable=True)
    tests = Column(String, nullable=True)
    peculiarity = Column(String, nullable=True)
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="medical_records")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="medical_records")
