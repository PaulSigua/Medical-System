import os
import nibabel as nib
import numpy as np
from sklearn.preprocessing import MinMaxScaler

UPLOADS_DIR = "src/uploads"

def normalize(image: np.ndarray) -> np.ndarray:
    scaler = MinMaxScaler()
    return scaler.fit_transform(image.reshape(-1, image.shape[-1])).reshape(image.shape)

def load_nifti(path: str) -> np.ndarray:
    """
    Carga y normaliza un archivo NIfTI dado su path completo.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo NIfTI: {path}")
    print(f"Cargando NIfTI desde: {path}")
    image = nib.load(path).get_fdata()
    return normalize(image)

def load_modality_image(upload_folder_id: str, modality_index: int = 0) -> np.ndarray:
    """
    Carga y normaliza una modalidad por índice (0=FLAIR, 1=T1, 2=T1c, 3=T2) desde nnunet_input/
    """
    path = os.path.join(UPLOADS_DIR, upload_folder_id, "nnunet_input", f"case_0000_000{modality_index}.nii.gz")
    return load_nifti(path)
