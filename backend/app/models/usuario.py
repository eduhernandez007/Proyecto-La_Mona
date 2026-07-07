from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class RolUsuario(str, enum.Enum):
    organizador = "organizador"
    centro_estudiantes = "centro_estudiantes"
    juez = "juez"
    jugador = "jugador"


class Usuario(Base):
    """
    Usuario del sistema con un rol que determina sus permisos.
    El departamento es opcional (los organizadores y jueces pueden no
    representar a un departamento específico).
    """
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    clave: Mapped[str] = mapped_column(String(100), nullable=False, default="1234")
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario), nullable=False)
    departamento_id: Mapped[int | None] = mapped_column(
        ForeignKey("departamentos.id"), nullable=True
    )

    departamento: Mapped["Departamento"] = relationship()

    def tiene_rol(self, rol: RolUsuario) -> bool:
        return self.rol == rol

    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, nombre={self.nombre!r}, rol={self.rol})"
