Universidad de Chile Facultad de Ciencias Físicas y Matemáticas Departamento de Ingeniería Civil Eléctrica – EL-4203 Programación Avanzada 

## Agentes de programación 

Guía práctica 

## **Autor: Christian Díaz Guerra** 

## **1. Introducción** 

Esta es una guía práctica del uso de agentes de programación, principalmente orientada a ayudarlos en la realización de sus proyectos. Lo que expongo aquí no es necesario que lo ocupen; es simplemente una guía por si no han usado agentes antes o si les surgen problemas en su uso. 

Como vieron en las presentaciones de agentes que tuvieron que hacer, existe una gran variedad. El problema es que algunos son solo pagados o tienen un límite muy estricto. Además, hoy en día están disminuyendo cada vez los límites de uso en algunas plataformas. Aquí les muestro algunas alternativas gratuitas que yo he ocupado y que deberían ser suficientes para sus proyectos. En mi caso, me gusta más utilizarlo por la interfaz de línea de comandos (CLI), pero, como vieron, existen alternativas que se incorporan directamente al IDE o tienen el suyo propio. 

Además, aquí muestro un flujo de trabajo sencillo que les permitirá trabajar con esos agentes de forma más fluida, evitando que el agente realice código incorrecto o se desvíe demasiado de las instrucciones que les den. 

## **2. Agentes gratuitos** 

## **2.1. Antigravity CLI** 

Este agente está creado por Google, por lo que necesitan una cuenta de Gmail para utilizarlo. Tiene un límite gratuito bastante amplio. Existe otra versión llamada Gemini CLI, pero se recomienda cambiar a Antigravity CLI (además, pronto no se podrá usar Gemini CLI en planes gratuitos). 

Para su instalación, deben seguir la documentación, en donde, para el caso de Windows, se debe utilizar: 

Código 1: Instalación desde PowerShell 

1 irm https://antigravity.google/cli/install.ps1 | iex 

_Agentes de programación_ 

1 

Código 2: Instalación desde CMD 

- 1 curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del _�→_ install.cmd 

En mi caso, cuando lo instalé desde CMD, no me abrió el login de mi cuenta y no podía copiar el link que aparecía en la línea de comandos. Mi solución fue utilizar la interfaz de VSCode que sí me dejaba copiar. 

## Código 3: Ejecución de Antigravity CLI 

## 1 agy 

## **2.2. Codex CLI** 

Creado por OpenAI, en su versión gratuita es muy limitado, además de que se renueva cada un mes. Para instalarlo, deben ver la documentación: 

Código 4: Instalación en Windows 

1 powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex" 

Código 5: Ejecución de Codex CLI 

1 codex 

## **2.3. OpenCode Terminal** 

Agente de código abierto que se puede conectar a varios proveedores. En su versión gratuita, tiene modelos abiertos, como _Deepseek V4 Flash_ o _Nemotron 3 Ultra_ (deben buscar los que digan Free). Sus límites son bajos, pero se pueden ir cambiando. Además, estos modelos, en principio, son peores que los más conocidos, como Gemini o GPT. Su instalación, de acuerdo a la documentación: 

Código 6: Instalación OpenCode usando npm 

## 1 npm i -g opencode-ai 

Nota: para instalar npm pueden ir a https://nodejs.org/en/download y descargar el archivo desde donde dice _Or get a prebuilt Node.js..._ 

Código 7: Ejecución OpenCode 

## 1 opencode 

OpenCode permite la conexión con los modelos de OpenRouter. Para ello, deben seguir la documentación: Abrir _opencode_ desde la línea de comandos, escribir _/connect_ y buscar _OpenRouter_ . Pegar la API Key de OpenRouter. Luego pueden seleccionar los modelos escribiendo _/models_ y buscar los que digan _(free)_ de _openrouter_ . 

_Agentes de programación_ 

2 

