from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.db import Base

class ManualEvaluation(Base):
    __tablename__ = "manual_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"), nullable=False)
    is_accurate = Column(String, nullable=False)  # "Sí", "Neutro", "No"
    observations = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
