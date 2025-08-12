from pydantic import BaseModel

class DiagnosticForm(BaseModel):
    patient_id: str
    description: str
    diagnostic: str