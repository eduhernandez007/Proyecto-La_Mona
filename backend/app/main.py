from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import departamentos, jugadores, equipos, partidos, inscripciones, calistenia, puntajes, usuarios

# Importamos todos los modelos para que SQLAlchemy los registre antes de crear las tablas
from app.models import departamento, jugador, equipo, partido, inscripcion, usuario, calistenia as _m_calistenia  # noqa: F401

import os
import alembic.config
import alembic.command

# Ejecutar las migraciones automáticamente en lugar de solo crear tablas
alembic_ini_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini")
alembic_cfg = alembic.config.Config(alembic_ini_path)
alembic.command.upgrade(alembic_cfg, "head")

def seed_data():
    from app.database import SessionLocal
    from app.models.departamento import Departamento
    from app.models.usuario import Usuario, RolUsuario
    from app.models.jugador import Jugador, Genero
    
    db = SessionLocal()
    try:
        # 1. Asegurar que existan todos los departamentos base
        nombres_deptos = ["Civil", "Computación", "Eléctrica", "Física-Astronomía", "Industrias", "Matemática", "Mecánica"]
        deptos_obj = {}
        for nombre in nombres_deptos:
            depto = db.query(Departamento).filter_by(nombre=nombre).first()
            if not depto:
                depto = Departamento(nombre=nombre)
                db.add(depto)
                db.commit()
                db.refresh(depto)
            deptos_obj[nombre] = depto
            
        # Si ya existe algún usuario organizador, asumimos que los datos iniciales (usuarios/jugadores) ya fueron insertados
        if db.query(Usuario).filter_by(rol=RolUsuario.organizador).first() is not None:
            return
            
        # 2. Crear usuarios (clave por defecto: "1234")
        u_org = Usuario(nombre="Jorge Zambrano (Organizador CDI)", clave="1234", rol=RolUsuario.organizador)
        u_org_comp = Usuario(nombre="Christian Díaz (Org. Competencia)", clave="1234", rol=RolUsuario.organizador)
        u_juez_basquet = Usuario(nombre="Pablo Vergara (Juez Básquetbol)", clave="1234", rol=RolUsuario.juez)
        u_juez_calis = Usuario(nombre="Ana Maria (Juez Calistenia)", clave="1234", rol=RolUsuario.juez)
        
        u_centro_civil = Usuario(nombre="Centro Civil", clave="1234", rol=RolUsuario.centro_estudiantes, departamento_id=deptos_obj["Civil"].id)
        u_centro_comp = Usuario(nombre="Centro Computación", clave="1234", rol=RolUsuario.centro_estudiantes, departamento_id=deptos_obj["Computación"].id)
        u_centro_elec = Usuario(nombre="Centro Eléctrica", clave="1234", rol=RolUsuario.centro_estudiantes, departamento_id=deptos_obj["Eléctrica"].id)
        u_centro_meca = Usuario(nombre="Centro Mecánica", clave="1234", rol=RolUsuario.centro_estudiantes, departamento_id=deptos_obj["Mecánica"].id)
        
        u_jug_civil1 = Usuario(nombre="Tomas Gonzalez (Jugador Civil)", clave="1234", rol=RolUsuario.jugador, departamento_id=deptos_obj["Civil"].id)
        u_jug_comp1 = Usuario(nombre="Andres Bello (Jugador Computación)", clave="1234", rol=RolUsuario.jugador, departamento_id=deptos_obj["Computación"].id)
        u_jug_meca1 = Usuario(nombre="Nikolaus Otto (Jugador Mecánica)", clave="1234", rol=RolUsuario.jugador, departamento_id=deptos_obj["Mecánica"].id)
        
        db.add_all([u_org, u_org_comp, u_juez_basquet, u_juez_calis, u_centro_civil, u_centro_comp, u_centro_elec, u_centro_meca, u_jug_civil1, u_jug_comp1, u_jug_meca1])
        
        # 3. Crear jugadores
        # Civil
        j_civil1 = Jugador(nombre="Tomas Gonzalez", genero=Genero.masculino, estrellas=2, departamento_id=deptos_obj["Civil"].id)
        j_civil2 = Jugador(nombre="Sofia Plaza", genero=Genero.femenino, estrellas=1, departamento_id=deptos_obj["Civil"].id)
        j_civil3 = Jugador(nombre="Carlos Muñoz", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Civil"].id)
        j_civil4 = Jugador(nombre="Marta Gomez", genero=Genero.femenino, estrellas=2, departamento_id=deptos_obj["Civil"].id)
        j_civil5 = Jugador(nombre="Pedro Ramirez", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Civil"].id)
        j_civil6 = Jugador(nombre="Lucia Fernandez", genero=Genero.femenino, estrellas=0, departamento_id=deptos_obj["Civil"].id)
        
        # Computacion
        j_comp1 = Jugador(nombre="Andres Bello", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Computación"].id)
        j_comp2 = Jugador(nombre="Elena Caffarena", genero=Genero.femenino, estrellas=3, departamento_id=deptos_obj["Computación"].id)
        j_comp3 = Jugador(nombre="Javier Silva", genero=Genero.masculino, estrellas=1, departamento_id=deptos_obj["Computación"].id)
        j_comp4 = Jugador(nombre="Camila Vallejo", genero=Genero.femenino, estrellas=1, departamento_id=deptos_obj["Computación"].id)
        j_comp5 = Jugador(nombre="Rodrigo Diaz", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Computación"].id)
        j_comp6 = Jugador(nombre="Francisca Perez", genero=Genero.femenino, estrellas=0, departamento_id=deptos_obj["Computación"].id)
 
        # Electrica
        j_elec1 = Jugador(nombre="Nicolas Tesla", genero=Genero.masculino, estrellas=3, departamento_id=deptos_obj["Eléctrica"].id)
        j_elec2 = Jugador(nombre="Marie Curie", genero=Genero.femenino, estrellas=2, departamento_id=deptos_obj["Eléctrica"].id)
        j_elec3 = Jugador(nombre="Albert Einstein", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Eléctrica"].id)
        j_elec4 = Jugador(nombre="Ada Lovelace", genero=Genero.femenino, estrellas=0, departamento_id=deptos_obj["Eléctrica"].id)
        j_elec5 = Jugador(nombre="Isaac Newton", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Eléctrica"].id)
        j_elec6 = Jugador(nombre="Rosalind Franklin", genero=Genero.femenino, estrellas=0, departamento_id=deptos_obj["Eléctrica"].id)
 
        # Mecánica
        j_meca1 = Jugador(nombre="Nikolaus Otto", genero=Genero.masculino, estrellas=2, departamento_id=deptos_obj["Mecánica"].id)
        j_meca2 = Jugador(nombre="Rudolf Diesel", genero=Genero.masculino, estrellas=1, departamento_id=deptos_obj["Mecánica"].id)
        j_meca3 = Jugador(nombre="Kate Gleason", genero=Genero.femenino, estrellas=1, departamento_id=deptos_obj["Mecánica"].id)
        j_meca4 = Jugador(nombre="James Watt", genero=Genero.masculino, estrellas=1, departamento_id=deptos_obj["Mecánica"].id)
        j_meca5 = Jugador(nombre="Verena Holmes", genero=Genero.femenino, estrellas=0, departamento_id=deptos_obj["Mecánica"].id)
        j_meca6 = Jugador(nombre="Margaret Ingels", genero=Genero.femenino, estrellas=0, departamento_id=deptos_obj["Mecánica"].id)
 
        # Industrias
        j_ind1 = Jugador(nombre="Henry Ford", genero=Genero.masculino, estrellas=2, departamento_id=deptos_obj["Industrias"].id)
        j_ind2 = Jugador(nombre="Frederick Taylor", genero=Genero.masculino, estrellas=1, departamento_id=deptos_obj["Industrias"].id)
        j_ind3 = Jugador(nombre="Lillian Gilbreth", genero=Genero.femenino, estrellas=3, departamento_id=deptos_obj["Industrias"].id)
        j_ind4 = Jugador(nombre="Taiichi Ohno", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Industrias"].id)
        j_ind5 = Jugador(nombre="Mary Parker", genero=Genero.femenino, estrellas=1, departamento_id=deptos_obj["Industrias"].id)
        j_ind6 = Jugador(nombre="Elton Mayo", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Industrias"].id)

        # Matemática
        j_mat1 = Jugador(nombre="Alan Turing", genero=Genero.masculino, estrellas=3, departamento_id=deptos_obj["Matemática"].id)
        j_mat2 = Jugador(nombre="Emmy Noether", genero=Genero.femenino, estrellas=2, departamento_id=deptos_obj["Matemática"].id)
        j_mat3 = Jugador(nombre="Carl Gauss", genero=Genero.masculino, estrellas=1, departamento_id=deptos_obj["Matemática"].id)
        j_mat4 = Jugador(nombre="Sofia Kovalevskaya", genero=Genero.femenino, estrellas=2, departamento_id=deptos_obj["Matemática"].id)
        j_mat5 = Jugador(nombre="Leonhard Euler", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Matemática"].id)
        j_mat6 = Jugador(nombre="Hypatia de Alejandría", genero=Genero.femenino, estrellas=0, departamento_id=deptos_obj["Matemática"].id)

        # Física-Astronomía
        j_fis1 = Jugador(nombre="Galileo Galilei", genero=Genero.masculino, estrellas=1, departamento_id=deptos_obj["Física-Astronomía"].id)
        j_fis2 = Jugador(nombre="Vera Rubin", genero=Genero.femenino, estrellas=2, departamento_id=deptos_obj["Física-Astronomía"].id)
        j_fis3 = Jugador(nombre="Max Planck", genero=Genero.masculino, estrellas=2, departamento_id=deptos_obj["Física-Astronomía"].id)
        j_fis4 = Jugador(nombre="Chien-Shiung Wu", genero=Genero.femenino, estrellas=1, departamento_id=deptos_obj["Física-Astronomía"].id)
        j_fis5 = Jugador(nombre="Niels Bohr", genero=Genero.masculino, estrellas=0, departamento_id=deptos_obj["Física-Astronomía"].id)
        j_fis6 = Jugador(nombre="Lise Meitner", genero=Genero.femenino, estrellas=0, departamento_id=deptos_obj["Física-Astronomía"].id)

        db.add_all([
            j_civil1, j_civil2, j_civil3, j_civil4, j_civil5, j_civil6,
            j_comp1, j_comp2, j_comp3, j_comp4, j_comp5, j_comp6,
            j_elec1, j_elec2, j_elec3, j_elec4, j_elec5, j_elec6,
            j_meca1, j_meca2, j_meca3, j_meca4, j_meca5, j_meca6,
            j_ind1, j_ind2, j_ind3, j_ind4, j_ind5, j_ind6,
            j_mat1, j_mat2, j_mat3, j_mat4, j_mat5, j_mat6,
            j_fis1, j_fis2, j_fis3, j_fis4, j_fis5, j_fis6
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
