from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.patients import Patient
from models.user import User
from schemas.patient_schema import PatientCreate, PatientOut
from fastapi import Query
from typing import List
from utils.security import get_current_user

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

# Dependency para obtener la sesión de la DB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    # <-- usa al usuario logueado
    current_user: User = Depends(get_current_user)
):
    patient_exist = db.query(Patient).filter(
        Patient.user_id == current_user.id,
        Patient.patient_id == patient_data.patient_id  # clave
    ).first()

    if patient_exist:
        raise HTTPException(status_code=409, detail="El paciente ya existe")

    new_patient = Patient(
        user_id=current_user.id,  # <-- usa el ID correcto
        patient_id=patient_data.patient_id,
        numero_historia_clinica=patient_data.numero_historia_clinica,
        # survey_completed=False,
        # t1ce_path="",
        # t2_path="",
        # flair_path="",
        # predicted_segmentation="",
        # graph1_path="",
        # graph2_path="",
        # graph3_path="",
        # graph4_path="",
        # graph5_path="",
        # graph6_path="",
        # graph_segmentation_path="",
        # t1_path=""
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {"message": "Paciente registrado correctamente."}


@router.get("/", response_model=List[PatientOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(Patient).all()


# <- indica que devolverás una lista de schemas
@router.get("/me", response_model=list[PatientOut])
def get_my_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # print(current_user)
    patients = db.query(Patient).filter(
        Patient.user_id == current_user.id).all()
    return patients


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient_id(
    patient_id: str,
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(
        Patient.patient_id == patient_id).first()
    return patient