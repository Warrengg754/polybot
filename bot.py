import requests
import json
import csv
from datetime import datetime
import os

ruta_archivo = "historico.csv"

ligas = {
    "NBA": 745,
    "NFL": 450,
    "Premier League": 82,
    "Champions League": 1234,
    "MLB": 100381,
}

existe = os.path.isfile(ruta_archivo)

with open(ruta_archivo, "a", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    if not existe:
        escritor.writerow(["fecha_hora", "liga", "pregunta", "opcion", "probabilidad"])

    for nombre_liga, tag_id in ligas.items():
        params = {
            "tag_id": tag_id,
            "active": "true",
            "closed": "false",
            "order": "volume24hr",
            "ascending": "false",
            "limit": 5
        }
        respuesta = requests.get("https://gamma-api.polymarket.com/markets", params=params)
        mercados = respuesta.json()

        for m in mercados:
            precios = json.loads(m["outcomePrices"])
            opciones = json.loads(m["outcomes"])
            for opcion, precio in zip(opciones, precios):
                escritor.writerow([
                    datetime.now().isoformat(),
                    nombre_liga,
                    m["question"],
                    opcion,
                    float(precio) * 100
                ])

print("Guardado correctamente")
