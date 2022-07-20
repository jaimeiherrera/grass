from sqlalchemy.orm import Session

from . import models, schemas


def get_persona(db: Session, user_id: int):
    return db.query(models.Persona).filter(models.Persona.id == user_id).first()


def get_personas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Persona).offset(skip).limit(limit).all()


def create_persona(db: Session, persona: schemas.PersonaCreate):
    fake_hashed_password = persona.password + "notreallyhashed"
    db_persona = models.Persona(name=persona.name,
                                email=persona.email, hashed_password=fake_hashed_password)
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona


def update_persona(db: Session, persona: schemas.PersonaBase, persona_id: int):
    db_persona = get_persona(db, persona_id)
    if db_persona:
        db_persona.name = persona.name
        db_persona.email = persona.email
        db.commit()
        db.refresh(db_persona)
        return db_persona
    return None
