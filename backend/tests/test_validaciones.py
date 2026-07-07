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


# ─── validar_equipo_para_partido ────────────────────────────────────────────

def test_validar_equipo_para_partido_ok():
    """Equipo válido (5 jugadores, 2 de cada género, <=5 estrellas) pasa."""
    jugadores = [
        crear_jugador(Genero.masculino, estrellas=1),
        crear_jugador(Genero.masculino, estrellas=1),
        crear_jugador(Genero.masculino, estrellas=1),
        crear_jugador(Genero.femenino, estrellas=1),
        crear_jugador(Genero.femenino, estrellas=1),
    ]
    equipo = crear_equipo(jugadores)
    assert validador.validar_equipo_para_partido(equipo) is None


def test_validar_equipo_para_partido_falla_por_pocos_jugadores():
    """Con 4 jugadores, validar_equipo_para_partido retorna error."""
    jugadores = [
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.femenino),
        crear_jugador(Genero.femenino),
    ]
    equipo = crear_equipo(jugadores)
    assert validador.validar_equipo_para_partido(equipo) is not None


def test_validar_equipo_para_partido_falla_por_genero():
    """Con 5 jugadores pero solo 1 femenina, falla por género."""
    jugadores = [
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.femenino),
    ]
    equipo = crear_equipo(jugadores)
    assert validador.validar_equipo_para_partido(equipo) is not None


def test_validar_equipo_para_partido_no_valida_estrellas():
    """
    validar_equipo_para_partido ya NO rechaza por límite de estrellas.
    Las estrellas se validan en validar_titulares (alineación del partido).
    """
    jugadores = [
        crear_jugador(Genero.masculino, estrellas=3),
        crear_jugador(Genero.masculino, estrellas=3),
        crear_jugador(Genero.masculino, estrellas=0),
        crear_jugador(Genero.femenino, estrellas=0),
        crear_jugador(Genero.femenino, estrellas=0),
    ]
    equipo = crear_equipo(jugadores)
    # Debe pasar (None) porque plantel solo se valida por cantidad y género
    assert validador.validar_equipo_para_partido(equipo) is None


# ─── validar_titulares ──────────────────────────────────────────────────

def test_validar_titulares_ok():
    """Alineación con 5 jugadores, 2 de cada género y <= 5 estrellas es válida."""
    titulares = [
        crear_jugador(Genero.masculino, estrellas=1),
        crear_jugador(Genero.masculino, estrellas=1),
        crear_jugador(Genero.masculino, estrellas=1),
        crear_jugador(Genero.femenino, estrellas=1),
        crear_jugador(Genero.femenino, estrellas=1),
    ]
    assert validador.validar_titulares(titulares) is None


def test_validar_titulares_falla_por_pocos_jugadores():
    """Con solo 4 titulares la alineación es inválida."""
    titulares = [
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.femenino),
        crear_jugador(Genero.femenino),
    ]
    assert validador.validar_titulares(titulares) is not None


def test_validar_titulares_falla_por_genero():
    """Con 5 titulares pero solo 1 femenina, la alineación es inválida."""
    titulares = [
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.femenino),
    ]
    assert validador.validar_titulares(titulares) is not None


def test_validar_titulares_falla_por_estrellas():
    """Con 5 titulares válidos pero 6 estrellas totales, la alineación es inválida."""
    titulares = [
        crear_jugador(Genero.masculino, estrellas=3),
        crear_jugador(Genero.masculino, estrellas=3),
        crear_jugador(Genero.masculino, estrellas=0),
        crear_jugador(Genero.femenino, estrellas=0),
        crear_jugador(Genero.femenino, estrellas=0),
    ]
    assert validador.validar_titulares(titulares) is not None


def test_validar_titulares_falla_por_demasiados_jugadores():
    """Con 13 titulares se supera el máximo de 12 por partido."""
    titulares = [
        crear_jugador(Genero.masculino) for _ in range(7)
    ] + [
        crear_jugador(Genero.femenino) for _ in range(6)
    ]
    assert validador.validar_titulares(titulares) is not None


# ─── determinar_wo ──────────────────────────────────────────────────────

def _equipo_valido() -> Equipo:
    """Crea un equipo que cumple todos los requisitos mínimos de básquetbol."""
    jugadores = [
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.femenino),
        crear_jugador(Genero.femenino),
    ]
    return crear_equipo(jugadores)


