from pydantic import BaseModel
from typing import Literal

class ManualEvaluationCreate(BaseModel):
    patient_id: str
    is_accurate: Literal["Sí", "Neutro", "No"]
    observations: str