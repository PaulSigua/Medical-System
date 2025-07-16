from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
import os, traceback
from services.ia.nnunet_segmentation import perform_segmentation_from_folder
from services.ia.plot_generator import (
    generate_segmentation_slice_html,
    generate_summary_png,
    plot_class_distribution,
    generate_comparison_html
)

from utils.nifti_utils import load_nifti
from services.ia.openai import build_explanation_prompt, explain_prediction_with_gpt

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
        
        explanation = None
        try:
            prompt = build_explanation_prompt(patient_id="desconocido", metrics=metrics)
            explanation = explain_prediction_with_gpt(prompt)
            print("🧠 Explicación generada:")
            print(explanation)
        except Exception as e:
            print("⚠ No se pudo generar explicación:", str(e))


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
            "metrics": metrics,
            "explanation": explanation
        })

    except Exception as e:
        print("EXCEPCIÓN EN SEGMENTACIÓN")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en segmentación: {str(e)}")


@router.get("/comparison_by_patient_id")
def generate_comparison_by_patient(patient_id: str):
    try:
        base_dir = "src/uploads"
        folders = [
            name for name in os.listdir(base_dir)
            if name.endswith(f"_{patient_id}")
        ]
        if not folders:
            raise HTTPException(status_code=404, detail="No se encontró carpeta del paciente")

        # Carpeta más reciente (YYYY-MM-DD_patient_id)
        latest_folder = sorted(folders, reverse=True)[0]
        folder_path = os.path.join(base_dir, latest_folder)

        flair_path = os.path.join(folder_path, "FLAIR.nii.gz")
        auto_seg_path = os.path.join(folder_path, "nnunet_input", "evaluation", "pred", "case_0000.nii.gz")
        manual_seg_path = os.path.join(folder_path, "manual", "manual_seg.nii.gz")

        for path in [flair_path, auto_seg_path, manual_seg_path]:
            if not os.path.exists(path):
                raise HTTPException(status_code=404, detail=f"No se encontró el archivo: {path}")

        # Cargar archivos NIfTI
        flair = load_nifti(flair_path)
        auto_seg = load_nifti(auto_seg_path)
        manual_seg = load_nifti(manual_seg_path)

        # Generar comparación en HTML
        html_output_dir = os.path.join("src/static", latest_folder, "html")
        os.makedirs(html_output_dir, exist_ok=True)
        out_path = os.path.join(html_output_dir, "comparison_result.html")

        html_content = generate_comparison_html(flair, auto_seg, manual_seg, latest_folder)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return JSONResponse(content={
            "comparison_url": f"/static/{latest_folder}/html/comparison_result.html"
        })

    except Exception as e:
        print("Error en comparación visual")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generando comparación: {str(e)}")