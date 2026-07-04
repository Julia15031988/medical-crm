from fastapi import FastAPI
import app.databasemodels  # noqa: F401
from app.routers.auth_register_login import router as auth_router
from app.routers.patient import router as patient_router


app = FastAPI(title="TEST MAIN WITH PATIENT")

app.include_router(auth_router)
app.include_router(patient_router)


@app.get("/test-patient-router")
async def test_patient_router():
    return {"status": "patient router test"}
