from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
import os, traceback
from services.ia.nnunet_segmentation import perform_segmentation_from_folder
from services.ia.plot_generator import (
    generate_segmentation_slice_html,
    generate_summary_png,
    plot_class_distribution,
)

from utils.nifti_utils import load_nifti

router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

@router.post("/segmentation")
async def segment_patient(
    upload_folder_id: str = Form(...),
    framework: str = Form("nnunet")
):
    try:
        input_dir = os.path.join("src/uploads", upload_folder_id)
        if not os.path.exists(input_dir):
            raise HTTPException(status_code=400, detail=f"Directorio {input_dir} no existe")

        # Carpeta de salida HTML/PNG
        html_output_dir = os.path.join("src/static", upload_folder_id, "html")
        os.makedirs(html_output_dir, exist_ok=True)

        # Segmentar usando los archivos procesados ya guardados
        segmentation, metrics = perform_segmentation_from_folder(input_dir)

        # Visualizar resultado usando FLAIR
        flair_path = os.path.join(input_dir, "case_0000_0000.nii.gz")
        flair_img = load_nifti(flair_path)

        # Generar HTML interactivo
        html_content = generate_segmentation_slice_html(flair_img, segmentation, upload_folder_id)
        html_output_path = os.path.join(html_output_dir, "segmentation_result.html")
        with open(html_output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Generar imagen resumen tipo matplotlib
        summary_png_path = os.path.join(html_output_dir, "segmentation_summary.png")
        generate_summary_png(flair_img, segmentation, summary_png_path)
        
        # Gráfica de distribución de clases
        class_dist_path = os.path.join(html_output_dir, "class_distribution.png")
        plot_class_distribution(segmentation, class_dist_path)

        return JSONResponse(content={
            "segmentation_url": f"/static/{upload_folder_id}/html/segmentation_result.html",
            "summary_image_url": f"/static/{upload_folder_id}/html/segmentation_summary.png",
            "class_distribution_url": f"/static/{upload_folder_id}/html/class_distribution.png",
            "metrics": metrics
        })

    except Exception as e:
        print("EXCEPCIÓN EN SEGMENTACIÓN")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en segmentación: {str(e)}")