Además, permite la conexión con modelos locales, como se vio en la clase auxiliar. Aunque estos modelos son pesados y se demoran bastante en la ejecución (además de que a veces no realizan la petición por completo), puede ser una alternativa si ya se les acabó el resto de planes gratuitos. Pueden utilizar Colab para montar el servidor donde se ejecuta el LLM y luego hacer túnel con _ngrok_ para poder conectarlo a OpenCode local. Para ello, pueden realizar lo siguiente: 

Código 8: Instalación de llama.cpp en Colab. Deben ejecutar cada línea en el **Terminal** de Colab (abrir desde esquina inferior izquierda). 

1 git clone https://github.com/keypaa/llamaup 

2 3 cd llamaup 4 5 chmod +x scripts/*.sh 6 7 export LLAMA_DEPLOY_REPO=keypaa/llamaup 8 9 ./scripts/pull.sh 10 

11 export PATH="$HOME/.local/bin:$PATH" 

Código 9: Configuración del túnel de ngrok. Ejecutar desde las celdas del notebook. 

1 !pip install -qU pyngrok 

2 !ngrok config add-authtoken <TOKEN-NGROK> 

3 4 from pyngrok import ngrok 5 port = 8000 6 # Open a ngrok tunnel to the HTTP server 7 public_url = ngrok.connect(port).public_url 8 print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"") 

Código 10: Correr modelo LLM desde **Terminal** de Colab. En este caso, se usa unsloth/Qwen3.5-9B-MTP-GGUF 

1 llama-server -hf unsloth/Qwen3.5-9B-MTP-GGUF:Qwen3.5-9B-Q4_K_M --host 0.0.0.0 -- 

_�→_ port 8000 -c 64000 -fa on -np 1 --spec-type draft-mtp --spec-draft-n-max 6 

Código 11: Conectar a OpenCode. Abrir archivo C:/Users/<USER>/.config/opencode/opencode.jsonc 1 { 2 "$schema": "https://opencode.ai/config.json", 3 "provider": { 4 "colab": { 5 "npm": "@ai-sdk/openai-compatible", 

_Agentes de programación_ 

3 

6 "name": "Servidor Colab", 7 "options": { 8 "baseURL": "<URL_NGROK>/v1", 9 "apiKey": "no-necesita-key" 10 }, 11 "models": { 12 "unsloth/Qwen3.5-9B-MTP-GGUF": { 13 "name": "unsloth/Qwen3.5-9B-MTP-GGUF", 14 "options": { 15 "max_tokens": 32768 16 } 17 } 18 } 19 }, 20 } 21 } 

Con esto, al abrir OpenCode y buscar _/models_ debería aparecer el modelo de Colab. Dado el límite de Colab, revisen periódicamente que no se haya caído el servidor. 

## **3. Guía de uso** 

## **3.1. Inicialización y contexto** 

Los agentes funcionan mucho mejor si conocen las reglas del proyecto. Aunque cada herramienta lee archivos específicos, una práctica general es crear un archivo de instrucciones global en la raíz del proyecto llamado AGENTS.md. Algunos agentes generan por sí solos este archivo o inicializan con _/init_ (no todos tienen este comando). Cuando inicien una conversación con el agente, pueden indicarle: “Lee el archivo AGENTS.md para conocer las reglas de este proyecto.” (a veces también los leen solos). 

Código 12: Ejemplo de AGENTS.md 

- 1 # Reglas del Proyecto y del Agente 

2 

- 3 ## Stack Tecnológico 

- 4 - **Lenguaje**: Python 3.11+ 

- 5 - **Frameworks**: FastAPI, SQLAlchemy 

- 6 - **Base de datos**: SQLite (desarrollo), PostgreSQL (producción) 

- 7 - **Estilo de código**: PEP 8 estricto, uso de type hints. 

8 

- 9 ## Directrices de Comportamiento del Agente 

- 10 1. **No asumas requerimientos**: Si una instrucción es ambigua o faltan detalles de diseño ( 

   - _�→_ ej. nombres de campos, rutas de API), detente y pregúntame antes de escribir código. 

- 11 2. **Conserva el código existente**: Mantén comentarios, docstrings y lógica que no esté 

   - _�→_ relacionada directamente con el cambio solicitado. 

- 12 3. **Pruebas primero**: Cada vez que agregues o modifiques lógica, escribe o ejecuta las _�→_ pruebas unitarias correspondientes. 

_Agentes de programación_ 

4 

- 13 4. **Respeta el entorno**: No instales paquetes globales; usa siempre el entorno virtual (`. _�→_ venv`). 

## **3.2. Flujo de trabajo con Git** 

Los agentes en ocasiones modifican demasiados archivos, lo que podría romper el código o hacer difícil la revisión de los cambios. Git permite tener un punto de retorno y revisar las líneas modificadas. Por esto, **se recomienda nunca invocar a un agente si hay cambios sin guardar en Git.** 

Flujo recomendado: 

1. **Hacer Commit:** Antes de pedirle una tarea al agente, guarda tu trabajo actual. 

2. **(Opcional) Crear una rama:** Para tareas experimentales o de mayor riesgo, trabaja en una rama separada. Así puedes descartar todo sin afectar tu rama principal. 

3. Pedir la tarea: Invoca al agente y dale la instrucción. 

4. **Revisar los Diffs:** Cuando el agente proponga cambios en los archivos, examina detalladamente el “diff” (las líneas agregadas en verde + y eliminadas en rojo -). 

5. **Si el agente falla:** Si el agente estropea el código o se mete en un bucle sin salida, simplemente cancela la ejecución y revierte los cambios. 

## **3.3. Tareas Atómicas e incrementales** 

Pedirle a un agente: “Crea todo el sistema de usuarios y login” funciona mal. El agente consumirá mucho contexto, se confundirá y probablemente cometerá errores. 

En su lugar, es mejor dividir el objetivo en tareas pequeñas y secuenciales: 

Tabla 1: División de tareas 

|Tarea Grande (Evitar)|Tareas Atómicas (Recomendado)|
|---|---|
|“Crea todo el sistema de usuarios y login”|1. “Diseña el modelo de base de datos<br>para el Usuario en SQLAlchemy.”|
||2. “Escribe la función para guardar<br>y verifcar contraseñas con bcrypt.”|
||3. “Implementa el endpoint<br>POST _/register_ y pruébalo.”|
||4. “Implementa el endpoint<br>POST _/login_ que devuelva un JWT.”|



## **3.4. Planning mode** 

Para tareas que no son simples retoques (por ejemplo, estructurar un nuevo módulo o hacer refactorizaciones), los agentes avanzados utilizan el **Modo de Planificación** , que 

_Agentes de programación_ 

5 

permiten un ciclo estructurado en donde uno tiene el control. Para utilizarlo de forma sencilla, generalmente los agentes exponen un comando. Por ejemplo: en antigravity, se utiliza _/planning_ ; en codex, se usa _/plan_ ; en opencode se debe utilizar _/agents_ y luego _plan_ . 

## **3.5. Hacer que el agente pregunte** 

Por defecto, los LLMs tienden a complacer al usuario y a rellenar los vacíos de información con suposiciones. Para evitar que el agente tome decisiones de diseño equivocadas, pueden forzarlo a preguntar: 

- **Instrucción directa en el prompt:** Cuando se pide algo, se puede añadir al final del mensaje: “Si hay algo que no esté completamente definido (por ejemplo, el nombre de los endpoints, el formato de respuesta o el manejo de errores), no asumas nada. Hazme una pregunta aclaratoria antes de proceder.” 

- **Preguntas multiopción** : Los agentes CLI avanzados cuentan con herramientas para presentar diálogos interactivos. Se puede pedir algo como: “Dame 3 alternativas de cómo estructurar esto y permíteme elegir una.” 

- **Declaración de dudas durante el plan** : Durante el Planning Mode, se puede exigir que el plan de implementación tenga una sección de preguntas abiertas. No aprueben el plan hasta que todas las preguntas en esa sección hayan sido resueltas en el chat. 

_Agentes de programación_ 

6 

