from pydantic import BaseModel
from app.models.partido import EstadoPartido


class PartidoCreate(BaseModel):
    equipo_local_id: int
    equipo_visitante_id: int
    fecha: str | None = None


class RegistrarResultado(BaseModel):
    puntos_local: int
    puntos_visitante: int


class PartidoRead(BaseModel):
    id: int
    equipo_local_id: int
    equipo_visitante_id: int
    puntos_local: int | None
    puntos_visitante: int | None
    estado: EstadoPartido
    fecha: str | None
    nombre_local: str = ""
    nombre_visitante: str = ""

    model_config = {"from_attributes": True}
