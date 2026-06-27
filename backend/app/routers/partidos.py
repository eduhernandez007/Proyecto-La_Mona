from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.partido import Partido, EstadoPartido
from app.models.equipo import Equipo
from app.models.jugador import Jugador
from app.schemas.partido import PartidoCreate, PartidoRead, RegistrarResultado, RegistrarWO
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
        fase=partido.fase,
        nombre_local=partido.equipo_local.nombre if partido.equipo_local else "",
        nombre_visitante=partido.equipo_visitante.nombre if partido.equipo_visitante else "",
        titulares_local_ids=[j.id for j in partido.titulares_local],
        titulares_visitante_ids=[j.id for j in partido.titulares_visitante],
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

    # Validar que ambos equipos tienen capitán asignado
    if not local.capitan_id:
        raise HTTPException(
            status_code=400,
            detail=f"El equipo local '{local.nombre}' no tiene capitán asignado. "
                   "Asigna un capitán antes de programar el partido."
        )
    if not visitante.capitan_id:
        raise HTTPException(
            status_code=400,
            detail=f"El equipo visitante '{visitante.nombre}' no tiene capitán asignado. "
                   "Asigna un capitán antes de programar el partido."
        )

    # Titulares son OBLIGATORIOS (mínimo 5 por equipo)
    if not data.titulares_local_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Debes seleccionar los titulares del equipo local '{local.nombre}' (mínimo 5)."
        )
    if not data.titulares_visitante_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Debes seleccionar los titulares del equipo visitante '{visitante.nombre}' (mínimo 5)."
        )

    # Procesar y validar titulares local
    titulares_local = [db.get(Jugador, j_id) for j_id in data.titulares_local_ids]
    if None in titulares_local:
        raise HTTPException(status_code=404, detail="Uno o más titulares del equipo local no fueron encontrados")
    for j in titulares_local:
        if j not in local.jugadores:
            raise HTTPException(
                status_code=400,
                detail=f"El jugador '{j.nombre}' no pertenece al equipo local"
            )
    error = validador.validar_titulares(titulares_local)
    if error:
        raise HTTPException(status_code=400, detail=f"Titulares local: {error}")

    # Procesar y validar titulares visitante
    titulares_visitante = [db.get(Jugador, j_id) for j_id in data.titulares_visitante_ids]
    if None in titulares_visitante:
        raise HTTPException(status_code=404, detail="Uno o más titulares del equipo visitante no fueron encontrados")
    for j in titulares_visitante:
        if j not in visitante.jugadores:
            raise HTTPException(
                status_code=400,
                detail=f"El jugador '{j.nombre}' no pertenece al equipo visitante"
            )
    error = validador.validar_titulares(titulares_visitante)
    if error:
        raise HTTPException(status_code=400, detail=f"Titulares visitante: {error}")

    partido = Partido(
        equipo_local_id=data.equipo_local_id,
        equipo_visitante_id=data.equipo_visitante_id,
        fecha=data.fecha,
        fase=data.fase,
    )
    partido.titulares_local = titulares_local
    partido.titulares_visitante = titulares_visitante

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


@router.patch("/{partido_id}/wo", response_model=PartidoRead)
def registrar_wo(partido_id: int, data: RegistrarWO, db: Session = Depends(get_db)):
    """
    Registra W.O. para un partido. El equipo que comete W.O. recibe 0 puntos.
    El equipo que no comete W.O. gana automáticamente (marcado en estado 'wo').
    Si ambos cometen W.O., ambos reciben 0 puntos.
    """
    partido = db.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    if partido.estado != EstadoPartido.pendiente:
        raise HTTPException(status_code=400, detail="El partido ya tiene un resultado registrado")

    opciones_validas = {"local", "visitante", "ambos"}
    if data.equipo_wo not in opciones_validas:
        raise HTTPException(status_code=400, detail=f"equipo_wo debe ser uno de: {opciones_validas}")

    equipo_local = db.get(Equipo, partido.equipo_local_id)
    equipo_visitante = db.get(Equipo, partido.equipo_visitante_id)

    wo_detectado = validador.determinar_wo(equipo_local, equipo_visitante)
    if wo_detectado is None:
        raise HTTPException(
            status_code=400,
            detail="Ninguno de los equipos incumple los requisitos mínimos para declarar W.O. "
                   "(mínimo 5 jugadores, al menos 2 de cada género)."
        )

    if data.equipo_wo == "local":
        partido.puntos_local = 0
        partido.puntos_visitante = 2
    elif data.equipo_wo == "visitante":
        partido.puntos_local = 2
        partido.puntos_visitante = 0
    else:  # ambos
        partido.puntos_local = 0
        partido.puntos_visitante = 0

    partido.estado = EstadoPartido.wo
    db.commit()
    db.refresh(partido)
    return _partido_a_schema(partido)
