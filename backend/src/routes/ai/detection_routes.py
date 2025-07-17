from fastapi import APIRouter, Form, HTTPException, Query
from fastapi.responses import JSONResponse
import os, traceback, json
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

        # 1. Ejecutar segmentación
        segmentation, metrics = perform_segmentation_from_folder(input_dir)

        # 2. Generar explicación con GPT
        explanation = None
        try:
            prompt = build_explanation_prompt(patient_id="desconocido", metrics=metrics)
            explanation = explain_prediction_with_gpt(prompt)
            print("Explicación generada:")
            # print(explanation)
        except Exception as e:
            print("⚠ No se pudo generar explicación:", str(e))

        # 3. Visualizar resultado usando FLAIR
        flair_path = os.path.join(input_dir, "case_0000_0000.nii.gz")
        flair_img = load_nifti(flair_path)

        # 4. Guardar HTML
        html_content = generate_segmentation_slice_html(flair_img, segmentation, upload_folder_id)
        with open(os.path.join(html_output_dir, "segmentation_result.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

        # 5. Imagen resumen
        generate_summary_png(flair_img, segmentation, os.path.join(html_output_dir, "segmentation_summary.png"))

        # 6. Distribución de clases
        plot_class_distribution(segmentation, os.path.join(html_output_dir, "class_distribution.png"))

        # 7. Guardar summary.json completo
        summary_path = os.path.join(html_output_dir, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump({**metrics, "explanation": explanation}, f, indent=2)

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

@router.get("/load_results/{folder_id}")
def load_segmentation_results(folder_id: str):
    try:
        if "/" in folder_id or "\\" in folder_id:
            raise HTTPException(status_code=400, detail="folder_id inválido")

        html_base = os.path.join("src/static", folder_id, "nnunet_input", "html")
        metrics_path = os.path.join(html_base, "summary.json")

        if not os.path.exists(metrics_path):
            raise HTTPException(status_code=404, detail="No se encontró summary.json")

        with open(metrics_path, "r", encoding="utf-8") as f:
            summary = json.load(f)

        return {
            "segmentation_url": f"/static/{folder_id}/nnunet_input/html/segmentation_result.html",
            "summary_image_url": f"/static/{folder_id}/nnunet_input/html/segmentation_summary.png",
            "class_distribution_url": f"/static/{folder_id}/nnunet_input/html/class_distribution.png",
            "metrics": {
                "dice_score": summary.get("dice_score"),
                "all_metrics": summary.get("all_metrics"),
            },
            "explanation": summary.get("explanation", "")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comparison_by_patient_id")
def generate_comparison_by_patient(
    patient_id: str,
    modality: str = Query("flair", enum=["flair", "t1c"]),
    orientation: str = Query("axial", enum=["axial", "coronal", "sagittal"])
):
    try:
        base_dir = "src/uploads"
        folders = [
            name for name in os.listdir(base_dir)
            if name.endswith(f"_{patient_id}")
        ]
        if not folders:
            raise HTTPException(status_code=404, detail="No se encontró carpeta del paciente")

        latest_folder = sorted(folders, reverse=True)[0]
        folder_path = os.path.join(base_dir, latest_folder)

        flair_path = os.path.join(folder_path, "FLAIR.nii.gz")
        t1c_path = os.path.join(folder_path, "T1c.nii.gz")
        auto_seg_path = os.path.join(folder_path, "nnunet_input", "evaluation", "pred", "case_0000.nii.gz")
        manual_seg_path = os.path.join(folder_path, "manual", "manual_seg.nii.gz")

        for path in [flair_path, t1c_path, auto_seg_path, manual_seg_path]:
            if not os.path.exists(path):
                raise HTTPException(status_code=404, detail=f"No se encontró el archivo: {path}")

        # Cargar archivos
        flair = load_nifti(flair_path)
        t1c = load_nifti(t1c_path)
        auto_seg = load_nifti(auto_seg_path)
        manual_seg = load_nifti(manual_seg_path)

        # Ruta de salida
        html_output_dir = os.path.join("src/static", latest_folder, "html")
        os.makedirs(html_output_dir, exist_ok=True)

        out_path = os.path.join(
            html_output_dir,
            f"comparison_result_{modality}_{orientation}.html"
        )

        html_content = generate_comparison_html(
            flair=flair,
            t1c=t1c,
            auto_seg=auto_seg,
            manual_seg=manual_seg,
            patient_id=latest_folder,
            modality=modality,
            orientation=orientation
        )

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        # print(f"Modality: {modality}, Orientation: {orientation}")

        return JSONResponse(content={
            "comparison_url": f"/static/{latest_folder}/html/comparison_result_{modality}_{orientation}.html"
        })

    except Exception as e:
        print("Error en comparación visual")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generando comparación: {str(e)}")
