Universidad de Chile Facultad de Ciencias Físicas y Matemáticas Departamento de Ingeniería Civil Eléctrica – EL-4203 Programación Avanzada 

## Proyecto Final 

Sistema de Gestión de “La Mona” 

**Profesor: Jorge Zambrano Ibujés** Auxiliar: Christian Díaz Guerra Ayudante: Pablo Vergara Llantén 

## **1. Contexto motivación y** 

Todos los años, nuestra facultad lleva a cabo las olimpiadas interdepartamentales “La Mona”, organizadas por el Centro Deportivo de Ingeniería (CDI). Durante varias semanas, distintos departamentos participan en competencias deportivas y recreativas organizadas en categorías A, B y C. 

El evento contempla múltiples disciplinas, cada una con reglas, formatos y restricciones particulares. Algunas competencias se desarrollan por equipos, mientras que otras son individuales. Además, existen distintos tipos de usuarios con permisos específicos, tales como organizadores, jueces, centros de estudiantes y jugadores. 

Actualmente, gran parte de la organización del evento se realiza manualmente o mediante planillas dispersas, dificultando la validación de restricciones, el manejo de inscripciones, el seguimiento de resultados, la administración de usuarios, y la centralización de la información del torneo. 

El objetivo de este proyecto es desarrollar una plataforma web funcional que permita gestionar parte importante de la organización de “La Mona”, aplicando conceptos avanzados de programación orientada a objetos, testing, arquitectura de software y despliegue. 

## **2. Objetivos** 

Los objetivos de este proyecto son: 

- Diseñar un sistema complejo utilizando Programación Orientada a Objetos. 

- Aplicar correctamente: herencia, polimorfismo, abstracción, encapsulamiento, composición. 

- Modelar un dominio real con múltiples reglas de negocio. 

- Diseñar una arquitectura mantenible y extensible. 

- Implementar tests automatizados. 

- Separar responsabilidades entre dominio, lógica de negocio, persistencia y presentación. 

- Desplegar una aplicación web funcional. 

- Utilizar herramientas de IA de manera efectiva para apoyar el desarrollo del sistema. 

_Proyecto Final_ 

1 

## **3. Descripción del proyecto** 

Se deberá implementar una plataforma web para administrar competencias de “La Mona”. El sistema deberá permitir: 

- Gestionar usuarios y permisos. 

- Administrar competencias. 

- Manejar inscripciones. 

- Registrar resultados. 

- Validar restricciones. 

- Calcular puntajes. 

- Visualizar información relevante del torneo. 

El foco principal del proyecto está en el diseño del backend, la arquitectura del sistema, y el modelado orientado a objetos. **La interfaz web no necesita ser visualmente compleja, pero sí debe ser funcional y usable** . 

## **3.1. Competencias incluidas** 

Uno de los objetivos principales del proyecto es modelar correctamente las competencias utilizando Programación Orientada a Objetos. Se espera que el sistema abstraiga comportamiento común entre competencias, permita reutilización de lógica, y facilite agregar nuevas competencias en el futuro. 

El sistema debe soportar inicialmente dos competencias: 

## **3.1.1. Básquetbol** 

Competencia grupal de categoría A. 

Debe considerar al menos: 

- Equipos. 

- Partidos. 

- Grupos clasificatorios. 

- Puntajes. 

- Restricciones de estrellas. 

- Validación de cantidad mínima de jugadores. 

- Validación de género. 

- Resultados. 

- Desempates básicos. 

## **3.1.2. Calistenia** 

Competencia individual de categoría B. 

Debe considerar al menos: 

- Pruebas individuales. 

- Categorías masculina y femenina. 

_Proyecto Final_ 

2 

- Jueces. 

- Registro de resultados. 

- Rankings. 

- Cálculo de puntajes por departamento. 

## **3.2. Usuarios y permisos** 

El sistema debe considerar distintos tipos de usuarios: 

- **Organizadores:** Tienen acceso completo al sistema. Pueden administrar competencias, gestionar usuarios, registrar fixtures, modificar resultados, validar inscripciones, visualizar toda la información del torneo. 

