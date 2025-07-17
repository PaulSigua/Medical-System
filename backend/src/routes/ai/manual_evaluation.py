# routes/manual_evaluation.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.manual_evaluations import ManualEvaluation
from schemas.manual_schema import ManualEvaluationCreate

router = APIRouter(prefix="/manual_evaluation", tags=["evaluación Manual"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def save_manual_evaluation(
    evaluation: ManualEvaluationCreate, db: Session = Depends(get_db)
):
    record = ManualEvaluation(
        patient_id=evaluation.patient_id,
        is_accurate=evaluation.is_accurate,
        observations=evaluation.observations
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": "Evaluación guardada correctamente"}

@router.get("/match/{patient_id}")
def get_manual_accuracy(patient_id: str, db: Session = Depends(get_db)):
    evaluation = db.query(ManualEvaluation).filter_by(patient_id=patient_id).order_by(ManualEvaluation.created_at.desc()).first()
    if evaluation:
        return {"accuracy_level": evaluation.is_accurate}
    return {"accuracy_level": None}