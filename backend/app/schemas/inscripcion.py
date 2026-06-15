from pydantic import BaseModel
from app.models.inscripcion import EstadoInscripcion


class InscripcionCreate(BaseModel):
    jugador_id: int
    equipo_id: int


class InscripcionRead(BaseModel):
    id: int
    jugador_id: int
    equipo_id: int
    estado: EstadoInscripcion
    creado_en: str | None = None

    model_config = {"from_attributes": True}
