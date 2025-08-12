from models.ai_evaluation import SatisfactionLevel
from pydantic import BaseModel

class EvaluationInput(BaseModel):
    patient_id: str
    usefulness: bool
    satisfaction: SatisfactionLevel
    comments: str | None = None