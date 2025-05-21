from .auth_routes import login_blueprint
from .user_routes import user
from .patient_routes import patient, diagnostic_patient
from .detection_routes import detectionBratsAI
from .report_routes import report

# Esto permite importarlos todos fácilmente desde app.py
__all__ = [
    "routes", "login_blueprint", "prediction", "user", "patient",
    "diagnostic", "predictionBrats", "resultVideo", "upload",
    "predictionBratsAI", "report", "diagnostic_patient", "detectionBratsAI"
]
