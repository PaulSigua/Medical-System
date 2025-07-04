import os
import nibabel as nib
import numpy as np
from sklearn.preprocessing import MinMaxScaler

UPLOADS_DIR = "src/uploads"

def normalize(image: np.ndarray) -> np.ndarray:
    scaler = MinMaxScaler()
    return scaler.fit_transform(image.reshape(-1, image.shape[-1])).reshape(image.shape)

def find_modality_file(patient_id: str, keywords: list[str]) -> str | None:
    """
    Busca un archivo en uploads/{patient_id}/ que contenga alguna palabra clave (insensible a mayúsculas).
    """
    patient_dir = os.path.join(UPLOADS_DIR, patient_id)
    if not os.path.exists(patient_dir):
        return None

    for filename in os.listdir(patient_dir):
        name = filename.lower()
        if any(keyword.lower() in name for keyword in keywords):
            return os.path.join(patient_dir, filename)
    return None

def load_modality_image(patient_id: str, keywords: list[str]) -> np.ndarray:
    """
    Carga y normaliza una imagen desde /uploads/{patient_id} que coincida con keywords como ['t2f'].
    """
    file_path = find_modality_file(patient_id, keywords)
    if not file_path:
        raise FileNotFoundError(f"No se encontró ninguna modalidad con {keywords} para el paciente {patient_id}")
    
    print(f"✅ Cargando modalidad: {file_path}")
    image = nib.load(file_path).get_fdata()
    return normalize(image)
