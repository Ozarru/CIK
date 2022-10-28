from ..config.database import Base
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    sec_level = Column(Integer, server_default='0', nullable=False)


class SubRole(Base):
    __tablename__ = 'subroles'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, nullable=False)
    sec_level = Column(Integer, server_default='0', nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, server_default='FALSE', nullable=False)
    reg_date = Column(TIMESTAMP(timezone=True),
                      server_default=text('now()'))
    last_login = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    role_id = Column(Integer, ForeignKey(
        'roles.id', ondelete="CASCADE"), nullable=True)
    role = relationship('Role', backref="users")
    subrole_id = Column(Integer, ForeignKey(
        'subroles.id', ondelete="CASCADE"), nullable=True)
    subrole = relationship('SubRole', backref="users")


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    # code = Column(String, nullable=False)
    title = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    matrimony = Column(String, nullable=True)
    reg_date = Column(TIMESTAMP(timezone=True),
                      server_default=text('now()'))
    # parameters
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    peculiarities = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
    history = Column(String, nullable=True)
    # contact info
    email = Column(String, unique=True, nullable=True)
    tel = Column(String, unique=True, nullable=True)
    cel = Column(String, unique=True, nullable=True)
    address = Column(String, nullable=True)
