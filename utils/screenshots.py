"""
screenshots.py

Captura de pantalla automática cuando falla un test. El archivo se
guarda con un nombre descriptivo: fecha_hora + nombre del test, por ej.:

    reports/screenshots/20261115_183045_test_login_usuario_bloqueado.png
"""

import base64
import os
import re
from datetime import datetime

from utils.config import CARPETA_CAPTURAS


def _nombre_seguro(texto):
    """Reemplaza caracteres no válidos para nombres de archivo ([, ], espacios, etc.)."""
    return re.sub(r"[^\w\-]+", "_", texto).strip("_")


def capturar_pantalla(driver, nombre_test):
    """
    Toma una captura del navegador y la guarda como PNG.

    Devuelve (ruta_del_archivo, imagen_en_base64). El base64 se usa para
    incrustar la imagen dentro del reporte HTML.
    """
    os.makedirs(CARPETA_CAPTURAS, exist_ok=True)

    marca_de_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{marca_de_tiempo}_{_nombre_seguro(nombre_test)}.png"
    ruta = os.path.join(CARPETA_CAPTURAS, nombre_archivo)

    imagen_base64 = driver.get_screenshot_as_base64()
    with open(ruta, "wb") as archivo:
        archivo.write(base64.b64decode(imagen_base64))

    return ruta, imagen_base64
