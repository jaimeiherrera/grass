from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .database import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=20), nullable=False)
    email = Column(String(length=30), unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), server_default=func.now())
