from pydantic import BaseModel
from app.models.usuario import RolUsuario


class UsuarioCreate(BaseModel):
    nombre: str
    rol: RolUsuario
    departamento_id: int | None = None


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    rol: RolUsuario
    departamento_id: int | None

    model_config = {"from_attributes": True}
