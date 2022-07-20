from datetime import datetime

from pydantic import BaseModel


class PersonaBase(BaseModel):
    name: str
    email: str


class PersonaCreate(PersonaBase):
    password: str


class Persona(PersonaBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
