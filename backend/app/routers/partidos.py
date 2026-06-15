from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.partido import Partido, EstadoPartido
from app.models.equipo import Equipo
from app.schemas.partido import PartidoCreate, PartidoRead, RegistrarResultado
from app.services.validaciones import ValidadorBasquetbol

router = APIRouter(prefix="/partidos", tags=["Partidos"])
validador = ValidadorBasquetbol()


def _partido_a_schema(partido: Partido) -> PartidoRead:
    return PartidoRead(
        id=partido.id,
        equipo_local_id=partido.equipo_local_id,
        equipo_visitante_id=partido.equipo_visitante_id,
        puntos_local=partido.puntos_local,
        puntos_visitante=partido.puntos_visitante,
        estado=partido.estado,
        fecha=partido.fecha,
        nombre_local=partido.equipo_local.nombre if partido.equipo_local else "",
        nombre_visitante=partido.equipo_visitante.nombre if partido.equipo_visitante else "",
    )


@router.get("/", response_model=list[PartidoRead])
def listar_partidos(db: Session = Depends(get_db)):
    partidos = db.query(Partido).all()
    return [_partido_a_schema(p) for p in partidos]


@router.post("/", response_model=PartidoRead, status_code=201)
def crear_partido(data: PartidoCreate, db: Session = Depends(get_db)):
    if data.equipo_local_id == data.equipo_visitante_id:
        raise HTTPException(status_code=400, detail="Un equipo no puede jugar contra sí mismo")

    local = db.get(Equipo, data.equipo_local_id)
    visitante = db.get(Equipo, data.equipo_visitante_id)

    if not local:
        raise HTTPException(status_code=404, detail="Equipo local no encontrado")
    if not visitante:
        raise HTTPException(status_code=404, detail="Equipo visitante no encontrado")

    # Validamos que ambos equipos cumplan las reglas antes de crear el partido
    error_local = validador.validar_equipo_para_partido(local)
    if error_local:
        raise HTTPException(status_code=400, detail=f"Equipo local: {error_local}")

    error_visitante = validador.validar_equipo_para_partido(visitante)
    if error_visitante:
        raise HTTPException(status_code=400, detail=f"Equipo visitante: {error_visitante}")

    partido = Partido(
        equipo_local_id=data.equipo_local_id,
        equipo_visitante_id=data.equipo_visitante_id,
        fecha=data.fecha,
    )
    db.add(partido)
    db.commit()
    db.refresh(partido)
    return _partido_a_schema(partido)


@router.patch("/{partido_id}/resultado", response_model=PartidoRead)
def registrar_resultado(partido_id: int, data: RegistrarResultado, db: Session = Depends(get_db)):
    partido = db.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    if partido.estado == EstadoPartido.jugado:
        raise HTTPException(status_code=400, detail="El partido ya tiene resultado registrado")

    partido.puntos_local = data.puntos_local
    partido.puntos_visitante = data.puntos_visitante
    partido.estado = EstadoPartido.jugado
    db.commit()
    db.refresh(partido)
    return _partido_a_schema(partido)
