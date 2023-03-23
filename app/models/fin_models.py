from ..config.database import Base
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .user_models import *


class Comodity(Base):
    __tablename__ = 'comodities'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)

    name = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    date_added = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))

# should delete this bill model in due time.


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
    due = Column(Integer, nullable=False)
    is_paid = Column(Boolean, nullable=False, server_default='False')
    comodity_id = Column(Integer, ForeignKey(
        'comodities.id', ondelete="CASCADE"), nullable=True)
    comodity = relationship('Comodity', backref="bills")
    insurance_tier_id = Column(Integer, ForeignKey(
        'insurance_tiers.id', ondelete="CASCADE"), nullable=True, server_default='0')
    insurance_tier = relationship('InsuranceTier', backref="bills")
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


# insurance-------------------------------------------------------------
class Insurance(Base):
    __tablename__ = 'insurances'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    overview = Column(String, nullable=True)


class InsuranceTier(Base):
    __tablename__ = 'insurance_tiers'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    percentage = Column(Float, nullable=True)
    ceiling = Column(Integer, nullable=True)
    custom_price = Column(Integer, nullable=True)
    overview = Column(String, nullable=True)
    insurance_id = Column(Integer, ForeignKey(
        "insurances.id", ondelete="CASCADE"), nullable=False)
    insurance = relationship("Insurance", backref="insurance_tiers")


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    overview = Column(String, nullable=True)
    insurance_id = Column(Integer, ForeignKey(
        "insurances.id", ondelete="CASCADE"), nullable=True)
    insurance = relationship("Insurance", backref="companies")


# accounts-------------------------------------------------------------
class Cashdesk(Base):
    __tablename__ = 'cashdesks'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    overview = Column(String, nullable=True)
    credit = Column(Integer, nullable=True)
    debit = Column(Integer, nullable=True)
    balance = Column(Integer, nullable=True)


class CashdeskComment(Base):
    __tablename__ = 'cashdesk_comments'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey(
        'cashdesks.id', ondelete="CASCADE"), nullable=True)
    account = relationship('Cashdesk', backref="cashdesk_comments")
    author_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    author = relationship('User', backref="cashdesk_comments")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class MomoAccount(Base):
    __tablename__ = 'momo_accounts'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    number = Column(String, unique=True, nullable=False)
    carrier = Column(String, nullable=False)
    overview = Column(String, nullable=True)
    credit = Column(Integer, nullable=True)
    debit = Column(Integer, nullable=True)
    balance = Column(Integer, nullable=True)


class MomoComment(Base):
    __tablename__ = 'momo_comments'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey(
        'momo_accounts.id', ondelete="CASCADE"), nullable=True)
    account = relationship('MomoAccount', backref="momo_comments")
    author_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    author = relationship('User', backref="momo_comments")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class Bank(Base):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    acc_number = Column(String, unique=True, nullable=False)
    overview = Column(String, nullable=True)
    credit = Column(Integer, nullable=True)
    debit = Column(Integer, nullable=True)
    balance = Column(Integer, nullable=True)


class BankComment(Base):
    __tablename__ = 'bank_comments'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey(
        'banks.id', ondelete="CASCADE"), nullable=True)
    account = relationship('Bank', backref="bank_comments")
    author_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    author = relationship('User', backref="bank_comments")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))

# patient transactions-------------------------------------------------------------


