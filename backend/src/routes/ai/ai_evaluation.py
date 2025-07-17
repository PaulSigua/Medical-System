from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from utils.security import get_current_user
from database.db import get_db
from services.ia.ai_evaluation_service import save_evaluation, get_satisfaction_summary
from schemas.ai_evaluation import EvaluationInput

router = APIRouter(prefix="/ai_evaluation", tags=["ai evaluation"])

@router.post("/")
def submit_ia_evaluation(
    data: EvaluationInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        evaluation = save_evaluation(
            db=db,
            user_id=current_user.id,
            patient_id=data.patient_id,
            usefulness=data.usefulness,
            satisfaction=data.satisfaction,
            comments=data.comments
        )
        return {"message": "Evaluación registrada correctamente", "id": evaluation.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar evaluación: {str(e)}")


@router.get("/summary")
def ai_evaluation_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_satisfaction_summary(db)