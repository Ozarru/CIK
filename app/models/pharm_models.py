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
