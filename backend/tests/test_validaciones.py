"""
Tests unitarios del ValidadorBasquetbol.

Construyen objetos Equipo y Jugador en memoria (sin base de datos) para
verificar las reglas de negocio de básquetbol de forma aislada.
"""
# Importamos TODOS los modelos para que SQLAlchemy pueda resolver las
# relaciones entre clases (Equipo referencia a Departamento y Partido por nombre).
from app.models.departamento import Departamento  # noqa: F401
from app.models.partido import Partido  # noqa: F401
from app.models.equipo import Equipo
from app.models.jugador import Jugador, Genero
from app.services.validaciones import ValidadorBasquetbol


def crear_jugador(genero: Genero, estrellas: int = 0) -> Jugador:
    """Crea un Jugador transitorio (sin guardar en base de datos)."""
    return Jugador(
        nombre="Test",
        genero=genero,
        estrellas=estrellas,
        departamento_id=1,
    )


def crear_equipo(jugadores: list[Jugador]) -> Equipo:
    """Crea un Equipo transitorio con la lista de jugadores dada."""
    equipo = Equipo(nombre="Equipo Test", departamento_id=1)
    for jugador in jugadores:
        equipo.jugadores.append(jugador)
    return equipo


validador = ValidadorBasquetbol()


# ─── validar_minimo_jugadores ────────────────────────────────────────────────

def test_minimo_jugadores_ok_con_5():
    """Con 5 jugadores la validación pasa (retorna None)."""
    jugadores = [crear_jugador(Genero.masculino) for _ in range(5)]
    equipo = crear_equipo(jugadores)
    assert validador.validar_minimo_jugadores(equipo) is None


def test_minimo_jugadores_error_con_4():
    """Con 4 jugadores la validación falla (retorna mensaje de error)."""
    jugadores = [crear_jugador(Genero.masculino) for _ in range(4)]
    equipo = crear_equipo(jugadores)
    error = validador.validar_minimo_jugadores(equipo)
    assert error is not None
    assert "4 jugadores" in error


# ─── validar_genero ──────────────────────────────────────────────────────────

def test_genero_error_con_menos_de_2_femeninas():
    """Equipo con 4 hombres y 1 mujer falla por falta de mujeres."""
    jugadores = [crear_jugador(Genero.masculino) for _ in range(4)]
    jugadores.append(crear_jugador(Genero.femenino))
    equipo = crear_equipo(jugadores)
    error = validador.validar_genero(equipo)
    assert error is not None


def test_genero_ok_con_2_de_cada():
    """Equipo con 3 hombres y 2 mujeres pasa la validación de género."""
    jugadores = [crear_jugador(Genero.masculino) for _ in range(3)]
    jugadores += [crear_jugador(Genero.femenino) for _ in range(2)]
    equipo = crear_equipo(jugadores)
    assert validador.validar_genero(equipo) is None


# ─── validar_estrellas ───────────────────────────────────────────────────────

def test_estrellas_error_superando_5():
    """Equipo con 6 estrellas en total falla la validación."""
    jugadores = [
        crear_jugador(Genero.masculino, estrellas=3),
        crear_jugador(Genero.masculino, estrellas=3),
        crear_jugador(Genero.femenino, estrellas=0),
    ]
    equipo = crear_equipo(jugadores)
    error = validador.validar_estrellas(equipo)
    assert error is not None
    assert "6 estrellas" in error


def test_estrellas_ok_con_5():
    """Equipo con exactamente 5 estrellas pasa la validación."""
    jugadores = [
        crear_jugador(Genero.masculino, estrellas=3),
        crear_jugador(Genero.femenino, estrellas=2),
    ]
    equipo = crear_equipo(jugadores)
    assert validador.validar_estrellas(equipo) is None
