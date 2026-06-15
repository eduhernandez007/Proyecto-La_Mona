from pydantic import BaseModel, Field
from app.models.jugador import Genero


class JugadorCreate(BaseModel):
    nombre: str
    genero: Genero
    estrellas: int = Field(default=0, ge=0, le=3)
    departamento_id: int


class JugadorRead(BaseModel):
    id: int
    nombre: str
    genero: Genero
    estrellas: int
    departamento_id: int

    model_config = {"from_attributes": True}
