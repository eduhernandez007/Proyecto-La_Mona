from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.departamento import Departamento
from app.schemas.usuario import UsuarioCreate, UsuarioRead

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.post("/", response_model=UsuarioRead, status_code=201)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    if data.departamento_id is not None:
        dept = db.get(Departamento, data.departamento_id)
        if not dept:
            raise HTTPException(status_code=404, detail="Departamento no encontrado")

    usuario = Usuario(**data.model_dump())
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
