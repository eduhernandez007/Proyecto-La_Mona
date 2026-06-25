from abc import ABC, abstractmethod
from app.models.equipo import Equipo

MAXIMO_ESTRELLAS_EN_CANCHA = 5
MINIMO_JUGADORES_POR_EQUIPO = 5
MINIMO_TITULARES_POR_PARTIDO = 5
MAXIMO_JUGADORES_POR_EQUIPO = 12   # límite del plantel
MAXIMO_TITULARES_POR_PARTIDO = 12  # máximo en cancha por partido
MINIMO_JUGADORES_POR_GENERO = 2


class ValidadorCompetencia(ABC):
    """
    Clase base abstracta para validadores de competencias.
    Cada competencia define sus propias reglas de negocio.
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
        """Valida el límite de estrellas para el plantel completo (no se usa al agregar)."""
        total = sum(j.estrellas for j in equipo.jugadores)
        if total > MAXIMO_ESTRELLAS_EN_CANCHA:
            return (
                f"El equipo '{equipo.nombre}' tiene {total} estrellas. "
                f"El máximo permitido es {MAXIMO_ESTRELLAS_EN_CANCHA}."
            )
        return None

    def validar_maximo_plantel(self, equipo: Equipo) -> str | None:
        """Valida que el plantel no exceda 12 jugadores."""
        cantidad = len(equipo.jugadores)
        if cantidad > MAXIMO_JUGADORES_POR_EQUIPO:
            return (
                f"El equipo '{equipo.nombre}' tiene {cantidad} jugadores. "
                f"El máximo por plantel es {MAXIMO_JUGADORES_POR_EQUIPO}."
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

    def validar_titulares(self, jugadores: list) -> str | None:
        """
        Valida la alineación titular antes de un partido:
        - Entre 5 y 12 jugadores
        - Al menos 2 de cada género
        - Máximo 5 estrellas totales
        """
        cantidad = len(jugadores)
        if cantidad < MINIMO_TITULARES_POR_PARTIDO:
            return f"La alineación titular debe tener al menos {MINIMO_TITULARES_POR_PARTIDO} jugadores (tiene {cantidad})."
        if cantidad > MAXIMO_TITULARES_POR_PARTIDO:
            return f"La alineación titular no puede superar {MAXIMO_TITULARES_POR_PARTIDO} jugadores (tiene {cantidad})."

        masculinos = sum(1 for j in jugadores if j.genero.value == "M")
        femeninos = sum(1 for j in jugadores if j.genero.value == "F")
        if masculinos < MINIMO_JUGADORES_POR_GENERO:
            return f"La alineación titular debe tener al menos {MINIMO_JUGADORES_POR_GENERO} jugadores masculinos (tiene {masculinos})."
        if femeninos < MINIMO_JUGADORES_POR_GENERO:
            return f"La alineación titular debe tener al menos {MINIMO_JUGADORES_POR_GENERO} jugadoras femeninas (tiene {femeninos})."

        total_estrellas = sum(j.estrellas for j in jugadores)
        if total_estrellas > MAXIMO_ESTRELLAS_EN_CANCHA:
            return (
                f"La alineación titular tiene {total_estrellas} estrellas. "
                f"El máximo permitido en cancha es {MAXIMO_ESTRELLAS_EN_CANCHA}."
            )
        return None

    def validar_equipo_para_partido(self, equipo: Equipo) -> str | None:
        """Valida sólo el mínimo de jugadores y género del plantel (para detectar WO)."""
        for validacion in [
            self.validar_minimo_jugadores,
            self.validar_genero,
        ]:
            error = validacion(equipo)
            if error:
                return error
        return None

    def determinar_wo(self, equipo_local: Equipo, equipo_visitante: Equipo) -> str | None:
        """
        Determina si alguno de los equipos comete W.O. según las reglas de básquetbol.
        Un equipo comete W.O. si no cumple el mínimo de jugadores (5) o
        el mínimo de jugadores por género (2 de cada uno).
        Retorna: 'local', 'visitante', 'ambos' o None.
        """
        error_local = self.validar_minimo_jugadores(equipo_local) or self.validar_genero(equipo_local)
        error_visitante = self.validar_minimo_jugadores(equipo_visitante) or self.validar_genero(equipo_visitante)

        if error_local and error_visitante:
            return "ambos"
        if error_local:
            return "local"
        if error_visitante:
            return "visitante"
        return None


class ValidadorCalistenia(ValidadorCompetencia):
    """
    Implementa las reglas de negocio específicas de calistenia:
    - Validación de pruebas según la categoría (masculina o femenina).
    - El valor del resultado no puede ser negativo.
    """

    def validar_prueba(self, categoria, prueba) -> str | None:
        from app.models.calistenia import PRUEBAS_POR_CATEGORIA
        pruebas_validas = PRUEBAS_POR_CATEGORIA[categoria]
        if prueba not in pruebas_validas:
            return (
                f"La prueba '{prueba.value}' no está permitida para la "
                f"categoría {categoria.value}."
            )
        return None

    def validar_valor(self, valor: float) -> str | None:
        if valor < 0:
            return "El valor no puede ser negativo"
        return None
