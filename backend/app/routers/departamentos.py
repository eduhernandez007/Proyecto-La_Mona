from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.departamento import Departamento
from app.schemas.departamento import DepartamentoCreate, DepartamentoRead

router = APIRouter(prefix="/departamentos", tags=["Departamentos"])


@router.get("/", response_model=list[DepartamentoRead])
def listar_departamentos(db: Session = Depends(get_db)):
    return db.query(Departamento).all()


@router.post("/", response_model=DepartamentoRead, status_code=201)
def crear_departamento(data: DepartamentoCreate, db: Session = Depends(get_db)):
    existente = db.query(Departamento).filter(Departamento.nombre == data.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un departamento con ese nombre")
    dept = Departamento(nombre=data.nombre)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@router.delete("/{departamento_id}", status_code=204)
def eliminar_departamento(departamento_id: int, db: Session = Depends(get_db)):
    dept = db.get(Departamento, departamento_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    db.delete(dept)
    db.commit()
    return None
