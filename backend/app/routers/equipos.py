from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.equipo import Equipo
from app.models.jugador import Jugador
from app.models.departamento import Departamento
from app.schemas.equipo import EquipoCreate, EquipoRead, AgregarJugador, AgregarJugadoresMulti, AsignarCapitan
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

    # Restricción: 1 equipo por departamento
    equipo_existente = db.query(Equipo).filter(Equipo.departamento_id == data.departamento_id).first()
    if equipo_existente:
        raise HTTPException(status_code=400, detail=f"El departamento '{dept.nombre}' ya tiene un equipo inscrito ('{equipo_existente.nombre}').")

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

    # Restricción: el jugador debe pertenecer al mismo departamento que el equipo
    if jugador.departamento_id != equipo.departamento_id:
        raise HTTPException(
            status_code=400, 
            detail=f"El jugador pertenece a un departamento distinto al del equipo."
        )

    if jugador in equipo.jugadores:
        raise HTTPException(status_code=400, detail="El jugador ya está en el equipo")

    # Validamos límite de plantel ANTES de agregar
    equipo.jugadores.append(jugador)
    error = validador.validar_maximo_plantel(equipo)
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


@router.post("/{equipo_id}/jugadores_lote", response_model=EquipoRead)
def agregar_jugadores_lote(equipo_id: int, data: AgregarJugadoresMulti, db: Session = Depends(get_db)):
    equipo = db.get(Equipo, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    jugadores_a_agregar = []
    for j_id in data.jugadores_ids:
        jugador = db.get(Jugador, j_id)
        if not jugador:
            raise HTTPException(status_code=404, detail=f"Jugador con id {j_id} no encontrado")
        
        # Restricción: el jugador debe pertenecer al mismo departamento que el equipo
        if jugador.departamento_id != equipo.departamento_id:
            raise HTTPException(
                status_code=400, 
                detail=f"El jugador '{jugador.nombre}' no pertenece al departamento del equipo."
            )

        if jugador not in equipo.jugadores:
            jugadores_a_agregar.append(jugador)

    # Simulamos la adición y validamos el máximo del plantel (12 jugadores)
    for j in jugadores_a_agregar:
        equipo.jugadores.append(j)

    error = validador.validar_maximo_plantel(equipo)
    if error:
        for j in jugadores_a_agregar:
            equipo.jugadores.remove(j)
        raise HTTPException(status_code=400, detail=error)

    db.commit()
    db.refresh(equipo)
    return equipo


@router.patch("/{equipo_id}/capitan", response_model=EquipoRead)
def asignar_capitan(equipo_id: int, data: AsignarCapitan, db: Session = Depends(get_db)):
    """Asigna un capitán al equipo. El jugador debe ser miembro del equipo."""
    equipo = db.get(Equipo, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    jugador = db.get(Jugador, data.jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    if jugador not in equipo.jugadores:
        raise HTTPException(status_code=400, detail="El jugador debe ser miembro del equipo para ser capitán")

    equipo.capitan_id = jugador.id
    db.commit()
    db.refresh(equipo)
    return equipo


@router.delete("/{equipo_id}/jugadores/{jugador_id}", response_model=EquipoRead)
def eliminar_jugador_de_equipo(equipo_id: int, jugador_id: int, db: Session = Depends(get_db)):
    equipo = db.get(Equipo, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    jugador = db.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    if jugador not in equipo.jugadores:
        raise HTTPException(status_code=400, detail="El jugador no pertenece a este equipo")

    # Si era el capitán, lo removemos también
    if equipo.capitan_id == jugador.id:
        equipo.capitan_id = None

    equipo.jugadores.remove(jugador)
    db.commit()
    db.refresh(equipo)
    return equipo


@router.delete("/{equipo_id}", status_code=204)
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.get(Equipo, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    db.delete(equipo)
    db.commit()
    return None
