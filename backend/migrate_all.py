import sqlite3

DB_PATH = r'C:\Users\harol\OneDrive\Escritorio\Proyecto-La_Mona-main\backend\lamona.db'

MIGRACIONES = {
    "partidos": [
        ("fase", "TEXT NOT NULL DEFAULT 'Fase de Grupos'"),
    ],
    "usuarios": [
        ("clave", "TEXT NOT NULL DEFAULT '1234'"),
    ],
}

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for tabla, columnas in MIGRACIONES.items():
    cur.execute(f"PRAGMA table_info({tabla})")
    existentes = {row[1] for row in cur.fetchall()}
    print(f"Tabla '{tabla}': {existentes}")

    for col_name, col_def in columnas:
        if col_name not in existentes:
            sql = f"ALTER TABLE {tabla} ADD COLUMN {col_name} {col_def}"
            cur.execute(sql)
            conn.commit()
            print(f"  OK: columna '{col_name}' agregada.")
        else:
            print(f"  SKIP: columna '{col_name}' ya existia.")

conn.close()
print("Migracion completada!")
