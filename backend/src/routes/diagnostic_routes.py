from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.orm import Session
from schemas.diagnostic_schema import DiagnosticForm
from database.db import get_db
from services.diagnostics.diagnostic_service import save_manual_diagnostic
from utils.security import get_current_user
from models.user import User
from models.diagnostics import Diagnostic
from datetime import datetime
from fastapi.responses import FileResponse
from services.diagnostics.report_generator import generate_pdf_report, find_folder_by_patient_id
import traceback, os, shutil

router = APIRouter(
    prefix="/diagnostic",
    tags=["diagnostic"]
)


@router.post("/save")
def save_diagnostic(
    form: DiagnosticForm,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return save_manual_diagnostic(db, form, current_user.id)
    except Exception as e:
        print("Error al guardar diagnóstico:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al guardar el diagnóstico")


@router.post("/upload_manual_segmentation")
async def upload_manual_segmentation(
    patient_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Generar folder_id con fecha y paciente
        today = datetime.now().strftime("%Y-%m-%d")
        folder_name = f"{today}_{patient_id}"
        manual_dir = os.path.join("src/uploads", folder_name, "manual")
        os.makedirs(manual_dir, exist_ok=True)

        # Guardar el archivo como manual_seg.nii.gz
        manual_path = os.path.join(manual_dir, "manual_seg.nii.gz")
        with open(manual_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Actualizar el campo manual_segmentation_path en BD
        diagnostic = db.query(Diagnostic).filter_by(patient_id=patient_id).order_by(Diagnostic.created_at.desc()).first()
        if not diagnostic:
            raise HTTPException(status_code=404, detail="No se encontró diagnóstico para este paciente")

        diagnostic.manual_segmentation_path = manual_path
        db.commit()

        return {
            "message": "Segmentación manual cargada y guardada",
            "path": manual_path
        }

    except Exception as e:
        print("Error al guardar segmentación manual")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.get("/generate_report/{patient_id}")
def generate_report(patient_id: str):
    try:
        pdf_path = generate_pdf_report(patient_id)
        return FileResponse(
            path=pdf_path,
            filename=f"{patient_id}_diagnosis_report.pdf",
            media_type='application/pdf'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
