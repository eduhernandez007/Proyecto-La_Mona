# Changelog — Proyecto La Mona

**Generado el:** 28 de Junio de 2026, 03:59 (GMT-4)

Este documento resume los cambios y mejoras implementados recientemente en el proyecto.

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

## ⚙️ Base de Datos y Sistema
- **Sincronización del esquema de la Base de Datos:**
  - Se detectaron errores 500 debido a que SQLAlchemy no aplica cambios de columnas a tablas ya existentes en SQLite.
  - Se desarrolló un script de migración temporal (`migrate_all.py`) que utilizó sentencias `ALTER TABLE` para agregar las columnas faltantes:
    - Columna `fase` en la tabla `partidos` (default: `'Fase de Grupos'`).
    - Columna `clave` en la tabla `usuarios` (default: `'1234'`).
  - Esto resolvió los errores al cargar la tabla de puntajes y al iniciar sesión.

## 📊 Estado de los Tests
- Todos los tests automatizados (31 en total) se encuentran pasando tras estos cambios, confirmando que las reglas de negocio (estrellas, géneros, mínimos de jugadores) no fueron afectadas negativamente.
