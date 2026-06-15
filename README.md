# Resultados Deportivos

Este proyecto es una página web estática que muestra resultados de partidos deportivos y controla el acceso según roles de usuario. Está diseñada para simular una aplicación donde diferentes usuarios pueden ver partidos, enviar solicitudes y administrar información según su permiso.

## Cómo funciona

- **Autenticación simulada**: el usuario elige un rol dentro de la aplicación y la interfaz cambia según ese rol.
- **Roles principales**:
  - `Invitado` / `Visitante`: puede ver la lista de partidos y la información pública.
  - `Organizador`: puede agregar o modificar partidos, establecer árbitros y estado.
  - `Jugador`: puede solicitar inscripción a un equipo.
  - `Centro de estudiantes`: puede revisar y aceptar o rechazar solicitudes de jugadores.
  - `Juez`: puede ver los partidos y su información, pero no modificar datos.
- **Persistencia local**: los datos de partidos y solicitudes se guardan en `localStorage`, por lo que se mantienen al recargar la página en el navegador.

## Archivos del proyecto

- `index.html`
  - Contiene la estructura de la página.
  - Define las secciones principales: encabezado, estado de sesión, lista de partidos y formularios de interacción.
  - Incluye elementos de interfaz para los distintos roles y secciones condicionales que se muestran según el usuario.

- `styles.css`
  - Contiene todas las reglas de estilo CSS.
  - Maneja el diseño visual, colores, tipografía y separación de bloques.
  - Define estilos específicos para tarjetas de partidos, botones y secciones de usuario.

- `script.js`
  - Controla la lógica de la aplicación en JavaScript.
  - Implementa el sistema de roles y autenticación local.
  - Renderiza dinámicamente la lista de partidos, las solicitudes de inscripción y los formularios.
  - Gestiona las acciones de agregar, editar y eliminar partidos.
  - Maneja la persistencia de datos en `localStorage` para que la información se mantenga entre recargas.

- `README.md`
  - Este archivo explica el propósito del proyecto y el papel de cada archivo.
