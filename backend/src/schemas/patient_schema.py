from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    patient_id: str
    numero_historia_clinica: str

class PatientOut(BaseModel):
    user_id: int
    patient_id: str
    numero_historia_clinica: str
    survey_completed: bool | None = None
    t1ce_path: str | None = None
    t2_path: str | None = None
    flair_path: str | None = None

    class Config:
        from_attributes = True
    
class PatientUpdate(BaseModel):
    user_id: Optional[int] = None
    patient_id: Optional[str] = None
    numero_historia_clinica: Optional[str] = None