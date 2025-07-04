import os
import glob
from typing import List

UPLOAD_FOLDER = "src/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def save_uploaded_files(files, patient_id):
    for file in files:
        filename = file.filename
        if patient_id not in filename:
            filename = f"{patient_id}_{filename}"
        path = os.path.join(UPLOAD_FOLDER, filename)
        with open(path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
        file.file.close()

def get_latest_patient_file(patient_id: str, suffix: str):
    pattern = os.path.join(UPLOAD_FOLDER, f"*{suffix}.nii.gz")
    files = [f for f in glob.glob(pattern) if patient_id in os.path.basename(f)]
    return max(files, key=os.path.getmtime) if files else None

def get_patient_folder(patient_id: str) -> str:
    return os.path.join(UPLOAD_FOLDER, patient_id)

def list_patient_files(patient_id: str) -> List[str]:
    patient_folder = get_patient_folder(patient_id)
    if not os.path.exists(patient_folder):
        return []
    
    return [
        os.path.join(patient_folder, f)
        for f in os.listdir(patient_folder)
        if os.path.isfile(os.path.join(patient_folder, f))
    ]