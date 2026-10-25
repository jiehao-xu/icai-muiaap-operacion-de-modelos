import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
env_api_key = os.getenv("AEMET_API_KEY")

api_key = env_api_key

headers = {
    "api_key": api_key
}

# Obtenemos la url en donde podemos coger los datos de las estaciones
url_estaciones = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
response = requests.get(url_estaciones, headers=headers, timeout=30)
url_acceso_dato_estaciones = response.json()["datos"]
print(url_acceso_dato_estaciones)

# Obetenemos los datos de las estaciones
estaciones_respuesta = requests.get(url_acceso_dato_estaciones, timeout=30)
estaciones = estaciones_respuesta.json()
print(estaciones)

# Obtenemos el indicativo de la estacion de ciudad universitaria
ciu_estacion = ""
for estacion in estaciones:
    if estacion["nombre"] == "MADRID, CIUDAD UNIVERSITARIA":
        ciu_estacion=estacion["indicativo"]

print(ciu_estacion)

# Obtemeos la url con los datos solicitados
fechaIniStr = "2019-10-01T00:00:00UTC"
fechaFinStr = "2019-10-30T23:59:59UTC"
url_climatologias= f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/estacion/{ciu_estacion}"
response_clima = requests.get(url_climatologias, headers=headers, timeout=30)
clima_ciu_url = response_clima.json()["datos"]
print(clima_ciu_url)

# Obtenemos los datos
response = requests.get(clima_ciu_url, timeout=30)
response_clima_ciu = response.json()
print(response_clima_ciu)

# Escribimos los datos

df = pd.DataFrame(response_clima_ciu)
output_path = Path("assets/datos_emet_ciu.csv")
output_path.parent.mkdir(parents=True, exist_ok = True)
df.to_csv(output_path, index = False)