- **Organizadores de competencia:** Tienen permisos limitados a su competencia. Pueden administrar participantes, gestionar encuentros, validar información relacionada con su disciplina, modificar resultados de su competencia. 

- **Jueces:** Pueden registrar y modificar resultados y validar desempeño en competencias donde corresponda. No deben tener acceso administrativo global. 

- **Centros de estudiantes:** Representan a un departamento. Pueden revisar jugadores inscritos, gestionar equipos, aprobar o rechazar solicitudes de inscripción, visualizar información de su departamento. 

- **Jugadores:** Pueden: registrarse, solicitar inscripción en competencias, visualizar sus participaciones, representar a un departamento. Un jugador puede participar en múltiples competencias simultáneamente. 

## **3.3. Flujo de inscripciones** 

El sistema debe incluir un sistema de inscripciones similar al que se lleva a cabo en la actualidad: (1) Un jugador solicita la inscripción, (2) el centro de estudiantes correspondiente revisa la solicitud, (3) la organización de la competencia valida la participación final. Aún así, el grupo puede proponer otro flujo, quedando a su criterio. 

## **3.4. Fixtures y calendario** 

NO es necesario generar automáticamente fixtures ni calendarios. Los fixtures podrán cargarse manualmente o ser ingresados desde la interfaz (lo que queda a criterio del grupo). El sistema sí debe validar consistencia, impedir estados inválidos y asegurar que las restricciones se cumplan correctamente. 

## **3.5. Testing** 

El proyecto debe incluir tests automatizados. Como mínimo, tests unitarios, tests de lógica de negocio y validación de reglas importantes del sistema. Por ejemplo, validación del límite de estrellas, validación de participantes mínimos, etc. 

## **3.6. Backend** 

El backend debe estar desarrollado en Python. Se recomienda el uso de FastAPI, SQLAlchemy y pytest, pero queda a criterio del grupo qué stack utilizar, justificando su elección. 

_Proyecto Final_ 

3 

La aplicación debe incluir persistencia de datos, autenticación básica y despliegue. 

## **3.7. Persistencia de datos** 

La aplicación debe utilizar una base de datos. No se evaluará la complejidad avanzada del modelo relacional, pero sí que funcione adecuadamente: que sea consistente, con relaciones adecuadas y manejo correcto de datos. 

## **3.8. Interfaz web** 

La aplicación debe incluir una interfaz web funcional. NO se evaluará diseño visual avanzado, solo que se sea funcional. Se espera como mínimo: navegación básica, formularios funcionales, visualización de información, e interacción con el backend. 

## **3.9. Despliegue** 

**La aplicación debe poder ser desplegada fácilmente mediante Docker** , sin instalación manual de dependencias. Debe poder mostrarse su funcionamiento, ya sea de forma local o pública. Puede utilizar servicios como: Render, Railway, Vercel u otros. El despliegue debe incluir aplicación funcional, acceso autenticado y persistencia operativa. NO se evaluarán componentes de seguridad informática. Se darán bonificaciones si se despliega en un servicio en la nube. 

## **4. Uso de herramientas de IA** 

Está permitido el uso de herramientas de inteligencia artificial para apoyar el desarrollo del proyecto. Sin embargo, deben tener en cuenta que el objetivo principal no es únicamente generar código, sino que también diseñar correctamente el sistema, tomar decisiones de arquitectura, modelar adecuadamente el dominio y justificar las soluciones implementadas. 

La evaluación y revisión considerará la explicación de sus arquitecturas, justificación de decisiones de diseño, explicación de las relaciones entre clases, descripción de responsabilidades de cada componente y la comprensión completa del código entregado. 

## **5. Entregables** 

- **Código fuente:** Repositorio en GitHub completo del proyecto. Debe incluir README con instrucciones de ejecución y despliegue, dockerfiles y estructura clara. 

- **Prompts utilizados:** Cada uno de los prompts utilizados para la generación del código usando herramientas de IA, indicando a qué parte del código se utilizó. 

