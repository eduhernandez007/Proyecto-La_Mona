# Changelog — Proyecto La Mona

**Generado el:** 28 de Junio de 2026, 03:59 (GMT-4)

Este documento resume los cambios y mejoras implementados recientemente en el proyecto.

## 🌟 Actualizaciones Recientes (2 de Julio de 2026)
- **Gestión de Lugares (Canchas y Patios):**
  - Se agregó el campo `lugar` de forma opcional a los modelos y esquemas de la base de datos de Partidos.
  - La interfaz de Básquetbol ahora permite asignar el lugar del partido a través de una lista desplegable ("Cancha de 850" o "Cancha -3 de 851").
  - La interfaz de Calistenia reemplazó el campo de texto libre por una lista desplegable con las opciones permitidas ("Patio de calistenia de 850" o "Gimnasio -3 de 851").
  - Las tablas de *Partidos Programados* y *Resultados* fueron actualizadas para mostrar esta nueva columna de `Lugar`.
- **Torneo Demostrativo (Básquetbol):**
  - Se generó un script (`populate_tournament.py`) que puebla la base de datos con un torneo simulado completo que incluye fase de grupos y semifinales, dejando programada la gran final entre **Eléctrica** y **Mecánica** para el día de mañana a las 12:00 hrs.
- **Torneo de Estrellas (Calistenia):**
  - Se ejecutó un script automático (`populate_calistenia.py`) para matricular a todos los jugadores de élite (3 estrellas) en torneos de Calistenia (categorías Masculina y Femenina) y poblar sus respectivas marcas y resultados.

## 🏀 Básquetbol y Partidos
- **Nueva funcionalidad de eliminación de partidos:** 
  - Se agregó el endpoint `DELETE /partidos/{id}` en el backend para permitir eliminar un partido y sus titulares asociados de la base de datos de manera segura.
  - Se implementó un botón **✖ Eliminar** en la interfaz web (tanto en partidos pendientes como jugados), visible únicamente para el rol `organizador`.
  - Se agregó confirmación preventiva (JS) antes de eliminar un partido.
- **Limpieza de código muerto:** 
  - Se eliminaron los archivos `backend/app/services/tabla_grupos.py` y `backend/tests/test_tabla_grupos.py` ya que su funcionalidad fue centralizada de mejor forma en `CalculadoraPuntajes` (soporte multi-fase).

## 💪 Calistenia
- **Nueva funcionalidad de eliminación de marcas y participantes:**
  - Se agregaron dos endpoints en el backend (`calistenia.py`):
    1. `DELETE /calistenia/resultados/{id}`: Para borrar una marca específica registrada por error.
    2. `DELETE /calistenia/participantes/{id}`: Para borrar a un participante completo junto con todas sus marcas.
  - En el frontend, se agregó un botón **✖** al lado de cada marca individual de calistenia, y una nueva columna en la tabla con un botón para eliminar al participante completo.
  - Ambos botones están protegidos por CSS/JS para que **solo sean visibles** para usuarios con rol de `organizador` o `juez`.
  - Se agregó una validación estricta para evitar la inscripción de un mismo jugador múltiples veces en la competencia de Calistenia.

## 📋 Inscripciones y Gestión de Usuarios
- **Validación de Departamento en Inscripciones:**
  - El backend ahora verifica estrictamente que los usuarios con rol de `centro_estudiantes` pertenezcan al mismo departamento del equipo (o jugador de calistenia) cuyas inscripciones intentan aprobar o rechazar (evitando que puedan gestionar equipos ajenos).

## 🐳 Docker y Despliegue
- **Servicio de Frontend agregado:**
  - Se añadió el servicio `frontend` al archivo `docker-compose.yml` utilizando una imagen ligera de Nginx (`nginx:alpine`).
  - Esto permite que tanto el backend (en el puerto 8000) como la interfaz de usuario (en el puerto 8080) se levanten simultáneamente con un solo comando `docker-compose up`, cumpliendo con el requisito de contenerización completo.

