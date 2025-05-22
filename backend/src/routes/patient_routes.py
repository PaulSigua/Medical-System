from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.patients import Patient
from models.user import User
from schemas.patient_schema import PatientCreate, PatientOut
from typing import List
from utils.security import get_current_user
import traceback

from services.processing import preprocessing, patient_db, file_handler

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

# UPLOAD FILES

def get_current_user_id(
    current_user: User = Depends(get_current_user)) -> int:
    return current_user.id

@router.post("/upload/files")
async def upload_and_process_files(
    files: List[UploadFile] = File(...),
    patient_id: str = Form(...),
    user_id: int = Depends(get_current_user_id)
):
    try:
        print(f"Subiendo archivos para paciente {patient_id} por usuario {user_id}...")

        # 1. Guardar archivos localmente
        await file_handler.save_uploaded_files(files, patient_id)

        # 2. Verificar si ya existen
        existing_paths = patient_db.get_patient_paths(patient_id, user_id)
        if existing_paths and all(existing_paths):
            print("Archivos ya existen en la base de datos.")
            return JSONResponse(content={"message": "Archivos ya existen."})

        # 3. Obtener archivos subidos
        t1ce = file_handler.get_latest_patient_file(patient_id, "t1c")
        t2   = file_handler.get_latest_patient_file(patient_id, "t2W")
        flair= file_handler.get_latest_patient_file(patient_id, "t2f")
        t1   = file_handler.get_latest_patient_file(patient_id, "t1n")

        if not all([t1ce, t2, flair, t1]):
            raise HTTPException(status_code=400, detail="Faltan archivos de modalidades.")

        print(f"Archivos detectados:\n - T1CE: {t1ce}\n - T2: {t2}\n - FLAIR: {flair}\n - T1: {t1}")

        # 4. Guardar paths en la DB
        patient_db.update_patient_paths(patient_id, user_id, t1ce, t2, flair, t1)
        print("Paths guardados en base de datos.")

        # 5. Cargar y procesar
        t1ce_img = preprocessing.load_and_normalize(t1ce)
        t2_img   = preprocessing.load_and_normalize(t2)
        flair_img= preprocessing.load_and_normalize(flair)
        t1_img   = preprocessing.load_and_normalize(t1)

        preprocessing.process_images_for_segmentation(patient_id, t1ce_img, t2_img, flair_img)
        preprocessing.process_images_for_classification(patient_id, t1_img, t1ce_img, t2_img, flair_img)

        print("Procesamiento completado.")
        return JSONResponse(content={"message": "Archivos procesados correctamente."})

    except Exception as e:
        print(f"Error durante procesamiento:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
