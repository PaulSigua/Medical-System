from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas.patient_schema import PatientRequest
from services.processing.load_model_h5 import load_hdf5_file
from services.graphs.graph_generator import generate_graph6_no_prediction
import os

router = APIRouter(
    prefix="/graphs",
    tags=["graphs"]
)

@router.post("/generate-graph6")
async def generate_graph6_route(payload: PatientRequest, request: Request):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        patient_id = payload.patient_id
        file_path = os.path.join("src/processed_files", f"{patient_id}.h5")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Archivo {file_path} no encontrado")

        test_img = load_hdf5_file(file_path)
        print(f"value: {test_img}")
        if test_img is None:
            raise HTTPException(status_code=500, detail="Error al cargar archivo HDF5")
    except Exception as e:
        print(f"[ERROR] : {e}")

    try:
        html_filename = generate_graph6_no_prediction(test_img)
        return JSONResponse(content={
            "html_url6": f"/static/{html_filename}"
        })
    except Exception as e:
        print(f"[ERROR] Generando gráfica 6: {e}")
        raise HTTPException(status_code=500, detail="Error interno al generar la gráfica")
