from sqlalchemy import Column, Integer, String, Boolean, VARCHAR
from database.db import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    patient_id = Column(String, nullable=False)
    numero_historia_clinica = Column(String, nullable=False)
    survey_completed = Column(Boolean, nullable=False)
    t1ce_path= Column(VARCHAR, nullable=False)
    t2_path = Column(VARCHAR, nullable=False)
    flair_path = Column(VARCHAR, nullable=False)
    predicted_segmentation = Column(VARCHAR, nullable=False)
    graph1_path = Column(VARCHAR, nullable=False)
    graph2_path = Column(VARCHAR, nullable=False)
    graph3_path = Column(VARCHAR, nullable=False)
    graph4_path = Column(VARCHAR, nullable=False)
    graph5_path = Column(VARCHAR, nullable=False)
    graph6_path = Column(VARCHAR, nullable=False)
    graph_segmentation_path = Column(VARCHAR, nullable=False)
    t1_path = Column(VARCHAR, nullable=False)