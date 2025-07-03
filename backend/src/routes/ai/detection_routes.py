from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import numpy as np
import h5py
import os
from tensorflow.keras.models import load_model
from database.db import get_db_connection
from utils.security import get_current_user_id  # asegúrate de que esté implementado correctamente
from services.processing.load_model_h5 import load_hdf5_file
from services.graphs.graph_generator import (
    generate_graph1,
    generate_graph2,
    generate_graph3,
    generate_graph4,
    generate_graph5,
    generate_graph6
)

router = APIRouter(
    prefix="/ai-clasification",
    tags=["ai-clasification"]
)

class DetectionRequest(BaseModel):
    patient_id: str


def cargar_modelo_clasificacion():
    classification_model_path = "src/models/ia/models_clasification/classification_brats_model_cnn.h5"
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
def detect_ia(request: DetectionRequest):
    patient_id = request.patient_id

    if not patient_id:
        raise HTTPException(status_code=400, detail="Patient ID is missing")

    print(f"Clasificando con paciente: {patient_id}")

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

class PredictRequest(BaseModel):
    patient_id: str

@router.post("/predict-ai")
async def predict_ia(
    payload: PredictRequest
):
    patient_id = payload.patient_id
    if not patient_id:
        raise HTTPException(status_code=400, detail="Patient ID is missing")

    # Ruta al HDF5
    h5_path = os.path.join('src/processed_files', f'{patient_id}.h5')
    if not os.path.exists(h5_path):
        raise HTTPException(
            status_code=404,
            detail=f"El archivo HDF5 {h5_path} no fue encontrado."
        )

    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            SELECT graph1_path, graph2_path, graph3_path,
                   graph4_path, graph5_path, graph6_path
            FROM patients
            WHERE patient_id = %s
            """,
            (patient_id,)
        )
        existing = cursor.fetchone()
        if existing and all(existing.values()):
            # Devuelve URLs de static si ya existen
            urls = {
                f"html_url{i+1}": f"/static/{existing[f'graph{i+1}_path']}"
                for i in range(6)
            }
            return JSONResponse(content=urls)

        # Generamos gráficas
        test_img = load_hdf5_file(h5_path)
        if test_img is None:
            raise HTTPException(status_code=500, detail="Error al cargar el archivo HDF5.")

        # Supongamos que tienes el modelo cargado globalmente o lo cargas aquí
        # prediction = model.predict(np.expand_dims(test_img, 0))
        # pred_argmax = np.argmax(prediction, axis=4)[0]
        # Para este ejemplo asumimos pred_argmax ya calculado o a pasar como parámetro
        pred_argmax = np.zeros(test_img.shape[:3], dtype=int)

        graph1 = generate_graph1(test_img, pred_argmax)
        graph2, report2 = generate_graph2(pred_argmax)
        graph3 = generate_graph3(test_img, pred_argmax)
        graph4 = generate_graph4(test_img, pred_argmax)
        graph5, report5 = generate_graph5(test_img, pred_argmax)
        graph6 = generate_graph6(test_img, pred_argmax)

        # Guardar rutas en base de datos    
        cursor.execute(
            """
            UPDATE patients
            SET graph1_path=%s, graph2_path=%s, graph3_path=%s,
                graph4_path=%s, graph5_path=%s, graph6_path=%s
            WHERE patient_id=%s
            """,
            (graph1, graph2, graph3, graph4, graph5, graph6, patient_id)
        )
        conn.commit()
        cursor.close()

        # Construir respuestas
        response = {
            'html_url1': f"/static/{graph1}",
            'html_url2': f"/static/{graph2}",
            'html_url3': f"/static/{graph3}",
            'html_url4': f"/static/{graph4}",
            'html_url5': f"/static/{graph5}",
            'html_url6': f"/static/{graph6}",
            'report_text2': report2,
            'report_text5': report5
        }
        return JSONResponse(content=response)

    except Exception as e:
        print(f"Error durante la predicción: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error durante la predicción. Consulta los registros del servidor para más detalles."
        )
    finally:
        conn.close()