## ⚙️ Base de Datos y Sistema
- **Sincronización y Migraciones Automáticas (Alembic):**
  - Se reemplazó el uso del script manual temporal (`migrate_all.py`) integrando de forma nativa **Alembic** para la gestión de migraciones de SQLAlchemy.
  - La aplicación ahora ejecuta automáticamente `alembic upgrade head` durante su arranque en `backend/app/main.py` (reemplazando al antiguo `Base.metadata.create_all`).
  - Esto garantiza que al levantar el proyecto desde cero (ej. vía Docker), las tablas nuevas y modificaciones en columnas (`fase`, `clave`, `lugar`, `competencia`, etc.) se generen y apliquen automáticamente sin requerir intervención manual.
  - Se agregó `alembic` a las dependencias en `requirements.txt`.

## 📊 Estado de los Tests
- Todos los tests automatizados (31 en total) se encuentran pasando tras estos cambios, confirmando que las reglas de negocio (estrellas, géneros, mínimos de jugadores) no fueron afectadas negativamente.

## 🛠️ Nuevos Departamentos y Jugadores (30 de Junio de 2026)
- **Creación del departamento de Mecánica:**
  - Se agregó el departamento **Mecánica** (ID: 7) a las bases de datos `lamona.db` (en el directorio raíz y en el directorio `backend`).
  - Se crearon 6 jugadores asignados al nuevo departamento con un total combinado de exactamente **5 estrellas**:
    1. Nikolaus Otto (Masculino, 2 estrellas)
    2. Rudolf Diesel (Masculino, 1 estrella)
    3. Kate Gleason (Femenino, 1 estrella)
    4. James Watt (Masculino, 1 estrella)
    5. Verena Holmes (Femenino, 0 estrellas)
    6. Margaret Ingels (Femenino, 0 estrellas)
  - Se crearon cuentas de usuario para el departamento:
    - `Centro Mecánica` (rol: `centro_estudiantes`, clave: `1234`)
    - `Nikolaus Otto (Jugador Mecánica)` (rol: `jugador`, clave: `1234`)
- **Actualización de las semillas (Seed Data):**
  - Se modificó la función `seed_data()` en `backend/app/main.py` para asegurar que el departamento de **Mecánica**, sus usuarios y sus jugadores se creen automáticamente al inicializar la base de datos desde cero.
- **Validación del sistema:**
  - Se ejecutaron los tests automatizados (`pytest`) para asegurar la integridad de las reglas de negocio, logrando que los 31 tests pasen correctamente.
- **Corrección de carga infinita en el frontend (Error 500 en `/jugadores/`):**
  - Se corrigió un error HTTP 500 en el endpoint `/jugadores/` que provocaba que la pantalla de carga del frontend se quedara congelada. El error era causado por el formato del campo `genero` en los nuevos jugadores agregados por SQL directo (se insertaron valores `'M'` / `'F'` en lugar de los nombres del Enum `'masculino'` / `'femenino'`). Se actualizaron los registros correspondientes en las bases de datos `lamona.db` de raíz y `backend`.
  - Se detuvieron procesos huérfanos de uvicorn en el puerto `8000` y se levantó correctamente el servidor backend local para recibir peticiones del frontend.
- **Soporte de solicitudes de inscripción para Calistenia:**
  - **Base de Datos:** Se migró la tabla `inscripciones` en las bases de datos para hacer que la columna `equipo_id` sea opcional (`NULL`) y se agregó la columna `competencia` (TEXT, NOT NULL, DEFAULT `'basquet'`) para identificar la disciplina.
  - **Backend:** 
    - Se modificaron los modelos y esquemas en `models/inscripcion.py` y `schemas/inscripcion.py` para soportar las solicitudes de calistenia sin equipo asociado.
    - Se actualizó el endpoint `POST /inscripciones/` para validar solicitudes de calistenia, verificando si el jugador ya participa en calistenia o si tiene una solicitud pendiente.
    - Se actualizó el endpoint `PATCH /inscripciones/{id}/aprobar` para que, al aprobarse una solicitud de competencia tipo `'calistenia'`, registre automáticamente al jugador como `ParticipanteCalistenia` determinando su categoría según el género.
  - **Frontend:**
    - Se modificó la interfaz del rol de jugador en `frontend/index.html` para permitirle elegir entre solicitar inscripción en Básquetbol o Calistenia, ocultando el selector de equipo cuando corresponda.
    - Se actualizaron las funciones `solicitarInscripcion()` y `renderInscripciones()` para enviar y mostrar respectivamente las solicitudes en la disciplina correcta ("Básquetbol" o "Calistenia").
