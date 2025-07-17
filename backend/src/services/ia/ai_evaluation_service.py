from models.ai_evaluation import IAEvaluation, SatisfactionLevel
from sqlalchemy.orm import Session
from sqlalchemy import func

def save_evaluation(db: Session, user_id: int, patient_id: str, usefulness: bool, satisfaction: SatisfactionLevel, comments: str = None):
    evaluation = IAEvaluation(
        user_id=user_id,
        patient_id=patient_id,
        usefulness=usefulness,
        satisfaction=satisfaction,
        comments=comments
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation

def get_satisfaction_summary(db: Session):
    results = (
        db.query(IAEvaluation.satisfaction, func.count(IAEvaluation.id))
        .group_by(IAEvaluation.satisfaction)
        .all()
    )

    summary = {label: count for label, count in results}
    print(summary)
    all_labels = ['Excelente', 'Satisfactorio', 'Neutro', 'No satisfactorio']
    # Asegura que estén todos los labels
    return {label: summary.get(label, 0) for label in all_labels}