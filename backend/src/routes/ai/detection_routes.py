from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse
import os, shutil
from services.ia.segmentation_dispatcher import perform_segmentation_dispatcher
from services.ia.plot_generator import generate_segmentation_slice_html
from utils.nifti_utils import load_modality_image

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

@router.post("/segmentation")
async def segment_patient(
    patient_id: str = Form(...),
    framework: str = Form("nnunet"),
    FLAIR: UploadFile = Form(...),
    T1: UploadFile = Form(...),
    T1c: UploadFile = Form(...),
    T2: UploadFile = Form(...)
):
    upload_dir = f"src/uploads/{patient_id}"
    os.makedirs(upload_dir, exist_ok=True)

    # Guardar archivos
    modality_files = {"FLAIR": FLAIR, "T1": T1, "T1c": T1c, "T2": T2}
    paths = {}
    for key, file in modality_files.items():
        dest = os.path.join(upload_dir, file.filename)
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        paths[key] = dest

    # Segmentación
    segmentation = perform_segmentation_dispatcher(paths, framework)

    # Visualización opcional
    modality_img = load_modality_image(patient_id, ["T2", "t2"])  # o FLAIR si lo prefieres
    html_content = generate_segmentation_slice_html(modality_img, segmentation, patient_id)

    output_dir = os.path.join("src/static", patient_id, "html")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "segmentation_result.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return JSONResponse(content={"segmentation_url": f"/static/{patient_id}/html/segmentation_result.html"})
