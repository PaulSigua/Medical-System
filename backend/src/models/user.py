from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    agree_terms = Column(Boolean, default=True)
    phone = Column(String, nullable=True)
    specialty = Column(String, nullable=True)
    ia_evaluations = relationship("IAEvaluation", back_populates="user")
