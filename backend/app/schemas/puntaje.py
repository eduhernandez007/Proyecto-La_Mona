from pydantic import BaseModel


class PuntajeDepartamento(BaseModel):
    departamento_id: int
    departamento: str
    puntaje_basquetbol: int
    puntaje_calistenia: int
    puntaje_total: int
