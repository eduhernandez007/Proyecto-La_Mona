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

    def _calcular_stats_grupo(self, team_id: int, partidos: list[Partido]) -> tuple[int, int, int]:
        """
        Retorna (puntos_torneo, diferencia_puntos, puntos_favor) para el equipo dado
        en los partidos de la 'Fase de Grupos'.
        En fase de grupos: victoria = 2 pts, derrota = 1 pt, WO = 0 pts.
        """
        pts = 0
        favor = 0
        contra = 0
        for p in partidos:
            if p.fase != "Fase de Grupos":
                continue
            if p.estado == "pendiente":
                continue
                
            is_local = (p.equipo_local_id == team_id)
            is_visitante = (p.equipo_visitante_id == team_id)
            if not (is_local or is_visitante):
                continue
                
            p_self = p.puntos_local if is_local else p.puntos_visitante
            p_other = p.puntos_visitante if is_local else p.puntos_local
            
            if p_self is None or p_other is None:
                continue
                
            favor += p_self
            contra += p_other
            
            if p.estado == "wo":
                if p_self == 2 and p_other == 0:
                    pts += 2
                elif p_self == 0 and p_other == 2:
                    pts += 0
                elif p_self == 0 and p_other == 0:
                    pts += 0
            else:  # jugado
                if p_self > p_other:
                    pts += 2
                else:
                    pts += 1
                    
        return pts, (favor - contra), favor

    def _comparar_equipos_ids(self, t1_id: int, t2_id: int, partidos: list[Partido], stats: dict) -> int:
        """
        Comparador para desempates:
        1. Puntos del grupo
        2. Diferencia de puntos
        3. Resultado entre equipos empatados (H2H)
        4. Puntos a favor
        """
        p1 = stats[t1_id]["puntos"]
        p2 = stats[t2_id]["puntos"]
        if p1 != p2:
            return 1 if p1 > p2 else -1
            
        d1 = stats[t1_id]["dif"]
        d2 = stats[t2_id]["dif"]
        if d1 != d2:
            return 1 if d1 > d2 else -1
            
        # Enfrentamiento directo en Fase de Grupos
        for p in partidos:
            if p.fase != "Fase de Grupos" or p.estado == "pendiente":
                continue
            is_t1_local = (p.equipo_local_id == t1_id and p.equipo_visitante_id == t2_id)
            is_t2_local = (p.equipo_local_id == t2_id and p.equipo_visitante_id == t1_id)
            
            if is_t1_local:
                if p.puntos_local > p.puntos_visitante:
                    return 1
                elif p.puntos_visitante > p.puntos_local:
                    return -1
            elif is_t2_local:
                if p.puntos_local > p.puntos_visitante:
                    return -1
                elif p.puntos_visitante > p.puntos_local:
                    return 1
                    
        # Puntos a favor
        f1 = stats[t1_id]["favor"]
        f2 = stats[t2_id]["favor"]
        if f1 != f2:
            return 1 if f1 > f2 else -1
            
        return 0

    def ranking_basquetbol(self) -> list[int]:
        """
        Retorna la lista de IDs de equipos ordenados de 1er a último lugar
        según el avance en las fases (Final, Semifinales, Clasificación, Fase de Grupos)
        y las reglas de desempate en Fase de Grupos.
        """
        from functools import cmp_to_key
        equipos = self.db.query(Equipo).all()
        partidos = self.db.query(Partido).filter(Partido.estado != "pendiente").all()
        
        # Calcular estadísticas de grupo para cada equipo
        stats = {}
        for eq in equipos:
            pts, dif, favor = self._calcular_stats_grupo(eq.id, partidos)
            stats[eq.id] = {"puntos": pts, "dif": dif, "favor": favor, "equipo": eq}
            
        # Determinar posiciones top basadas en fases avanzadas
        final_match = next((p for p in partidos if p.fase == "Final"), None)
        semis_matches = [p for p in partidos if p.fase == "Semifinales"]
        clasif_matches = [p for p in partidos if p.fase == "Clasificación"]
        
        primer_lugar = None
        segundo_lugar = None
        tercer_lugar = None
        cuarto_lugar = None
        
        # 1. Final
        if final_match:
            if final_match.puntos_local is not None and final_match.puntos_visitante is not None:
                if final_match.puntos_local > final_match.puntos_visitante:
                    primer_lugar = final_match.equipo_local_id
                    segundo_lugar = final_match.equipo_visitante_id
                else:
                    primer_lugar = final_match.equipo_visitante_id
                    segundo_lugar = final_match.equipo_local_id
                    
        # 2. Semifinales (3º y 4º)
        perdedores_semis = []
        for p in semis_matches:
            if p.puntos_local is not None and p.puntos_visitante is not None:
                if p.puntos_local > p.puntos_visitante:
                    perdedores_semis.append(p.equipo_visitante_id)
                else:
                    perdedores_semis.append(p.equipo_local_id)
                    
        # Verificar si hay partido por el 3er lugar
        partido_tercer = None
        if len(perdedores_semis) >= 2:
            t1, t2 = perdedores_semis[0], perdedores_semis[1]
            for p in partidos:
                is_h2h = (p.equipo_local_id == t1 and p.equipo_visitante_id == t2) or (p.equipo_local_id == t2 and p.equipo_visitante_id == t1)
                if is_h2h and p not in semis_matches and p.fase in ["Semifinales", "Clasificación"]:
                    partido_tercer = p
                    break
                    
        if partido_tercer:
            if partido_tercer.puntos_local > partido_tercer.puntos_visitante:
                tercer_lugar = partido_tercer.equipo_local_id
                cuarto_lugar = partido_tercer.equipo_visitante_id
            else:
                tercer_lugar = partido_tercer.equipo_visitante_id
                cuarto_lugar = partido_tercer.equipo_local_id
        elif len(perdedores_semis) == 2:
            # Desempate por estadísticas de Fase de Grupos
            t1, t2 = perdedores_semis[0], perdedores_semis[1]
            comp = self._comparar_equipos_ids(t1, t2, partidos, stats)
            if comp >= 0:
                tercer_lugar = t1
                cuarto_lugar = t2
            else:
                tercer_lugar = t2
                cuarto_lugar = t1
        elif len(perdedores_semis) == 1:
            tercer_lugar = perdedores_semis[0]
            
        # 3. Clasificación (5º a 8º)
        top_4 = {primer_lugar, segundo_lugar, tercer_lugar, cuarto_lugar}
        equipos_clasif = set()
        for p in clasif_matches:
            equipos_clasif.add(p.equipo_local_id)
            equipos_clasif.add(p.equipo_visitante_id)
        equipos_clasif = {eid for eid in equipos_clasif if eid not in top_4}
        
        clasif_ordenados = sorted(
            list(equipos_clasif),
            key=cmp_to_key(lambda a, b: self._comparar_equipos_ids(b, a, partidos, stats))
        )
        
        # 4. Fase de grupos únicamente
        restante = [eq.id for eq in equipos if eq.id not in top_4 and eq.id not in equipos_clasif]
        restante_ordenados = sorted(
            restante,
            key=cmp_to_key(lambda a, b: self._comparar_equipos_ids(b, a, partidos, stats))
        )
        
        # Combinar ranking
        ranking = []
        if primer_lugar: ranking.append(primer_lugar)
        if segundo_lugar: ranking.append(segundo_lugar)
        if tercer_lugar: ranking.append(tercer_lugar)
        if cuarto_lugar: ranking.append(cuarto_lugar)
        ranking.extend(clasif_ordenados)
        ranking.extend(restante_ordenados)
        
        # Equipos sin ningún partido
        for eq in equipos:
            if eq.id not in ranking:
                ranking.append(eq.id)
                
        return ranking

    def puntajes_basquetbol(self) -> dict[int, int]:
        """
        Asigna puntaje de categoría A a cada departamento según su ranking final.
        """
        ranking_equipos = self.ranking_basquetbol()
        equipos_map = {e.id: e.departamento_id for e in self.db.query(Equipo).all()}
        
        puntajes = {}
        for lugar, eq_id in enumerate(ranking_equipos, start=1):
            dep_id = equipos_map.get(eq_id)
            if dep_id:
                puntajes[dep_id] = _puntaje_por_lugar(PUNTAJES_CATEGORIA_A, lugar)
                
        for d in self.db.query(Departamento).all():
            puntajes.setdefault(d.id, 0)
            
        return puntajes

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
