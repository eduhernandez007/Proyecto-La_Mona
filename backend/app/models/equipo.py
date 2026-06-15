from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

# Tabla de asociación muchos-a-muchos entre Equipo y Jugador
equipo_jugador = Table(
    "equipo_jugador",
    Base.metadata,
    Column("equipo_id", Integer, ForeignKey("equipos.id"), primary_key=True),
    Column("jugador_id", Integer, ForeignKey("jugadores.id"), primary_key=True),
)


class Equipo(Base):
    """
    Equipo de básquetbol que representa a un departamento.
    La validación de reglas (estrellas, género, mínimo jugadores)
    se realiza en el servicio antes de crear partidos.
    """
    __tablename__ = "equipos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    departamento_id: Mapped[int] = mapped_column(ForeignKey("departamentos.id"), nullable=False)

    departamento: Mapped["Departamento"] = relationship(back_populates="equipos")
    jugadores: Mapped[list["Jugador"]] = relationship(secondary="equipo_jugador", back_populates="equipos")
    partidos_como_local: Mapped[list["Partido"]] = relationship(
        foreign_keys="Partido.equipo_local_id", back_populates="equipo_local"
    )
    partidos_como_visitante: Mapped[list["Partido"]] = relationship(
        foreign_keys="Partido.equipo_visitante_id", back_populates="equipo_visitante"
    )

    def total_estrellas(self) -> int:
        return sum(j.estrellas for j in self.jugadores)

    def jugadores_por_genero(self, genero: str) -> int:
        return sum(1 for j in self.jugadores if j.genero.value == genero)

    def __repr__(self) -> str:
        return f"Equipo(id={self.id}, nombre={self.nombre!r})"
