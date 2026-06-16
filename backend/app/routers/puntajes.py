from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.puntaje import PuntajeDepartamento
from app.services.puntajes import CalculadoraPuntajes

router = APIRouter(prefix="/puntajes", tags=["Puntajes"])


@router.get("/", response_model=list[PuntajeDepartamento])
def obtener_puntajes(db: Session = Depends(get_db)):
    """
    Tabla general del torneo: puntaje total de cada departamento
    sumando básquetbol (categoría A) y calistenia (categoría B),
    ordenada de mayor a menor.
    """
    calculadora = CalculadoraPuntajes(db)
    return calculadora.calcular()
