from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.jugador import Jugador
from app.models.departamento import Departamento
from app.schemas.jugador import JugadorCreate, JugadorRead

router = APIRouter(prefix="/jugadores", tags=["Jugadores"])


@router.get("/", response_model=list[JugadorRead])
def listar_jugadores(db: Session = Depends(get_db)):
    return db.query(Jugador).all()


@router.post("/", response_model=JugadorRead, status_code=201)
def crear_jugador(data: JugadorCreate, db: Session = Depends(get_db)):
    dept = db.get(Departamento, data.departamento_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    jugador = Jugador(**data.model_dump())
    db.add(jugador)
    db.commit()
    db.refresh(jugador)
    return jugador


@router.get("/{jugador_id}", response_model=JugadorRead)
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


@router.delete("/{jugador_id}", status_code=204)
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    db.delete(jugador)
    db.commit()
    return None
