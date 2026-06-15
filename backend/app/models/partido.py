from sqlalchemy import Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class EstadoPartido(str, enum.Enum):
    pendiente = "pendiente"
    jugado = "jugado"
    wo = "wo"  # Walk Over: equipo no se presentó o no cumple mínimos


class Partido(Base):
    """
    Partido de básquetbol entre dos equipos.
    Estado 'pendiente' hasta que se registre el resultado.
    """
    __tablename__ = "partidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_local_id: Mapped[int] = mapped_column(ForeignKey("equipos.id"), nullable=False)
    equipo_visitante_id: Mapped[int] = mapped_column(ForeignKey("equipos.id"), nullable=False)
    puntos_local: Mapped[int | None] = mapped_column(Integer, nullable=True)
    puntos_visitante: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estado: Mapped[EstadoPartido] = mapped_column(default=EstadoPartido.pendiente)
    fecha: Mapped[str | None] = mapped_column(String(50), nullable=True)
    creado_en: Mapped[str] = mapped_column(String(50), default=func.now())

    equipo_local: Mapped["Equipo"] = relationship(
        foreign_keys=[equipo_local_id], back_populates="partidos_como_local"
    )
    equipo_visitante: Mapped["Equipo"] = relationship(
        foreign_keys=[equipo_visitante_id], back_populates="partidos_como_visitante"
    )

    def ganador(self) -> str | None:
        if self.estado != EstadoPartido.jugado:
            return None
        if self.puntos_local > self.puntos_visitante:
            return self.equipo_local.nombre
        elif self.puntos_visitante > self.puntos_local:
            return self.equipo_visitante.nombre
        return "Empate"

    def __repr__(self) -> str:
        return f"Partido(id={self.id}, local={self.equipo_local_id}, visitante={self.equipo_visitante_id})"
