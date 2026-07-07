from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.departamento import Departamento
from app.schemas.usuario import UsuarioCreate, UsuarioRead, LoginRequest, LoginResponse

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


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica un usuario por nombre y clave.
    Retorna los datos del usuario si las credenciales son correctas.
    """
    import re
    # Buscar el usuario de forma insensible a mayúsculas/minúsculas usando casefold()
    # y removiendo cualquier contenido entre paréntesis en el nombre almacenado
    usuarios = db.query(Usuario).all()
    usuario = None
    for u in usuarios:
        db_nombre_limpio = re.sub(r"\s*\(.*?\)\s*", "", u.nombre).strip().casefold()
        if db_nombre_limpio == data.nombre.strip().casefold():
            usuario = u
            break
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado. Verifica tu nombre.")
    if usuario.clave != data.clave:
        raise HTTPException(status_code=401, detail="Clave incorrecta.")
    return usuario
