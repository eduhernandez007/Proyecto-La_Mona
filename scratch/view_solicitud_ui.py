with open(r"C:\Users\hp\OneDrive\Escritorio\ramos universidad\otoño 2026\progra avanzada\Proyecto_la_mona\Proyecto-La_Mona\frontend\index.html", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("id=\"inscripcion-solicitar-card\"")
if idx != -1:
    print(content[idx-100:idx+1500].encode('ascii', errors='replace').decode('ascii'))
else:
    print("Not found")
