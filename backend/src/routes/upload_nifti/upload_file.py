from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from models.user import User
from typing import List
from utils.security import get_current_user
import traceback, os, re
from services.processing import preprocessing, patient_db, file_handler

router = APIRouter(
    prefix="/upload",
    tags=["upload"]
)

# UPLOAD FILES
# Función robusta para detectar archivos por palabras clave
def find_modality_file(files: List[str], keywords: List[str]) -> str | None:
    for file in files:
        name = os.path.basename(file).lower()
        clean_name = re.sub(r'[^a-z0-9]', '', name)  # elimina guiones, puntos, etc.
        if any(keyword in clean_name for keyword in keywords):
            return file
    return None

def get_current_user_id(
    current_user: User = Depends(get_current_user)) -> int:
    return current_user.id

@router.post("/nifti_files")
async def upload_and_process_files(
    files: List[UploadFile] = File(...),
    patient_id: str = Form(...),
    user_id: int = Depends(get_current_user_id)
):
    try:
        print(f"Subiendo archivos para paciente {patient_id} por usuario {user_id}...")

        # 1. Guardar archivos localmente
        await file_handler.save_uploaded_files(files, patient_id)

        # 2. Obtener todos los archivos guardados del paciente
        uploaded_files = file_handler.list_patient_files(patient_id)  # ⬅ debe retornar lista de rutas

        # 3. Detectar archivos según palabras clave
        t1    = find_modality_file(uploaded_files, ["t1", "t1n"])
        t1c   = find_modality_file(uploaded_files, ["t1c"])
        t2    = find_modality_file(uploaded_files, ["t2", "t2w"])
        flair = find_modality_file(uploaded_files, ["t2f", "flair"])

        if not all([t1, t1c, t2, flair]):
            raise HTTPException(status_code=400, detail="Faltan archivos de modalidades requeridas.")

        print(f"Archivos detectados:\n - T1: {t1}\n - T1c: {t1c}\n - T2: {t2}\n - Flair: {flair}")

        # 4. Guardar rutas en base de datos
        patient_db.update_patient_paths(patient_id, user_id, t1c, t2, flair, t1)
        print("Paths guardados en base de datos.")

        # 5. Procesar imágenes
        t1_img    = preprocessing.load_and_normalize(t1)
        t1c_img   = preprocessing.load_and_normalize(t1c)
        t2_img    = preprocessing.load_and_normalize(t2)
        flair_img = preprocessing.load_and_normalize(flair)

        preprocessing.process_images_for_segmentation(patient_id, t1c_img, t2_img, flair_img)
        preprocessing.process_images_for_classification(patient_id, t1_img, t1c_img, t2_img, flair_img)

        print("Procesamiento completado.")
        return JSONResponse(content={"message": "Archivos procesados correctamente."})

    except Exception as e:
        print(f"Error durante procesamiento:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
