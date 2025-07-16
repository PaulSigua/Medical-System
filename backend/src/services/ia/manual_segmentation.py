import os, shutil
from datetime import datetime
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models.diagnostics import Diagnostic

def save_manual_segmentation_file(patient_id: str, file: UploadFile, db: Session) -> str:
    diagnostic = (
        db.query(Diagnostic)
        .filter(Diagnostic.patient_id == patient_id)
        .order_by(Diagnostic.created_at.desc())
        .first()
    )
    if not diagnostic:
        raise ValueError("No se encontró diagnóstico para este paciente")

    # Usar el mismo folder_id ya existente
    folder_name = diagnostic.upload_folder_id
    save_dir = os.path.join("src/uploads", folder_name, "manual")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, "manual_seg.nii.gz")
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return save_path


def update_diagnostic_with_manual_segmentation(db: Session, patient_id: str, manual_path: str) -> None:
    diagnostic = (
        db.query(Diagnostic)
        .filter(Diagnostic.patient_id == patient_id)
        .order_by(Diagnostic.created_at.desc())
        .first()
    )
    if not diagnostic:
        raise ValueError("No se encontró diagnóstico para este paciente")

    diagnostic.manual_segmentation_path = manual_path
    db.commit()
