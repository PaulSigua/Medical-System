import os
import subprocess
import nibabel as nib
import numpy as np
import json
from nibabel.processing import resample_from_to
from services.ai.metrics import load_nnunet_metrics

def extract_dice_scores_from_summary(summary_path: str) -> dict:
    with open(summary_path, "r") as f:
        data = json.load(f)

    dice_per_class = {
        "ET_Dice": [],
        "WT_Dice": [],
        "TC_Dice": []
    }

    for result in data.get("results", {}).get("all", []):
        for class_id, label_name in zip(["1", "2", "3"], ["ET_Dice", "WT_Dice", "TC_Dice"]):
            class_result = result.get(class_id, {})
            dice = class_result.get("Dice", None)
            if dice is not None and not isinstance(dice, str) and not np.isnan(dice):
                dice_per_class[label_name].append(dice)

    return {
        key: float(np.mean(vals)) if vals else None
        for key, vals in dice_per_class.items()
    }

def clean_metrics(raw_metrics: dict) -> dict:
    dice_score = {
        "whole_tumor (WT)": None,
        "tumor_core (TC)": None,
        "enhancing_tumor (ET)": None
    }
    hausdorff_95 = {"WT": None, "TC": None, "ET": None}
    all_metrics = {}

    id_to_label = {
        "1": "enhancing_tumor (ET)",
        "2": "whole_tumor (WT)",
        "3": "tumor_core (TC)"
    }

    try:
        for label_id, label_name in id_to_label.items():
            label_data = raw_metrics.get("mean", {}).get(label_id, {})
            cleaned_metrics = {}
            for metric_name, value in label_data.items():
                if isinstance(value, float) and np.isnan(value):
                    cleaned_metrics[metric_name] = None
                else:
                    cleaned_metrics[metric_name] = float(value) if isinstance(value, (float, int)) else value

            all_metrics[label_name] = cleaned_metrics
            dice_score[label_name] = cleaned_metrics.get("Dice")
            hausdorff_95[label_name.split()[0]] = cleaned_metrics.get("Hausdorff Distance (95%)")

        return {
            "dice_score": dice_score,
            "hausdorff_95": hausdorff_95,
            "all_metrics": all_metrics
        }
    except Exception as e:
        return {"error": f"Error limpiando métricas: {str(e)}"}

