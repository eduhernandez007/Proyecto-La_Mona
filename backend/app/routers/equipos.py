from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.equipo import Equipo
from app.models.jugador import Jugador
from app.models.departamento import Departamento
from app.schemas.equipo import EquipoCreate, EquipoRead, AgregarJugador
from app.services.validaciones import ValidadorBasquetbol

router = APIRouter(prefix="/equipos", tags=["Equipos"])
validador = ValidadorBasquetbol()


@router.get("/", response_model=list[EquipoRead])
def listar_equipos(db: Session = Depends(get_db)):
    return db.query(Equipo).all()


@router.post("/", response_model=EquipoRead, status_code=201)
def crear_equipo(data: EquipoCreate, db: Session = Depends(get_db)):
    dept = db.get(Departamento, data.departamento_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    equipo = Equipo(**data.model_dump())
    db.add(equipo)
    db.commit()
    db.refresh(equipo)
    return equipo


@router.post("/{equipo_id}/jugadores", response_model=EquipoRead)
def agregar_jugador(equipo_id: int, data: AgregarJugador, db: Session = Depends(get_db)):
    equipo = db.get(Equipo, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    jugador = db.get(Jugador, data.jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    if jugador in equipo.jugadores:
        raise HTTPException(status_code=400, detail="El jugador ya está en el equipo")

    # Validamos estrellas ANTES de agregar (simulamos el equipo con el jugador nuevo)
    equipo.jugadores.append(jugador)
    error = validador.validar_estrellas(equipo)
    if error:
        equipo.jugadores.remove(jugador)
        raise HTTPException(status_code=400, detail=error)

    db.commit()
    db.refresh(equipo)
    return equipo


@router.get("/{equipo_id}", response_model=EquipoRead)
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.get(Equipo, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo
