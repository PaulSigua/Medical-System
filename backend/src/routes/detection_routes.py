from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
import h5py
import os
from tensorflow.keras.models import load_model
from src.database import get_db_connection
from utils.security import get_current_user_id  # asegúrate de que esté implementado correctamente

router = APIRouter()


class DetectionRequest(BaseModel):
    patient_id: str


def cargar_modelo_clasificacion():
    classification_model_path = "src/ia/models/classification_brats_model_cnn.h5"
    classification_model = load_model(classification_model_path)
    return classification_model

def save_classification(prediccion: float, patient_id: str):
    try:
        cancer_prediction = bool(round(float(prediccion)))
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE diagnostics
            SET cancer_prediction = %s,
                is_generated_by_ia = %s
            WHERE patient_id = %s;
        """, (cancer_prediction, True, patient_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Predicci\u00f3n guardada en la base de datos para el paciente {patient_id}: {cancer_prediction}")
    except Exception as e:
        print(f"Error al guardar la predicci\u00f3n en la base de datos: {e}")


@router.post("/detection-ai")
def detect_ia(request: DetectionRequest, user_id: int = Depends(get_current_user_id)):
    patient_id = request.patient_id

    if not patient_id:
        raise HTTPException(status_code=400, detail="Patient ID is missing")

    print(f"Clasificando con paciente: {patient_id}, usuario: {user_id}")

    h5_classification_path = f"src/processed_files/{patient_id}_to_classify.h5"

    if not os.path.exists(h5_classification_path):
        raise HTTPException(status_code=404, detail=f"El archivo HDF5 {h5_classification_path} no fue encontrado.")

    model = cargar_modelo_clasificacion()

    with h5py.File(h5_classification_path, 'r') as hf:
        h5_classification = np.array(hf['images'])

    h5_classification = np.expand_dims(h5_classification, axis=0)
    print("Dimensiones de h5_classification:", h5_classification.shape)

    pred = model.predict(h5_classification)
    prob = float(pred[0][0])

    print(f"Prediccionn de clasificacion: {prob:.2f}")

    save_classification(prob, patient_id)

    return JSONResponse(content={"message": round(prob, 2)}, status_code=200)
