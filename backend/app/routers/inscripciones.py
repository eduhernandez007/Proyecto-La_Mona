from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inscripcion import Inscripcion, EstadoInscripcion
from app.models.jugador import Jugador
from app.models.equipo import Equipo
from app.schemas.inscripcion import InscripcionCreate, InscripcionRead

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


@router.get("/", response_model=list[InscripcionRead])
def listar_inscripciones(db: Session = Depends(get_db)):
    return db.query(Inscripcion).all()


@router.post("/", response_model=InscripcionRead, status_code=201)
def solicitar_inscripcion(data: InscripcionCreate, db: Session = Depends(get_db)):
    """Un jugador solicita inscribirse en un equipo. Estado inicial: pendiente."""
    jugador = db.get(Jugador, data.jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    equipo = db.get(Equipo, data.equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    # Evitamos solicitudes duplicadas pendientes para el mismo jugador y equipo
    duplicada = (
        db.query(Inscripcion)
        .filter(
            Inscripcion.jugador_id == data.jugador_id,
            Inscripcion.equipo_id == data.equipo_id,
            Inscripcion.estado == EstadoInscripcion.pendiente,
        )
        .first()
    )
    if duplicada:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una solicitud pendiente para este jugador y equipo",
        )

    inscripcion = Inscripcion(
        jugador_id=data.jugador_id,
        equipo_id=data.equipo_id,
        estado=EstadoInscripcion.pendiente,
    )
    db.add(inscripcion)
    db.commit()
    db.refresh(inscripcion)
    return inscripcion


def _cambiar_estado(
    inscripcion_id: int, nuevo_estado: EstadoInscripcion, db: Session
) -> Inscripcion:
    """Helper que valida la inscripción y aplica el cambio de estado."""
    inscripcion = db.get(Inscripcion, inscripcion_id)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    if inscripcion.estado != EstadoInscripcion.pendiente:
        raise HTTPException(
            status_code=400,
            detail=f"La inscripción ya fue {inscripcion.estado.value}, no se puede modificar",
        )
    inscripcion.estado = nuevo_estado
    db.commit()
    db.refresh(inscripcion)
    return inscripcion


@router.patch("/{inscripcion_id}/aprobar", response_model=InscripcionRead)
def aprobar_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    """El centro de estudiantes aprueba la solicitud."""
    return _cambiar_estado(inscripcion_id, EstadoInscripcion.aprobada, db)


@router.patch("/{inscripcion_id}/rechazar", response_model=InscripcionRead)
def rechazar_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    """El centro de estudiantes rechaza la solicitud."""
    return _cambiar_estado(inscripcion_id, EstadoInscripcion.rechazada, db)
