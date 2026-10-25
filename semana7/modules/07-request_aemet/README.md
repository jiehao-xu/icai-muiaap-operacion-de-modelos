# Semana 7 — Consulta de datos de AEMET con Requests

Esta práctica utiliza un cliente HTTP en Python para consultar AEMET OpenData,
interpretar respuestas JSON y guardar los datos obtenidos en un CSV. Permite
practicar el consumo de una API antes de exponer un modelo como servicio.


## Qué se ha implementado

El script [main.py](src/07_request_amet/main.py) realiza esta secuencia:

1. Consulta el inventario de estaciones con `requests.get()`, enviando la
   credencial en el encabezado `api_key` y usando `timeout=30`.
2. Lee el campo `datos` del JSON recibido. Este campo contiene la URL de
   descarga, por lo que hace una segunda petición para obtener las estaciones.
3. Recorre el inventario y busca el nombre exacto
   `MADRID, CIUDAD UNIVERSITARIA` para obtener su `indicativo`.
4. Construye la URL de climatologías diarias con ese identificador y las fechas
   definidas en el script: del **1 al 30 de octubre de 2019**, ambos incluidos.
5. Consulta ese endpoint y descarga los registros desde la URL del campo
   `datos`, siguiendo el mismo flujo de dos peticiones.
6. Convierte los registros en un `pandas.DataFrame`, crea `assets/` si no existe
   y exporta el resultado con `to_csv(index=False)`.

Durante la ejecución imprime las URL de descarga, el inventario, el indicativo
seleccionado y los registros meteorológicos.


## Entorno y ejecución

El proyecto utiliza Python **3.13 o superior** y `uv`. Las dependencias están
declaradas en `pyproject.toml` y su resolución se conserva en `uv.lock`.
`requests` realiza las peticiones, `pandas` genera el CSV y `pathlib.Path`
gestiona la ruta de salida. `python-dotenv` permite cargar la configuración
local desde un archivo `.env`.

Desde la raíz del repositorio, en Git Bash o PowerShell:

```bash
cd semana7/modules/07-request_amet
uv sync --locked
cp .env.example .env
```

Edita `.env` y sustituye el valor de ejemplo por tu API key de AEMET:

```dotenv
AEMET_API_KEY=tu_api_key_de_aemet
```

Si ya tienes un `.env` configurado, consérvalo y omite la copia. Después ejecuta
desde el directorio del módulo:

```bash
uv run python -m 07_request_amet.main
```

Se necesita acceso a Internet y una API key válida de AEMET.

El script llama a `load_dotenv()` y obtiene la credencial mediante
`os.getenv("AEMET_API_KEY")`. También puedes definir esa variable directamente
en la terminal; por defecto, `load_dotenv()` conserva las variables ya
definidas. `.gitignore` excluye `.env`, `.venv` y `__pycache__/`; el archivo
`.env.example` sirve como plantilla sin credenciales reales.

Utiliza el comando `python -m` indicado: el ejecutable `07-request-amet`
declarado en el proyecto apunta por ahora al saludo de `__init__.py`, no a la
consulta de datos.

