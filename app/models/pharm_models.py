from ..config.database import Base
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Pharmacy (Base):
    __tablename__ = 'pharmacies'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=True)


class Lot (Base):
    __tablename__ = 'lots'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class Medication (Base):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    maker = Column(String, nullable=False)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Integer, nullable=False)
    notice = Column(String, nullable=True)
    alternatives = Column(String, nullable=True)
    ailments = Column(String, nullable=True)
    date_added = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    produced_on = Column(TIMESTAMP(timezone=True), nullable=True)
    expires_on = Column(TIMESTAMP(timezone=True), nullable=True)
    lot_id = Column(Integer, ForeignKey(
        'lots.id', ondelete="CASCADE"), nullable=True)
    lot = relationship('Lot', backref="medications")


class Accessory(Base):
    __tablename__ = 'accessories'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    maker = Column(String, nullable=True)
    name = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Integer, nullable=False)
    date_added = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    produced_on = Column(TIMESTAMP(timezone=True), nullable=True)
    expires_on = Column(TIMESTAMP(timezone=True), nullable=True)
    lot_id = Column(Integer, ForeignKey(
        'lots.id', ondelete="CASCADE"), nullable=True)
    lot = relationship('Lot', backref="accessories")


# RX management-----------------------
class ExternalRx(Base):
    __tablename__ = 'external_rx'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    prescriptions = Column(String, nullable=False)
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="external_rx")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="external_rx")


class Prescription(Base):
    __tablename__ = 'prescriptions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
    note = Column(String, nullable=True)
    treatment = Column(String, nullable=True)
    status = Column(String, nullable=True)
    # drugs = relationship("RxLine", backref="prescriptions")
    doctor_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    doctor = relationship('User', backref="prescriptions")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="prescriptions")


class RxLine(Base):
    __tablename__ = 'rx_lines'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    qsp = Column(String, nullable=True)
    boxes = Column(Integer, nullable=True)
    dosage = Column(String, nullable=True)
    ailments = Column(String, nullable=True)
    medication_id = Column(Integer, ForeignKey(
        'medications.id', ondelete="CASCADE"), nullable=True)
    medication = relationship('Medication', backref="rx_lines")
    prescription_id = Column(Integer, ForeignKey(
        "prescriptions.id", ondelete="CASCADE"), nullable=True)
    prescription = relationship('Prescription', backref="rx_lines")
