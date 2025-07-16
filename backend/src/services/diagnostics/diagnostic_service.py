from sqlalchemy.orm import Session
from models.diagnostics import Diagnostic
from schemas.diagnostic_schema import DiagnosticForm
from models.diagnostics import CancerStatusEnum

def save_manual_diagnostic(db: Session, form: DiagnosticForm, user_id: int):
    new_diag = Diagnostic(
        user_id=user_id,
        patient_id=form.patient_id,
        description=form.description,
        is_generated_by_ia=False,
        diagnostic_text=form.diagnostic,    
        cancer_status=CancerStatusEnum.INCIERTO.value,
    )
    db.add(new_diag)
    db.commit()
    db.refresh(new_diag)
    return new_diag
