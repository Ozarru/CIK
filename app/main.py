from fastapi import FastAPI

from .routers.finances import cashdesk, patient_cash_transactions

from .routers import auth
from .routers.activities import appointments, admissions, bills, certifications, consultations, pay_salaries, pay_wages, external_rx
from .routers.parameters import roles, specialties, accessories, insurances, insurance_tiers, comodities, medications, rooms, salaries, wages, med_diagnostics, med_imageries, med_operations, med_records, med_tests, med_therapies, consultation_genres
from .routers.persons import admins, patients, staff, users, doctors
from .config import config
from fastapi.middleware.cors import CORSMiddleware

# # creates tables based on models on first run if the table doesn't exist yet
# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

print(config.settings.database_name)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# -----------Routes-------------------------------------------------------------------

# -------------authentication---------
app.include_router(auth.router)
# -------------Users----------------
app.include_router(users.router)
app.include_router(admins.router)
app.include_router(staff.router)
app.include_router(patients.router)
app.include_router(doctors.router)
# -------------activities---------------------
app.include_router(appointments.router)
app.include_router(admissions.router)
app.include_router(bills.router)
app.include_router(certifications.router)
app.include_router(consultations.router)
app.include_router(specialties.router)
app.include_router(external_rx.router)
# -------------medical stuf---------------------
app.include_router(med_tests.router)
# app.include_router(med_records.router)
# app.include_router(med_therapies.router)
# app.include_router(med_imageries.router)
# app.include_router(med_operations.router)
# app.include_router(med_diagnostics.router)
# -------------personnel payments----------------
app.include_router(pay_salaries.router)
app.include_router(pay_wages.router)
# -------------parameters----------------
app.include_router(accessories.router)
app.include_router(consultation_genres.router)
app.include_router(insurances.router)
app.include_router(insurance_tiers.router)
app.include_router(cashdesk.router)
app.include_router(med_diagnostics.router)
app.include_router(med_imageries.router)
app.include_router(med_operations.router)
app.include_router(med_tests.router)
app.include_router(med_therapies.router)
app.include_router(medications.router)
# app.include_router(pharmacies.router)
app.include_router(roles.router)
app.include_router(rooms.router)
app.include_router(salaries.router)
app.include_router(specialties.router)
app.include_router(wages.router)
# -------------parameters----------------
app.include_router(comodities.router)
# -------------finances----------------
app.include_router(cashdesk.router)
app.include_router(patient_cash_transactions.router)


@app.get("/")
async def root():
    return {"message": "Clinique International Kodome (CIK)"}
