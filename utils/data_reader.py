"""
data_reader.py

Funciones para leer datos de prueba desde archivos externos (CSV / JSON)
ubicados en la carpeta datos/. Permiten parametrizar los tests sin
escribir los datos directamente en el código.
"""

import csv
import json
import os

from utils.config import CARPETA_DATOS


def leer_csv(nombre_archivo):
    """
    Lee un CSV de datos/ y devuelve una lista de diccionarios,
    uno por fila (las claves son los nombres de las columnas).
    """
    ruta = os.path.join(CARPETA_DATOS, nombre_archivo)
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def leer_json(nombre_archivo):
    """Lee un JSON de datos/ y devuelve su contenido (dict o lista)."""
    ruta = os.path.join(CARPETA_DATOS, nombre_archivo)
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)
