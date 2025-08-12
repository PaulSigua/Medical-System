from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
import enum

# Enum para el campo cancer_status
class CancerStatusEnum(enum.Enum):
    NO_CANCER = 'no se detecta cancer'
    CANCER = 'cancer detectado'
    INCIERTO = 'diagnostico incierto'

class Diagnostic(Base):
    __tablename__ = "diagnostics"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=False)
    is_generated_by_ia = Column(Boolean, default=False)
    report_path = Column(Text, nullable=True)
    cancer_status = Column(
    PGEnum(CancerStatusEnum, name="cancerstatus", values_callable=lambda x: [e.value for e in x]),
    default=CancerStatusEnum.INCIERTO.value,
    nullable=False
    )
    diagnostic_text = Column(Text, nullable=True) 
    cancer_prediction = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    manual_segmentation_path = Column(Text, nullable=True)

    # Relaciones (opcional, útil para queries con JOIN)
    user = relationship("User", backref="diagnostics")
    patient = relationship("Patient", backref="diagnostics")