class PatientBankTransaction(Base):
    __tablename__ = 'patient_bank_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    overview = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    comodity_id = Column(Integer, ForeignKey(
        'comodities.id', ondelete="CASCADE"), nullable=True)
    comodity = relationship('Comodity', backref="patient_bank_transactions")
    insurance_tier_id = Column(Integer, ForeignKey(
        'insurance_tiers.id', ondelete="CASCADE"), nullable=True, server_default='0')
    insurance_tier = relationship(
        'InsuranceTier', backref="patient_bank_transactions")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="patient_bank_transactions")
    genre = Column(String, nullable=False)
    bank_id = Column(Integer, ForeignKey(
        'banks.id', ondelete="CASCADE"), nullable=True)
    bank = relationship('Bank', backref="patient_bank_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class PatientMobileTransaction(Base):
    __tablename__ = 'patient_mobile_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    overview = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    comodity_id = Column(Integer, ForeignKey(
        'comodities.id', ondelete="CASCADE"), nullable=True)
    comodity = relationship('Comodity', backref="patient_mobile_transactions")
    insurance_tier_id = Column(Integer, ForeignKey(
        'insurance_tiers.id', ondelete="CASCADE"), nullable=True, server_default='0')
    insurance_tier = relationship(
        'InsuranceTier', backref="patient_mobile_transactions")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="patient_mobile_transactions")
    genre = Column(String, nullable=False)
    momo_id = Column(Integer, ForeignKey(
        'momo_accounts.id', ondelete="CASCADE"), nullable=True)
    momo_account = relationship(
        'MomoAccount', backref="patient_mobile_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class PatientCashTransaction(Base):
    __tablename__ = 'patient_cash_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    overview = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    comodity_id = Column(Integer, ForeignKey(
        'comodities.id', ondelete="CASCADE"), nullable=True)
    comodity = relationship('Comodity', backref="patient_cash_transactions")
    insurance_tier_id = Column(Integer, ForeignKey(
        'insurance_tiers.id', ondelete="CASCADE"), nullable=True, server_default='0')
    insurance_tier = relationship(
        'InsuranceTier', backref="patient_cash_transactions")
    patient_id = Column(Integer, ForeignKey(
        'patients.id', ondelete="CASCADE"), nullable=True)
    patient = relationship('Patient', backref="patient_cash_transactions")
    genre = Column(String, nullable=False)
    cashdesk_id = Column(Integer, ForeignKey(
        'cashdesks.id', ondelete="CASCADE"), nullable=True)
    cashdesk = relationship('Cashdesk', backref="patient_cash_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


# users transactions-------------------------------------------------------------
class UserBankTransaction(Base):
    __tablename__ = 'user_bank_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    overview = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    user = relationship('User', backref="user_bank_transactions")
    genre = Column(String, nullable=False)
    bank_id = Column(Integer, ForeignKey(
        'banks.id', ondelete="CASCADE"), nullable=True)
    bank = relationship('Bank', backref="user_bank_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class UserMobileTransaction(Base):
    __tablename__ = 'user_mobile_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    overview = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    user = relationship('User', backref="user_mobile_transactions")
    genre = Column(String, nullable=False)
    momo_id = Column(Integer, ForeignKey(
        'momo_accounts.id', ondelete="CASCADE"), nullable=True)
    momo_account = relationship(
        'MomoAccount', backref="user_mobile_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class UserCashTransaction(Base):
    __tablename__ = 'user_cash_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    overview = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=True)
    user = relationship('User', backref="user_cash_transactions")
    genre = Column(String, nullable=False)
    cashdesk_id = Column(Integer, ForeignKey(
        'cashdesks.id', ondelete="CASCADE"), nullable=True)
    cashdesk = relationship('Cashdesk', backref="user_cash_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


# other transactions-------------------------------------------------------------
class OtherBankTransaction(Base):
    __tablename__ = 'other_bank_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    persona = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    motive = Column(String, nullable=True)
    description = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    genre = Column(String, nullable=False)
    bank_id = Column(Integer, ForeignKey(
        'banks.id', ondelete="CASCADE"), nullable=True)
    bank = relationship('Bank', backref="other_bank_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class OtherMobileTransaction(Base):
    __tablename__ = 'other_mobile_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    persona = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    motive = Column(String, nullable=True)
    description = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    genre = Column(String, nullable=False)
    momo_id = Column(Integer, ForeignKey(
        'momo_accounts.id', ondelete="CASCADE"), nullable=True)
    momo_account = relationship(
        'MomoAccount', backref="other_mobile_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))


class OtherCashTransaction(Base):
    __tablename__ = 'other_cash_transactions'

    id = Column(Integer, primary_key=True,  autoincrement=True, nullable=False)
    persona = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    motive = Column(String, nullable=True)
    description = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    paid = Column(Integer, nullable=True)
    due = Column(Integer, nullable=True)
    genre = Column(String, nullable=False)
    cashdesk_id = Column(Integer, ForeignKey(
        'cashdesks.id', ondelete="CASCADE"), nullable=True)
    cashdesk = relationship('Cashdesk', backref="other_cash_transactions")
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('now()'))
