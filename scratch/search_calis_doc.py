with open(r"C:\Users\hp\OneDrive\Escritorio\ramos universidad\otoño 2026\progra avanzada\Proyecto_la_mona\Proyecto-La_Mona\Proyecto_La_Mona.md", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.findall(r'.{0,100}(?:Calistenia|categor).{0,100}', content, re.IGNORECASE)
for m in matches[:30]:
    clean_m = m.strip().replace('\n', ' ')
    print(clean_m.encode('ascii', errors='replace').decode('ascii'))
