from abc import ABC, abstractmethod
from app.models.equipo import Equipo

MAXIMO_ESTRELLAS_EN_CANCHA = 5
MINIMO_JUGADORES_POR_EQUIPO = 5
MAXIMO_JUGADORES_POR_EQUIPO = 12
MINIMO_JUGADORES_POR_GENERO = 2


class ValidadorCompetencia(ABC):
    """
    Clase base abstracta para validadores de competencias.
    Cada competencia define sus propias reglas de negocio.
    """

    @abstractmethod
    def validar_equipo_para_partido(self, equipo: Equipo) -> str | None:
        """
        Valida si un equipo cumple las reglas para jugar.
        Retorna un mensaje de error si no cumple, None si está ok.
        """
        pass

    @abstractmethod
    def validar_estrellas(self, equipo: Equipo) -> str | None:
        """
        Valida la restricción de estrellas del equipo.
        Retorna un mensaje de error si no cumple, None si está ok.
        """
        pass


class ValidadorBasquetbol(ValidadorCompetencia):
    """
    Implementa las reglas de negocio específicas de básquetbol:
    - Mínimo 5 jugadores
    - Máximo 12 jugadores
    - Al menos 2 de cada género
    - Máximo 5 estrellas totales en cancha
    """

    def validar_estrellas(self, equipo: Equipo) -> str | None:
        total = sum(j.estrellas for j in equipo.jugadores)
        if total > MAXIMO_ESTRELLAS_EN_CANCHA:
            return (
                f"El equipo '{equipo.nombre}' tiene {total} estrellas. "
                f"El máximo permitido es {MAXIMO_ESTRELLAS_EN_CANCHA}."
            )
        return None

    def validar_minimo_jugadores(self, equipo: Equipo) -> str | None:
        cantidad = len(equipo.jugadores)
        if cantidad < MINIMO_JUGADORES_POR_EQUIPO:
            return (
                f"El equipo '{equipo.nombre}' tiene {cantidad} jugadores. "
                f"Se necesitan al menos {MINIMO_JUGADORES_POR_EQUIPO}."
            )
        return None

    def validar_genero(self, equipo: Equipo) -> str | None:
        masculinos = sum(1 for j in equipo.jugadores if j.genero.value == "M")
        femeninos = sum(1 for j in equipo.jugadores if j.genero.value == "F")
        if masculinos < MINIMO_JUGADORES_POR_GENERO:
            return (
                f"El equipo '{equipo.nombre}' tiene solo {masculinos} jugador(es) masculino(s). "
                f"Se necesitan al menos {MINIMO_JUGADORES_POR_GENERO}."
            )
        if femeninos < MINIMO_JUGADORES_POR_GENERO:
            return (
                f"El equipo '{equipo.nombre}' tiene solo {femeninos} jugadora(s). "
                f"Se necesitan al menos {MINIMO_JUGADORES_POR_GENERO}."
            )
        return None

    def validar_equipo_para_partido(self, equipo: Equipo) -> str | None:
        """Ejecuta todas las validaciones en orden."""
        for validacion in [
            self.validar_minimo_jugadores,
            self.validar_genero,
            self.validar_estrellas,
        ]:
            error = validacion(equipo)
            if error:
                return error
        return None
