with open(r"C:\Users\hp\OneDrive\Escritorio\ramos universidad\otoño 2026\progra avanzada\Proyecto_la_mona\Proyecto-La_Mona\frontend\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "agregarJugadoresAEquipo" in line:
        safe_line = line.strip().encode('ascii', errors='replace').decode('ascii')
        print(f"Line {i+1}: {safe_line}")
