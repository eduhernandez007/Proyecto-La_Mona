import os

backend_dir = r"C:\Users\hp\OneDrive\Escritorio\ramos universidad\otoño 2026\progra avanzada\Proyecto_la_mona\Proyecto-La_Mona\backend\app\routers"
for filename in os.listdir(backend_dir):
    if filename.endswith(".py"):
        filepath = os.path.join(backend_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if "rol" in content or "Usuario" in content:
            print(f"File {filename} has reference to rol/Usuario")