def perform_segmentation_from_folder(
    nnunet_input_dir: str,
    case_id: str = "case_0000"
) -> tuple[np.ndarray, dict | None]:
    for i in range(4):
        path = os.path.join(nnunet_input_dir, f"{case_id}_{i:04d}.nii.gz")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Falta la modalidad: {path}")

    eval_root = os.path.join(nnunet_input_dir, "evaluation")
    pred_dir = os.path.join(eval_root, "pred")
    ref_dir = os.path.join(eval_root, "ref")
    os.makedirs(pred_dir, exist_ok=True)
    os.makedirs(ref_dir, exist_ok=True)

    pred_path = os.path.join(pred_dir, f"{case_id}.nii.gz")
    ref_path = os.path.join(ref_dir, f"{case_id}.nii.gz")

    subprocess.run([
        "nnUNet_predict",
        "-i", nnunet_input_dir,
        "-o", pred_dir,
        "-t", "501",
        "-m", "3d_fullres",
        "-f", "0",
        "-tr", "nnUNetTrainerV2",
        "-chk", "model_best",
        "--save_npz"
    ], check=True, capture_output=True, env=os.environ.copy())

    if not os.path.exists(pred_path):
        raise FileNotFoundError(f"No se generó predicción en: {pred_path}")

    pred_img = nib.load(pred_path)
    pred_data = pred_img.get_fdata()

    flair_path = os.path.join(nnunet_input_dir, f"{case_id}_0000.nii.gz")
    flair_img = nib.load(flair_path)
    if pred_data.shape != flair_img.shape:
        pred_img = resample_from_to(pred_img, flair_img)
        pred_data = pred_img.get_fdata()
        nib.save(nib.Nifti1Image(pred_data, flair_img.affine), pred_path)

    print(f"Predicción guardada en: {pred_path}")
    # print("Etiquetas únicas en predicción:", np.unique(pred_data))

    gt_reference_path = "/media/mateo/8AF48D20F48D0F9D/Users/mateo/Desktop/U/Octavo_Ciclo/Tesis/nnUNet_trained_models/nnUNet/3d_fullres/Task501_BrainTumour/nnUNetTrainerV2__nnUNetPlansv2.1/gt_niftis/BRATS_006.nii.gz"
    if not os.path.exists(gt_reference_path):
        # print("⚠ Ground truth real no encontrado.")
        return np.round(pred_data).astype(np.uint8), None

    gt_img = nib.load(gt_reference_path)
    gt_data = gt_img.get_fdata()

    # print("Etiquetas únicas en GT:", np.unique(gt_data))

    if gt_img.shape != pred_data.shape:
        # print(f"Reescalando GT de {gt_img.shape} → {pred_data.shape}")
        gt_img = resample_from_to(gt_img, pred_img)
        gt_data = gt_img.get_fdata()

    if np.count_nonzero(gt_data) == 0:
        # print("GT sin etiquetas. Saltando evaluación.")
        return np.round(pred_data).astype(np.uint8), {
            "error": "El ground truth no contiene etiquetas distintas de cero"
        }

    nib.save(nib.Nifti1Image(gt_data, flair_img.affine), ref_path)
    print(f"Ground truth real copiado desde {gt_reference_path} a {ref_path}")

    # Métricas
    metrics = {
        "dice_score": {},
        "hausdorff_95": {},
        "all_metrics": {},
        "official_dice": {}
    }

    try:
        # Ejecutar evaluación
        result = subprocess.run([
            "nnUNet_evaluate_folder",
            "-ref", ref_dir,
            "-pred", pred_dir,
            "-l", "1", "2", "3"
        ], capture_output=True, text=True)

        # print("STDOUT evaluación:\n", result.stdout)
        # print("⚠ STDERR evaluación:\n", result.stderr)

        summary_path = os.path.join(pred_dir, "summary.json")
        if os.path.exists(summary_path):
            print(f"Leyendo métricas desde: {summary_path}")
            with open(summary_path, "r") as f:
                data = json.load(f)

            mean = data.get("results", {}).get("mean", {})
            id_to_label = {
                "1": "enhancing_tumor (ET)",
                "2": "whole_tumor (WT)",
                "3": "tumor_core (TC)"
            }

            dice_score = {}
            hausdorff_95 = {}
            all_metrics = {}

            for class_id, label in id_to_label.items():
                class_metrics = mean.get(class_id, {})
                cleaned = {
                    k: (None if isinstance(v, float) and np.isnan(v) else v)
                    for k, v in class_metrics.items()
                }
                all_metrics[label] = cleaned
                dice_score[label] = cleaned.get("Dice")
                hausdorff_95[label.split()[0]] = cleaned.get("Hausdorff Distance (95%)")

            metrics["dice_score"] = dice_score
            metrics["hausdorff_95"] = hausdorff_95
            metrics["all_metrics"] = all_metrics

            print("Métricas del summary.json extraídas correctamente.")
        else:
            print("summary.json no fue generado.")
            metrics["error"] = "summary.json no generado"

    except Exception as e:
        print("⚠ Error general al extraer métricas:", str(e))
        metrics["error"] = str(e)


    # Métricas de validación general
    summary_val_path = "/media/mateo/8AF48D20F48D0F9D/Users/mateo/Desktop/U/Octavo_Ciclo/Tesis/nnUNet_trained_models/nnUNet/3d_fullres/Task501_BrainTumour/nnUNetTrainerV2__nnUNetPlansv2.1/fold_0/validation_raw/summary.json"
    if os.path.exists(summary_val_path):
        official_dice = extract_dice_scores_from_summary(summary_val_path)
        metrics["official_dice"] = official_dice

    return np.round(pred_data).astype(np.uint8), metrics
