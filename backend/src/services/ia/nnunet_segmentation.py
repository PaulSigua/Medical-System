import os
import tempfile
import subprocess
import nibabel as nib
import numpy as np
import nibabel.processing  # ✅ Necesario para resample_from_to

def perform_segmentation(modality_paths: dict) -> np.ndarray:
    tmp_input = tempfile.mkdtemp()
    tmp_output = tempfile.mkdtemp()

    # Debug shapes
    for key, path in modality_paths.items():
        img = nib.load(path).get_fdata()
        print(f"{key}: {img.shape}")

    # Crear archivos: case_0000_0000.nii.gz → case_0000_0003.nii.gz
    save_modalities_in_order(modality_paths, tmp_input, case_id="case_0000")

    cmd = [
        "nnUNet_predict",
        "-i", tmp_input,
        "-o", tmp_output,
        "-t", "501",
        "-m", "3d_fullres",
        "-f", "0",
        "-tr", "nnUNetTrainerV2",
        "-chk", "model_best",
        "--save_npz",
        "--num_threads_preprocessing", "1",
        "--num_threads_nifti_save", "1"
    ]

    try:
        print("Archivos generados en tmp_input:")
        print(os.listdir(tmp_input))
        subprocess.run(cmd, check=True, capture_output=True, env=os.environ.copy())
    except subprocess.CalledProcessError as e:
        stderr_msg = e.stderr.decode() if e.stderr else "Sin salida de error."
        raise RuntimeError(f"Error en nnUNetv2_predict: {stderr_msg}")

    result_path = os.path.join(tmp_output, "case_0000.nii.gz")
    if not os.path.exists(result_path):
        raise FileNotFoundError(f"Resultado no encontrado: {result_path}")

    result = nib.load(result_path).get_fdata()
    
    print("Modalidades disponibles:", modality_paths.keys())

    # Reescalar al espacio de la imagen original (T2F si está, o T2 si no)
    print("Reescalando la segmentación al espacio de la imagen original...")
    result_img = nib.load(result_path)
    reference_key = "T2F" if "T2F" in modality_paths else "T2"
    reference_img = nib.load(modality_paths[reference_key])
    resampled = nib.processing.resample_from_to(result_img, reference_img)
    result = resampled.get_fdata()

    return np.round(result).astype(np.uint8)


def save_modalities_in_order(modality_paths: dict, output_dir: str, case_id: str):
    os.makedirs(output_dir, exist_ok=True)

    # Orden esperado por BraTS/nnUNet: 0000=FLAIR, 0001=T1, 0002=T1c, 0003=T2
    order = ["FLAIR", "T1", "T1c", "T2"]
    for idx, modality in enumerate(order):
        if modality not in modality_paths:
            raise ValueError(f"Falta la modalidad requerida: {modality}")
        img = nib.load(modality_paths[modality])
        out_path = os.path.join(output_dir, f"{case_id}_{idx:04d}.nii.gz")
        nib.save(img, out_path)
