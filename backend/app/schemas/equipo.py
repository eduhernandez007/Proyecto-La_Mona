from pydantic import BaseModel
from app.schemas.jugador import JugadorRead


class EquipoCreate(BaseModel):
    nombre: str
    departamento_id: int


class AgregarJugador(BaseModel):
    jugador_id: int


class AgregarJugadoresMulti(BaseModel):
    jugadores_ids: list[int]


class AsignarCapitan(BaseModel):
    jugador_id: int


class EquipoRead(BaseModel):
    id: int
    nombre: str
    departamento_id: int
    capitan_id: int | None = None
    jugadores: list[JugadorRead] = []

    model_config = {"from_attributes": True}
