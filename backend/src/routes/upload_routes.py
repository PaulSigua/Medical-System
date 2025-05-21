from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import List
import os
import shutil

from services.processing.upload_service import process_and_save_hdf5


router = APIRouter(
    prefix="/uploads",
    tags=["uploads"]
)

UPLOAD_FOLDER = "uploads/"  # asegúrate de que esta carpeta exista

@router.post("/file")
async def upload_files(
    patient_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(status_code=400, detail="No se subieron archivos")
    
    saved_files = []
    for file in files:
        filename = file.filename
        if patient_id not in filename:
            filename = f"{patient_id}_{filename}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        saved_files.append(save_path)

    # Procesar y guardar .h5
    try:
        result = process_and_save_hdf5(patient_id)
        return {"message": "Archivos cargados y procesados exitosamente.", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar imágenes: {e}")
