from fastapi import APIRouter, Form, HTTPException, Query
from fastapi.responses import JSONResponse
import os, traceback, json
from services.ai.nnunet_segmentation import perform_segmentation_from_folder
from services.ai.plot_generator import (
    generate_segmentation_slice_html,
    generate_modalities_segmentation_png,
    plot_class_distribution,
    generate_comparison_html,
    generate_gradcam_overlay_html
)

from utils.nifti_utils import load_nifti
from services.ai.openai import build_explanation_prompt, explain_prediction_with_gpt
from services.ai.grad_cam_generator import generate_gradcam_nifti

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
        # Limpiar el folder_id
        clean_folder_name = upload_folder_id.replace("/nnunet_input", "").replace("\\nnunet_input", "")
        input_dir = os.path.join("src", "uploads", clean_folder_name, "nnunet_input")
        if not os.path.exists(input_dir):
            raise HTTPException(status_code=400, detail=f"Directorio {input_dir} no existe")

        html_output_dir = os.path.join("src/static", clean_folder_name, "html")
        os.makedirs(html_output_dir, exist_ok=True)

        # 1. Segmentación
        segmentation, metrics = perform_segmentation_from_folder(input_dir)

        # 2. Grad-CAM
        cam_stats = None
        try:
            _, cam, t1c, cam_stats = generate_gradcam_nifti(
                patient_id="desconocido",
                upload_folder=clean_folder_name
            )
            gradcam_html = generate_gradcam_overlay_html(cam, t1c, clean_folder_name)
            with open(os.path.join(html_output_dir, "gradcam_overlay.html"), "w", encoding="utf-8") as f:
                f.write(gradcam_html)
        except Exception as e:
            print("⚠ Grad-CAM no generado:", str(e))

        # 3. Explicación GPT (con Grad-CAM si se pudo)
        explanation = None
        try:
            prompt = build_explanation_prompt(
                patient_id="desconocido",
                metrics=metrics,
                gradcam_stats=cam_stats  # ✅ nuevo argumento
            )
            explanation = explain_prediction_with_gpt(prompt)
        except Exception as e:
            print("⚠ No se pudo generar explicación:", str(e))

        # 4. HTML Plot principal
        flair_path = os.path.join(input_dir, "case_0000_0000.nii.gz")
        t1c_img = load_nifti(flair_path)
        html_content = generate_segmentation_slice_html(t1c_img, segmentation, clean_folder_name)
        with open(os.path.join(html_output_dir, "segmentation_result.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

        # 5. Imagen resumen
        # 4. HTML Plot principal
        flair_path = os.path.join(input_dir, "case_0000_0002.nii.gz")
        t1c_img = load_nifti(flair_path)
        html_content = generate_segmentation_slice_html(t1c_img, segmentation, clean_folder_name)
        with open(os.path.join(html_output_dir, "segmentation_result.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

        # 5. Imagen resumen (por modalidad con segmentación)
        modalities = {
            "T1": load_nifti(os.path.join(input_dir, "case_0000_0001.nii.gz")),
            "T1c": t1c_img,
            "T2": load_nifti(os.path.join(input_dir, "case_0000_0003.nii.gz")),
            "Flair": load_nifti(os.path.join(input_dir, "case_0000_0000.nii.gz")),
        }
        generate_modalities_segmentation_png(
            modalities=modalities,
            mask=segmentation,
            output_path=os.path.join(html_output_dir, "segmentation_summary.png")
        )


        # 6. Distribución de clases
        plot_class_distribution(segmentation, os.path.join(html_output_dir, "class_distribution.png"))

        # 7. Guardar summary.json
        summary_path = os.path.join(html_output_dir, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump({**metrics, "explanation": explanation}, f, indent=2)

        return JSONResponse({"results": "ok"})

    except Exception as e:
        print("EXCEPCIÓN EN SEGMENTACIÓN")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en segmentación: {str(e)}")


@router.get("/load_results/{folder_id}")
def load_segmentation_results(folder_id: str):
    try:
        if "/" in folder_id or "\\" in folder_id:
            raise HTTPException(status_code=400, detail="folder_id inválido")

        # Limpiar si viene con nnunet_input de más
        clean_folder = folder_id.replace("/nnunet_input", "").replace("\\nnunet_input", "")

        # Carpeta HTML directa
        html_base = os.path.join("src/static", clean_folder, "html")
        metrics_path = os.path.join(html_base, "summary.json")

        if not os.path.exists(metrics_path):
            raise HTTPException(status_code=404, detail="No se encontró summary.json")

        with open(metrics_path, "r", encoding="utf-8") as f:
            summary = json.load(f)

        return {
            "segmentation_url": f"/static/{clean_folder}/html/segmentation_result.html",
            "summary_image_url": f"/static/{clean_folder}/html/segmentation_summary.png",
            "class_distribution_url": f"/static/{clean_folder}/html/class_distribution.png",
            "gradcam_url": f"/static/{clean_folder}/html/gradcam_overlay.html",  # ✅ NUEVO
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
