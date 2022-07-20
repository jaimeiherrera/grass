from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from .database import crud, models, schemas
from .database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grass", description="Grass API")


@app.get("/")
async def root():
    return {"message": "Welcome to Grass"}


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


@app.get("/personas/", response_model=list[schemas.Persona])
def read_personas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_personas(db, skip=skip, limit=limit)
    return users


@app.get("/personas/{user_id}", response_model=schemas.Persona)
def read_persona(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_persona(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/personas/", response_model=schemas.Persona)
def create_persona(persona: schemas.PersonaCreate, db: Session = Depends(get_db)):
    try:
        if db.query(models.Persona).filter(models.Persona.email == persona.email).first():
            raise HTTPException(
                status_code=400, detail="Email already registered")
        return crud.create_persona(db=db, persona=persona)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/personas/{persona_id}")
def update_persona(persona_id: int, persona: schemas.PersonaBase, db: Session = Depends(get_db)):
    try:
        db_persona = crud.get_persona(db, persona_id)
        if db_persona is None:
            raise HTTPException(status_code=404, detail="Persona not found")
        db_persona = crud.update_persona(db, persona, persona_id)
        return db_persona
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