def _equipo_invalido_pocos_jugadores() -> Equipo:
    """Crea un equipo con menos de 5 jugadores (comete W.O.)."""
    jugadores = [
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.femenino),
    ]
    return crear_equipo(jugadores)


def _equipo_invalido_genero() -> Equipo:
    """Crea un equipo con 5 jugadores pero solo 1 femenina (comete W.O.)."""
    jugadores = [
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.masculino),
        crear_jugador(Genero.femenino),
    ]
    return crear_equipo(jugadores)


def test_determinar_wo_ninguno():
    """Ambos equipos cumplen los requisitos: no hay W.O."""
    local = _equipo_valido()
    visitante = _equipo_valido()
    assert validador.determinar_wo(local, visitante) is None


def test_determinar_wo_local_por_pocos_jugadores():
    """El equipo local tiene menos de 5 jugadores: W.O. local."""
    local = _equipo_invalido_pocos_jugadores()
    visitante = _equipo_valido()
    assert validador.determinar_wo(local, visitante) == "local"


def test_determinar_wo_visitante_por_genero():
    """El equipo visitante no tiene 2 jugadoras mínimas: W.O. visitante."""
    local = _equipo_valido()
    visitante = _equipo_invalido_genero()
    assert validador.determinar_wo(local, visitante) == "visitante"


def test_determinar_wo_ambos():
    """Ambos equipos son inválidos: W.O. de ambos."""
    local = _equipo_invalido_pocos_jugadores()
    visitante = _equipo_invalido_genero()
    assert validador.determinar_wo(local, visitante) == "ambos"


# ─── ValidadorCalistenia ─────────────────────────────────────────────────

from app.models.calistenia import CategoriaCalistenia, PruebaCalistenia
from app.services.validaciones import ValidadorCalistenia

validador_calis = ValidadorCalistenia()


def test_calistenia_prueba_valida_masculina():
    """muscle_ups es una prueba válida para la categoría masculina."""
    error = validador_calis.validar_prueba(
        CategoriaCalistenia.masculina, PruebaCalistenia.muscle_ups
    )
    assert error is None


def test_calistenia_prueba_invalida_masculina():
    """hang_hold no está permitida para la categoría masculina."""
    error = validador_calis.validar_prueba(
        CategoriaCalistenia.masculina, PruebaCalistenia.hang_hold
    )
    assert error is not None


def test_calistenia_prueba_valida_femenina():
    """hang_hold es válida para la categoría femenina."""
    error = validador_calis.validar_prueba(
        CategoriaCalistenia.femenina, PruebaCalistenia.hang_hold
    )
    assert error is None


def test_calistenia_prueba_invalida_femenina():
    """muscle_ups no está permitida para la categoría femenina."""
    error = validador_calis.validar_prueba(
        CategoriaCalistenia.femenina, PruebaCalistenia.muscle_ups
    )
    assert error is not None


def test_calistenia_pruebas_comunes_masculina():
    """pull_ups, push_ups y handstand_hold son válidas para la categoría masculina."""
    for prueba in [
        PruebaCalistenia.pull_ups,
        PruebaCalistenia.push_ups,
        PruebaCalistenia.handstand_hold,
    ]:
        assert validador_calis.validar_prueba(CategoriaCalistenia.masculina, prueba) is None


def test_calistenia_pruebas_comunes_femenina():
    """pull_ups, push_ups y handstand_hold son válidas para la categoría femenina."""
    for prueba in [
        PruebaCalistenia.pull_ups,
        PruebaCalistenia.push_ups,
        PruebaCalistenia.handstand_hold,
    ]:
        assert validador_calis.validar_prueba(CategoriaCalistenia.femenina, prueba) is None


def test_calistenia_valor_positivo_ok():
    """Un valor positivo pasa la validación."""
    assert validador_calis.validar_valor(10.5) is None


def test_calistenia_valor_cero_ok():
    """El valor 0 es permitido (el participante no realizó ninguna repetición)."""
    assert validador_calis.validar_valor(0) is None


def test_calistenia_valor_negativo_error():
    """Un valor negativo retorna error (sin sentido físico)."""
    error = validador_calis.validar_valor(-1)
    assert error is not None
