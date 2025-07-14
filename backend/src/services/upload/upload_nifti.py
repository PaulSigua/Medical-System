import os, shutil, re
from datetime import datetime
import nibabel as nib
from skimage.transform import resize
from database.db import get_db_connection

# Mapeo flexible por keywords
MODALITY_KEYWORDS = {
    "FLAIR": ["flair", "t2f"],
    "T1":    ["t1", "t1n"],
    "T1c":   ["t1c", "t1ce"],
    "T2":    ["t2", "t2w"]
}

def detect_modality(file_name: str) -> str | None:
    name = re.sub(r'[^a-z0-9]', '', file_name.lower())  # Limpieza agresiva
    priority = ["T1c", "T1", "FLAIR", "T2"]  # Prioridad para que "t1c" no se confunda con "t1"

    for modality in priority:
        keywords = MODALITY_KEYWORDS[modality]
        if any(k in name for k in keywords):
            return modality
    return None

def save_uploaded_nifti_files(patient_id: str, user_id: int, upload_files: list) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    folder_name = f"{timestamp}_{patient_id}"
    upload_dir = os.path.join("src/uploads", folder_name)
    os.makedirs(upload_dir, exist_ok=True)

    # Detectar modalidades
    modality_paths = {}
    for upload_file in upload_files:
        modality = detect_modality(upload_file.filename)
        if not modality:
            print(f"No se reconoce la modalidad: {upload_file.filename}")
            continue
        temp_path = os.path.join(upload_dir, f"{modality}.nii.gz")
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(upload_file.file, f)
        modality_paths[modality] = temp_path

    # Validar presencia de las 4 modalidades
    expected = ["FLAIR", "T1", "T1c", "T2"]
    if not all(mod in modality_paths for mod in expected):
        raise ValueError(f"Faltan modalidades obligatorias. Detectadas: {list(modality_paths.keys())}")

    # Crear archivos procesados para nnUNet
    processed_dir = os.path.join(upload_dir, "nnunet_input")
    save_modalities_in_order(modality_paths, processed_dir, case_id="case_0000")

    # Actualizar BD con rutas a archivos originales
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE patients
            SET flair_path = %s,
                t1_path = %s,
                t1ce_path = %s,
                t2_path = %s
            WHERE patient_id = %s AND user_id = %s
        """, (
            modality_paths["FLAIR"],
            modality_paths["T1"],
            modality_paths["T1c"],
            modality_paths["T2"],
            patient_id,
            user_id
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print("Rutas actualizadas en base de datos.")
    except Exception as e:
        print(f"Error al actualizar la base de datos: {e}")

    return processed_dir


def save_modalities_in_order(modality_paths: dict, output_dir: str, case_id: str):
    os.makedirs(output_dir, exist_ok=True)

    order = ["FLAIR", "T1", "T1c", "T2"]
    shapes = [nib.load(modality_paths[mod]).shape for mod in order]
    target_shape = shapes[0]  # usar la forma de referencia

    print(f"Reescalando a shape objetivo: {target_shape}")

    for idx, modality in enumerate(order):
        img_obj = nib.load(modality_paths[modality])
        data = img_obj.get_fdata()

        if data.shape != target_shape:
            print(f"⚠ Reescalando {modality} de {data.shape} a {target_shape}")
            data = resize(data, target_shape, preserve_range=True, mode='constant', anti_aliasing=True)
        else:
            print(f"{modality} ya tiene shape correcto")

        out_img = nib.Nifti1Image(data, affine=img_obj.affine)
        out_path = os.path.join(output_dir, f"{case_id}_{idx:04d}.nii.gz")
        nib.save(out_img, out_path)

    print(f"Modalidades procesadas guardadas en: {output_dir}")
