from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class Genero(str, enum.Enum):
    masculino = "M"
    femenino = "F"


class Jugador(Base):
    """
    Representa a un participante de La Mona.
    Las estrellas limitan cuántos jugadores avanzados puede tener un equipo en cancha.
    """
    __tablename__ = "jugadores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    genero: Mapped[Genero] = mapped_column(Enum(Genero), nullable=False)
    estrellas: Mapped[int] = mapped_column(Integer, default=0)  # 0=amateur, 1=rama, 2=federado, 3=selección nacional
    departamento_id: Mapped[int] = mapped_column(ForeignKey("departamentos.id"), nullable=False)

    departamento: Mapped["Departamento"] = relationship(back_populates="jugadores")
    equipos: Mapped[list["Equipo"]] = relationship(secondary="equipo_jugador", back_populates="jugadores")

    def es_estrella_alta(self) -> bool:
        return self.estrellas >= 2

    def __repr__(self) -> str:
        return f"Jugador(id={self.id}, nombre={self.nombre!r}, estrellas={self.estrellas})"
