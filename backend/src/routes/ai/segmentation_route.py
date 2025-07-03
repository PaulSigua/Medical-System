from fastapi import APIRouter, UploadFile, Form
from typing import Dict
import shutil
import os
from services.ia.segmentation_service import perform_segmentation, generate_segmentation_3d_plot

router = APIRouter(
    prefix="/ai-segmentation",
    tags=["ai-segmentation"]
)

@router.post("/segmentation")
async def segment_patient(
    patient_id: str = Form(...),
    T1c: UploadFile = Form(...),
    T2W: UploadFile = Form(...),
    T2F: UploadFile = Form(...)
):
    # Guardar temporalmente los archivos
    upload_dir = f"src/uploads/{patient_id}"
    os.makedirs(upload_dir, exist_ok=True)

    modality_files = {"T1c": T1c, "T2W": T2W, "T2F": T2F}
    paths = {}

    for key, file in modality_files.items():
        dest = os.path.join(upload_dir, file.filename)
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        paths[key] = dest

    # Segmentar
    segmentation = perform_segmentation(paths)

    # Generar HTML 3D
    html_path = generate_segmentation_3d_plot(segmentation, patient_id)

    return {
        "success": True,
        "patient_id": patient_id,
        "segmentation_html": html_path.replace("src/", "/static/")
    }
