from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Departamento(Base):
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    jugadores: Mapped[list["Jugador"]] = relationship(back_populates="departamento")
    equipos: Mapped[list["Equipo"]] = relationship(back_populates="departamento")

    def __repr__(self) -> str:
        return f"Departamento(id={self.id}, nombre={self.nombre!r})"
