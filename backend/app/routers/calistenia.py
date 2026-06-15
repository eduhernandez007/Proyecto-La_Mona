from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.calistenia import (
    ParticipanteCalistenia,
    ResultadoCalistenia,
    PRUEBAS_POR_CATEGORIA,
)
from app.models.jugador import Jugador
from app.models.departamento import Departamento
from app.schemas.calistenia import (
    ParticipanteCreate,
    ParticipanteRead,
    ResultadoCreate,
    ResultadoRead,
)

router = APIRouter(prefix="/calistenia", tags=["Calistenia"])


# ─── Participantes ────────────────────────────────────────────────────────────

@router.get("/participantes", response_model=list[ParticipanteRead])
def listar_participantes(db: Session = Depends(get_db)):
    return db.query(ParticipanteCalistenia).all()


@router.post("/participantes", response_model=ParticipanteRead, status_code=201)
def registrar_participante(data: ParticipanteCreate, db: Session = Depends(get_db)):
    jugador = db.get(Jugador, data.jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    dept = db.get(Departamento, data.departamento_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    participante = ParticipanteCalistenia(**data.model_dump())
    db.add(participante)
    db.commit()
    db.refresh(participante)
    return participante


# ─── Resultados ───────────────────────────────────────────────────────────────

@router.get("/resultados", response_model=list[ResultadoRead])
def listar_resultados(db: Session = Depends(get_db)):
    return db.query(ResultadoCalistenia).all()


@router.post("/resultados", response_model=ResultadoRead, status_code=201)
def registrar_resultado(data: ResultadoCreate, db: Session = Depends(get_db)):
    participante = db.get(ParticipanteCalistenia, data.participante_id)
    if not participante:
        raise HTTPException(status_code=404, detail="Participante no encontrado")

    if data.valor < 0:
        raise HTTPException(status_code=400, detail="El valor no puede ser negativo")

    # Validamos que la prueba corresponda a la categoría del participante.
    # Esto cubre la regla: hang_hold solo para F, muscle_ups solo para M.
    pruebas_validas = PRUEBAS_POR_CATEGORIA[participante.categoria]
    if data.prueba not in pruebas_validas:
        raise HTTPException(
            status_code=400,
            detail=(
                f"La prueba '{data.prueba.value}' no está permitida para la "
                f"categoría {participante.categoria.value}."
            ),
        )

    resultado = ResultadoCalistenia(**data.model_dump())
    db.add(resultado)
    db.commit()
    db.refresh(resultado)
    return resultado
