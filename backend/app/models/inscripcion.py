from sqlalchemy import Integer, ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class EstadoInscripcion(str, enum.Enum):
    pendiente = "pendiente"
    aprobada = "aprobada"
    rechazada = "rechazada"


class Inscripcion(Base):
    """
    Solicitud de un jugador para inscribirse en un equipo.
    Flujo: el jugador solicita (pendiente) -> el centro de estudiantes
    aprueba o rechaza la solicitud.
    """
    __tablename__ = "inscripciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    jugador_id: Mapped[int] = mapped_column(ForeignKey("jugadores.id"), nullable=False)
    equipo_id: Mapped[int] = mapped_column(ForeignKey("equipos.id"), nullable=False)
    estado: Mapped[EstadoInscripcion] = mapped_column(
        Enum(EstadoInscripcion), default=EstadoInscripcion.pendiente
    )
    creado_en: Mapped[str] = mapped_column(String(50), default=func.now())

    jugador: Mapped["Jugador"] = relationship()
    equipo: Mapped["Equipo"] = relationship()

    def __repr__(self) -> str:
        return f"Inscripcion(id={self.id}, jugador={self.jugador_id}, equipo={self.equipo_id}, estado={self.estado})"
