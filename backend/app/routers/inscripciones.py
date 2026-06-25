from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inscripcion import Inscripcion, EstadoInscripcion
from app.models.jugador import Jugador
from app.models.equipo import Equipo
from app.models.usuario import Usuario, RolUsuario
from app.schemas.inscripcion import InscripcionCreate, InscripcionRead, AccionInscripcion

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


def _validar_usuario_con_rol(usuario_id: int, rol_requerido: RolUsuario, db: Session) -> Usuario:
    """Obtiene el usuario y verifica que tenga el rol requerido."""
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not usuario.tiene_rol(rol_requerido):
        raise HTTPException(
            status_code=403,
            detail=f"El usuario debe tener rol '{rol_requerido.value}' para esta acción",
        )
    return usuario


@router.get("/", response_model=list[InscripcionRead])
def listar_inscripciones(db: Session = Depends(get_db)):
    return db.query(Inscripcion).all()


@router.post("/", response_model=InscripcionRead, status_code=201)
def solicitar_inscripcion(data: InscripcionCreate, db: Session = Depends(get_db)):
    """Un jugador solicita inscribirse en un equipo. Estado inicial: pendiente."""
    # Solo un usuario con rol 'jugador' puede solicitar inscripción
    _validar_usuario_con_rol(data.usuario_id, RolUsuario.jugador, db)

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
def aprobar_inscripcion(
    inscripcion_id: int, data: AccionInscripcion, db: Session = Depends(get_db)
):
    """El centro de estudiantes aprueba la solicitud."""
    _validar_usuario_con_rol(data.usuario_id, RolUsuario.centro_estudiantes, db)
    
    inscripcion = db.get(Inscripcion, inscripcion_id)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    
    equipo = inscripcion.equipo
    jugador = inscripcion.jugador
    
    # Si el jugador ya está en el equipo, solo aprobamos el estado de la inscripción
    if jugador not in equipo.jugadores:
        # Agregamos el jugador temporalmente para validar estrellas
        equipo.jugadores.append(jugador)
        from app.services.validaciones import ValidadorBasquetbol
        validador = ValidadorBasquetbol()
        error = validador.validar_estrellas(equipo)
        if error:
            equipo.jugadores.remove(jugador)
            raise HTTPException(status_code=400, detail=error)
            
    return _cambiar_estado(inscripcion_id, EstadoInscripcion.aprobada, db)


@router.patch("/{inscripcion_id}/rechazar", response_model=InscripcionRead)
def rechazar_inscripcion(
    inscripcion_id: int, data: AccionInscripcion, db: Session = Depends(get_db)
):
    """El centro de estudiantes rechaza la solicitud."""
    _validar_usuario_con_rol(data.usuario_id, RolUsuario.centro_estudiantes, db)
    return _cambiar_estado(inscripcion_id, EstadoInscripcion.rechazada, db)
