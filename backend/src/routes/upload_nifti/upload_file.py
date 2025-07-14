from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from models.user import User
from typing import List
from utils.security import get_current_user
from services.upload.upload_nifti import save_uploaded_nifti_files

router = APIRouter(
    prefix="/upload",
    tags=["upload"]
)

def get_current_user_id(
    current_user: User = Depends(get_current_user)) -> int:
    return current_user.id

@router.post("/nifti_files")
async def upload_nifti_files(
    patient_id: str = Form(...),
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        folder_path = save_uploaded_nifti_files(patient_id, current_user.id, files)

        return JSONResponse(content={
            "message": "Archivos NIfTI guardados correctamente",
            "upload_folder_id": folder_path.split("src/uploads/")[-1]  # solo la carpeta
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar archivos: {str(e)}")
