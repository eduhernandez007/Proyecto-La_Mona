from pydantic import BaseModel
from app.models.calistenia import CategoriaCalistenia, PruebaCalistenia


class ParticipanteCreate(BaseModel):
    jugador_id: int
    categoria: CategoriaCalistenia
    departamento_id: int


class ParticipanteRead(BaseModel):
    id: int
    jugador_id: int
    categoria: CategoriaCalistenia
    departamento_id: int

    model_config = {"from_attributes": True}


class CompetenciaCalisteniaCreate(BaseModel):
    nombre: str
    categoria: CategoriaCalistenia
    lugar: str
    fecha_hora: str


class CompetenciaCalisteniaRead(BaseModel):
    id: int
    nombre: str
    categoria: CategoriaCalistenia
    lugar: str
    fecha_hora: str

    model_config = {"from_attributes": True}


class ResultadoCreate(BaseModel):
    participante_id: int
    competencia_id: int
    prueba: PruebaCalistenia
    valor: float


class ResultadoRead(BaseModel):
    id: int
    participante_id: int
    competencia_id: int
    prueba: PruebaCalistenia
    valor: float

    model_config = {"from_attributes": True}
