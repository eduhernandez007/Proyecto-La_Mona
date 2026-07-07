from sqlalchemy import Integer, ForeignKey, Float, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class CategoriaCalistenia(str, enum.Enum):
    masculina = "M"
    femenina = "F"


class PruebaCalistenia(str, enum.Enum):
    muscle_ups = "muscle_ups"        # solo categoría masculina
    pull_ups = "pull_ups"
    push_ups = "push_ups"
    handstand_hold = "handstand_hold"
    hang_hold = "hang_hold"          # solo categoría femenina


# Pruebas válidas por categoría (según las bases de La Mona, anexo A.4.2)
PRUEBAS_POR_CATEGORIA = {
    CategoriaCalistenia.masculina: {
        PruebaCalistenia.muscle_ups,
        PruebaCalistenia.pull_ups,
        PruebaCalistenia.push_ups,
        PruebaCalistenia.handstand_hold,
    },
    CategoriaCalistenia.femenina: {
        PruebaCalistenia.pull_ups,
        PruebaCalistenia.push_ups,
        PruebaCalistenia.handstand_hold,
        PruebaCalistenia.hang_hold,
    },
}


class CompetenciaCalistenia(Base):
    """
    Representa una competencia organizada de calistenia.
    Debe especificar un nombre, la categoría (masculina o femenina), el lugar y la fecha/hora.
    """
    __tablename__ = "competencias_calistenia"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria: Mapped[CategoriaCalistenia] = mapped_column(Enum(CategoriaCalistenia), nullable=False)
    lugar: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_hora: Mapped[str] = mapped_column(String(50), nullable=False)

    resultados: Mapped[list["ResultadoCalistenia"]] = relationship(
        back_populates="competencia", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"CompetenciaCalistenia(id={self.id}, nombre={self.nombre!r}, categoria={self.categoria}, lugar={self.lugar!r}, fecha_hora={self.fecha_hora!r})"


class ParticipanteCalistenia(Base):
    """
    Participante individual de la competencia de Calistenia (categoría B).
    Cada participante compite en una categoría (masculina o femenina) y
    representa a un departamento.
    """
    __tablename__ = "participantes_calistenia"

    id: Mapped[int] = mapped_column(primary_key=True)
    jugador_id: Mapped[int] = mapped_column(ForeignKey("jugadores.id"), nullable=False)
    categoria: Mapped[CategoriaCalistenia] = mapped_column(Enum(CategoriaCalistenia), nullable=False)
    departamento_id: Mapped[int] = mapped_column(ForeignKey("departamentos.id"), nullable=False)

    jugador: Mapped["Jugador"] = relationship()
    departamento: Mapped["Departamento"] = relationship()
    resultados: Mapped[list["ResultadoCalistenia"]] = relationship(
        back_populates="participante", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ParticipanteCalistenia(id={self.id}, jugador={self.jugador_id}, categoria={self.categoria})"


class ResultadoCalistenia(Base):
    """
    Resultado de un participante en una prueba específica.
    El 'valor' representa repeticiones (pruebas de conteo) o segundos
    sostenidos (pruebas de tipo hold).
    """
    __tablename__ = "resultados_calistenia"

    id: Mapped[int] = mapped_column(primary_key=True)
    participante_id: Mapped[int] = mapped_column(
        ForeignKey("participantes_calistenia.id"), nullable=False
    )
    competencia_id: Mapped[int] = mapped_column(
        ForeignKey("competencias_calistenia.id"), nullable=False
    )
    prueba: Mapped[PruebaCalistenia] = mapped_column(Enum(PruebaCalistenia), nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)

    participante: Mapped["ParticipanteCalistenia"] = relationship(back_populates="resultados")
    competencia: Mapped["CompetenciaCalistenia"] = relationship(back_populates="resultados")

    def __repr__(self) -> str:
        return f"ResultadoCalistenia(id={self.id}, prueba={self.prueba}, valor={self.valor})"
