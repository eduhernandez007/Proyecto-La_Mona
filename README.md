# Sistema de Gestión "La Mona" — CDI

Plataforma web para administrar las olimpiadas interdepartamentales **"La Mona"**, organizadas por el Centro Deportivo de Ingeniería (CDI) de la Universidad de Chile. El sistema centraliza la gestión de competencias, inscripciones, resultados y el cálculo de puntajes por departamento, reemplazando las planillas dispersas que se usan actualmente.

El proyecto modela el dominio con Programación Orientada a Objetos y soporta dos competencias: **Básquetbol** (grupal, categoría A) y **Calistenia** (individual, categoría B). Incluye validación de reglas de negocio (límite de estrellas, mínimo de jugadores, restricciones de género y categoría), un flujo de inscripciones con aprobación, un sistema de roles de usuario y el cálculo automático de la tabla general del torneo.

## Stack tecnológico

- **Lenguaje:** Python 3.11+
- **Framework backend:** FastAPI
- **ORM:** SQLAlchemy 2.0
- **Validación de datos:** Pydantic v2
- **Servidor:** Uvicorn
- **Base de datos:** SQLite (desarrollo)
- **Tests:** pytest
- **Frontend:** HTML + CSS + JavaScript (vanilla, sin frameworks)
- **Despliegue:** Docker + docker-compose

## Instalación y ejecución local

Requiere tener Python 3.11 o superior instalado.

```bash
# 1. Entrar a la carpeta del backend
cd backend

# 2. Crear un entorno virtual
python -m venv .venv

# 3. Activar el entorno virtual
#    En Windows (PowerShell):
.venv\Scripts\Activate.ps1
#    En Linux / macOS:
source .venv/bin/activate

# 4. Instalar las dependencias
pip install -r requirements.txt

# 5. Levantar el servidor
uvicorn app.main:app --reload
```

El backend quedará disponible en `http://localhost:8000`.
La documentación interactiva de la API (Swagger) está en `http://localhost:8000/docs`.

### Abrir el frontend

Con el backend corriendo, abre el archivo `frontend/index.html` directamente en el navegador (doble clic). La interfaz se conecta automáticamente al backend en `http://localhost:8000`.

## Correr los tests

Desde la carpeta `backend/`, con el entorno virtual activado:

```bash
python -m pytest tests/ -v
```

Los tests verifican las reglas de negocio de básquetbol (mínimo de jugadores, restricción de género y límite de estrellas).

## Levantar con Docker

No requiere instalar Python ni dependencias manualmente. Desde la raíz del proyecto:

```bash
docker-compose up --build
```

El backend quedará disponible en `http://localhost:8000`. Para detenerlo, presiona `Ctrl+C` o ejecuta `docker-compose down`.

## Usuarios de prueba y credenciales

El sistema cuenta con inicio de sesión e identificación de roles. Para ingresar en el login, los usuarios deben ingresar su **nombre simplificado** (sin paréntesis ni departamento) y la contraseña por defecto **`1234`**:

| Nombre para iniciar sesión | Contraseña | Nombre Completo en Sistema | Rol / Permisos |
| :--- | :---: | :--- | :--- |
| `jorge zambrano` | `1234` | `Jorge Zambrano (Organizador CDI)` | Organizador |
| `christian díaz` | `1234` | `Christian Díaz (Org. Competencia)` | Organizador |
| `pablo vergara` | `1234` | `Pablo Vergara (Juez Básquetbol)` | Juez |
| `ana maria` | `1234` | `Ana Maria (Juez Calistenia)` | Juez |
| `centro civil` | `1234` | `Centro Civil` | Centro Estudiantes (Civil) |
| `centro computación` | `1234` | `Centro Computación` | Centro Estudiantes (Computación) |
| `centro eléctrica` | `1234` | `Centro Eléctrica` | Centro Estudiantes (Eléctrica) |
| `tomas gonzalez` | `1234` | `Tomas Gonzalez (Jugador Civil)` | Jugador (Civil) |
| `andres bello` | `1234` | `Andres Bello (Jugador Computación)` | Jugador (Computación) |

- **Organizador**: Permisos totales globales (crear/eliminar departamentos, equipos, jugadores, partidos y calistenia).
- **Centro de Estudiantes**: Pueden añadir y eliminar equipos y jugadores, además de aprobar/rechazar solicitudes de inscripción de su departamento.
- **Juez**: Pueden registrar marcas de calistenia y resultados de básquetbol.
- **Jugador**: Pueden solicitar inscribirse en equipos de básquetbol.

## Estructura de carpetas

```
.
├── README.md                  Este archivo
├── docker-compose.yml         Orquestación de Docker
├── AGENTS.md                  Reglas del proyecto para agentes de IA
├── frontend/
│   └── index.html             Interfaz web (HTML + CSS + JS)
└── backend/
    ├── Dockerfile             Imagen del backend
    ├── requirements.txt       Dependencias de Python
    ├── tests/                 Tests automatizados (pytest)
    └── app/
        ├── main.py            Punto de entrada: registra routers y crea tablas
        ├── database.py        Configuración de la base de datos y la sesión
        ├── models/            Modelos SQLAlchemy (tablas de la BD)
        ├── schemas/           Esquemas Pydantic (entrada/salida de la API)
        ├── routers/           Endpoints REST agrupados por entidad
        └── services/          Lógica de negocio (validaciones y cálculo de puntajes)
```

La arquitectura separa responsabilidades en capas: los **modelos** definen los datos, los **schemas** validan lo que entra y sale de la API, los **routers** exponen los endpoints y los **services** contienen la lógica de negocio.

## Principales flujos

### 1. Crear un equipo y agregar jugadores (básquetbol)

1. Crear un departamento: `POST /departamentos`
2. Registrar jugadores indicando género y estrellas: `POST /jugadores`
3. Crear un equipo asociado a un departamento: `POST /equipos`
4. Agregar jugadores al equipo: `POST /equipos/{id}/jugadores`

Al agregar jugadores se valida que el equipo no supere el límite de **5 estrellas** simultáneas. Al crear un partido se valida además el mínimo de jugadores y la restricción de género de ambos equipos.

### 2. Flujo de inscripción

1. El **jugador** solicita inscribirse en un equipo: `POST /inscripciones` (la solicitud queda en estado `pendiente`).
2. El **centro de estudiantes** revisa la solicitud y la aprueba o la rechaza:
   - `PATCH /inscripciones/{id}/aprobar`
   - `PATCH /inscripciones/{id}/rechazar`

Cada acción valida el rol del usuario que la realiza: solo un usuario con rol `jugador` puede solicitar, y solo uno con rol `centro_estudiantes` puede aprobar o rechazar.

### 3. Registrar el resultado de un partido

1. Crear un partido entre dos equipos: `POST /partidos`
2. Registrar el marcador: `PATCH /partidos/{id}/resultado`

Una vez registrado, el partido pasa a estado `jugado` y su resultado se considera en el cálculo de puntajes.

### 4. Ver la tabla general del torneo

`GET /puntajes` devuelve el puntaje total de cada departamento, sumando los puntos obtenidos en básquetbol (categoría A) y calistenia (categoría B), ordenado de mayor a menor.
