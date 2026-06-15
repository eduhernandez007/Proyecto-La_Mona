from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import departamentos, jugadores, equipos, partidos, inscripciones

# Importamos todos los modelos para que SQLAlchemy los registre antes de crear las tablas
from app.models import departamento, jugador, equipo, partido, inscripcion  # noqa: F401

Base.metadata.create_all(bind=engine)

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


@app.get("/")
def root():
    return {
        "sistema": "La Mona - CDI",
        "version": "1.0.0",
        "docs": "/docs",
    }
