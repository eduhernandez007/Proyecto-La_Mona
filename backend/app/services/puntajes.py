"""
Cálculo de puntajes por departamento para el torneo La Mona.

Cada competencia entrega puntaje al departamento según su posición final
(ver Anexo A.1 de las bases). Aquí se combinan básquetbol (categoría A) y
calistenia (categoría B) en un puntaje total por departamento.
"""
from sqlalchemy.orm import Session
from app.models.departamento import Departamento
from app.models.equipo import Equipo
from app.models.partido import Partido, EstadoPartido
from app.models.calistenia import ParticipanteCalistenia, CategoriaCalistenia

# Tabla A.1 — puntaje según lugar (índice 0 = 1er lugar, ... índice 7 = 8vo lugar)
PUNTAJES_CATEGORIA_A = [4000, 3200, 2400, 2000, 1600, 1200, 800, 400]  # básquetbol
PUNTAJES_CATEGORIA_B = [2000, 1600, 1200, 1000, 800, 600, 400, 200]    # calistenia


def _puntaje_por_lugar(tabla: list[int], lugar: int) -> int:
    """Retorna el puntaje del lugar dado (1-indexado). 0 si está fuera de la tabla."""
    if 1 <= lugar <= len(tabla):
        return tabla[lugar - 1]
    return 0


class CalculadoraPuntajes:
    """
    Calcula el puntaje total de cada departamento sumando los puntos
    obtenidos en básquetbol y calistenia.
    """

    def __init__(self, db: Session):
        self.db = db

    # ─── Básquetbol ───────────────────────────────────────────────────────────

    def victorias_por_departamento(self) -> dict[int, int]:
        """Cuenta las victorias de cada departamento en partidos jugados."""
        victorias: dict[int, int] = {}
        partidos = (
            self.db.query(Partido)
            .filter(Partido.estado == EstadoPartido.jugado)
            .all()
        )
        for partido in partidos:
            if partido.puntos_local is None or partido.puntos_visitante is None:
                continue
            if partido.puntos_local > partido.puntos_visitante:
                ganador = partido.equipo_local
            elif partido.puntos_visitante > partido.puntos_local:
                ganador = partido.equipo_visitante
            else:
                continue  # empate: no otorga victoria
            if ganador:
                dep = ganador.departamento_id
                victorias[dep] = victorias.get(dep, 0) + 1
        return victorias

    def puntajes_basquetbol(self) -> dict[int, int]:
        """
        Asigna puntaje de categoría A a cada departamento según su ranking
        de victorias. Solo participan departamentos con equipos.
        """
        victorias = self.victorias_por_departamento()
        # Departamentos que tienen al menos un equipo participan del ranking
        deptos_con_equipo = {
            e.departamento_id for e in self.db.query(Equipo).all()
        }
        for dep in deptos_con_equipo:
            victorias.setdefault(dep, 0)

        # Ranking: más victorias = mejor lugar
        ranking = sorted(victorias.items(), key=lambda x: x[1], reverse=True)
        return {
            dep: _puntaje_por_lugar(PUNTAJES_CATEGORIA_A, lugar)
            for lugar, (dep, _) in enumerate(ranking, start=1)
        }

    # ─── Calistenia ───────────────────────────────────────────────────────────

    def _puntaje_participante(self, participante: ParticipanteCalistenia) -> float:
        """Suma de los valores de todas las pruebas del participante."""
        return sum(r.valor for r in participante.resultados)

    def rendimiento_calistenia_por_departamento(self) -> dict[int, float]:
        """
        Para cada departamento, suma los 4 mejores resultados:
        los 2 mejores participantes masculinos + los 2 mejores femeninos.
        """
        participantes = self.db.query(ParticipanteCalistenia).all()

        # Agrupamos puntajes por (departamento, categoría)
        por_depto: dict[int, dict[CategoriaCalistenia, list[float]]] = {}
        for p in participantes:
            puntaje = self._puntaje_participante(p)
            por_depto.setdefault(p.departamento_id, {
                CategoriaCalistenia.masculina: [],
                CategoriaCalistenia.femenina: [],
            })
            por_depto[p.departamento_id][p.categoria].append(puntaje)

        rendimiento: dict[int, float] = {}
        for dep, categorias in por_depto.items():
            mejores_m = sorted(categorias[CategoriaCalistenia.masculina], reverse=True)[:2]
            mejores_f = sorted(categorias[CategoriaCalistenia.femenina], reverse=True)[:2]
            rendimiento[dep] = sum(mejores_m) + sum(mejores_f)
        return rendimiento

    def puntajes_calistenia(self) -> dict[int, int]:
        """Asigna puntaje de categoría B según el ranking de rendimiento."""
        rendimiento = self.rendimiento_calistenia_por_departamento()
        ranking = sorted(rendimiento.items(), key=lambda x: x[1], reverse=True)
        return {
            dep: _puntaje_por_lugar(PUNTAJES_CATEGORIA_B, lugar)
            for lugar, (dep, _) in enumerate(ranking, start=1)
        }

    # ─── Total ────────────────────────────────────────────────────────────────

    def calcular(self) -> list[dict]:
        """
        Retorna la tabla final de puntajes, ordenada de mayor a menor total.
        Incluye el desglose por competencia.
        """
        basquetbol = self.puntajes_basquetbol()
        calistenia = self.puntajes_calistenia()
        departamentos = self.db.query(Departamento).all()

        tabla = []
        for dep in departamentos:
            pts_basquet = basquetbol.get(dep.id, 0)
            pts_calist = calistenia.get(dep.id, 0)
            tabla.append({
                "departamento_id": dep.id,
                "departamento": dep.nombre,
                "puntaje_basquetbol": pts_basquet,
                "puntaje_calistenia": pts_calist,
                "puntaje_total": pts_basquet + pts_calist,
            })

        tabla.sort(key=lambda x: x["puntaje_total"], reverse=True)
        return tabla
