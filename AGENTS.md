# Reglas del Proyecto y del Agente — La Mona CDI

## Stack Tecnológico
- **Lenguaje**: Python 3.11+
- **Framework backend**: FastAPI
- **ORM**: SQLAlchemy 2.0 (con Mapped / mapped_column)
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción futura)
- **Validación**: Pydantic v2
- **Servidor**: Uvicorn
- **Tests**: pytest
- **Frontend**: HTML + CSS + JavaScript vanilla (sin frameworks)
- **Estilo de código**: PEP 8 estricto, type hints obligatorios en toda función

## Estructura del Proyecto
```
tarea 2/
├── AGENTS.md               ← este archivo
├── docker-compose.yml
├── frontend/
│   └── index.html
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py         ← entrada FastAPI, registra routers
        ├── database.py     ← motor SQLite, sesión, Base
        ├── models/         ← clases SQLAlchemy (tablas)
        ├── schemas/        ← clases Pydantic (entrada/salida API)
        ├── routers/        ← endpoints REST por entidad
        └── services/       ← lógica de negocio y validaciones OOP
```

## Directrices de Comportamiento del Agente

1. **No asumas requerimientos**: Si una instrucción es ambigua (nombres de campos, rutas, comportamiento en casos borde), detente y pregunta antes de escribir código.

2. **Tareas atómicas**: Trabaja una función o endpoint a la vez. No refactorices código que no fue pedido.

3. **Conserva el código existente**: No toques comentarios, docstrings ni lógica que no esté directamente relacionada con el cambio solicitado.

4. **Pruebas primero**: Cada vez que agregues lógica de negocio en `services/`, escribe o actualiza el test correspondiente en `tests/`.

5. **Respeta el entorno virtual**: No instales paquetes globales. Usa siempre el `.venv` del proyecto. Si se necesita un paquete nuevo, agréga lo a `requirements.txt`.

6. **Commits atómicos**: Cada commit debe corresponder a una sola tarea. Formato: `tipo(scope): descripción breve`. Tipos: `feat`, `fix`, `refactor`, `test`, `docs`.

7. **Formato de respuesta de API**: Siempre retornar JSON. Errores con `HTTPException` y código HTTP correcto (400 para regla de negocio, 404 para no encontrado, 422 para validación).

8. **OOP obligatorio en services/**: Las clases de servicio deben usar herencia o clases abstractas donde tenga sentido. No colocar lógica de negocio dentro de los routers.

## Convenciones de Nombres
- Archivos Python: `snake_case.py`
- Clases: `PascalCase`
- Variables y funciones: `snake_case`
- Endpoints REST: plural y en español (`/jugadores`, `/equipos`, `/partidos`)
- Commits: en español, imperativo (`feat(equipos): agregar validación de género`)

## Flujo de trabajo recomendado (para el humano)
1. Hacer commit del estado actual antes de pedir una nueva tarea al agente
2. Pedir tareas atómicas (una cosa a la vez)
3. Revisar el diff antes de aceptar los cambios
4. Si algo falla, revertir con `git checkout -- .`
