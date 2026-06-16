from pydantic import BaseModel
from app.models.inscripcion import EstadoInscripcion


class InscripcionCreate(BaseModel):
    jugador_id: int
    equipo_id: int
    usuario_id: int  # usuario que realiza la solicitud (debe tener rol jugador)


class AccionInscripcion(BaseModel):
    usuario_id: int  # usuario que aprueba/rechaza (debe ser centro_estudiantes)


class InscripcionRead(BaseModel):
    id: int
    jugador_id: int
    equipo_id: int
    estado: EstadoInscripcion
    creado_en: str | None = None

    model_config = {"from_attributes": True}
