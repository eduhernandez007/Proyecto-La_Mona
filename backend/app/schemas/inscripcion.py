from pydantic import BaseModel
from app.models.inscripcion import EstadoInscripcion


class InscripcionCreate(BaseModel):
    jugador_id: int
    equipo_id: int | None = None
    usuario_id: int  # usuario que realiza la solicitud (debe tener rol jugador)
    competencia: str = "basquet"  # "basquet" o "calistenia"


class AccionInscripcion(BaseModel):
    usuario_id: int  # usuario que aprueba/rechaza (debe ser centro_estudiantes)


class InscripcionRead(BaseModel):
    id: int
    jugador_id: int
    equipo_id: int | None = None
    competencia: str
    estado: EstadoInscripcion
    creado_en: str | None = None

    model_config = {"from_attributes": True}
