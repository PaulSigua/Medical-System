from fastapi import APIRouter
from psycopg2.extras import RealDictCursor
from database.db import get_db_connection
from fastapi.responses import JSONResponse
from datetime import datetime

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

MONTHS_ES = {
    "January": "Enero", "February": "Febrero", "March": "Marzo",
    "April": "Abril", "May": "Mayo", "June": "Junio",
    "July": "Julio", "August": "Agosto", "September": "Septiembre",
    "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
}

@router.get("/statistics")
def get_system_statistics():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT COUNT(*) AS total_predictions
            FROM diagnostics;
        """)
        total_predictions = cursor.fetchone()["total_predictions"]

        cursor.execute("""
            SELECT COUNT(*) AS total_patients
            FROM patients;
        """)
        total_patients = cursor.fetchone()["total_patients"]

        cursor.execute("""
            SELECT MAX(updated_at) AS last_prediction
            FROM diagnostics;
        """)
        last_prediction_raw = cursor.fetchone()["last_prediction"]

        if last_prediction_raw:
            day = last_prediction_raw.day
            month = MONTHS_ES[last_prediction_raw.strftime("%B")]
            year = last_prediction_raw.year
            hour_min = last_prediction_raw.strftime("%H:%M")
            last_prediction = f"{day} de {month} de {year} a las {hour_min}"
        else:
            last_prediction = None

        cursor.close()
        conn.close()

        return JSONResponse({
            "total_predictions": total_predictions,
            "total_patients": total_patients,
            "last_prediction": last_prediction
        })

    except Exception as e:
        print("Error al obtener estadísticas:", str(e))
        return JSONResponse(
            {"error": "Error al obtener estadísticas del sistema"},
            status_code=500
        )