- **Organización de Competencias de Calistenia (Masculinas y Femeninas con Lugar y Hora):**
  - **Base de Datos:** Se crearon las tablas `competencias_calistenia` en las bases de datos para programar competencias individuales especificando `nombre`, `categoria` (M/F), `lugar` y `fecha_hora`. Se recreó la tabla `resultados_calistenia` asociando cada marca a una competencia específica mediante `competencia_id`.
  - **Backend:**
    - Se agregaron las clases del modelo `CompetenciaCalistenia` en `models/calistenia.py` e implementaron los esquemas `CompetenciaCalisteniaCreate` y `CompetenciaCalisteniaRead` en `schemas/calistenia.py`.
    - Se crearon los endpoints en `routers/calistenia.py` para listar (`GET`), crear (`POST`) y eliminar (`DELETE`) competencias.
    - Se modificó la ruta `POST /calistenia/resultados` para validar que la marca de calistenia se registre a una competencia existente y se cumpla que la categoría de la competencia coincida con el género del participante.
  - **Frontend:**
    - Se incorporó la tarjeta de administración "🏆 Organizar Competencia" en `frontend/index.html` para que los organizadores creen eventos deportivos.
    - Se añadió una tabla "📅 Competencias de Calistenia Organizadas" para listar los eventos y permitir su eliminación.
    - Se actualizó el formulario "📝 Registrar Marca" para requerir la selección de la competencia organizada, filtrando dinámicamente las competencias para mostrar únicamente las de la misma categoría que el participante seleccionado.
    - Se actualizó el listado general de marcas de los competidores para mostrar el nombre del evento/competencia en el que se obtuvo.

- **Mejoras en la UI del Frontend:**
  - Se implementó dinámicamente un visualizador de **Llaves del Torneo (Brackets)** en `frontend/index.html`. Esta tabla escanea partidos en fases de `Clasificación`, `Semifinales` y `Final`, mostrando visualmente quién avanza y destacando al ganador (sea por puntaje en cancha o por W.O.).
  - Se modificó la disposición de la interfaz de Básquetbol para colocar la Tabla de Posiciones de la Fase de Grupos justo encima de los Brackets, mejorando el flujo narrativo del torneo.
  - Se eliminó la columna obsoleta "Estrellas en Cancha" de la tabla de visualización de equipos, dado que esta validación se hace dinámicamente sobre los titulares de los partidos.
- **Correcciones y Refinamiento del Backend y Base de Datos:**
  - Se parcheó la función `seed_data()` en `backend/app/main.py`. Originalmente abortaba la siembra si encontraba al menos 1 departamento; ahora revisa la base de datos departamento por departamento e inyecta los que falten, permitiendo la inserción exitosa de Industrias, Matemática y Física-Astronomía en instalaciones ya existentes.
  - Se agregaron a `seed_data()` un total de 18 jugadores nuevos (6 por cada departamento faltante) para equilibrar los datos semilla (ej. *Alan Turing* en Matemáticas, *Henry Ford* en Industrias, *Galileo Galilei* en Física).
  - Se eliminaron por saneamiento de la base de datos inscripciones antiguas o corrompidas (jugadores sin departamentos asignados).
  - **Creación de Dream Teams:** Se automatizó en la base de datos local la creación de los "Dream Teams" para todos los departamentos faltantes (Física-Astronomía, Industrias, Matemática, Mecánica). Cada equipo incluye a todos los estudiantes de su respectivo departamento y asigna automáticamente como capitán al jugador con más estrellas.
  - Se subió excepcionalmente (mediante push forzado ignorando el `.gitignore`) el archivo de base de datos `lamona.db` a GitHub, para garantizar que todos los desarrolladores tengan acceso inmediato a los datos, usuarios de prueba y los Dream Teams recién configurados, agilizando el proceso de presentación en vivo.
