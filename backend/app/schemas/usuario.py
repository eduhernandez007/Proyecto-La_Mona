from pydantic import BaseModel
from app.models.usuario import RolUsuario


class UsuarioCreate(BaseModel):
    nombre: str
    clave: str = "1234"
    rol: RolUsuario
    departamento_id: int | None = None


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    rol: RolUsuario
    departamento_id: int | None

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    nombre: str
    clave: str


class LoginResponse(BaseModel):
    id: int
    nombre: str
    rol: RolUsuario
    departamento_id: int | None

    model_config = {"from_attributes": True}
