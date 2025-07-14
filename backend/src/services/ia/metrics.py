import os
import json

def load_nnunet_metrics(metrics_dir: str) -> dict:
    """
    Carga y parsea las métricas JSON generadas por nnUNet_evaluate_folder.

    :param metrics_dir: Ruta al directorio que contiene el archivo summary.json
    :return: Diccionario con métricas clave de segmentación
    """
    metrics_path = os.path.join(metrics_dir, "summary.json")

    if not os.path.exists(metrics_path):
        raise FileNotFoundError(f"No se encontró el archivo de métricas: {metrics_path}")

    with open(metrics_path, "r", encoding="utf-8") as f:
        summary = json.load(f)

    metrics = {
        "dice_score": {
            "whole_tumor (WT)": summary.get("mean", {}).get("Dice_whole", None),
            "tumor_core (TC)": summary.get("mean", {}).get("Dice_core", None),
            "enhancing_tumor (ET)": summary.get("mean", {}).get("Dice_enhancing", None)
        },
        "hausdorff_95": {
            "WT": summary.get("mean", {}).get("Hausdorff_95_whole", None),
            "TC": summary.get("mean", {}).get("Hausdorff_95_core", None),
            "ET": summary.get("mean", {}).get("Hausdorff_95_enhancing", None)
        }
    }

    return metrics