- **Presentación final:** Deben realizar una presentación final la semana de exámenes, enfocándose en el problema abordado, las decisiones de diseño tomadas y la solución implementada. Se espera que cada grupo muestre el sistema funcionando en vivo, destacando los principales flujos de uso, la arquitectura general, las decisiones técnicas más relevantes y los desafíos enfrentados durante el desarrollo. La evaluación considerará tanto la calidad técnica del sistema como la capacidad del grupo para explicar y defender su solución de manera clara. 

_Proyecto Final_ 

4 

## **Anexo A. Bases de La Mona** 

## **A.1. Categorías de competencias** 

Las competencias se clasifican en: 

- Categoría A: Deportes principales/colectivos. 

- Categoría B: Competencias secundarias. 

- Categoría C: Actividades recreativas. 

Cada competencia entrega puntajes al departamento representado según la posición final obtenida: 

Tabla A.1: Puntajes por categoría 

|Lugar|Puntaje<br>Categoría|A|Puntaje<br>Categoría|B|Puntaje<br>Categoría|C|
|---|---|---|---|---|---|---|
|1o|4000||2000||1000||
|2o|3200||1600||800||
|3o|2400||1200||600||
|4o|2000||1000||500||
|5o|1600||800||400||
|6o|1200||600||300||
|7o|800||400||200||
|8o|400||200||100||



## **A.2. Departamentos participantes** 

El torneo considera distintos departamentos/especialidades: Civil, Computación, Eléctrica, Física-Astronomía, Industrias, Matemática, etc. Cada jugador representa a un departamento. 

## **A.3. Sistema de estrellas** 

Algunas competencias utilizan un sistema de “estrellas” para limitar la cantidad de jugadores profesionales o avanzados presentes simultáneamente. Cada jugador posee una cantidad de estrellas según su nivel competitivo, las que deben informarse al momento de su inscripción. 

De forma general: 

- **Jugador amateur:** 0 estrellas 

- **Participa en ramas internas:** 1 estrella 

- **Federado o selección universitaria:** 2 estrellas 

- **Selección nacional:** 3 estrellas 

Las reglas específicas dependen de cada competencia. 

_Proyecto Final_ 

5 

## **A.4. Reglas de las competencias** 

## **A.4.1. Básquetbol** 

Competencia grupal de categoría A. Cada equipo debe tener mínimo 5 jugadores, puede tener un máximo de 12 jugadores por partido, debe incluir al menos 2 jugadores de cada género y debe tener un capitán. 

Los partidos poseen 4 cuartos de 10 minutos, con tiempo extra de 5 minutos en caso de empate. 

El torneo considera fase de grupos, clasificación, semifinales/final. Para este proyecto NO es necesario generar automáticamente el fixture. 

En fase de grupos, las victorias otorgan 2 puntos, la derrota 1 punto y W.O. 0 puntos. Se considera W.O. cuando el equipo no se presenta o no cumple con el mínimo de jugadores. Los desempates se realizan por (1) diferencia de puntos y (2) resultado entre equipos empatados. 

Los equipos podrán tener como máximo 5 estrellas simultáneas en cancha (para evitar crear un sistema que administre los cambios en tiempo real durante el partido, esta restricción solo se debe cumplir para el equipo titular que comienza el partido). 

## **A.4.2. Calistenia** 

Competencia de categoría B. Existen dos categorías: masculina y femenina. Los participantes compiten individualmente, pudiendo haber varios competidores por departamento. Para el puntaje, se consideran los 4 mejores resultados por departamento (2 de categoría masculina y 2 de categoría femenina). 

Las pruebas son diferenciadas: para la categoría masculina, se tienen muscle ups, pull ups, push ups y handstand hold; para la categoría femenina, se tienen pull ups, push ups, handstand hold y hang hold. Las pruebas se evalúan mediante cantidad de repeticiones o tiempo sostenido (esto último para aquellas de tipo _hold_ ). En caso de empate puede existir ronda adicional o resolución determinada por la organización. 

_Proyecto Final_ 

6 

