from fastapi import FastAPI

from .routers import auth
from .routers.todos import pending_consultations
from .routers.activities import admissions, bills, certifications, consultations, pay_salaries, pay_wages
from .routers.management import accessories, insurances, medications, rooms, salaries, wages, med_diagnostics, med_imageries, med_operations, med_records, med_tests, med_therapies
from .routers.persons import admins, patients, staff
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
app.include_router(admins.router)
app.include_router(staff.router)
app.include_router(patients.router)
# -------------activities---------------------
app.include_router(admissions.router)
app.include_router(bills.router)
app.include_router(certifications.router)
app.include_router(consultations.router)
# -------------things to dos---------------------
app.include_router(pending_consultations.router)
# -------------medical stuf---------------------
app.include_router(med_tests.router)
# app.include_router(med_records.router)
app.include_router(med_therapies.router)
app.include_router(med_imageries.router)
app.include_router(med_operations.router)
app.include_router(med_diagnostics.router)
# -------------personnel payments----------------
app.include_router(pay_salaries.router)
app.include_router(pay_wages.router)
# -------------management----------------
app.include_router(accessories.router)
app.include_router(insurances.router)
app.include_router(medications.router)
app.include_router(rooms.router)
app.include_router(wages.router)
app.include_router(salaries.router)


@app.get("/")
async def root():
    return {"message": "Clinique International Kodome (CIK)"}
