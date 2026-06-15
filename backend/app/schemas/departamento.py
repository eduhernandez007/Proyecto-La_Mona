from pydantic import BaseModel


class DepartamentoCreate(BaseModel):
    nombre: str


class DepartamentoRead(BaseModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}
