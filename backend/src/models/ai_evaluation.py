from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database.db import Base
import enum

class SatisfactionLevel(str, enum.Enum):
    excellent = "Excelente"
    satisfactory = "Satisfactorio"
    neutral = "Neutro"
    unsatisfactory = "No satisfactorio"

class IAEvaluation(Base):
    __tablename__ = "ia_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    usefulness = Column(Boolean, default=True)  # ¿La IA fue útil?
    satisfaction = Column(Enum(SatisfactionLevel), default=SatisfactionLevel.neutral)
    comments = Column(String, nullable=True)

    user = relationship("User", back_populates="ia_evaluations")
