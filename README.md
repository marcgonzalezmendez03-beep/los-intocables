# Los Intocables — Web independiente FC27

Web FastAPI independiente del bot de Discord. Consulta **directamente** FC27 mediante `fc-clubs-api==0.3.0`, igual que el `app.py` proporcionado. No necesita `data.json` ni bot en ejecución.

## Windows

1. Descomprime el ZIP en una carpeta nueva (no dentro de tu bot).
2. Ejecuta `start_windows.bat`. La primera vez instalará dependencias y creará `.env`.
3. Edita `.env` con un `ADMIN_PASSWORD` fuerte y `SESSION_SECRET` aleatorio largo (nunca los compartas).
4. Reinicia `start_windows.bat` y abre **http://localhost:8081**. Admin: **http://localhost:8081/login**.
5. Para parar, cierra la consola o pulsa Ctrl+C.

Si `py` no está disponible, sustituye `py -m venv` por `python -m venv` en el `.bat`.

## API
- `GET /api/club`: datos reales de FC27 y personalización pública.
- `GET /api/health`: estado de actualización.
- `POST /api/login`, `POST /api/logout`: sesión admin.
- `PUT /api/admin/settings`: editar identidad del club (admin).
- `POST /api/admin/refresh`: refresco manual (admin).

La web mantiene los últimos datos correctos en memoria si falla temporalmente la API, pero tras reiniciar necesita consultar FC27 de nuevo. El panel de administración guarda textos y URL del escudo en SQLite (`site.db`). No se inventan clasificaciones externas ni datos por partido que la API no proporciona. La API consultada es un cliente comunitario, no un servicio oficial garantizado por EA.

## Seguridad y publicación

La web está configurada por defecto para **uso local** (`127.0.0.1`). Para publicarla necesitas alojamiento para Python con salida a internet, variables de entorno, HTTPS, `COOKIE_SECURE=true`, una contraseña robusta y `SESSION_SECRET` persistente. No uses credenciales `admin/admin`. El inicio de sesión básico no incorpora limitación de intentos; añade rate limiting antes de exponerlo públicamente. Si despliegas con varios workers, añade un almacenamiento compartido para la caché. No publiques `.env` ni `site.db`.

## Alcance inicial

Implementado: dashboard, partidos recientes, tabla de jugadores con estadísticas acumuladas, métricas, actualización automática y panel admin para identidad visual y anuncio.

Pendiente de una segunda fase: clasificación de liga desde fuente verificable, subida directa de fotos, edición de fichas de jugador, gráficas avanzadas y bot Discord independiente. La estructura de campos de jugadores puede variar según la respuesta de FC27; se ajustará con una muestra real de `/api/club` si fuera necesario.


## Versión 3: perfiles de jugadores
- Página de inicio incluye fichas con foto (URL pública), dorsal y posición.
- Panel `/admin` permite guardar perfil de cada jugador de la API, sin alterar sus estadísticas reales.
- Los perfiles se guardan en `site.db` (SQLite), separado de FC27.
- Arranca en puerto **8081** para coexistir con la web anterior en 8080.
- **Para migrar tus ajustes antiguos:** copia el `.env` y, si quieres conservar personalizaciones, también `site.db` (solo con los servidores apagados). No compartas esos archivos.
- Recomendado: copia la carpeta y prueba la nueva versión antes de sustituir tu versión anterior.


## Versión neón v4
El logo real está incluido localmente en `static/escudo-intocables.webp`; no depende de una URL externa. Si no se ha configurado un escudo personalizado en administración, se utiliza este logo. La API FC27 y el bot permanecen independientes. Inicio por defecto en puerto 8081. Para conservar ajustes anteriores, copiar `.env` y `site.db` de la versión antigua (con ambas webs apagadas).

## Filtro de amistosos (V6)
La API de partidos consulta los últimos 50 encuentros y devuelve solo los primeros 10 cuyo campo `matchType` contiene `friendly` o `amistoso` (sin distinguir mayúsculas). Los modos no identificados se excluyen. Si la API usa un nombre distinto para los amistosos, será necesario adaptar el filtro. Las estadísticas generales y las acumuladas de jugadores siguen siendo de todos los modos. Para actualizar tu instalación actual basta sustituir `main.py`, `templates/index.html` y `static/app.js`; conserva `.env` y `site.db`.

## V7: contadores solo de amistosos
Los cuatro contadores de portada muestran partidos, victorias, goles y derrotas de amistosos confirmados en los últimos **50 encuentros consultados**. El balance, diferencia de goles y porcentaje de victorias usan el mismo subconjunto. Se muestran hasta 10 amistosos en el historial. No son totales históricos si existen amistosos anteriores a esos 50 encuentros. El **skill rating** se reemplaza por **derrotas**, porque no puede inferirse de los resultados individuales. Las estadísticas acumuladas de jugadores siguen siendo globales y no se deben interpretar como exclusivas de amistosos. Si el campo `matchType` de la API no coincide con `friendly`/`amistoso`, los partidos se excluyen para evitar datos engañosos.

Para actualizar una V6 funcional: sustituir `main.py`, `templates/index.html`, `static/app.js`, conservar `.env` y `site.db` y reiniciar.
