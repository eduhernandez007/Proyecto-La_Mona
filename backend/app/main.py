from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import departamentos, jugadores, equipos, partidos, inscripciones, calistenia, puntajes, usuarios

# Importamos todos los modelos para que SQLAlchemy los registre antes de crear las tablas
from app.models import departamento, jugador, equipo, partido, inscripcion, usuario, calistenia as _m_calistenia  # noqa: F401

Base.metadata.create_all(bind=engine)

def seed_data():
    from app.database import SessionLocal
    from app.models.departamento import Departamento
    from app.models.usuario import Usuario, RolUsuario
    from app.models.jugador import Jugador, Genero
    
    db = SessionLocal()
    try:
        if db.query(Departamento).first() is not None:
            return
            
        # 1. Crear departamentos
        civil = Departamento(nombre="Civil")
        computacion = Departamento(nombre="Computación")
        electrica = Departamento(nombre="Eléctrica")
        fisica = Departamento(nombre="Física-Astronomía")
        industrias = Departamento(nombre="Industrias")
        matematica = Departamento(nombre="Matemática")
        
        db.add_all([civil, computacion, electrica, fisica, industrias, matematica])
        db.commit()
        
        # 2. Crear usuarios (clave por defecto: "1234")
        u_org = Usuario(nombre="Jorge Zambrano (Organizador CDI)", clave="1234", rol=RolUsuario.organizador)
        u_org_comp = Usuario(nombre="Christian Díaz (Org. Competencia)", clave="1234", rol=RolUsuario.organizador)
        u_juez_basquet = Usuario(nombre="Pablo Vergara (Juez Básquetbol)", clave="1234", rol=RolUsuario.juez)
        u_juez_calis = Usuario(nombre="Ana Maria (Juez Calistenia)", clave="1234", rol=RolUsuario.juez)
        
        u_centro_civil = Usuario(nombre="Centro Civil", clave="1234", rol=RolUsuario.centro_estudiantes, departamento_id=civil.id)
        u_centro_comp = Usuario(nombre="Centro Computación", clave="1234", rol=RolUsuario.centro_estudiantes, departamento_id=computacion.id)
        u_centro_elec = Usuario(nombre="Centro Eléctrica", clave="1234", rol=RolUsuario.centro_estudiantes, departamento_id=electrica.id)
        
        u_jug_civil1 = Usuario(nombre="Tomas Gonzalez (Jugador Civil)", clave="1234", rol=RolUsuario.jugador, departamento_id=civil.id)
        u_jug_comp1 = Usuario(nombre="Andres Bello (Jugador Computación)", clave="1234", rol=RolUsuario.jugador, departamento_id=computacion.id)
        
        db.add_all([u_org, u_org_comp, u_juez_basquet, u_juez_calis, u_centro_civil, u_centro_comp, u_centro_elec, u_jug_civil1, u_jug_comp1])
        
        # 3. Crear jugadores
        # Civil
        j_civil1 = Jugador(nombre="Tomas Gonzalez", genero=Genero.masculino, estrellas=2, departamento_id=civil.id)
        j_civil2 = Jugador(nombre="Sofia Plaza", genero=Genero.femenino, estrellas=1, departamento_id=civil.id)
        j_civil3 = Jugador(nombre="Carlos Muñoz", genero=Genero.masculino, estrellas=0, departamento_id=civil.id)
        j_civil4 = Jugador(nombre="Marta Gomez", genero=Genero.femenino, estrellas=2, departamento_id=civil.id)
        j_civil5 = Jugador(nombre="Pedro Ramirez", genero=Genero.masculino, estrellas=0, departamento_id=civil.id)
        j_civil6 = Jugador(nombre="Lucia Fernandez", genero=Genero.femenino, estrellas=0, departamento_id=civil.id)
        
        # Computacion
        j_comp1 = Jugador(nombre="Andres Bello", genero=Genero.masculino, estrellas=0, departamento_id=computacion.id)
        j_comp2 = Jugador(nombre="Elena Caffarena", genero=Genero.femenino, estrellas=3, departamento_id=computacion.id)
        j_comp3 = Jugador(nombre="Javier Silva", genero=Genero.masculino, estrellas=1, departamento_id=computacion.id)
        j_comp4 = Jugador(nombre="Camila Vallejo", genero=Genero.femenino, estrellas=1, departamento_id=computacion.id)
        j_comp5 = Jugador(nombre="Rodrigo Diaz", genero=Genero.masculino, estrellas=0, departamento_id=computacion.id)
        j_comp6 = Jugador(nombre="Francisca Perez", genero=Genero.femenino, estrellas=0, departamento_id=computacion.id)

        # Electrica
        j_elec1 = Jugador(nombre="Nicolas Tesla", genero=Genero.masculino, estrellas=3, departamento_id=electrica.id)
        j_elec2 = Jugador(nombre="Marie Curie", genero=Genero.femenino, estrellas=2, departamento_id=electrica.id)
        j_elec3 = Jugador(nombre="Albert Einstein", genero=Genero.masculino, estrellas=0, departamento_id=electrica.id)
        j_elec4 = Jugador(nombre="Ada Lovelace", genero=Genero.femenino, estrellas=0, departamento_id=electrica.id)
        j_elec5 = Jugador(nombre="Isaac Newton", genero=Genero.masculino, estrellas=0, departamento_id=electrica.id)
        j_elec6 = Jugador(nombre="Rosalind Franklin", genero=Genero.femenino, estrellas=0, departamento_id=electrica.id)

        db.add_all([
            j_civil1, j_civil2, j_civil3, j_civil4, j_civil5, j_civil6,
            j_comp1, j_comp2, j_comp3, j_comp4, j_comp5, j_comp6,
            j_elec1, j_elec2, j_elec3, j_elec4, j_elec5, j_elec6
        ])
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

seed_data()

app = FastAPI(
    title="Sistema La Mona - CDI",
    description="API para gestionar las Olimpiadas Interdepartamentales La Mona",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(departamentos.router)
app.include_router(jugadores.router)
app.include_router(equipos.router)
app.include_router(partidos.router)
app.include_router(inscripciones.router)
app.include_router(calistenia.router)
app.include_router(puntajes.router)
app.include_router(usuarios.router)


@app.get("/")
def root():
    return {
        "sistema": "La Mona - CDI",
        "version": "1.0.0",
        "docs": "/docs",
    }
