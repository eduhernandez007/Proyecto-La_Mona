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

    from app.services.validaciones import ValidadorCalistenia
    validador = ValidadorCalistenia()

    error_valor = validador.validar_valor(data.valor)
    if error_valor:
        raise HTTPException(status_code=400, detail=error_valor)

    error_prueba = validador.validar_prueba(participante.categoria, data.prueba)
    if error_prueba:
        raise HTTPException(status_code=400, detail=error_prueba)

    resultado = ResultadoCalistenia(**data.model_dump())
    db.add(resultado)
    db.commit()
    db.refresh(resultado)
    return resultado
