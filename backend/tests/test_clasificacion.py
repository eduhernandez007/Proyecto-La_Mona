import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.departamento import Departamento
from app.models.equipo import Equipo
from app.models.partido import Partido, EstadoPartido
from app.services.puntajes import CalculadoraPuntajes

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_grupo_stage_scoring_and_tiebreakers(db_session):
    d1 = Departamento(nombre="Depto A")
    d2 = Departamento(nombre="Depto B")
    d3 = Departamento(nombre="Depto C")
    db_session.add_all([d1, d2, d3])
    db_session.commit()

    e1 = Equipo(nombre="Equipo A", departamento_id=d1.id)
    e2 = Equipo(nombre="Equipo B", departamento_id=d2.id)
    e3 = Equipo(nombre="Equipo C", departamento_id=d3.id)
    db_session.add_all([e1, e2, e3])
    db_session.commit()

    # Partido 1: A vs B (Jugado: A gana 10 - 8)
    p1 = Partido(
        equipo_local_id=e1.id,
        equipo_visitante_id=e2.id,
        puntos_local=10,
        puntos_visitante=8,
        estado=EstadoPartido.jugado,
        fase="Fase de Grupos"
    )
    # Partido 2: B vs C (Jugado: B gana 15 - 5)
    p2 = Partido(
        equipo_local_id=e2.id,
        equipo_visitante_id=e3.id,
        puntos_local=15,
        puntos_visitante=5,
        estado=EstadoPartido.jugado,
        fase="Fase de Grupos"
    )
    # Partido 3: C vs A (W.O: C comete W.O., A gana 2 - 0)
    p3 = Partido(
        equipo_local_id=e3.id,
        equipo_visitante_id=e1.id,
        puntos_local=0,
        puntos_visitante=2,
        estado=EstadoPartido.wo,
        fase="Fase de Grupos"
    )
    db_session.add_all([p1, p2, p3])
    db_session.commit()

    calc = CalculadoraPuntajes(db_session)
    
    # Equipo A: 4 pts, Dif: +4
    pts_a, dif_a, pf_a = calc._calcular_stats_grupo(e1.id, [p1, p2, p3])
    assert pts_a == 4
    assert dif_a == 4
    assert pf_a == 12

    # Equipo B: 3 pts, Dif: +8
    pts_b, dif_b, pf_b = calc._calcular_stats_grupo(e2.id, [p1, p2, p3])
    assert pts_b == 3
    assert dif_b == 8

    # Equipo C: 1 pt, Dif: -12
    pts_c, dif_c, pf_c = calc._calcular_stats_grupo(e3.id, [p1, p2, p3])
    assert pts_c == 1
    assert dif_c == -12

    # Probar ranking final
    ranking = calc.ranking_basquetbol()
    assert ranking == [e1.id, e2.id, e3.id]

def test_desempate_resultado_directo(db_session):
    d1 = Departamento(nombre="Depto A")
    d2 = Departamento(nombre="Depto B")
    d3 = Departamento(nombre="Depto C")
    db_session.add_all([d1, d2, d3])
    db_session.commit()

    e1 = Equipo(nombre="Equipo A", departamento_id=d1.id)
    e2 = Equipo(nombre="Equipo B", departamento_id=d2.id)
    e3 = Equipo(nombre="Equipo C", departamento_id=d3.id)
    db_session.add_all([e1, e2, e3])
    db_session.commit()

    p1 = Partido(equipo_local_id=e1.id, equipo_visitante_id=e2.id, puntos_local=10, puntos_visitante=8, estado=EstadoPartido.jugado, fase="Fase de Grupos")
    p2 = Partido(equipo_local_id=e2.id, equipo_visitante_id=e3.id, puntos_local=10, puntos_visitante=8, estado=EstadoPartido.jugado, fase="Fase de Grupos")
    p3 = Partido(equipo_local_id=e3.id, equipo_visitante_id=e1.id, puntos_local=10, puntos_visitante=8, estado=EstadoPartido.jugado, fase="Fase de Grupos")
    db_session.add_all([p1, p2, p3])
    db_session.commit()

    calc = CalculadoraPuntajes(db_session)
    stats = {}
    for eq in [e1, e2, e3]:
        pts, dif, favor = calc._calcular_stats_grupo(eq.id, [p1, p2, p3])
        stats[eq.id] = {"puntos": pts, "dif": dif, "favor": favor}

    # H2H A vs B: A gana
    comp_ab = calc._comparar_equipos_ids(e1.id, e2.id, [p1, p2, p3], stats)
    assert comp_ab == 1

    # H2H B vs C: B gana
    comp_bc = calc._comparar_equipos_ids(e2.id, e3.id, [p1, p2, p3], stats)
    assert comp_bc == 1

def test_phase_progression_ranking(db_session):
    e_ids = []
    for name in ["A", "B", "C", "D"]:
        d = Departamento(nombre=f"Depto {name}")
        db_session.add(d)
        db_session.commit()
        e = Equipo(nombre=f"Equipo {name}", departamento_id=d.id)
        db_session.add(e)
        db_session.commit()
        e_ids.append(e.id)

    e1_id, e2_id, e3_id, e4_id = e_ids

    ps1 = Partido(equipo_local_id=e1_id, equipo_visitante_id=e2_id, puntos_local=20, puntos_visitante=15, estado=EstadoPartido.jugado, fase="Semifinales")
    ps2 = Partido(equipo_local_id=e3_id, equipo_visitante_id=e4_id, puntos_local=30, puntos_visitante=25, estado=EstadoPartido.jugado, fase="Semifinales")
    pf = Partido(equipo_local_id=e1_id, equipo_visitante_id=e3_id, puntos_local=10, puntos_visitante=15, estado=EstadoPartido.jugado, fase="Final")
    
    db_session.add_all([ps1, ps2, pf])
    db_session.commit()

    calc = CalculadoraPuntajes(db_session)
    ranking = calc.ranking_basquetbol()

    assert ranking[0] == e3_id
    assert ranking[1] == e1_id
